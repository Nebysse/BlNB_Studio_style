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
from .operators import op_init_project, op_new_asset, op_new_shot

classes = [
    addon_prefs.StudioProjectAddonPreferences,
    ui_panel.StudioProjectProperties,
    op_init_project.STUDIO_OT_InitProject,
    op_new_asset.STUDIO_OT_NewAsset,
    op_new_shot.STUDIO_OT_NewShot,
    ui_panel.STUDIO_PT_ProjectPanel,
    ui_panel.STUDIO_PT_DirectoryGuide,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.studio_project_props = bpy.props.PointerProperty(
        type=ui_panel.StudioProjectProperties
    )

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.studio_project_props

