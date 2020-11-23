import bpy
from math import radians

# config
AXES_SIZE = 2
RAD90 = radians(90)

# global
_C = bpy.context
_D = bpy.data
_O = bpy.ops


def remove_objects():
    _O.object.select_all(action="SELECT")
    _O.object.delete(use_global=False)


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


def _create_text(TXT: str, name: str, scale=(0.3, 0.3, 0.3)):
    curve = _D.curves.new(type="FONT", name=name)
    curve.body = TXT
    curve_obj = _D.objects.new(name, curve)

    curve_obj.scale = scale
    curve_obj.rotation_euler[0] = RAD90

    _C.scene.collection.objects.link(curve_obj)

    mod = curve_obj.modifiers.new(name="solid", type="SOLIDIFY")
    mod.thickness = 0.1

    return curve_obj


def _create_axis():
    axis_x_obj = _create_text("X", "axis_x")
    axis_x_obj.location[0] = AXES_SIZE

    axis_y_obj = _create_text("Y", "axis_y")
    axis_y_obj.location = (AXES_SIZE, AXES_SIZE, 0)

    axis_z_obj = _create_text("Z", "axis_z")
    axis_z_obj.location = (AXES_SIZE, AXES_SIZE, AXES_SIZE)


def build_axes():
    _create_plane()
    _create_axis()


remove_objects()
build_axes()