import bpy
import shutil
from bpy.props import StringProperty, EnumProperty
from bpy.types import Operator
from pathlib import Path
from ..core import detector, generator

class STUDIO_OT_ChangeAssetType(Operator):
    bl_idname = "studio.change_asset_type"
    bl_label = "Change Asset Type"
    bl_description = "Change current asset type and move to corresponding folder"
    bl_options = {'REGISTER', 'UNDO'}
    bl_translation_context = "Operator"
    
    def execute(self, context):
        props = context.scene.studio_project_props
        new_asset_type = props.current_asset_type
        if not bpy.data.filepath:
            self.report({'ERROR'}, "File not saved, please save file first")
            return {'CANCELLED'}
        
        current_file = Path(bpy.data.filepath).resolve()
        project_root = detector.find_project_root()
        
        if not project_root:
            self.report({'ERROR'}, "Project root directory not detected")
            return {'CANCELLED'}
        
        old_asset_type = detector.detect_current_asset_type()
        asset_id = detector.get_current_asset_id()
        
        if not old_asset_type or not asset_id:
            self.report({'ERROR'}, "Current file is not in asset directory")
            return {'CANCELLED'}
        
        if old_asset_type == new_asset_type:
            self.report({'INFO'}, "Asset type unchanged")
            return {'FINISHED'}
        
        old_asset_dir = project_root / "01_assets" / old_asset_type / asset_id
        new_asset_dir = project_root / "01_assets" / new_asset_type / asset_id
        
        if not old_asset_dir.exists():
            self.report({'ERROR'}, bpy.app.translations.pgettext_iface(f"Original asset directory does not exist: {old_asset_dir}"))
            return {'CANCELLED'}
        
        if new_asset_dir.exists():
            self.report({'ERROR'}, bpy.app.translations.pgettext_iface(f"Target asset directory already exists: {new_asset_dir}"))
            return {'CANCELLED'}
        
        try:
            bpy.ops.wm.save_mainfile()
            
            rel_path = current_file.relative_to(old_asset_dir)
            new_file_path = new_asset_dir / rel_path
            
            new_asset_dir.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(old_asset_dir), str(new_asset_dir))
            
            bpy.ops.wm.open_mainfile(filepath=str(new_file_path.resolve()))
            
            self.report({'INFO'}, bpy.app.translations.pgettext_iface(f"Asset type changed: {old_asset_type} -> {new_asset_type}"))
            return {'FINISHED'}
        
        except Exception as e:
            self.report({'ERROR'}, bpy.app.translations.pgettext_iface(f"Failed to move asset directory: {str(e)}"))
            return {'CANCELLED'}

