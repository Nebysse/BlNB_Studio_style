import bpy
from bpy.props import StringProperty
from bpy.types import Operator
from pathlib import Path
from ..core import generator, detector, naming

class STUDIO_OT_NewShot(Operator):
    bl_idname = "studio.new_shot"
    bl_label = "New Shot Structure"
    bl_description = "Create new shot directory structure in current project"
    bl_options = {'REGISTER', 'UNDO'}
    bl_translation_context = "Operator"
    
    seq_id: StringProperty(
        name="Sequence ID",
        description="Sequence identifier (e.g., 010 or seq_010)",
        default="010",
    )
    
    shot_id: StringProperty(
        name="Shot ID",
        description="Shot identifier (e.g., 0010 or sh_0010)",
        default="0010",
    )
    
    def execute(self, context):
        if not bpy.data.filepath:
            self.report({'ERROR'}, "File not saved, please save file first")
            return {'CANCELLED'}
        
        project_root = detector.find_project_root()
        
        if not project_root:
            self.report({'ERROR'}, "Project root directory not detected, please initialize project first")
            return {'CANCELLED'}
        
        success, result, target_file = generator.create_shot_structure(
            project_root,
            self.seq_id,
            self.shot_id
        )
        
        if not success:
            self.report({'ERROR'}, result)
            return {'CANCELLED'}
        
        if target_file:
            is_valid, error_msg = naming.validate_shot_filename(target_file.name)
            if not is_valid:
                self.report({'INFO'}, bpy.app.translations.pgettext_iface(f"Naming reminder: {error_msg}"))
            
            if target_file.exists():
                self.report({'ERROR'}, bpy.app.translations.pgettext_iface(f"Target file already exists: {target_file}"))
                return {'CANCELLED'}
        
        try:
            bpy.ops.wm.save_as_mainfile(filepath=str(target_file))
            self.report({'INFO'}, bpy.app.translations.pgettext_iface(f"Shot structure created successfully, file saved: {target_file}"))
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, bpy.app.translations.pgettext_iface(f"Failed to save file: {str(e)}"))
            return {'CANCELLED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "seq_id")
        layout.prop(self, "shot_id")

