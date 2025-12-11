import os
from pathlib import Path
from typing import Optional

try:
    import bpy
except ImportError:
    bpy = None

def find_project_root(current_file_path: Optional[str] = None) -> Optional[Path]:
    if bpy:
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

