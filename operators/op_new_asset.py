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
            ('char', '角色 (Character)', '角色模型资产，包括主角、配角、NPC等'),
            ('prop', '道具 (Prop)', '道具和非角色模型资产，如武器、工具、家具等'),
            ('env', '环境 (Environment)', '场景和环境资产，如建筑、地形、背景等'),
            ('fx', '特效 (Effects)', '视觉特效资产，如爆炸、火焰、烟雾、粒子等'),
            ('veh', '载具 (Vehicle)', '载具资产，如汽车、飞机、船只等'),
            ('veg', '植被 (Vegetation)', '植被资产，如树木、花草、灌木等'),
            ('light', '灯光 (Light)', '灯光设置资产，如HDRI、灯光预设等'),
        ],
        default='char',
    )
    
    asset_id: StringProperty(
        name="资产ID",
        description="资产标识符（小写、下划线分隔）",
        default="new_asset",
    )
    
    def execute(self, context):
        if not bpy.data.filepath:
            self.report({'ERROR'}, "文件未保存，请先保存文件")
            return {'CANCELLED'}
        
        project_root = detector.find_project_root()
        
        if not project_root:
            self.report({'ERROR'}, "未检测到项目根目录，请先初始化项目")
            return {'CANCELLED'}
        
        success, result, target_file = generator.create_asset_structure(
            project_root,
            self.asset_type,
            self.asset_id
        )
        
        if not success:
            self.report({'ERROR'}, result)
            return {'CANCELLED'}
        
        if target_file and target_file.exists():
            self.report({'ERROR'}, f"目标文件已存在: {target_file}")
            return {'CANCELLED'}
        
        try:
            bpy.ops.wm.save_as_mainfile(filepath=str(target_file))
            self.report({'INFO'}, f"资产结构创建成功，文件已保存: {target_file}")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"保存文件失败: {str(e)}")
            return {'CANCELLED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "asset_type")
        layout.prop(self, "asset_id")

