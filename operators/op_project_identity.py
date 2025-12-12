import bpy
from bpy.types import Operator
from pathlib import Path
from ..core import metadata, blend_meta, detector

class STUDIO_OT_WriteToProjectMetadata(Operator):
    bl_idname = "studio.write_to_project_metadata"
    bl_label = "写入项目元数据"
    bl_description = "将当前身份信息写入 project.json"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.studio_project_identity_props
        
        project_root = detector.find_project_root()
        if not project_root:
            self.report({'ERROR'}, "未检测到项目根目录")
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
            self.report({'INFO'}, "项目元数据已更新")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "写入项目元数据失败")
            return {'CANCELLED'}

class STUDIO_OT_WriteToCurrentBlend(Operator):
    bl_idname = "studio.write_to_current_blend"
    bl_label = "写入当前文件"
    bl_description = "将身份信息写入当前 .blend 文件的 Custom Properties"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        if not bpy.data.filepath:
            self.report({'ERROR'}, "文件未保存，请先保存文件")
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
            self.report({'INFO'}, "文件元数据已更新")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "写入文件元数据失败")
            return {'CANCELLED'}

class STUDIO_OT_SyncFromProjectMetadata(Operator):
    bl_idname = "studio.sync_from_project_metadata"
    bl_label = "从项目元数据同步"
    bl_description = "用 project.json 覆盖当前 .blend 的身份信息"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        if not bpy.data.filepath:
            self.report({'ERROR'}, "文件未保存，请先保存文件")
            return {'CANCELLED'}
        
        project_meta = metadata.read_project_metadata()
        if not project_meta:
            self.report({'ERROR'}, "未找到项目元数据文件")
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
            
            self.report({'INFO'}, "已从项目元数据同步")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "同步失败")
            return {'CANCELLED'}

class STUDIO_OT_LoadToEditor(Operator):
    bl_idname = "studio.load_identity_to_editor"
    bl_label = "加载到编辑器"
    bl_description = "从文件或项目元数据加载身份信息到编辑器"
    bl_options = {'REGISTER', 'UNDO'}
    
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
                self.report({'INFO'}, "已从文件元数据加载")
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
                self.report({'INFO'}, "已从项目元数据加载")
            else:
                self.report({'WARNING'}, "未找到可用的身份信息")
            
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"加载失败: {str(e)}")
            return {'CANCELLED'}

