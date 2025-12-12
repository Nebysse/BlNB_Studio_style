# Blender Studio-Style 插件架构文档

**版本**: 1.0.0  
**最后更新**: 2025-01-18  
**Blender 版本**: 4.5+

---

## 1. 概述

本插件为 Blender 4.5+ 提供符合 Blender Studio 规范的项目目录结构初始化和管理功能，包括：

- 标准化项目目录结构创建
- 项目身份元数据管理（Project Identity）
- 资产和镜头结构快速创建
- 文件级身份信息持久化

---

## 2. 目录结构

```
Blender Studio-Style/
├── __init__.py                 # 插件注册入口
├── addon_prefs.py              # 插件偏好设置
├── ui_panel.py                 # UI 面板定义
├── core/                       # 核心功能模块
│   ├── __init__.py
│   ├── schema.py               # 项目结构 Schema 定义
│   ├── generator.py            # 目录和文件生成器
│   ├── detector.py             # 项目根目录检测
│   ├── metadata.py             # 项目级元数据管理 (project.json)
│   └── blend_meta.py            # 文件级元数据管理 (WindowManager IDProperties)
├── operators/                  # 操作符模块
│   ├── __init__.py
│   ├── op_init_project.py      # 项目初始化操作符
│   ├── op_new_asset.py          # 新建资产操作符
│   ├── op_new_shot.py           # 新建镜头操作符
│   ├── op_change_asset_type.py # 修改资产类型操作符
│   └── op_project_identity.py  # 项目身份操作符
└── resources/                  # 资源文件
    ├── icons/                  # 图标资源
    └── templates/              # 模板文件
```

---

## 3. 核心模块说明

### 3.1 插件入口 (`__init__.py`)

**职责**:
- 注册所有 Blender 类和属性
- 注册文件保存前处理器 (`save_pre` handler)
- 管理插件生命周期

**关键组件**:
- `classes`: 所有需要注册的 Blender 类列表
- `on_save_pre()`: 文件保存前自动同步项目身份信息
- `register()` / `unregister()`: 插件注册和卸载

**注册的属性**:
- `bpy.types.Scene.studio_project_props`: 项目属性组
- `bpy.types.Scene.studio_project_identity_props`: 身份属性组（临时 UI 编辑用）

---

### 3.2 核心模块 (`core/`)

#### 3.2.1 `schema.py` - 项目结构定义

**职责**: 定义项目目录结构的 Schema

**数据结构**:
- `PROJECT_SCHEMAS`: 项目类型模板（single_shot, short_film, asset_library）
- `ASSET_TEMPLATES`: 资产类型模板（char, prop, env, fx, veh, veg, light）
- `SHOT_TEMPLATES`: 镜头结构模板

**特点**:
- 使用嵌套字典定义目录结构
- 支持文件模板模式（使用 `{variable}` 占位符）

#### 3.2.2 `generator.py` - 目录和文件生成器

**职责**: 根据 Schema 创建目录结构和文件

**主要函数**:
- `create_project()`: 创建完整项目结构
- `create_asset_structure()`: 创建资产目录结构（返回目标文件路径）
- `create_shot_structure()`: 创建镜头目录结构（返回目标文件路径）
- `create_directory_structure()`: 递归创建目录结构
- `create_readme()`: 生成项目结构说明文档
- `create_project_settings()`: 创建项目设置文件

**重要设计**:
- **不创建空的 .blend 文件**：资产和镜头创建时只创建目录，返回目标路径
- 使用 `save_as_mainfile` 保存当前工作状态到新位置

#### 3.2.3 `detector.py` - 项目检测器

**职责**: 检测当前文件所在的项目根目录

**主要函数**:
- `find_project_root()`: 向上查找项目根目录（查找 `01_assets` 和 `02_shots` 目录）
- `detect_project_type()`: 检测项目类型（single_shot / short_film / asset_library）
- `detect_current_asset_type()`: 检测当前文件的资产类型
- `get_current_asset_id()`: 获取当前文件的资产 ID

**检测逻辑**:
1. 从当前文件路径向上查找包含 `01_assets` 或 `02_shots` 的目录
2. 如果找不到，尝试使用存储的 `project_root_path` 属性
3. 支持最大深度限制（10 层）

#### 3.2.4 `metadata.py` - 项目级元数据管理

**职责**: 管理项目根目录的 `project.json` 文件

**关键常量**:
- `PROJECT_MARKER`: `.blender_project` 标记文件
- `METADATA_FILE`: `project.json`
- `SCHEMA_VERSION`: 元数据版本号

