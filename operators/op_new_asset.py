import bpy
from bpy.props import StringProperty, EnumProperty
from bpy.types import Operator
from pathlib import Path
from ..core import generator, detector, naming

class STUDIO_OT_NewAsset(Operator):
    bl_idname = "studio.new_asset"
    bl_label = "New Asset Structure"
    bl_description = "Create new asset directory structure in current project"
    bl_options = {'REGISTER', 'UNDO'}
    bl_translation_context = "Operator"
    
    asset_type: EnumProperty(
        name="Asset Type",
        items=[
            ('char', 'Character (Character)', 'Character model assets, including main characters, supporting characters, NPCs, etc.'),
            ('prop', 'Prop (Prop)', 'Prop and non-character model assets, such as weapons, tools, furniture, etc.'),
            ('env', 'Environment (Environment)', 'Scene and environment assets, such as buildings, terrain, backgrounds, etc.'),
            ('fx', 'Effects (Effects)', 'Visual effects assets, such as explosions, fire, smoke, particles, etc.'),
            ('veh', 'Vehicle (Vehicle)', 'Vehicle assets, such as cars, aircraft, ships, etc.'),
            ('veg', 'Vegetation (Vegetation)', 'Vegetation assets, such as trees, flowers, shrubs, etc.'),
            ('light', 'Light (Light)', 'Lighting setup assets, such as HDRI, lighting presets, etc.'),
        ],
        default='char',
    )
    
    asset_id: StringProperty(
        name="Asset ID",
        description="Asset identifier (lowercase, underscore separated)",
        default="new_asset",
    )
    
    def execute(self, context):
        if not bpy.data.filepath:
            self.report({'ERROR'}, "File not saved, please save file first")
            return {'CANCELLED'}
        
        project_root = detector.find_project_root()
        
        if not project_root:
            self.report({'ERROR'}, "Project root directory not detected, please initialize project first")
            return {'CANCELLED'}
        
        success, result, target_file = generator.create_asset_structure(
            project_root,
            self.asset_type,
            self.asset_id
        )
        
        if not success:
            self.report({'ERROR'}, result)
            return {'CANCELLED'}
        
        if target_file:
            is_valid, error_msg = naming.validate_asset_filename(target_file.name)
            if not is_valid:
                self.report({'INFO'}, bpy.app.translations.pgettext_iface(f"Naming reminder: {error_msg}"))
            
            if target_file.exists():
                self.report({'ERROR'}, bpy.app.translations.pgettext_iface(f"Target file already exists: {target_file}"))
                return {'CANCELLED'}
        
        try:
            bpy.ops.wm.save_as_mainfile(filepath=str(target_file))
            self.report({'INFO'}, bpy.app.translations.pgettext_iface(f"Asset structure created successfully, file saved: {target_file}"))
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, bpy.app.translations.pgettext_iface(f"Failed to save file: {str(e)}"))
            return {'CANCELLED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "asset_type")
        layout.prop(self, "asset_id")

