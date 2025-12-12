import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

try:
    import bpy
except ImportError:
    bpy = None

SCHEMA_VERSION = 1
PROJECT_MARKER = ".blender_project"
METADATA_FILE = "project.json"

def get_project_root() -> Optional[Path]:
    if not bpy:
        return None
    
    if not bpy.data.filepath:
        return None
    
    current_path = Path(bpy.data.filepath).resolve().parent
    
    max_depth = 10
    depth = 0
    check_path = current_path
    
    while check_path != check_path.parent and depth < max_depth:
        marker_file = check_path / PROJECT_MARKER
        if marker_file.exists():
            return check_path
        check_path = check_path.parent
        depth += 1
    
    return None

def is_project_root(path: Path) -> bool:
    return (path / PROJECT_MARKER).exists()

def create_project_marker(project_root: Path):
    marker_file = project_root / PROJECT_MARKER
    marker_file.touch()

def read_project_metadata(project_root: Optional[Path] = None) -> Optional[Dict[str, Any]]:
    if project_root is None:
        project_root = get_project_root()
    
    if not project_root or not is_project_root(project_root):
        return None
    
    metadata_path = project_root / METADATA_FILE
    if not metadata_path.exists():
        return None
    
    try:
        content = metadata_path.read_text(encoding='utf-8')
        return json.loads(content)
    except Exception:
        return None

def write_project_metadata(
    project_root: Path,
    author_name: str,
    studio: str = "",
    role: str = "",
    contact: str = "",
    project_code: str = "",
    project_type: str = "",
    copyright: str = ""
) -> bool:
    if not is_project_root(project_root):
        create_project_marker(project_root)
    
    metadata_path = project_root / METADATA_FILE
    
    existing_data = read_project_metadata(project_root) or {}
    
    metadata = {
        "project": {
            "code": project_code or existing_data.get("project", {}).get("code", ""),
            "type": project_type or existing_data.get("project", {}).get("type", ""),
            "schema_version": SCHEMA_VERSION,
            "created_at": existing_data.get("project", {}).get("created_at", datetime.now().strftime("%Y-%m-%d")),
            "created_with": "studio_project_scaffolder"
        },
        "author": {
            "name": author_name or existing_data.get("author", {}).get("name", ""),
            "studio": studio or existing_data.get("author", {}).get("studio", ""),
            "role": role or existing_data.get("author", {}).get("role", ""),
            "contact": contact or existing_data.get("author", {}).get("contact", ""),
            "copyright": copyright or existing_data.get("author", {}).get("copyright", "")
        }
    }
    
    try:
        metadata_path.write_text(
            json.dumps(metadata, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
        return True
    except Exception:
        return False

