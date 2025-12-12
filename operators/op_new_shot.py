import bpy
from bpy.props import StringProperty
from bpy.types import Operator
from pathlib import Path
from ..core import generator, detector

class STUDIO_OT_NewShot(Operator):
    bl_idname = "studio.new_shot"
    bl_label = "新建镜头结构"
    bl_description = "在当前项目中创建新的镜头目录结构"
    bl_options = {'REGISTER', 'UNDO'}
    
    seq_id: StringProperty(
        name="序列ID",
        description="序列标识符（如 010 或 seq_010）",
        default="010",
    )
    
    shot_id: StringProperty(
        name="镜头ID",
        description="镜头标识符（如 0010 或 sh_0010）",
        default="0010",
    )
    
    def execute(self, context):
        if not bpy.data.filepath:
            self.report({'ERROR'}, "文件未保存，请先保存文件")
            return {'CANCELLED'}
        
        project_root = detector.find_project_root()
        
        if not project_root:
            self.report({'ERROR'}, "未检测到项目根目录，请先初始化项目")
            return {'CANCELLED'}
        
        success, result, target_file = generator.create_shot_structure(
            project_root,
            self.seq_id,
            self.shot_id
        )
        
        if not success:
            self.report({'ERROR'}, result)
            return {'CANCELLED'}
        
        if target_file and target_file.exists():
            self.report({'ERROR'}, f"目标文件已存在: {target_file}")
            return {'CANCELLED'}
        
        try:
            bpy.ops.wm.save_as_mainfile(filepath=str(target_file))
            self.report({'INFO'}, f"镜头结构创建成功，文件已保存: {target_file}")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"保存文件失败: {str(e)}")
            return {'CANCELLED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "seq_id")
        layout.prop(self, "shot_id")

