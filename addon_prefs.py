import bpy
import os
from bpy.props import StringProperty

class StudioProjectAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__
    
    default_project_root: StringProperty(
        name="Default Project Root Directory",
        description="Default root directory for new projects",
        default=os.path.expanduser("~/blender_projects"),
        subtype='DIR_PATH',
    )
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "default_project_root")

