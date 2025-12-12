import os
from pathlib import Path
from typing import Optional

try:
    import bpy
except ImportError:
    bpy = None

def find_project_root(current_file_path: Optional[str] = None) -> Optional[Path]:
    if current_file_path is None:
        if not bpy or not bpy.data.filepath:
            return None
        current_file_path = bpy.data.filepath
    
    current_path = Path(current_file_path).resolve()
    
    if current_path.is_file():
        current_path = current_path.parent
    
    check_path = current_path
    max_depth = 10
    depth = 0
    
    while check_path != check_path.parent and depth < max_depth:
        assets_dir = check_path / "01_assets"
        shots_dir = check_path / "02_shots"
        
        if assets_dir.exists() or shots_dir.exists():
            return check_path
        
        check_path = check_path.parent
        depth += 1
    
    if bpy:
        try:
            scene = bpy.context.scene if hasattr(bpy.context, 'scene') else None
            if scene and hasattr(scene, 'studio_project_props'):
                props = scene.studio_project_props
                if props.project_root_path:
                    root_path = Path(props.project_root_path)
                    if root_path.exists():
                        assets_dir = root_path / "01_assets"
                        shots_dir = root_path / "02_shots"
                        if assets_dir.exists() or shots_dir.exists():
                            return root_path
        except:
            pass
    
    return None

def detect_project_type(project_root: Path) -> str:
    if not project_root or not project_root.exists():
        return "unknown"
    
    shots_dir = project_root / "02_shots"
    if not shots_dir.exists():
        return "asset_library"
    
    seq_dirs = [d for d in shots_dir.iterdir() if d.is_dir() and d.name.startswith("seq_")]
    shot_dirs = [d for d in shots_dir.iterdir() if d.is_dir() and d.name.startswith("sh_")]
    
    if seq_dirs:
        return "short_film"
    elif shot_dirs:
        return "single_shot"
    else:
        return "unknown"

def detect_current_asset_type() -> Optional[str]:
    if not bpy or not bpy.data.filepath:
        return None
    
    file_path = Path(bpy.data.filepath).resolve()
    project_root = find_project_root()
    
    if not project_root:
        return None
    
    assets_dir = project_root / "01_assets"
    if not assets_dir.exists():
        return None
    
    asset_types = ['char', 'prop', 'env', 'fx', 'veh', 'veg', 'light']
    
    for asset_type in asset_types:
        asset_type_dir = assets_dir / asset_type
        if asset_type_dir.exists():
            try:
                file_path.resolve().relative_to(asset_type_dir.resolve())
                return asset_type
            except ValueError:
                continue
    
    return None

def get_current_asset_id() -> Optional[str]:
    if not bpy or not bpy.data.filepath:
        return None
    
    file_path = Path(bpy.data.filepath).resolve()
    project_root = find_project_root()
    
    if not project_root:
        return None
    
    assets_dir = project_root / "01_assets"
    if not assets_dir.exists():
        return None
    
    asset_types = ['char', 'prop', 'env', 'fx', 'veh', 'veg', 'light']
    
    for asset_type in asset_types:
        asset_type_dir = assets_dir / asset_type
        if asset_type_dir.exists():
            try:
                rel_path = file_path.resolve().relative_to(asset_type_dir.resolve())
                parts = rel_path.parts
                if len(parts) > 0:
                    return parts[0]
            except ValueError:
                continue
    
    return None

