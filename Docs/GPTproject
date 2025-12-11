
---
# Blender Studio-Style 项目初始化插件 – 工程范式文档

> 本文档用于指导 Cursor Composer 为 Blender 4.5–5.0 生成一个 **项目初始化插件**（Add-on / Extension），通过侧边栏面板一键创建符合 Blender Studio 工作习惯的项目目录与命名规范。
> 插件不涉及渲染、资产管理 UI 等高级功能，专注于「**标准化项目结构 + 快速初始化**」。

---

## 1. 总体目标

1. 用户在 Blender 4.5–5.0 中安装本插件后：

   * 在 **N 面板** 出现一个新的选项卡（例如 `Studio Project`）。
   * 用户只需：

     * 指定项目根目录（可选：输入项目名）。
     * 选择预设项目类型（例如：单镜头练习 / 短片 / 长期资产库）。
   * 点击「创建项目结构」按钮后，插件按预设规则创建目录与若干空 `.blend` 模板文件。

2. 设计目标：

   * 尽量靠近 Blender Studio 公开的命名 / 目录理念，比如

     * **全小写**、**下划线分隔**、不使用空格和大写（"no caps, no gaps"）([studio.blender.org][1])
     * 将 **assets** 与 **shots/sequences** 分离管理([studio.blender.org][2])
   * 支持 **Blender 4.5 – 5.0**（含新的 Extensions 系统，但代码兼容传统 add-on 方式）。

3. 非目标：

   * 不实现复杂资产数据库、Shot 管理 UI。
   * 不实现线上协作、SVN/Git 集成（只预留目录位置即可）。
   * 不实现大的 Pipeline 系统，只做「轻量模板生成器」。

---

## 2. 目标用户使用流程（UX）

### 2.1 首次使用

1. 用户安装插件并启用。
2. 打开任意 `.blend`，在 3D 视图 **N 面板** 中看到新 Tab：`Studio Project`。
3. 在面板中：

   * 输入 / 浏览选择「项目根目录」。
   * 输入「项目代号」（如 `wing_it`, `coffee_run` 风格，全部小写、下划线）。
   * 选择 **项目模板类型**：

     * `single_shot` – 单镜头练习 / 小作品。
     * `short_film` – 多镜头短篇。
     * `asset_library` – 纯资产库项目（用于长期积累模型、材质等）。
4. 点击「初始化项目」：

   * 在选定目录下创建标准结构。
   * 在关键目录内创建若干空的 `.blend` 模板文件，例如：

     * `project_root/prod/project_overview_v001.blend`
     * `project_root/assets/char/main_char/work/main_char_layout_v001.blend`
   * 在根目录创建一份 `README_project_structure.md` 自动说明目录含义。

### 2.2 再次使用 / 已存在项目

1. 插件能检测当前 `.blend` 是否位于标准结构内：

   * 判断：向上查找包含关键子目录（`assets`, `shots` 等）的根路径。
2. 若检测到：

   * 面板显示「当前项目根目录」与项目类型。
   * 提供按钮：

     * 「打开资产目录」
     * 「打开镜头目录」
     * 「新建资产/镜头子结构」等（可做最小 MVP：仅新建子结构）。

---

## 3. 标准目录结构规范

> 以下结构是面向小型/中型工作室的通用方案，参考了 Blender Studio 的资产/镜头分离理念和常见 VFX/动画目录布局([studio.blender.org][2])。
> **Composer 需按此生成模板结构与常量定义。**

### 3.1 顶层目录

以项目代号 `wing_it` 为例：

```text
wing_it/
├── 00_admin/          # 管理&文档
├── 01_assets/         # 资产库（角色、场景、道具…）
├── 02_shots/          # 镜头 / 序列
├── 03_edit/           # 剪辑、音频相关
├── 04_renders/        # 最终输出（图像/序列输出）
├── 05_lib/            # 外部库（贴图、HDRI、脚本…）
├── 90_temp/           # 临时缓存
└── prod/              # 项目级主工程文件
```

**命名规则：**

* 顶层目录推荐前缀序号：`00_`, `01_` ... 方便排序。
* 所有目录与文件名：

  * 使用 **小写字母**。
  * 使用 **下划线 `_` 分隔单词**。
  * 避免空格与大写（"no caps, no gaps"）([studio.blender.org][1])

### 3.2 Assets 资产结构

