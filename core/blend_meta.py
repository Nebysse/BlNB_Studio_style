try:
    import bpy
except ImportError:
    bpy = None

NAMESPACE_PREFIX = "studio_meta"

def get_meta_key(key: str) -> str:
    return f"{NAMESPACE_PREFIX}.{key}"

def _get_window_manager():
    if not bpy:
        return None
    try:
        return bpy.context.window_manager
    except:
        if bpy.data.window_managers:
            return bpy.data.window_managers[0]
        return None

def write_blend_metadata(
    author_name: str = "",
    studio: str = "",
    role: str = "",
    contact: str = "",
    project_code: str = "",
    project_type: str = "",
    copyright: str = "",
    schema_version: int = 1
) -> bool:
    if not bpy:
        return False
    
    wm = _get_window_manager()
    if not wm:
        return False
    
    if author_name:
        wm[get_meta_key("author.name")] = author_name
    if studio:
        wm[get_meta_key("author.studio")] = studio
    if role:
        wm[get_meta_key("author.role")] = role
    if contact:
        wm[get_meta_key("author.contact")] = contact
    if project_code:
        wm[get_meta_key("project.code")] = project_code
    if project_type:
        wm[get_meta_key("project.type")] = project_type
    if copyright:
        wm[get_meta_key("author.copyright")] = copyright
    
    wm[get_meta_key("project.schema_version")] = schema_version
    
    return True

def read_blend_metadata() -> dict:
    if not bpy:
        return {}
    
    wm = _get_window_manager()
    if not wm:
        return {}
    
    return {
        "author_name": wm.get(get_meta_key("author.name"), ""),
        "studio": wm.get(get_meta_key("author.studio"), ""),
        "role": wm.get(get_meta_key("author.role"), ""),
        "contact": wm.get(get_meta_key("author.contact"), ""),
        "project_code": wm.get(get_meta_key("project.code"), ""),
        "project_type": wm.get(get_meta_key("project.type"), ""),
        "copyright": wm.get(get_meta_key("author.copyright"), ""),
        "schema_version": wm.get(get_meta_key("project.schema_version"), 0)
    }

def sync_from_project_metadata() -> bool:
    if not bpy:
        return False
    
    from .metadata import read_project_metadata
    
    project_meta = read_project_metadata()
    if not project_meta:
        return False
    
    author = project_meta.get("author", {})
    project = project_meta.get("project", {})
    
    return write_blend_metadata(
        author_name=author.get("name", ""),
        studio=author.get("studio", ""),
        role=author.get("role", ""),
        contact=author.get("contact", ""),
        project_code=project.get("code", ""),
        project_type=project.get("type", ""),
        copyright=author.get("copyright", ""),
        schema_version=project.get("schema_version", 1)
    )

