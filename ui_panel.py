import bpy
import os
from bpy.props import StringProperty, EnumProperty
from bpy.types import Panel, PropertyGroup
from pathlib import Path
from .core import detector, metadata, blend_meta, naming

class StudioProjectProperties(PropertyGroup):
    project_code: StringProperty(
        name="Project Code",
        default="",
    )
    
    base_path: StringProperty(
        name="Project Root Directory",
        default="",
        subtype='DIR_PATH',
    )
    
    project_root_path: StringProperty(
        name="Project Root Path",
        default="",
        subtype='DIR_PATH',
    )
    
    project_type: EnumProperty(
        name="Project Type",
        items=[
            ('single_shot', 'Single Shot Practice', ''),
            ('short_film', 'Multi-Shot Short Film', ''),
            ('asset_library', 'Asset Library Project', ''),
        ],
        default='single_shot',
    )
    
    current_asset_type: EnumProperty(
        name="Current Asset Type",
        items=[
            ('char', 'Character (Character)', ''),
            ('prop', 'Prop (Prop)', ''),
            ('env', 'Environment (Environment)', ''),
            ('fx', 'Effects (Effects)', ''),
            ('veh', 'Vehicle (Vehicle)', ''),
            ('veg', 'Vegetation (Vegetation)', ''),
            ('light', 'Light (Light)', ''),
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
    bl_translation_context = "*"
    
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
                        hint_box.label(text="💡 Naming Convention Reminder", icon='INFO')
                        hint_box.label(text=error_msg)
                        layout.separator()
            
            box = layout.box()
            box.label(text="Current Project")
            box.label(text=bpy.app.translations.pgettext_iface(f"Root Directory: {project_root}"))
            
            project_type = detector.detect_project_type(project_root)
            box.label(text=bpy.app.translations.pgettext_iface(f"Type: {project_type}"))
            
            current_asset_type = detector.detect_current_asset_type()
            if current_asset_type:
                box.separator()
                box.label(text=bpy.app.translations.pgettext_iface(f"Current Asset Type: {current_asset_type}"))
                asset_id = detector.get_current_asset_id()
                if asset_id:
                    box.label(text=bpy.app.translations.pgettext_iface(f"Asset ID: {asset_id}"))
                box.prop(props, "current_asset_type", text="Change to")
                if props.current_asset_type != current_asset_type:
                    box.operator("studio.change_asset_type", text="Apply Changes and Move")
            
            layout.separator()
            
            row = layout.row()
            row.operator("studio.new_asset")
            row.operator("studio.new_shot")
            
            layout.separator()
            
            col = layout.column()
            op1 = col.operator("wm.path_open", text="Open Asset Directory")
            op1.filepath = str(project_root / "01_assets")
            op2 = col.operator("wm.path_open", text="Open Shot Directory")
            op2.filepath = str(project_root / "02_shots")
        else:
            box = layout.box()
            box.label(text="No project detected")
            box.label(text="Please initialize new project")
            
            layout.separator()
            
            layout.label(text="Project Settings:")
            layout.prop(props, "project_code")
            layout.prop(props, "base_path")
            layout.prop(props, "project_type")
            
            layout.separator()
            
            op = layout.operator("studio.init_project", text="Initialize Project Structure")
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
        box.label(text="  Management documents, schedules, production-related files")
        box.label(text="  - docs/ Production documents")
        box.label(text="  - spreadsheets/ Schedules")
        box.label(text="  - mgmt/ Production files")
        
        layout.separator()
        
        box = layout.box()
        box.label(text="01_assets/")
        box.label(text="  Asset library directory")
        box.label(text="  - char/ Character assets (Character)")
        box.label(text="  - prop/ Prop assets (Prop)")
        box.label(text="  - env/ Environment assets (Environment)")
        box.label(text="  - fx/ Effects assets (Effects)")
        box.label(text="  - veh/ Vehicle assets (Vehicle)")
        box.label(text="  - veg/ Vegetation assets (Vegetation)")
        box.label(text="  - light/ Lighting assets (Light)")
        box.label(text="  Each asset contains:")
        box.label(text="    • work/ Work files")
        box.label(text="    • publish/ Published versions")
        box.label(text="    • render/ Render output (fx is cache/)")
        
        layout.separator()
        
        box = layout.box()
        box.label(text="02_shots/")
        box.label(text="  Shot/sequence directory")
        box.label(text="  - seq_###/ Sequence directory")
        box.label(text="    • sh_####/ Shot directory")
        box.label(text="      Contains:")
        box.label(text="        • work/ Work files")
        box.label(text="        • publish/ Published versions")
        box.label(text="        • cache/ Cache files")
        box.label(text="        • render/ Render output")
        
        layout.separator()
        
        box = layout.box()
        box.label(text="03_edit/")
        box.label(text="  Editing and audio related files")
        box.label(text="  - audio/ Audio files")
        box.label(text="  - timelines/ Timeline files")
        
        layout.separator()
        
        box = layout.box()
        box.label(text="04_renders/")
        box.label(text="  Final render output")
        box.label(text="  - preview/ Preview version")
        box.label(text="  - final/ Final delivery")
        
        layout.separator()
        
        box = layout.box()
        box.label(text="05_lib/")
        box.label(text="  External resource library")
        box.label(text="  - textures/ Textures")
        box.label(text="  - hdri/ Environment maps")
        box.label(text="  - scripts/ Scripts")
        box.label(text="  - fonts/ Fonts")
        
        layout.separator()
        
        box = layout.box()
        box.label(text="90_temp/")
        box.label(text="  Temporary file directory")
        
        layout.separator()
        
        box = layout.box()
        box.label(text="prod/")
        box.label(text="  Project-level main project files")
        box.label(text="  - project_overview_v001.blend")
        box.label(text="  - project_settings.json")
        
        layout.separator()
        
        box = layout.box()
        box.label(text="File Naming Convention:")
        box.label(text="Format: <scope>_<subject>_<task>_v###.blend")
        box.label(text="Examples:")
        box.label(text="  • char_hero_boy_model_v001.blend")
        box.label(text="  • shot_seq010sh0010_anim_v012.blend")

class STUDIO_PT_ProjectIdentity(Panel):
    bl_label = "Project Identity"
    bl_idname = "STUDIO_PT_ProjectIdentity"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Studio Project"
    bl_translation_context = "*"
    
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
            row.operator("studio.load_identity_to_editor", text="Load to Editor", icon='IMPORT')
            if has_file_meta:
                row.label(text="", icon='FILE_BLEND')
            if has_project_meta:
                row.label(text="", icon='FILE_FOLDER')
        
        layout.separator()
        
        box = layout.box()
        box.label(text="Author Information")
        box.prop(props, "author_name")
        box.prop(props, "studio")
        box.prop(props, "role")
        box.prop(props, "contact")
        
        layout.separator()
        
        box = layout.box()
        box.label(text="Project Information")
        box.prop(props, "project_code")
        box.prop(props, "project_type")
        box.prop(props, "copyright")
        
        layout.separator()
        
        col = layout.column()
        col.operator("studio.write_to_project_metadata", text="Write to Project Metadata")
        col.operator("studio.write_to_current_blend", text="Write to Current File")
        
        if project_meta:
            col.operator("studio.sync_from_project_metadata", text="Sync from Project Metadata")

