import bpy
from bpy.types import Operator
from pathlib import Path
from ..core import metadata, blend_meta, detector

class STUDIO_OT_WriteToProjectMetadata(Operator):
    bl_idname = "studio.write_to_project_metadata"
    bl_label = "Write to Project Metadata"
    bl_description = "Write current identity information to project.json"
    bl_options = {'REGISTER', 'UNDO'}
    bl_translation_context = "Operator"
    
    def execute(self, context):
        props = context.scene.studio_project_identity_props
        
        project_root = detector.find_project_root()
        if not project_root:
            self.report({'ERROR'}, "Project root directory not detected")
            return {'CANCELLED'}
        
        if not metadata.is_project_root(project_root):
            metadata.create_project_marker(project_root)
        
        success = metadata.write_project_metadata(
            project_root=project_root,
            author_name=props.author_name,
            studio=props.studio,
            role=props.role,
            contact=props.contact,
            project_code=props.project_code,
            project_type=props.project_type,
            copyright=props.copyright
        )
        
        if success:
            self.report({'INFO'}, "Project metadata updated")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "Failed to write project metadata")
            return {'CANCELLED'}

class STUDIO_OT_WriteToCurrentBlend(Operator):
    bl_idname = "studio.write_to_current_blend"
    bl_label = "Write to Current File"
    bl_description = "Write identity information to current .blend file's Custom Properties"
    bl_options = {'REGISTER', 'UNDO'}
    bl_translation_context = "Operator"
    
    def execute(self, context):
        if not bpy.data.filepath:
            self.report({'ERROR'}, "File not saved, please save file first")
            return {'CANCELLED'}
        
        props = context.scene.studio_project_identity_props
        
        success = blend_meta.write_blend_metadata(
            author_name=props.author_name,
            studio=props.studio,
            role=props.role,
            contact=props.contact,
            project_code=props.project_code,
            project_type=props.project_type,
            copyright=props.copyright
        )
        
        if success:
            self.report({'INFO'}, "File metadata updated")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "Failed to write file metadata")
            return {'CANCELLED'}

class STUDIO_OT_SyncFromProjectMetadata(Operator):
    bl_idname = "studio.sync_from_project_metadata"
    bl_label = "Sync from Project Metadata"
    bl_description = "Overwrite current .blend identity information with project.json"
    bl_options = {'REGISTER', 'UNDO'}
    bl_translation_context = "Operator"
    
    def execute(self, context):
        if not bpy.data.filepath:
            self.report({'ERROR'}, "File not saved, please save file first")
            return {'CANCELLED'}
        
        project_meta = metadata.read_project_metadata()
        if not project_meta:
            self.report({'ERROR'}, "Project metadata file not found")
            return {'CANCELLED'}
        
        success = blend_meta.sync_from_project_metadata()
        
        if success:
            props = context.scene.studio_project_identity_props
            author = project_meta.get("author", {})
            project = project_meta.get("project", {})
            
            props.author_name = author.get("name", "")
            props.studio = author.get("studio", "")
            props.role = author.get("role", "")
            props.contact = author.get("contact", "")
            props.project_code = project.get("code", "")
            props.project_type = project.get("type", "")
            props.copyright = author.get("copyright", "")
            
            self.report({'INFO'}, "Synced from project metadata")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "Sync failed")
            return {'CANCELLED'}

class STUDIO_OT_LoadToEditor(Operator):
    bl_idname = "studio.load_identity_to_editor"
    bl_label = "Load to Editor"
    bl_description = "Load identity information from file or project metadata to editor"
    bl_options = {'REGISTER', 'UNDO'}
    bl_translation_context = "Operator"
    
    def execute(self, context):
        try:
            props = context.scene.studio_project_identity_props
            
            blend_meta_data = blend_meta.read_blend_metadata()
            project_root = detector.find_project_root()
            project_meta = None
            if project_root:
                project_meta = metadata.read_project_metadata(project_root)
            
            valid_project_types = ['single_shot', 'short_film', 'asset_library']
            
            if blend_meta_data.get("author_name") or blend_meta_data.get("project_code"):
                props.author_name = blend_meta_data.get("author_name", "")
                props.studio = blend_meta_data.get("studio", "")
                props.role = blend_meta_data.get("role", "")
                props.contact = blend_meta_data.get("contact", "")
                props.project_code = blend_meta_data.get("project_code", "")
                project_type = blend_meta_data.get("project_type", "single_shot")
                if project_type in valid_project_types:
                    props.project_type = project_type
                else:
                    props.project_type = "single_shot"
                props.copyright = blend_meta_data.get("copyright", "")
                self.report({'INFO'}, "Loaded from file metadata")
            elif project_meta:
                author = project_meta.get("author", {})
                project = project_meta.get("project", {})
                
                props.author_name = author.get("name", "")
                props.studio = author.get("studio", "")
                props.role = author.get("role", "")
                props.contact = author.get("contact", "")
                props.project_code = project.get("code", "")
                project_type = project.get("type", "single_shot")
                if project_type in valid_project_types:
                    props.project_type = project_type
                else:
                    props.project_type = "single_shot"
                props.copyright = author.get("copyright", "")
                self.report({'INFO'}, "Loaded from project metadata")
            else:
                self.report({'WARNING'}, "No available identity information found")
            
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, bpy.app.translations.pgettext_iface(f"Load failed: {str(e)}"))
            return {'CANCELLED'}

