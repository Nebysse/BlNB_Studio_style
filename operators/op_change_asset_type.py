import bpy
import shutil
from bpy.props import StringProperty, EnumProperty
from bpy.types import Operator
from pathlib import Path
from ..core import detector, generator

class STUDIO_OT_ChangeAssetType(Operator):
    bl_idname = "studio.change_asset_type"
    bl_label = "修改资产类型"
    bl_description = "修改当前资产的类型并移动到对应文件夹"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.studio_project_props
        new_asset_type = props.current_asset_type
        if not bpy.data.filepath:
            self.report({'ERROR'}, "文件未保存，请先保存文件")
            return {'CANCELLED'}
        
        current_file = Path(bpy.data.filepath).resolve()
        project_root = detector.find_project_root()
        
        if not project_root:
            self.report({'ERROR'}, "未检测到项目根目录")
            return {'CANCELLED'}
        
        old_asset_type = detector.detect_current_asset_type()
        asset_id = detector.get_current_asset_id()
        
        if not old_asset_type or not asset_id:
            self.report({'ERROR'}, "当前文件不在资产目录中")
            return {'CANCELLED'}
        
        if old_asset_type == new_asset_type:
            self.report({'INFO'}, "资产类型未改变")
            return {'FINISHED'}
        
        old_asset_dir = project_root / "01_assets" / old_asset_type / asset_id
        new_asset_dir = project_root / "01_assets" / new_asset_type / asset_id
        
        if not old_asset_dir.exists():
            self.report({'ERROR'}, f"原资产目录不存在: {old_asset_dir}")
            return {'CANCELLED'}
        
        if new_asset_dir.exists():
            self.report({'ERROR'}, f"目标资产目录已存在: {new_asset_dir}")
            return {'CANCELLED'}
        
        try:
            bpy.ops.wm.save_mainfile()
            
            rel_path = current_file.relative_to(old_asset_dir)
            new_file_path = new_asset_dir / rel_path
            
            new_asset_dir.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(old_asset_dir), str(new_asset_dir))
            
            bpy.ops.wm.open_mainfile(filepath=str(new_file_path.resolve()))
            
            self.report({'INFO'}, f"资产类型已修改: {old_asset_type} -> {new_asset_type}")
            return {'FINISHED'}
        
        except Exception as e:
            self.report({'ERROR'}, f"移动资产目录失败: {str(e)}")
            return {'CANCELLED'}