**主要函数**:
- `get_project_root()`: 通过标记文件查找项目根
- `is_project_root()`: 检查路径是否为项目根
- `create_project_marker()`: 创建项目标记文件
- `read_project_metadata()`: 读取项目元数据
- `write_project_metadata()`: 写入项目元数据

**元数据结构**:
```json
{
  "project": {
    "code": "wing_it",
    "type": "short_film",
    "schema_version": 1,
    "created_at": "2025-01-18",
    "created_with": "studio_project_scaffolder"
  },
  "author": {
    "name": "Nebysse",
    "studio": "ZIMA Digital Lab",
    "role": "Character Artist",
    "contact": "nebysse@studio.com",
    "copyright": "© 2025 Nebysse"
  }
}
```

#### 3.2.5 `blend_meta.py` - 文件级元数据管理

**职责**: 管理 .blend 文件中的身份元数据（存储在 WindowManager IDProperties）

**关键设计**:
- **存储位置**: `bpy.context.window_manager["studio_meta.*"]`
- **命名空间**: `studio_meta.*`（避免冲突）
- **持久化**: WindowManager IDProperties 随文件保存

**主要函数**:
- `_get_window_manager()`: 获取 WindowManager 实例
- `write_blend_metadata()`: 写入文件元数据
- `read_blend_metadata()`: 读取文件元数据
- `sync_from_project_metadata()`: 从项目元数据同步到文件

**元数据键**:
- `studio_meta.author.name`
- `studio_meta.author.studio`
- `studio_meta.author.role`
- `studio_meta.author.contact`
- `studio_meta.author.copyright`
- `studio_meta.project.code`
- `studio_meta.project.type`
- `studio_meta.project.schema_version`

---

### 3.3 UI 模块 (`ui_panel.py`)

**职责**: 定义所有 UI 面板和属性组

**属性组**:
- `StudioProjectProperties`: 项目相关属性（临时 UI 状态）
- `StudioProjectIdentityProperties`: 身份信息属性（临时 UI 编辑用）

**面板**:
- `STUDIO_PT_ProjectPanel`: 主项目面板
  - 显示当前项目信息
  - 项目初始化界面
  - 资产/镜头创建按钮
- `STUDIO_PT_ProjectIdentity`: 项目身份面板
  - Author 信息编辑
  - Project 信息编辑
  - 元数据操作按钮
- `STUDIO_PT_DirectoryGuide`: 目录结构说明面板

**重要约束**:
- **不在 `draw()` 方法中写入属性**：避免 `AttributeError`
- UI 属性组仅用于临时编辑，实际数据存储在 WindowManager 或 project.json

---

### 3.4 操作符模块 (`operators/`)

#### 3.4.1 `op_init_project.py` - 项目初始化

**操作符**: `STUDIO_OT_InitProject`

**功能**:
- 创建项目目录结构
- 创建项目标记文件 (`.blender_project`)
- 写入项目元数据 (`project.json`)
- 写入当前文件的身份信息

**流程**:
1. 验证输入参数
2. 调用 `generator.create_project()` 创建结构
3. 写入项目元数据
4. 写入当前文件元数据

#### 3.4.2 `op_new_asset.py` - 新建资产

**操作符**: `STUDIO_OT_NewAsset`

**功能**:
- 创建资产目录结构
- **使用 `save_as_mainfile` 保存当前工作状态到新位置**

**重要设计**:
- **不复制或打开文件**
- **只创建目录结构**
- **使用 `bpy.ops.wm.save_as_mainfile` 保存当前内存状态**
- 保留所有当前工作状态，无数据丢失

**流程**:
1. 检查文件是否已保存
2. 创建资产目录结构
3. 使用 `save_as_mainfile` 保存到目标位置

#### 3.4.3 `op_new_shot.py` - 新建镜头

**操作符**: `STUDIO_OT_NewShot`

**功能**:
- 创建镜头目录结构
- **使用 `save_as_mainfile` 保存当前工作状态到新位置**

**设计原则**: 与 `op_new_asset.py` 相同

#### 3.4.4 `op_change_asset_type.py` - 修改资产类型

**操作符**: `STUDIO_OT_ChangeAssetType`

**功能**:
- 检测当前文件的资产类型
- 移动资产目录到新类型
- 重新打开文件

#### 3.4.5 `op_project_identity.py` - 项目身份操作

**操作符**:
- `STUDIO_OT_WriteToProjectMetadata`: 写入项目元数据
- `STUDIO_OT_WriteToCurrentBlend`: 写入当前文件元数据
- `STUDIO_OT_SyncFromProjectMetadata`: 从项目元数据同步
- `STUDIO_OT_LoadToEditor`: 加载元数据到 UI 编辑器

