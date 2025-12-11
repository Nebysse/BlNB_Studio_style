import bpy
from bpy.props import StringProperty, EnumProperty
from bpy.types import Operator
from pathlib import Path
from ..core import generator, detector

class STUDIO_OT_NewAsset(Operator):
    bl_idname = "studio.new_asset"
    bl_label = "新建资产结构"
    bl_description = "在当前项目中创建新的资产目录结构"
    bl_options = {'REGISTER', 'UNDO'}
    
    asset_type: EnumProperty(
        name="资产类型",
        items=[
            ('char', '角色', '角色资产'),
            ('env', '场景', '场景环境资产'),
            ('prop', '道具', '道具资产'),
            ('fx', '特效', '特效资产'),
        ],
        default='char',
    )
    
    asset_id: StringProperty(
        name="资产ID",
        description="资产标识符（小写、下划线分隔）",
        default="new_asset",
    )
    
    def execute(self, context):
        project_root = detector.find_project_root()
        
        if not project_root:
            self.report({'ERROR'}, "未检测到项目根目录，请先初始化项目")
            return {'CANCELLED'}
        
        success, result = generator.create_asset_structure(
            project_root,
            self.asset_type,
            self.asset_id
        )
        
        if success:
            self.report({'INFO'}, f"资产结构创建成功: {result}")
        else:
            self.report({'ERROR'}, result)
        
        return {'FINISHED'} if success else {'CANCELLED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "asset_type")
        layout.prop(self, "asset_id")

