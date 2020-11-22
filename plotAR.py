import bpy
from math import radians

# config
AXES_SIZE = 2
RAD90 = radians(90)


def remove_objects():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def _create_plane():
    plane_xy = bpy.ops.mesh.primitive_plane_add(size=AXES_SIZE,
                                                location=(AXES_SIZE / 2,
                                                          AXES_SIZE / 2, 0),
                                                scale=(1, 1, 1))
    plane_yz = bpy.ops.mesh.primitive_plane_add(size=AXES_SIZE,
                                                location=(0, AXES_SIZE / 2,
                                                          AXES_SIZE / 2),
                                                rotation=(0, RAD90, 0),
                                                scale=(1, 1, 1))
    plane_xz = bpy.ops.mesh.primitive_plane_add(size=AXES_SIZE,
                                                location=(AXES_SIZE / 2,
                                                          AXES_SIZE,
                                                          AXES_SIZE / 2),
                                                rotation=(RAD90, 0, 0),
                                                scale=(1, 1, 1))


def _create_axis():
    axis_x = bpy.data.curves.new(type="FONT", name="axis_x")
    axis_x.body = "X"
    axis_x_obj = bpy.data.objects.new("Axis_X", axis_x)
    axis_x_obj.location[0] = AXES_SIZE
    axis_x_obj.rotation_euler[0] = RAD90
    axis_x_obj.scale = (0.3, 0.3, 0.3)
    bpy.context.scene.collection.objects.link(axis_x_obj)

    axis_y = bpy.data.curves.new(type="FONT", name="axis_y")
    axis_y.body = "Y"
    axis_y_obj = bpy.data.objects.new("Axis_Y", axis_y)
    axis_y_obj.location = (AXES_SIZE, AXES_SIZE, 0)
    axis_y_obj.rotation_euler[0] = RAD90
    axis_y_obj.scale = (0.3, 0.3, 0.3)
    bpy.context.scene.collection.objects.link(axis_y_obj)

    axis_z = bpy.data.curves.new(type="FONT", name="axis_z")
    axis_z.body = "Z"
    axis_z_obj = bpy.data.objects.new("Axis_Z", axis_z)
    axis_z_obj.location = (AXES_SIZE, AXES_SIZE, AXES_SIZE)
    axis_z_obj.rotation_euler[0] = RAD90
    axis_z_obj.scale = (0.3, 0.3, 0.3)
    bpy.context.scene.collection.objects.link(axis_z_obj)


def build_axes():
    _create_plane()
    _create_axis()


remove_objects()
build_axes()