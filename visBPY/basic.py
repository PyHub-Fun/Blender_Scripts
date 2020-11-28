import bpy
from typing import Iterator, Any
from math import radians

class VisCore:
	PLANE_SIZE = 2
	RAD90 = radians(90)

	_C = bpy.context
	_D = bpy.data
	_O = bpy.ops
	_C2COLOR = {
		'r': (1,0,0,1),
		'g': (0,1,0,1),
		'b': (0,0,1,1)
	}
	def __init__(self, size):
		self._remove_objects()
		self._bg_material = self._create_material_with_color("BG", (0.3,0.3,0.3,1))
		for plane in ["xy", "xz", "yz"]:
			self._create_plane(plane, size=size)
			self._C.object.data.materials.append( self._bg_material )

	def _create_material_with_color(self, name, color):
		material = self._D.materials.new(name)
		material.use_nodes = True
		material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = color
		# material.diffuse_color = color
		return material

	def _create_text(self, TXT, name, scale=(0.3, 0.3, 0.3)):
	    curve = self._D.curves.new(type="FONT", name=name)
	    curve.body = TXT
	    curve_obj = self._D.objects.new(name, curve)

	    curve_obj.scale = scale
	    curve_obj.rotation_euler[0] = self.RAD90

	    self._C.scene.collection.objects.link(curve_obj)

	    mod = curve_obj.modifiers.new(name="solid", type="SOLIDIFY")
	    mod.thickness = 0.1

	    return curve_obj

	def _add_3d_curve(self, points, thickness = 0.1, c=None):

		_material = self._create_material_with_color("_ForPlot", self._C2COLOR.get(c))

		curve_data = self._D.curves.new("_plot", type = "CURVE")
		curve_data.dimensions = '3D'
		curve_data.resolution_u = 20
		curve_data.render_resolution_u = 32
		curve_data.fill_mode = 'FULL'
		curve_data.extrude = 0.01
		curve_data.bevel_depth = 0.01
		curve_data.materials.append(_material)

		polyline = curve_data.splines.new("NURBS")
		polyline.points.add(len(points))
		for i, coord in enumerate(points):
			x, y, z = coord
			polyline.points[i].co = (x, y, z, 1)
		curve_obj = self._D.objects.new("_Plot", curve_data)

		
		self._C.scene.collection.objects.link(curve_obj)

	def _add_scatters(self, points, size: float=0.05, marker:str = 'o', c:str=None):
		"""
		:marker: o | ^ | #
		"""
		#TODO: create new material with color - c
		_mark_material = self._create_material_with_color("_ForMarker", self._C2COLOR.get(c))

		for point in points:
			# TODO: transform needed, maybe
			location = [ l * self.PLANE_SIZE for l in point]
			self._add_object(location, size = size, marker = marker, c = c)
			self._C.object.data.materials.append( _mark_material )

	def _add_object(self, loc: Iterator[Any], size: float=0.1, marker:str = None, c:str=None):
		if marker == '#': # Cube
			self._O.mesh.primitive_cube_add(size = size, location = loc)
		elif marker == '^': # Cone
			self._O.mesh.primitive_cone_add(radius1 = size, depth = size * 2, location = loc)
		else: # 'o' Sphere by default
			self._O.mesh.primitive_uv_sphere_add(radius = size,
											location = loc)

	def _create_plane(self, which : str ='xy', size :int=1):
		_plane_size = self.PLANE_SIZE * size
		_loc = [_plane_size / 2] * 3
		_rot = [0.,0.,0.]

		if which == 'xy':
			_loc[2] = 0

			axis_x_obj = self._create_text("X", "axis_x")
			axis_x_obj.location[0] = _plane_size
		elif which == 'yz':
			_loc[0] = 0
			_rot[1] = self.RAD90

			axis_y_obj = self._create_text("Y", "axis_y")
			axis_y_obj.location = (_plane_size, _plane_size, 0)

		elif which == 'xz':
			_loc[1] *= 2
			_rot[0] = self.RAD90

			axis_z_obj = self._create_text("Z", "axis_z")
			axis_z_obj.location = (_plane_size, _plane_size, _plane_size)


		self._O.mesh.primitive_grid_add(size = _plane_size,
										location = _loc,
										rotation = _rot)
		self._C.object.modifiers.new(f'Plane_{which}', type = "WIREFRAME")

	def _remove_objects(self):
		self._O.object.select_all(action="SELECT")
		self._O.object.delete(use_global=False)