```text
01_assets/
├── char/        # 角色
│   └── <char_id>/
│       ├── work/
│       ├── publish/
│       └── render/
├── env/         # 场景/环境
│   └── <env_id>/
│       ├── work/
│       ├── publish/
│       └── render/
├── prop/        # 道具
│   └── <prop_id>/
│       ├── work/
│       ├── publish/
│       └── render/
└── fx/          # 特效资产（烟雾、爆炸、资产化特效）
    └── <fx_id>/
        ├── work/
        ├── publish/
        └── cache/    # 模拟缓存
```

* `<char_id>` 等统一使用：`type_name` 格式，如：

  * `char/hero_boy/`
  * `env/city_rooftop/`
* `work/`：工作文件，允许频繁改动。
* `publish/`：对外提供的稳定版本（资产交付、下游引用）。
* `render/`：专门用于 lookdev / turntable 渲染的工程与输出。

### 3.3 Shots / Sequences 结构（短片、系列项目）

```text
02_shots/
└── seq_<###>/           # 序列号，例如 seq_010
    └── sh_<####>/       # 镜头号，例如 sh_0010
        ├── work/
        ├── publish/
        ├── cache/       # 模拟缓存（布料、流体…）
        └── render/
```

* 序列 / 镜头命名：`seq_010/sh_0010` 格式，三位/四位数字。
* `work/`：动画、布局、灯光工作工程。
* `publish/`：对剪辑 / 渲染农场稳定可用的 shot 文件。
* `cache/`：Alembic / VDB / MDD 等缓存文件。
* `render/`：镜头级渲染输出（exr、png 等）。

### 3.4 其他关键目录

```text
00_admin/
├── docs/                     # 生产文档，pdf, md等
├── spreadsheets/             # 进度表、shot 列表
└── mgmt/                     # 制片相关文件

03_edit/
├── audio/
└── timelines/

04_renders/
├── preview/    # 快速 playblast / 预览
└── final/      # 最终交付版本（图像/视频）

05_lib/
├── textures/
├── hdri/
├── scripts/
└── fonts/

prod/
├── project_overview_v001.blend     # 总控工程（可空文件）
└── project_settings.json           # 插件用的项目元数据

90_temp/
└── .gitignore 或清理脚本专用
```

---

## 4. 文件命名与版本规范

为了避免「final_final_really_final.blend」这种情况，定义统一规则供插件使用：

### 4.1 通用文件命名模式

```text
<scope>_<subject>_<task>_v<###>.blend
```

* `<scope>`：`char`, `env`, `prop`, `fx`, `shot`, `proj` 等。
* `<subject>`：具体名字，如 `hero_boy`, `city_rooftop`, `seq010sh0010`。
* `<task>`：`model`, `rig`, `layout`, `anim`, `lighting`, `comp` 等。
* `v<###>`：版本号，从 `v001` 开始递增。

示例：

* `char_hero_boy_model_v001.blend`
* `char_hero_boy_rig_v003.blend`
* `shot_seq010sh0010_anim_v012.blend`
* `proj_wing_it_overview_v001.blend`

### 4.2 插件职责

* 不自动推送版本控制，只负责：

  * 默认创建 `v001` 的空工程文件。
  * 后续可选：提供「创建新版本」按钮，复制当前文件并自动 `v### + 1`。

---

## 5. 技术设计约束（给 Composer 的实现指导）

> 本节描述 **Blender 插件工程结构** 及关键模块职责，Composer 应按此拆分 Python 模块与 UI 逻辑。无需具体实现细节，但要保证接口清晰、易扩展。

### 5.1 插件形态

* 形态：**传统 Add-on + 兼容 Extension**（尽量）。
* Python 包结构建议：

```text
blender_studio_project_scaffolder/
├── __init__.py              # Blender 注册入口
├── addon_prefs.py           # 插件偏好设置（默认根路径等）
├── ui_panel.py              # N 面板 UI
├── operators/
│   ├── __init__.py
│   ├── op_init_project.py   # 初始化项目结构
│   ├── op_new_asset.py      # 新建资产（可选）
│   └── op_new_shot.py       # 新建镜头结构（可选）
├── core/
│   ├── __init__.py
│   ├── schema.py            # 项目目录 schema 定义
│   ├── generator.py         # 目录和空 .blend 文件创建逻辑
│   └── detector.py          # 项目根目录检测与类型识别
└── resources/
    ├── templates/           # 未来可放模板文件
    └── icons/               # 面板图标
```

### 5.2 版本兼容性（Blender 4.5–5.0）

