import bpy
import os
from bpy.props import StringProperty, EnumProperty
from bpy.types import Panel, PropertyGroup
from pathlib import Path
from .core import detector

class StudioProjectProperties(PropertyGroup):
    project_code: StringProperty(
        name="项目代号",
        default="",
    )
    
    base_path: StringProperty(
        name="项目根目录",
        default="",
        subtype='DIR_PATH',
    )
    
    project_root_path: StringProperty(
        name="项目根路径",
        default="",
        subtype='DIR_PATH',
    )
    
    project_type: EnumProperty(
        name="项目类型",
        items=[
            ('single_shot', '单镜头练习', ''),
            ('short_film', '多镜头短篇', ''),
            ('asset_library', '资产库项目', ''),
        ],
        default='single_shot',
    )

class STUDIO_PT_ProjectPanel(Panel):
    bl_label = "Studio Project"
    bl_idname = "STUDIO_PT_ProjectPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Studio Project"
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.studio_project_props
        
        project_root = detector.find_project_root()
        
        if project_root:
            box = layout.box()
            box.label(text="当前项目", icon='FILE_FOLDER')
            box.label(text=f"根目录: {project_root}")
            
            project_type = detector.detect_project_type(project_root)
            box.label(text=f"类型: {project_type}")
            
            layout.separator()
            
            row = layout.row()
            row.operator("studio.new_asset", icon='ADD')
            row.operator("studio.new_shot", icon='ADD')
            
            layout.separator()
            
            col = layout.column()
            op1 = col.operator("wm.path_open", text="打开资产目录", icon='FILEBROWSER')
            op1.filepath = str(project_root / "01_assets")
            op2 = col.operator("wm.path_open", text="打开镜头目录", icon='FILEBROWSER')
            op2.filepath = str(project_root / "02_shots")
        else:
            box = layout.box()
            box.label(text="未检测到项目", icon='INFO')
            box.label(text="请初始化新项目")
            
            layout.separator()
            
            layout.label(text="项目设置:")
            layout.prop(props, "project_code")
            layout.prop(props, "base_path")
            layout.prop(props, "project_type")
            
            layout.separator()
            
            op = layout.operator("studio.init_project", text="初始化项目结构", icon='FILE_NEW')
            op.project_code = props.project_code
            op.base_path = props.base_path
            op.project_type = props.project_type

class STUDIO_PT_DirectoryGuide(Panel):
    bl_label = "目录结构说明"
    bl_idname = "STUDIO_PT_DirectoryGuide"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Studio Project"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        
        box = layout.box()
        box.label(text="00_admin/", icon='DOCUMENTS')
        box.label(text="  管理文档、进度表、制片相关文件")
        box.label(text="  - docs/ 生产文档")
        box.label(text="  - spreadsheets/ 进度表")
        box.label(text="  - mgmt/ 制片文件")
        
        layout.separator()
        
        box = layout.box()
        box.label(text="01_assets/", icon='OUTLINER_OB_MESH')
        box.label(text="  资产库目录")
        box.label(text="  - char/ 角色资产")
        box.label(text="  - env/ 场景环境资产")
        box.label(text="  - prop/ 道具资产")
        box.label(text="  - fx/ 特效资产")
        box.label(text="  每个资产包含:")
        box.label(text="    • work/ 工作文件")
        box.label(text="    • publish/ 发布版本")
        box.label(text="    • render/ 渲染输出")
        
        layout.separator()
        
        box = layout.box()
        box.label(text="02_shots/", icon='SEQUENCE')
        box.label(text="  镜头/序列目录")
        box.label(text="  - seq_###/ 序列目录")
        box.label(text="    • sh_####/ 镜头目录")
        box.label(text="      包含:")
        box.label(text="        • work/ 工作文件")
        box.label(text="        • publish/ 发布版本")
        box.label(text="        • cache/ 缓存文件")
        box.label(text="        • render/ 渲染输出")
        
        layout.separator()
        
        box = layout.box()
        box.label(text="03_edit/", icon='SOUND')
        box.label(text="  剪辑和音频相关文件")
        box.label(text="  - audio/ 音频文件")
        box.label(text="  - timelines/ 时间线文件")
        
        layout.separator()
        
        box = layout.box()
        box.label(text="04_renders/", icon='RENDER_RESULT')
        box.label(text="  最终渲染输出")
        box.label(text="  - preview/ 预览版本")
        box.label(text="  - final/ 最终交付")
        
        layout.separator()
        
        box = layout.box()
        box.label(text="05_lib/", icon='LIBRARY_DATA_DIRECT')
        box.label(text="  外部资源库")
        box.label(text="  - textures/ 贴图")
        box.label(text="  - hdri/ 环境贴图")
        box.label(text="  - scripts/ 脚本")
        box.label(text="  - fonts/ 字体")
        
        layout.separator()
        
        box = layout.box()
        box.label(text="90_temp/", icon='FILE_BACKUP')
        box.label(text="  临时文件目录")
        
        layout.separator()
        
        box = layout.box()
        box.label(text="prod/", icon='FILEBLEND')
        box.label(text="  项目级主工程文件")
        box.label(text="  - project_overview_v001.blend")
        box.label(text="  - project_settings.json")
        
        layout.separator()
        
        box = layout.box()
        box.label(text="文件命名规范:", icon='TEXT')
        box.label(text="格式: <scope>_<subject>_<task>_v###.blend")
        box.label(text="示例:")
        box.label(text="  • char_hero_boy_model_v001.blend")
        box.label(text="  • shot_seq010sh0010_anim_v012.blend")

