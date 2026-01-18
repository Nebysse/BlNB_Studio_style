import bpy
import os
from bpy.props import StringProperty, EnumProperty
from bpy.types import Operator
from pathlib import Path
from ..core import generator, metadata, blend_meta

class STUDIO_OT_InitProject(Operator):
    bl_idname = "studio.init_project"
    bl_label = "Initialize Project Structure"
    bl_description = "Create project directory structure conforming to Blender Studio standards"
    bl_options = {'REGISTER', 'UNDO'}
    bl_translation_context = "Operator"
    
    project_code: StringProperty(
        name="Project Code",
        description="Project code (lowercase, underscore separated)",
        default="wing_it",
    )
    
    base_path: StringProperty(
        name="Project Root Directory",
        description="Directory where the project will be created",
        default="",
        subtype='DIR_PATH',
    )
    
    project_type: EnumProperty(
        name="Project Type",
        description="Select project template type",
        items=[
            ('single_shot', 'Single Shot Practice', 'Single shot practice/small work'),
            ('short_film', 'Multi-Shot Short Film', 'Multi-shot short film project'),
            ('asset_library', 'Asset Library Project', 'Pure asset library project'),
        ],
        default='single_shot',
    )
    
    def execute(self, context):
        addon_name = __package__.split('.')[0] if '.' in __package__ else __package__
        prefs = context.preferences.addons[addon_name].preferences
        
        base_path = self.base_path
        if not base_path:
            base_path = prefs.default_project_root
        
        if not base_path:
            self.report({'ERROR'}, "Please specify project root directory")
            return {'CANCELLED'}
        
        success, result = generator.create_project(
            base_path,
            self.project_code,
            self.project_type
        )
        
        if success:
            project_root = Path(result)
            identity_props = context.scene.studio_project_identity_props
            
            metadata.write_project_metadata(
                project_root=project_root,
                author_name=identity_props.author_name or "",
                studio=identity_props.studio or "",
                role=identity_props.role or "",
                contact=identity_props.contact or "",
                project_code=self.project_code,
                project_type=self.project_type,
                copyright=identity_props.copyright or ""
            )
            
            blend_meta.write_blend_metadata(
                author_name=identity_props.author_name or "",
                studio=identity_props.studio or "",
                role=identity_props.role or "",
                contact=identity_props.contact or "",
                project_code=self.project_code,
                project_type=self.project_type,
                copyright=identity_props.copyright or ""
            )
            
            self.report({'INFO'}, bpy.app.translations.pgettext_iface(f"Project created successfully: {result}"))
            context.scene.studio_project_props.project_code = self.project_code
            context.scene.studio_project_props.base_path = base_path
            context.scene.studio_project_props.project_root_path = result
            context.scene.studio_project_props.project_type = self.project_type
        else:
            self.report({'ERROR'}, result)
        
        return {'FINISHED'} if success else {'CANCELLED'}
    
    def invoke(self, context, event):
        addon_name = __package__.split('.')[0] if '.' in __package__ else __package__
        prefs = context.preferences.addons[addon_name].preferences
        if not self.base_path:
            self.base_path = prefs.default_project_root
        
        return context.window_manager.invoke_props_dialog(self, width=400)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "project_code")
        layout.prop(self, "base_path")
        layout.prop(self, "project_type")

