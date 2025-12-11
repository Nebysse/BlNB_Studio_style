import os
import json
from pathlib import Path
from typing import Dict, Any, Tuple
from . import schema

def create_directory_structure(base_path: Path, dirs: Dict[str, Any], parent_path: Path = None):
    if parent_path is None:
        parent_path = base_path
    
    for dir_name, subdirs in dirs.items():
        dir_path = parent_path / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        
        if isinstance(subdirs, dict) and subdirs:
            create_directory_structure(base_path, subdirs, dir_path)

def create_blend_file(file_path: Path):
    try:
        import bpy
        file_path.parent.mkdir(parents=True, exist_ok=True)
        old_filepath = bpy.data.filepath
        bpy.ops.wm.read_homefile(app_template="")
        bpy.ops.wm.save_as_mainfile(filepath=str(file_path))
        if old_filepath:
            bpy.ops.wm.open_mainfile(filepath=old_filepath)
    except Exception:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch()

def create_readme(project_root: Path, project_code: str, project_type: str):
    readme_path = project_root / "00_admin" / "docs" / "README_project_structure.md"
    readme_path.parent.mkdir(parents=True, exist_ok=True)
    
    content = f"""# {project_code} 项目结构说明

## 项目类型
{project_type}

## 目录结构

### 00_admin/
管理文档、进度表、制片相关文件

### 01_assets/
资产库目录
- char/ 角色资产
- env/ 场景环境资产
- prop/ 道具资产
- fx/ 特效资产

每个资产目录包含：
- work/ 工作文件
- publish/ 发布版本
- render/ 渲染输出（fx 为 cache/）

### 02_shots/
镜头/序列目录
- seq_###/ 序列目录（短片项目）
  - sh_####/ 镜头目录
    - work/ 工作文件
    - publish/ 发布版本
    - cache/ 缓存文件
    - render/ 渲染输出

### 03_edit/
剪辑和音频相关文件

### 04_renders/
最终渲染输出
- preview/ 预览版本
- final/ 最终交付

### 05_lib/
外部资源库
- textures/ 贴图
- hdri/ 环境贴图
- scripts/ 脚本
- fonts/ 字体

### 90_temp/
临时文件目录

### prod/
项目级主工程文件

## 文件命名规范

格式：`<scope>_<subject>_<task>_v<###>.blend`

示例：
- char_hero_boy_model_v001.blend
- shot_seq010sh0010_anim_v012.blend
"""
    
    readme_path.write_text(content, encoding='utf-8')

def create_project_settings(project_root: Path, project_code: str, project_type: str):
    settings_path = project_root / "prod" / "project_settings.json"
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    
    settings = {
        "project_code": project_code,
        "project_type": project_type,
        "version": "1.0.0",
    }
    
    settings_path.write_text(json.dumps(settings, indent=2, ensure_ascii=False), encoding='utf-8')

def create_project(
    base_path: str,
    project_code: str,
    project_type: str
) -> Tuple[bool, str]:
    try:
        project_code = project_code.lower().replace(" ", "_").replace("-", "_")
        
        if not project_code:
            return False, "项目代号不能为空"
        
        if project_type not in schema.PROJECT_SCHEMAS:
            return False, f"未知的项目类型: {project_type}"
        
        schema_data = schema.PROJECT_SCHEMAS[project_type]
        root_name = schema_data["root_name_pattern"].format(project_code=project_code)
        project_root = Path(base_path) / root_name
        
        if project_root.exists() and any(project_root.iterdir()):
            return False, f"项目目录已存在且不为空: {project_root}"
        
        project_root.mkdir(parents=True, exist_ok=True)
        
        create_directory_structure(project_root, schema_data["directories"])
        
        for file_pattern in schema_data["files"]:
            file_path = project_root / file_pattern.format(project_code=project_code)
            if file_path.suffix == ".blend":
                create_blend_file(file_path)
            else:
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.touch()
        
        create_readme(project_root, project_code, project_type)
        create_project_settings(project_root, project_code, project_type)
        
        return True, str(project_root)
    
    except Exception as e:
        return False, f"创建项目失败: {str(e)}"

def create_asset_structure(
    project_root: Path,
    asset_type: str,
    asset_id: str
) -> Tuple[bool, str]:
    try:
        asset_id = asset_id.lower().replace(" ", "_").replace("-", "_")
        
        if asset_type not in schema.ASSET_TEMPLATES:
            return False, f"未知的资产类型: {asset_type}"
        
        asset_dir = project_root / "01_assets" / asset_type / asset_id
        if asset_dir.exists():
            return False, f"资产目录已存在: {asset_dir}"
        
        template = schema.ASSET_TEMPLATES[asset_type]
        create_directory_structure(asset_dir, template["directories"], asset_dir)
        
        for file_pattern in template["files"]:
            file_path = asset_dir / file_pattern.format(asset_id=asset_id)
            if file_path.suffix == ".blend":
                create_blend_file(file_path)
            else:
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.touch()
        
        return True, str(asset_dir)
    
    except Exception as e:
        return False, f"创建资产结构失败: {str(e)}"

def create_shot_structure(
    project_root: Path,
    seq_id: str,
    shot_id: str
) -> Tuple[bool, str]:
    try:
        seq_id = seq_id.lower().replace(" ", "_").replace("-", "_")
        shot_id = shot_id.lower().replace(" ", "_").replace("-", "_")
        
        if not seq_id.startswith("seq_"):
            seq_id = f"seq_{seq_id.zfill(3)}"
        if not shot_id.startswith("sh_"):
            shot_id = f"sh_{shot_id.zfill(4)}"
        
        shot_dir = project_root / "02_shots" / seq_id / shot_id
        if shot_dir.exists():
            return False, f"镜头目录已存在: {shot_dir}"
        
        template = schema.SHOT_TEMPLATES
        create_directory_structure(shot_dir, template["directories"], shot_dir)
        
        for file_pattern in template["files"]:
            file_path = shot_dir / file_pattern.format(shot_id=shot_id)
            if file_path.suffix == ".blend":
                create_blend_file(file_path)
            else:
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.touch()
        
        return True, str(shot_dir)
    
    except Exception as e:
        return False, f"创建镜头结构失败: {str(e)}"

