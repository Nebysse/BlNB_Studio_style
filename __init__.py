bl_info = {
    "name": "Studio Project Scaffolder",
    "author": "nebysse (岚苍穹)",
    "version": (1, 0, 0),
    "blender": (4, 5, 0),
    "location": "View3D > N-Panel > Studio Project",
    "description": "创建符合 Blender Studio 规范的项目目录结构\n作者: 岚苍穹\n哔哩哔哩: https://b23.tv/yQkgpAf",
    "category": "Project",
}

import bpy
from . import addon_prefs
from . import ui_panel
from .operators import op_init_project, op_new_asset, op_new_shot, op_change_asset_type, op_project_identity

classes = [
    addon_prefs.StudioProjectAddonPreferences,
    ui_panel.StudioProjectProperties,
    ui_panel.StudioProjectIdentityProperties,
    op_init_project.STUDIO_OT_InitProject,
    op_new_asset.STUDIO_OT_NewAsset,
    op_new_shot.STUDIO_OT_NewShot,
    op_change_asset_type.STUDIO_OT_ChangeAssetType,
    op_project_identity.STUDIO_OT_WriteToProjectMetadata,
    op_project_identity.STUDIO_OT_WriteToCurrentBlend,
    op_project_identity.STUDIO_OT_SyncFromProjectMetadata,
    op_project_identity.STUDIO_OT_LoadToEditor,
    ui_panel.STUDIO_PT_ProjectPanel,
    ui_panel.STUDIO_PT_DirectoryGuide,
    ui_panel.STUDIO_PT_ProjectIdentity,
]

def on_save_pre(scene):
    from .core import metadata, blend_meta, detector, naming
    from pathlib import Path
    
    if not bpy.data.filepath:
        return
    
    file_path = Path(bpy.data.filepath)
    if not file_path.suffix == ".blend":
        return
    
    project_root = detector.find_project_root()
    if not project_root:
        return
    
    domain = naming.detect_domain_from_path(file_path)
    if domain:
        filename = file_path.name
        is_valid, error_msg = naming.validate_filename_by_domain(filename, domain, file_path)
        if not is_valid:
            if not hasattr(bpy.types.Scene, 'studio_naming_hint'):
                bpy.types.Scene.studio_naming_hint = bpy.props.StringProperty()
            scene.studio_naming_hint = error_msg
    
    project_meta = metadata.read_project_metadata(project_root)
    if project_meta:
        blend_meta.sync_from_project_metadata()

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.studio_project_props = bpy.props.PointerProperty(
        type=ui_panel.StudioProjectProperties
    )
    bpy.types.Scene.studio_project_identity_props = bpy.props.PointerProperty(
        type=ui_panel.StudioProjectIdentityProperties
    )
    
    if on_save_pre not in bpy.app.handlers.save_pre:
        bpy.app.handlers.save_pre.append(on_save_pre)

def unregister():
    if on_save_pre in bpy.app.handlers.save_pre:
        bpy.app.handlers.save_pre.remove(on_save_pre)
    
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.studio_project_props
    del bpy.types.Scene.studio_project_identity_props