---

## 4. 数据存储架构

### 4.1 存储层次

```
项目级 (project.json)
    ↓ 权威来源
文件级 (WindowManager IDProperties)
    ↓ 持久化
UI 级 (Scene PropertyGroup)
    ↓ 临时编辑
```

### 4.2 存储位置

| 数据类型 | 存储位置 | 持久化 | 说明 |
|---------|---------|--------|------|
| 项目元数据 | `project.json` | ✅ | 项目根目录，权威来源 |
| 文件元数据 | `WindowManager["studio_meta.*"]` | ✅ | 文件级，随文件保存 |
| UI 编辑状态 | `Scene.studio_project_identity_props` | ❌ | 临时编辑缓冲区 |

### 4.3 数据流

**项目初始化**:
```
用户输入 → PropertyGroup → project.json + WindowManager
```

**文件保存**:
```
save_pre handler → project.json → WindowManager (自动同步)
```

**手动同步**:
```
project.json → WindowManager → PropertyGroup (UI 显示)
```

---

## 5. 关键设计原则

### 5.1 文件操作原则

**禁止的操作**:
- ❌ 复制文件 (`shutil.copy`)
- ❌ 打开文件 (`bpy.ops.wm.open_mainfile`)
- ❌ 创建空文件后打开

**唯一允许的操作**:
- ✅ `bpy.ops.wm.save_as_mainfile` - 保存当前内存状态到新位置

**原因**: 保留当前工作状态，避免数据丢失

### 5.2 属性写入约束

**禁止在 `draw()` 方法中写入属性**:
- ❌ `props.field = value` (在 Panel.draw 中)
- ✅ 使用操作符的 `execute()` 方法写入

**原因**: Blender 不允许在 UI 绘制时修改 ID 类属性

### 5.3 元数据存储位置

**项目级元数据**: `project.json` (权威来源)
**文件级元数据**: `WindowManager IDProperties` (不是 Scene，不是 bpy.data)

**原因**:
- WindowManager 代表文件级身份
- 支持多场景文件
- 持久化到文件

---

## 6. 项目结构规范

### 6.1 目录结构

```
{project_code}/
├── .blender_project          # 项目标记文件
├── project.json              # 项目元数据（权威来源）
├── 00_admin/                 # 管理文档
├── 01_assets/                # 资产库
│   ├── char/                 # 角色
│   ├── prop/                 # 道具
│   ├── env/                  # 环境
│   ├── fx/                   # 特效
│   ├── veh/                  # 载具
│   ├── veg/                  # 植被
│   └── light/                # 灯光
├── 02_shots/                 # 镜头/序列
│   └── seq_###/
│       └── sh_####/
├── 03_edit/                  # 剪辑
├── 04_renders/               # 渲染输出
├── 05_lib/                   # 外部库
├── 90_temp/                  # 临时文件
└── prod/                     # 项目级工程文件
```

### 6.2 命名规范

- **全小写**
- **下划线分隔** (`snake_case`)
- **无空格、无大写** ("no caps, no gaps")

### 6.3 文件命名模式

```
<scope>_<subject>_<task>_v<###>.blend
```

示例:
- `char_hero_boy_model_v001.blend`
- `shot_seq010sh0010_anim_v012.blend`

---

## 7. 版本兼容性

- **Blender 版本**: 4.5 - 5.0+
- **Python 版本**: Blender 内置 Python
- **API 使用**: 仅使用稳定 API，避免实验性功能

---

## 8. 扩展点

### 8.1 未来可扩展功能

- Render Metadata 自动注入 Author
- Publish 阶段版权锁定
- Asset Manifest 自动生成
- 防盗水印 / 署名校验
- Blender File Browser 元数据显示

### 8.2 模块化设计

- Schema 驱动的目录生成
- 可扩展的资产类型模板
- 可配置的项目类型

---

## 9. 注意事项

1. **文件操作**: 始终使用 `save_as_mainfile`，不复制或打开文件
2. **属性写入**: 不在 UI `draw()` 方法中写入属性
3. **元数据存储**: 项目级用 `project.json`，文件级用 `WindowManager`
4. **数据同步**: 文件保存时自动从项目元数据同步
5. **错误处理**: 所有操作符包含完整的错误处理和用户反馈

---

## 10. 参考文档

- `Docs/GPTproject` (旧案 - 初始设计文档)
- `Docs/project_identity_panel_spec.md` (旧案 - 身份面板规范)

---

**文档维护**: 本文档应与代码实现保持同步，重大架构变更时需更新。

