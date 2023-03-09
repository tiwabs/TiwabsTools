import bpy
import bpy.utils.previews
import os

import bmesh
from mathutils import Vector

bl_info = {
    "name": "Tiwabs Tools",
    "author": "Tiwabs",
    "description": "This plugins allows you to paste location/rotation in codewalker world viewer.",
    "blender": (3, 2, 2),
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

        transform_box = layout.box()

        obj = context.active_object
        if len(context.selected_objects) < 1 or not obj:
            transform_box.label(text="No object selected.", icon="ERROR")
        elif len(context.selected_objects) > 1:
            transform_box.label(text="You need to select only one object.", icon="ERROR")
            misc_tools = layout.box()
            misc_tools.label(text="Misc Tools :")
            row = misc_tools.row()
            row.prop(context.scene, "offset_location", text="Offset ")
            misc_tools.label(text="Axis :")
            row = misc_tools.row()
            row.prop(context.scene, "offset_axis_X", text="X")
            row.prop(context.scene, "offset_axis_Y", text="Y")
            row.prop(context.scene, "offset_axis_Z", text="Z")
            row = misc_tools.row()
            row.operator(TIWABS_OT_OFFSET_LOCATION.bl_idname)
            row = misc_tools.row()
            misc_tools.label(text="Clear parent :")
            row = misc_tools.row()
            row.prop(context.scene, "object_contain_name", text="Contain ")
            row = misc_tools.row()
            row.operator(TIWABS_OT_CLEAR_PARENT.bl_idname)
        else:
            transform_box.label(text="Tranform options :")
            
            row = transform_box.row()
            row.prop(context.scene, "object_name_field", text="Object name ")
            row = transform_box.row()
            row.prop(context.scene, "location_field", text="Location ")
            row = transform_box.row()
            row.prop(context.scene, "rotation_field", text="Rotation ")
            row = transform_box.row()
            row.operator(TIWABS_OT_COPY_LOCATION.bl_idname)
            row.operator(TIWABS_OT_COPY_ROTATION.bl_idname)
            row = transform_box.row()
            row.prop(context.scene, "object_inertia", text="Inertia ")
            row = transform_box.row()
            row.prop(context.scene, "object_volume", text="Volume ")

            object_data_box = layout.box()
            object_data_box.label(text="Object data options :")
            row = object_data_box.row()
            row.operator(TIWABS_OT_UVNAME.bl_idname)
            row.operator(TIWABS_OT_COLORNAME.bl_idname)

            lightProxy_box = layout.box()
            lightProxy_box.label(text="Light proxy options :")
            row = lightProxy_box.row()
            row.prop(context.scene, "create_lightproxy_size", text="Size of triangle")
            row = lightProxy_box.row()
            row.prop(context.scene, "create_lightproxy_name", text="Name")
            row = lightProxy_box.row()
            row.operator(TIWABS_OT_CREATE_LIGHTPROXY.bl_idname)

            get_obj_name()
            get_obj_location()
            get_obj_rotation()
            get_obj_inertia()
            get_obj_volume()

class TIWABS_OT_COPY_LOCATION(bpy.types.Operator):
    """Copy selected object location (X,Y,Z)"""
    bl_idname = "tiwabs.copy_location"
    bl_label = "Copy Location"
    
    def execute(self, context):
        active_object = context.active_object
        
        loc_x = round(active_object.location.x, 3)
        loc_y = round(active_object.location.y, 3)
        loc_z = round(active_object.location.z, 3)
        location = str(loc_x) + ", " + str(loc_y) + ", " + str(loc_z)
        command = "echo " + location.strip() + "| clip"
        os.system(command)
        self.report({"INFO"}, f"Location of " + active_object.name + " have been copied to the clipboard")
        
        return {"FINISHED"}

class TIWABS_OT_COPY_ROTATION(bpy.types.Operator):
    """Copy selected object quaternion rotation (X,Y,Z,W)"""
    bl_idname = "tiwabs.copy_rotation"
    bl_label = "Copy Rotation"

    def execute(self, context):        
        active_object = context.active_object
        
        if active_object.rotation_mode == "XYZ" or active_object.rotation_mode == "XZY" or active_object.rotation_mode == "YXZ" or active_object.rotation_mode == "YZX" or active_object.rotation_mode == "ZXY" or active_object.rotation_mode == "ZYX" :
            rot_x = round(active_object.rotation_euler.to_quaternion().x, 3)
            rot_y = round(active_object.rotation_euler.to_quaternion().y, 3)
            rot_z = round(active_object.rotation_euler.to_quaternion().z, 3)
            rot_w = round(active_object.rotation_euler.to_quaternion().w, 3)
        elif active_object.rotation_mode == "QUATERNION" :
            rot_x = round(active_object.rotation_quaternion.x, 3)
            rot_y = round(active_object.rotation_quaternion.y, 3)
            rot_z = round(active_object.rotation_quaternion.z, 3)
            rot_w = round(active_object.rotation_quaternion.w, 3)
        rotation = str(rot_x) + ", " + str(rot_y) + ", " + str(rot_z) + ", " + str(rot_w)
        command = "echo " + rotation.strip() + "| clip"
        os.system(command)
        self.report({"INFO"}, f"Rotation of " + active_object.name + " have been copied to the clipboard")
        return {"FINISHED"}
        
class TIWABS_OT_UVNAME(bpy.types.Operator):
    """Change UV Name to match with sollumz"""
    bl_idname = "tiwabs.uv_name"
    bl_label = "UV Name"

    def execute(self, context):        
        active_object = context.active_object

        count = -1
        if len(active_object.data.uv_layers) > 0:
            for uvmap in active_object.data.uv_layers:
                count = count + 1
                uvmap.name = "texcoord" + str(count)
        else:
            active_object.data.uv_layers.new(name="texcoord0")
        return {"FINISHED"}
        
class TIWABS_OT_COLORNAME(bpy.types.Operator):
    """Change Color attribute Name to match with sollumz"""
    bl_idname = "tiwabs.color_name"
    bl_label = "Color Name"

    def execute(self, context):        
        active_object = context.active_object

        count = -1
        if len(active_object.data.color_attributes) > 0:
            for color in active_object.data.color_attributes:
                count = count + 1
                color.name = "colour" + str(count)
        else:
            active_object.data.color_attributes.new(name="colour0", domain="CORNER", type="BYTE_COLOR")
        return {"FINISHED"}

class TIWABS_OT_OFFSET_LOCATION(bpy.types.Operator):
    """Set Offset Location of selected objects"""
    bl_idname = "tiwabs.offset_location"
    bl_label = "Set Offset"
    bl_option = {"UNDO"}

    def execute(self, context):
        selected_object = context.selected_objects
        offset = float(context.scene.offset_location)
        use_x_axis = bool(context.scene.offset_axis_X)
        use_y_axis = bool(context.scene.offset_axis_Y)
        use_z_axis = bool(context.scene.offset_axis_Z)

        if not use_x_axis and not use_y_axis and not use_z_axis:
            print("You don't have select axis!")
        else:            
            for obj in selected_object:
                x = obj.location[0]
                y = obj.location[1]
                z = obj.location[2]
                
                if use_x_axis:
                    x += offset
                if use_y_axis:
                    y += offset
                if use_z_axis:
                    z += offset
                    
                obj.location = (x, y, z)
                offset += float(context.scene.offset_location)
        return {"FINISHED"}

class TIWABS_OT_CLEAR_PARENT(bpy.types.Operator):
    """Clear parent and keep transform of selected objects if name contain a specific value"""
    bl_idname = "tiwabs.clear_parent"
    bl_label = "Clear parent"
    bl_option = {"UNDO"}

    def execute(self, context):
        selected_object = context.selected_objects
        contains = str(context.scene.object_contain_name)

        for obj in selected_object:
            if contains in obj.name:
                bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")
        return {"FINISHED"}

class TIWABS_OT_CALCULATE_INERTIA(bpy.types.Operator):
    """Calculate inertia of selected object"""
    bl_idname = "tiwabs.calculate_inertia"
    bl_label = "Calculate Inertia"

    def execute(self, context):
        selected_object = context.selected_objects
        for obj in selected_object:
            box_max = get_max_vector_list(obj.bound_box)
            box_min = get_min_vector_list(obj.bound_box)
            inertia = calculate_inertia(box_min, box_max)
            print(inertia)
            
        return {"FINISHED"}

class TIWABS_OT_CALCULATE_VOLUME(bpy.types.Operator):
    """Calculate volume of selected object"""
    bl_idname = "tiwabs.calculate_volume"
    bl_label = "Calculate Volume"

    def execute(self, context):
        selected_object = context.selected_objects
        for obj in selected_object:
            box_max = get_max_vector_list(obj.bound_box)
            box_min = get_min_vector_list(obj.bound_box)        
            volume = calculate_volume(box_min, box_max)
            print(volume)
            
        return {"FINISHED"}

class TIWABS_OT_CREATE_LIGHTPROXY(bpy.types.Operator):
    """Create a light procy for the selected object"""
    bl_idname = "tiwabs.create_lightproxy"
    bl_label = "Create Light Proxy"

    def execute(self, context):
        active_object = bpy.context.active_object
        size = float(context.scene.create_lightproxy_size)

        min, max = get_bound_extents(active_object)
        min_mesh = bpy.data.meshes.new(name="MinTriangle")
        max_mesh = bpy.data.meshes.new(name="MaxTriangle")

        min_verts = [Vector((min.x, min.y, min.z)), 
                    Vector((min.x, max.y, min.z)), 
                    Vector((max.x, min.y, min.z))]
        max_verts = [Vector((max.x, max.y, max.z)), 
                    Vector((max.x, min.y, max.z)), 
                    Vector((min.x, max.y, max.z))]

        edges = [(0, 1), (1, 2), (2, 0)]

        min_faces = [(0, 1, 2)]
        max_faces = [(0, 1, 2)]

        min_obj = bpy.data.objects.new(name="MinTriangle", object_data=min_mesh)
        max_obj = bpy.data.objects.new(name="MaxTriangle", object_data=max_mesh)
        bpy.context.scene.collection.objects.link(min_obj)
        bpy.context.scene.collection.objects.link(max_obj)

        min_mesh.from_pydata(min_verts, edges, min_faces)
        max_mesh.from_pydata(max_verts, edges, max_faces)

        min_obj.scale = (size, size, size)
        max_obj.scale = (size, size, size)

        min_obj.location = min + Vector((0, 0, -0.2))
        max_obj.location = max + Vector((0, 0, -0.2))

        bpy.ops.object.select_all(action='DESELECT')

        min_obj.select_set(True)
        max_obj.select_set(True)
        bpy.context.view_layer.objects.active = min_obj

        bpy.ops.object.join()
        if context.scene.create_lightproxy_name == "":
            min_obj.name = active_object.name + "_lightproxy"
        else:
            min_obj.name = context.scene.create_lightproxy_name
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        
        return {"FINISHED"}

def set_obj_name(self, value):
    name = value
    bpy.context.view_layer.objects.active.name = name

def set_obj_location(self, value):
    loc_x, loc_y, loc_z = map(float, value.split(", "))
    bpy.context.view_layer.objects.active.location = (loc_x, loc_y, loc_z)

def set_obj_rotation(self, value):
    loc_x, loc_y, loc_z = map(float, value.split(", "))
    bpy.context.view_layer.objects.active.location = (loc_x, loc_y, loc_z)

def get_obj_name(arg = None):
    active_object = bpy.context.view_layer.objects.active
    return str(active_object.name)
    
def get_obj_location(arg = None):
    active_object = bpy.context.view_layer.objects.active
    loc_x = round(active_object.location.x, 3)
    loc_y = round(active_object.location.y, 3)
    loc_z = round(active_object.location.z, 3)
    location = str(loc_x) + ", " + str(loc_y) + ", " + str(loc_z)
    return str(location)

def get_obj_rotation(arg = None):
    active_object = bpy.context.view_layer.objects.active

    if active_object.rotation_mode == "XYZ" or active_object.rotation_mode == "XZY" or active_object.rotation_mode == "YXZ" or active_object.rotation_mode == "YZX" or active_object.rotation_mode == "ZXY" or active_object.rotation_mode == "ZYX" :
        rot_x = round(active_object.rotation_euler.to_quaternion().x, 3)
        rot_y = round(active_object.rotation_euler.to_quaternion().y, 3)
        rot_z = round(active_object.rotation_euler.to_quaternion().z, 3)
        rot_w = round(active_object.rotation_euler.to_quaternion().w, 3)
    elif active_object.rotation_mode == "QUATERNION" :
        rot_x = round(active_object.rotation_quaternion.x, 3)
        rot_y = round(active_object.rotation_quaternion.y, 3)
        rot_z = round(active_object.rotation_quaternion.z, 3)
        rot_w = round(active_object.rotation_quaternion.w, 3)

    rotation = str(rot_x) + ", " + str(rot_y) + ", " + str(rot_z) + ", " + str(rot_w)
    return str(rotation)

def get_obj_inertia(arg = None):
    active_object = bpy.context.view_layer.objects.active
    box_max = get_max_vector_list(active_object.bound_box)
    box_min = get_min_vector_list(active_object.bound_box)
    inertia = calculate_inertia(box_min, box_max)
    inertia_ = str(round(inertia[0], 3)) + ", " + str(round(inertia[1], 3)) + ", " + str(round(inertia[2], 3))
    return str(inertia_)

def get_obj_volume(arg = None):
    active_object = bpy.context.view_layer.objects.active
    box_max = get_max_vector_list(active_object.bound_box)
    box_min = get_min_vector_list(active_object.bound_box)
    volume = calculate_volume(box_min, box_max)
    return str(round(volume, 3))

def get_min_vector_list(vecs):
    x = []
    y = []
    z = []
    for v in vecs:
        x.append(v[0])
        y.append(v[1])
        z.append(v[2])
    return Vector((min(x), min(y), min(z)))

def get_max_vector_list(vecs):
    x = []
    y = []
    z = []
    for v in vecs:
        x.append(v[0])
        y.append(v[1])
        z.append(v[2])
    return Vector((max(x), max(y), max(z)))

def get_dimensions(bbmin, bbmax):
    x = bbmax.x - bbmin.x
    y = bbmax.y - bbmin.y
    z = bbmax.z - bbmin.z

    return x, y, z

def calculate_volume(bbmin, bbmax):
    x, y, z = get_dimensions(bbmin, bbmax)

    return x * y * z

def calculate_inertia(bbmin, bbmax):
    x, y, z = get_dimensions(bbmin, bbmax)

    I_h = (1/12) * (pow(y, 2) + pow(z, 2))
    I_w = (1/12) * (pow(z, 2) + pow(x, 2))
    I_d = (1/12) * (pow(y, 2) + pow(x, 2))

    # Gta props using this values ( y, x, z )
    return Vector((I_h, I_w, I_d))

    # maybe x= I_w, y= I_h, z= I_d
    # return Vector((I_w, I_h, I_d))

## LightProxy

def subtract_from_vector(v, f):
    r = Vector((0, 0, 0))
    r.x = v.x - f
    r.y = v.y - f
    r.z = v.z - f
    return r

def add_to_vector(v, f):
    r = Vector((0, 0, 0))
    r.x = v.x + f
    r.y = v.y + f
    r.z = v.z + f
    return r

def get_min_vector_list(vecs):
    x = []
    y = []
    z = []
    for v in vecs:
        x.append(v[0])
        y.append(v[1])
        z.append(v[2])
    return Vector((min(x), min(y), min(z)))

def get_max_vector_list(vecs):
    x = []
    y = []
    z = []
    for v in vecs:
        x.append(v[0])
        y.append(v[1])
        z.append(v[2])
    return Vector((max(x), max(y), max(z)))

def get_bound_extents(obj, margin=0):
    corners = get_total_bounds(obj)

    if not corners:
        return Vector(), Vector()

    min = subtract_from_vector(get_min_vector_list(corners), margin)
    max = add_to_vector(get_max_vector_list(corners), margin)
    return min, max

def get_total_bounds(obj):
    corners = []
    
    for child in [obj, *get_children_recursive(obj)]:
        if child.type != "MESH":
            continue

        matrix = child.matrix_basis

        corners.extend([matrix @ Vector(pos)
                       for pos in child.bound_box])

    return corners

def get_children_recursive(obj) -> list[bpy.types.Object]:
    children = []

    if obj is None:
        return children

    if len(obj.children) < 1:
        return children

    for child in obj.children:
        children.append(child)
        if len(child.children) > 0:
            children.extend(get_children_recursive(child))

    return children

## End LightProxy

classes = (
    TIWABS_PT_TOOLS,
    TIWABS_OT_COPY_LOCATION,
    TIWABS_OT_COPY_ROTATION,
    TIWABS_OT_UVNAME,
    TIWABS_OT_COLORNAME,
    TIWABS_OT_OFFSET_LOCATION,
    TIWABS_OT_CLEAR_PARENT,
    TIWABS_OT_CALCULATE_INERTIA,
    TIWABS_OT_CALCULATE_VOLUME,
    TIWABS_OT_CREATE_LIGHTPROXY
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.object_name_field = bpy.props.StringProperty(
        name="",
        default="No object select", 
        description="Name of selected object",
        maxlen=50,
        get=get_obj_name,
        set=set_obj_name)
    bpy.types.Scene.location_field = bpy.props.StringProperty(
        name="",
        default="0, 0, 0", 
        description="Location of selected object",
        maxlen=50,
        get=get_obj_location,
        set=set_obj_location)
    bpy.types.Scene.rotation_field = bpy.props.StringProperty(
        name="", 
        default="0, 0, 0, 1", 
        description="Rotation of selected object",
        maxlen=150,
        get=get_obj_rotation,
        set=set_obj_rotation)
    bpy.types.Scene.offset_location = bpy.props.StringProperty(
        name="",
        default="-0.2", 
        description="Offset for place object in Z axis",
        maxlen=50)
    bpy.types.Scene.offset_axis_X = bpy.props.BoolProperty(
        name="X")
    bpy.types.Scene.offset_axis_Y = bpy.props.BoolProperty(
        name="Y")
    bpy.types.Scene.offset_axis_Z = bpy.props.BoolProperty(
        name="Z")
    bpy.types.Scene.object_contain_name = bpy.props.StringProperty(
        name="",
        default="#dr", 
        description="The mesh contain a specific name",
        maxlen=50)
    bpy.types.Scene.object_inertia = bpy.props.StringProperty(
        name="",
        default="0, 0, 0", 
        description="The mesh contain a specific name",
        maxlen=150,
        get=get_obj_inertia)
    bpy.types.Scene.object_volume = bpy.props.StringProperty(
        name="",
        default="0, 0, 0",
        description="Volume of active object",
        maxlen=150,
        get=get_obj_volume)
    bpy.types.Scene.create_lightproxy_size = bpy.props.StringProperty(
        name="",
        default="0.01",
        description="Size of the triangles for the light proxy",
        maxlen=150)
    bpy.types.Scene.create_lightproxy_name = bpy.props.StringProperty(
        name="",
        default="",
        description="Name of your light proxy, if not set, the name will be the same as the object + _lightproxy",
        maxlen=150)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.object_name_field
    del bpy.types.Scene.location_field
    del bpy.types.Scene.rotation_field
    del bpy.types.Scene.offset_location
    del bpy.types.Scene.offset_axis_X
    del bpy.types.Scene.offset_axis_Y
    del bpy.types.Scene.offset_axis_Z
    del bpy.types.Scene.object_contain_name
    del bpy.types.Scene.create_lightproxy_size

if __name__ == "__main__":
    register()
