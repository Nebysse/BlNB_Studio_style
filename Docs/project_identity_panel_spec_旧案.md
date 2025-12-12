Project Identity Panel – Build Specification

Blender Studio Project Scaffolder

1. 功能目标（Purpose）

本模块用于在 Blender 项目初始化（blend init）阶段 和 工程接管阶段：

建立明确的 作者 / 项目身份信息（Project Identity）

将身份信息：

写入 项目级元数据文件

写入 每一个 .blend 文件

为后续 pipeline、发布、防盗、归档提供可靠来源

该模块是 Studio Project Scaffolder 插件的核心组成部分。

2. UI 设计规范
2.1 面板位置

Blender UI：VIEW_3D → N Panel

插件 Tab：Studio Project

新增独立区块：

▶ Project Identity


Project Identity 必须是 独立逻辑面板，不能混在 Project Init 或 File Actions 中。

2.2 UI 字段定义
Author 信息（作者 / 制作方）
字段名	类型	示例
Author Name	String	Nebysse
Studio / Team	String	ZIMA Digital Lab
Role	String	Character Artist
Contact (Optional)	String	nebysse@studio.com
Project 信息（项目身份）
字段名	类型	示例
Project Code	String	wing_it
Project Type	Enum	short_film
Copyright	String	© 2025 Nebysse
2.3 行为按钮

Write to Project Metadata

Write to Current Blend

（可选）Sync from Project Metadata

3. 数据存储规范（核心）
3.1 项目级存储（Project Root）
文件名（固定）
project.json

写入规则

位于项目根目录

由插件维护

作为 项目权威身份信息源

JSON 结构规范
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

设计原则

project.json 是 唯一可信来源

.blend 文件中的信息必须可由此文件同步

必须支持 schema_version 升级

3.2 文件级存储（.blend 内）
存储方式

使用 Blender Custom Properties（ID Properties）

存储在 Scene 或 BlendData 层级

命名空间规范（强制）
studio_meta.author.name
studio_meta.author.studio
studio_meta.author.role
studio_meta.author.contact
studio_meta.project.code
studio_meta.project.type
studio_meta.project.schema_version


禁止使用无前缀字段
禁止覆盖 Blender 原生属性

设计目标

不影响 Blender UI

不与其他插件冲突

可被 pipeline / exporter / render 工具读取

4. 生命周期行为规范
4.1 项目初始化（Project Init）

当用户执行 Initialize Project 时，插件必须：

创建项目根目录

创建 .blender_project 标记文件

创建 project.json

从 Project Identity 面板读取 Author / Project 信息

写入 project.json

将同样的信息写入当前 .blend

4.2 工程接管（Adopt Current File into Project）

当用户执行 Adopt Current File into Project 时：

插件从项目根目录读取 project.json

自动将 Author / Project 信息写入新保存的 .blend

保证：

所有纳入项目的工程文件具有统一身份信息

4.3 手动同步

Write to Current Blend

仅更新当前 .blend 的 Custom Properties

Write to Project Metadata

更新 project.json

Sync from Project Metadata

用 project.json 覆盖当前 .blend

5. 工程结构建议（给 Cursor）
模块位置
addon/
├── ui/
│   └── panel_project_identity.py
├── operators/
│   └── op_project_identity.py
├── core/
│   ├── metadata.py      # project.json 读写
│   └── blend_meta.py    # Custom Properties 封装

6. 错误与保护逻辑

插件必须处理以下情况：

未检测到 .blender_project：

禁止写入 project.json

当前文件未保存：

禁止写入 blend metadata

project.json 不存在或损坏：

提示用户修复或重新初始化

7. 设计原则总结（给 Cursor 的核心理解）

Project Identity ≠ 单个 .blend 文件

project.json 是 项目身份权威

.blend 只保存 可复制的身份快照

所有字段必须：

小写

snake_case

有统一命名空间

系统必须 schema-versioned

8. 未来扩展（非本阶段实现）

Render Metadata 自动注入 Author

Publish 阶段写入版权锁定信息

Asset Manifest 自动生成

防盗水印 / 署名校验

Blender File Browser 元数据显示

9. Cursor Composer 指令摘要（可直接使用）

Implement a Project Identity system with a dedicated UI panel.
Store author and project metadata in both a project-level project.json file and file-level Blender Custom Properties under a unified namespace (studio_meta.*).

Metadata must be written during project initialization and automatically synced when adopting files into the project.

The system must be schema-versioned, future-proof, and non-invasive to Blender’s native data structures.