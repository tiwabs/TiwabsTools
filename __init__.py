import bpy

from bpy.utils import ( register_class, unregister_class )
from bpy.props import ( StringProperty,
                        BoolProperty,
                        IntProperty,
                        FloatProperty,
                        FloatVectorProperty,
                        EnumProperty,
                        PointerProperty,
                       )
from bpy.types import ( Panel,
                        AddonPreferences,
                        Operator,
                        PropertyGroup,
                      )
                      
import os

bl_info = {
    "name": "Tiwabs Tools",
    "author": "Tiwabs",
    "description": "This plugins allows you to paste location/rotation in codewalker world viewer.",
    "blender": (2, 93, 0),
    "location": "View3D",
    "warning": "",
    "wiki_url": "",
    "category": "Misc Tools"
}

class TiwabsTools:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tiwabs Tools"
    bl_options = {"DEFAULT_CLOSED"}


class TIWABS_PT_TOOLS(TiwabsTools, bpy.types.Panel):
    bl_idname = "TIWABS_PT_TOOLS"
    bl_label = "Tiwabs Tools"

    def draw(self, context):
        layout = self.layout        
        layout.label(text="Copy to clipboard location/rotation")


class TIWABS_PT_TOOLS_LOCATION(TiwabsTools, bpy.types.Panel):
    bl_parent_id = "TIWABS_PT_TOOLS"
    bl_label = "Copy Location"

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.enabled = False
        row.prop(context.scene, "loc_object_name_field", text="Object name ")
        row = layout.row()
        row.enabled = False
        row.prop(context.scene, "location_field", text="Location ")
        layout.operator(TIWABS_OT_COPY_LOCATION.bl_idname)

class TIWABS_PT_TOOLS_ROTATION(TiwabsTools, bpy.types.Panel):
    bl_parent_id = "TIWABS_PT_TOOLS"
    bl_label = "Copy Rotation"

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.enabled = False
        row.prop(context.scene, "rot_object_name_field", text="Object name ")
        row = layout.row()
        row.enabled = False
        row.prop(context.scene, "rotation_field", text="Rotation ")
        layout.operator(TIWABS_OT_COPY_ROTATION.bl_idname)

class TIWABS_OT_COPY_LOCATION(bpy.types.Operator):
    """Copy selected object location (X,Y,Z)"""
    bl_idname = "tiwabs.copy_location"
    bl_label = "Copy Location"
    
    def execute(self, context): 
               
        selected_object = bpy.context.selected_objects

        if not selected_object:
            self.report({'ERROR'}, f"You need to select an object!")
            context.scene.location_field = ""
            context.scene.loc_object_name_field = "No object select"
            return {'FINISHED'}
        if len(selected_object) > 2 :
            self.report({'ERROR'}, f"You need to select only one object!")
            context.scene.location_field = ""
            context.scene.loc_object_name_field = "No object select"
            return {'FINISHED'}
        
        for obj in selected_object:
            loc_x = round(obj.location.x, 3)
            loc_y = round(obj.location.y, 3)
            loc_z = round(obj.location.z, 3)
            location = str(loc_x) + ", " + str(loc_y) + ", " + str(loc_z)
            context.scene.location_field = location
            context.scene.loc_object_name_field = obj.name
            command = 'echo ' + location.strip() + '| clip'
            os.system(command)
            self.report({'INFO'}, f"Location of " + obj.name + " have been copied to the clipboard")
        
        return {'FINISHED'}

class TIWABS_OT_COPY_ROTATION(bpy.types.Operator):
    """Copy selected object quaternion rotation (X,Y,Z,W)"""
    bl_idname = "tiwabs.copy_rotation"
    bl_label = "Copy Rotation"
    
    def execute(self, context):        
        
        selected_object = bpy.context.selected_objects

        if not selected_object:
            self.report({'ERROR'}, f"You need to select an object!")
            context.scene.rotation_field = ""
            context.scene.rot_object_name_field = "No object select"
            return {'FINISHED'}
        if len(selected_object) > 2 :
            self.report({'ERROR'}, f"You need to select only one object!")
            context.scene.rotation_field = ""
            context.scene.rot_object_name_field = ""
            return {'FINISHED'}
        
        for rot_obj in selected_object:
            if rot_obj.rotation_mode == "XYZ" or rot_obj.rotation_mode == "XZY" or rot_obj.rotation_mode == "YXZ" or rot_obj.rotation_mode == "YZX" or rot_obj.rotation_mode == "ZXY" or rot_obj.rotation_mode == "ZYX" :
                rot_x = round(rot_obj.rotation_euler.to_quaternion().x, 3)
                rot_y = round(rot_obj.rotation_euler.to_quaternion().y, 3)
                rot_z = round(rot_obj.rotation_euler.to_quaternion().z, 3)
                rot_w = round(rot_obj.rotation_euler.to_quaternion().w, 3)
            elif rot_obj.rotation_mode == "QUATERNION" :
                rot_x = round(rot_obj.rotation_quaternion.x, 3)
                rot_y = round(rot_obj.rotation_quaternion.y, 3)
                rot_z = round(rot_obj.rotation_quaternion.z, 3)
                rot_w = round(rot_obj.rotation_quaternion.w, 3)
            rotation = str(rot_x) + ", " + str(rot_y) + ", " + str(rot_z) + ", " + str(rot_w)
            context.scene.rotation_field = rotation
            context.scene.rot_object_name_field = rot_obj.name
            command = 'echo ' + rotation.strip() + '| clip'
            os.system(command)
            self.report({'INFO'}, f"Rotation of " + rot_obj.name + " have been copied to the clipboard")
        return {'FINISHED'}
    
classes = (
    TIWABS_PT_TOOLS,
    TIWABS_PT_TOOLS_LOCATION, 
    TIWABS_PT_TOOLS_ROTATION,
    TIWABS_OT_COPY_LOCATION,
    TIWABS_OT_COPY_ROTATION
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.loc_object_name_field = bpy.props.StringProperty(
        name="",
        default="No object select", 
        description="Name of selected object",
        maxlen=50)
    bpy.types.Scene.rot_object_name_field = bpy.props.StringProperty(
        name="",
        default="No object select", 
        description="Name of selected object",
        maxlen=50)
    bpy.types.Scene.location_field = bpy.props.StringProperty(
        name="",
        default="0, 0, 0", 
        description="Location of selected object",
        maxlen=50)
    bpy.types.Scene.rotation_field = bpy.props.StringProperty(
        name="", 
        default="0, 0, 0, 1", 
        description="Rotation of selected object",
        maxlen=150)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.loc_object_name_field
    del bpy.types.Scene.rot_object_name_field
    del bpy.types.Scene.location_field
    del bpy.types.Scene.rotation_field


if __name__ == "__main__":
    register()