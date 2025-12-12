import bpy
import os
from bpy.props import StringProperty, EnumProperty
from bpy.types import Panel, PropertyGroup
from pathlib import Path
from .core import detector, metadata, blend_meta, naming

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
    
    current_asset_type: EnumProperty(
        name="当前资产类型",
        items=[
            ('char', '角色 (Character)', ''),
            ('prop', '道具 (Prop)', ''),
            ('env', '环境 (Environment)', ''),
            ('fx', '特效 (Effects)', ''),
            ('veh', '载具 (Vehicle)', ''),
            ('veg', '植被 (Vegetation)', ''),
            ('light', '灯光 (Light)', ''),
        ],
        default='char',
    )

class StudioProjectIdentityProperties(PropertyGroup):
    author_name: StringProperty(
        name="Author Name",
        default="",
    )
    
    studio: StringProperty(
        name="Studio / Team",
        default="",
    )
    
    role: StringProperty(
        name="Role",
        default="",
    )
    
    contact: StringProperty(
        name="Contact",
        default="",
    )
    
    project_code: StringProperty(
        name="Project Code",
        default="",
    )
    
    project_type: EnumProperty(
        name="Project Type",
        items=[
            ('single_shot', '单镜头练习', ''),
            ('short_film', '多镜头短篇', ''),
            ('asset_library', '资产库项目', ''),
        ],
        default='single_shot',
    )
    
    copyright: StringProperty(
        name="Copyright",
        default="",
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
            if bpy.data.filepath:
                file_path = Path(bpy.data.filepath)
                domain = naming.detect_domain_from_path(file_path)
                if domain:
                    filename = file_path.name
                    is_valid, error_msg = naming.validate_filename_by_domain(filename, domain, file_path)
                    if not is_valid:
                        hint_box = layout.box()
                        hint_box.label(text="💡 命名规范提醒", icon='INFO')
                        hint_box.label(text=error_msg)
                        layout.separator()
            
            box = layout.box()
            box.label(text="当前项目")
            box.label(text=f"根目录: {project_root}")
            
            project_type = detector.detect_project_type(project_root)
            box.label(text=f"类型: {project_type}")
            
            current_asset_type = detector.detect_current_asset_type()
            if current_asset_type:
                box.separator()
                box.label(text=f"当前资产类型: {current_asset_type}")
                asset_id = detector.get_current_asset_id()
                if asset_id:
                    box.label(text=f"资产ID: {asset_id}")
                box.prop(props, "current_asset_type", text="修改为")
                if props.current_asset_type != current_asset_type:
                    box.operator("studio.change_asset_type", text="应用修改并移动")
            
            layout.separator()
            
            row = layout.row()
            row.operator("studio.new_asset")
            row.operator("studio.new_shot")
            
            layout.separator()
            
            col = layout.column()
            op1 = col.operator("wm.path_open", text="打开资产目录")
            op1.filepath = str(project_root / "01_assets")
            op2 = col.operator("wm.path_open", text="打开镜头目录")
            op2.filepath = str(project_root / "02_shots")
        else:
            box = layout.box()
            box.label(text="未检测到项目")
            box.label(text="请初始化新项目")
            
            layout.separator()
            
            layout.label(text="项目设置:")
            layout.prop(props, "project_code")
            layout.prop(props, "base_path")
            layout.prop(props, "project_type")
            
            layout.separator()
            
            op = layout.operator("studio.init_project", text="初始化项目结构")
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
        box.label(text="00_admin/")
        box.label(text="  管理文档、进度表、制片相关文件")
        box.label(text="  - docs/ 生产文档")
        box.label(text="  - spreadsheets/ 进度表")
        box.label(text="  - mgmt/ 制片文件")
        
        layout.separator()
        
        box = layout.box()
        box.label(text="01_assets/")
        box.label(text="  资产库目录")
        box.label(text="  - char/ 角色资产 (Character)")
        box.label(text="  - prop/ 道具资产 (Prop)")
        box.label(text="  - env/ 环境资产 (Environment)")
        box.label(text="  - fx/ 特效资产 (Effects)")
        box.label(text="  - veh/ 载具资产 (Vehicle)")
        box.label(text="  - veg/ 植被资产 (Vegetation)")
        box.label(text="  - light/ 灯光资产 (Light)")
        box.label(text="  每个资产包含:")
        box.label(text="    • work/ 工作文件")
        box.label(text="    • publish/ 发布版本")
        box.label(text="    • render/ 渲染输出 (fx为cache/)")
        
        layout.separator()
        
        box = layout.box()
        box.label(text="02_shots/")
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
        box.label(text="03_edit/")
        box.label(text="  剪辑和音频相关文件")
        box.label(text="  - audio/ 音频文件")
        box.label(text="  - timelines/ 时间线文件")
        
        layout.separator()
        
        box = layout.box()
        box.label(text="04_renders/")
        box.label(text="  最终渲染输出")
        box.label(text="  - preview/ 预览版本")
        box.label(text="  - final/ 最终交付")
        
        layout.separator()
        
        box = layout.box()
        box.label(text="05_lib/")
        box.label(text="  外部资源库")
        box.label(text="  - textures/ 贴图")
        box.label(text="  - hdri/ 环境贴图")
        box.label(text="  - scripts/ 脚本")
        box.label(text="  - fonts/ 字体")
        
        layout.separator()
        
        box = layout.box()
        box.label(text="90_temp/")
        box.label(text="  临时文件目录")
        
        layout.separator()
        
        box = layout.box()
        box.label(text="prod/")
        box.label(text="  项目级主工程文件")
        box.label(text="  - project_overview_v001.blend")
        box.label(text="  - project_settings.json")
        
        layout.separator()
        
        box = layout.box()
        box.label(text="文件命名规范:")
        box.label(text="格式: <scope>_<subject>_<task>_v###.blend")
        box.label(text="示例:")
        box.label(text="  • char_hero_boy_model_v001.blend")
        box.label(text="  • shot_seq010sh0010_anim_v012.blend")

class STUDIO_PT_ProjectIdentity(Panel):
    bl_label = "Project Identity"
    bl_idname = "STUDIO_PT_ProjectIdentity"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Studio Project"
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.studio_project_identity_props
        
        blend_meta_data = blend_meta.read_blend_metadata()
        project_root = detector.find_project_root()
        project_meta = None
        if project_root:
            project_meta = metadata.read_project_metadata(project_root)
        
        has_file_meta = bool(blend_meta_data.get("author_name") or blend_meta_data.get("project_code"))
        has_project_meta = bool(project_meta)
        
        if has_file_meta or has_project_meta:
            row = layout.row()
            row.operator("studio.load_identity_to_editor", text="加载到编辑器", icon='IMPORT')
            if has_file_meta:
                row.label(text="", icon='FILE_BLEND')
            if has_project_meta:
                row.label(text="", icon='FILE_FOLDER')
        
        layout.separator()
        
        box = layout.box()
        box.label(text="Author 信息")
        box.prop(props, "author_name")
        box.prop(props, "studio")
        box.prop(props, "role")
        box.prop(props, "contact")
        
        layout.separator()
        
        box = layout.box()
        box.label(text="Project 信息")
        box.prop(props, "project_code")
        box.prop(props, "project_type")
        box.prop(props, "copyright")
        
        layout.separator()
        
        col = layout.column()
        col.operator("studio.write_to_project_metadata", text="写入项目元数据")
        col.operator("studio.write_to_current_blend", text="写入当前文件")
        
        if project_meta:
            col.operator("studio.sync_from_project_metadata", text="从项目元数据同步")

