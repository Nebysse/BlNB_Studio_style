import bpy
import os
from bpy.props import StringProperty, EnumProperty
from bpy.types import Operator
from pathlib import Path
from ..core import generator, metadata, blend_meta

class STUDIO_OT_InitProject(Operator):
    bl_idname = "studio.init_project"
    bl_label = "初始化项目结构"
    bl_description = "创建符合 Blender Studio 规范的项目目录结构"
    bl_options = {'REGISTER', 'UNDO'}
    
    project_code: StringProperty(
        name="项目代号",
        description="项目代号（小写、下划线分隔）",
        default="wing_it",
    )
    
    base_path: StringProperty(
        name="项目根目录",
        description="项目将创建在此目录下",
        default="",
        subtype='DIR_PATH',
    )
    
    project_type: EnumProperty(
        name="项目类型",
        description="选择项目模板类型",
        items=[
            ('single_shot', '单镜头练习', '单镜头练习/小作品'),
            ('short_film', '多镜头短篇', '多镜头短篇项目'),
            ('asset_library', '资产库项目', '纯资产库项目'),
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
            self.report({'ERROR'}, "请指定项目根目录")
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
            
            self.report({'INFO'}, f"项目创建成功: {result}")
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

