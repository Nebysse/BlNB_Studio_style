import bpy
import os
from bpy.props import StringProperty

class StudioProjectAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__
    
    default_project_root: StringProperty(
        name="默认项目根目录",
        description="新建项目时的默认根目录",
        default=os.path.expanduser("~/blender_projects"),
        subtype='DIR_PATH',
    )
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "default_project_root")