* 使用 `bpy.app.version` 分支，若某些 API 在 5.0 有变动，则在模块中集中处理。
* 尽量只使用稳定 API：

  * `bpy.props.*` 定义属性。
  * `bpy.types.Panel`, `bpy.types.Operator`, `bpy.types.AddonPreferences`。
* 不依赖废弃模块或实验性功能。

### 5.3 项目 Schema 定义（核心）

在 `core/schema.py` 中以数据结构的形式描述目录和文件模板：

* 使用嵌套字典 / dataclass / 简单 JSON schema 表示：

```python
PROJECT_SCHEMAS = {
    "single_shot": {...},
    "short_film": {...},
    "asset_library": {...},
}
```

每个 schema 定义：

* `root_name_pattern`: `<project_code>`（或 `YYYYMMDD_<project_code>` 等）。
* `directories`: 嵌套结构，包括路径模式与说明。
* `files`: 要创建的初始 `.blend` 和 `.md` 文件列表（路径 + 文件名模式）。

> Composer 需要在文档中定义清晰的 schema 结构，使 `generator.py` 能通用地根据 schema 创建目录和文件。

### 5.4 生成器模块

`core/generator.py` 职责：

1. 根据用户输入（根目录 + 项目代号 + 项目类型）和 schema：

   * 拼接出最终项目根路径。
   * 创建目录（使用 `os.makedirs(..., exist_ok=True)`）。
2. 创建空文件：

   * `.blend` 文件：可以通过复制当前空场景的临时保存，或先只创建占位 `.txt` / `.md`（第一版可仅创建 README，`.blend` 留给后续迭代）。
   * `README_project_structure.md`：写入自动生成的结构说明（可由模板字符串生成）。
3. 所有路径处理需兼容 Windows / Linux / macOS。

### 5.5 检测模块

`core/detector.py` 职责：

* 从当前 `.blend` 文件路径向上查找，定位包含 `01_assets` 与 `02_shots` 等标志目录的「项目根」。
* 提供函数：

  * `find_project_root(current_file_path) -> Optional[Path]`
  * `detect_project_type(project_root) -> str`  (`"single_shot"` / `"short_film"` / `"asset_library"` / `"unknown"`)

UI 面板可基于此显示当前项目状态。

### 5.6 UI 面板 & Operator

`ui_panel.py`：

* 在 3D 视图 `VIEW_3D` > `UI` 区域创建 Panel（`bl_space_type='VIEW_3D'`, `bl_region_type='UI'`）。
* 显示：

  * 当前项目根（检测结果）。
  * 输入框：

    * 项目代号 `project_code`。
    * 浏览按钮选择根目录 `base_path`。
    * 下拉框选择 `project_type`。
  * 按钮：

    * `初始化项目结构`（调用 `op_init_project`）。
    * （可选）`在当前项目中新建资产/镜头结构`。

`operators/op_init_project.py`：

* 负责：

  * 收集面板属性。
  * 调用 `generator.create_project(...)`。
  * 根据结果报告 INFO / ERROR。

---

## 6. 与版本控制 / 团队协作的衔接（可选扩展点）

本阶段仅在结构中预留位置，不实现具体集成：

* 在 `00_admin/mgmt/` 中创建占位文件：

  * `pipeline_notes.md`
  * `todo_shot_list.csv`
* 在根目录创建 `.gitignore` 模板：

  * 忽略 `90_temp/`、缓存目录、渲染输出等。
* 将这些作为未来扩展点在注释/README 中说明。

---

## 7. 对 Cursor Composer 的具体要求总结

当我在 Cursor 中新建一个项目并引用本规范时，希望 Composer：

1. 创建如 **5.1** 中所述的 Python 包结构（空模块 + 基础 `bl_info`）。
2. 按 **3 & 4 章节** 将目录与命名规则抽象到 `core/schema.py` 的数据结构中。
3. 在 `core/generator.py` / `core/detector.py` 中实现清晰的函数接口（即使暂时留空或伪代码，也要结构完备）。
4. 在 `ui_panel.py` 中实现：

   * Blender UI Panel 骨架。
   * 属性定义（项目类型选择、路径选择、项目代号）。
   * 触发初始化 Operator 的逻辑。
5. 在 `README.md` / `README_project_structure.md` 中用简洁文字说明：

   * 本插件的用途。
   * 目录与命名规则的简要说明。
6. 确保所有命名遵守「全小写、下划线分隔、不带空格」的原则，并保持资产与镜头文件夹拆分([studio.blender.org][1])。

---