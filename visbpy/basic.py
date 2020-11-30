import bpy
from typing import Iterator, Any
from math import radians
from mathutils import Vector
import bmesh
import numpy as np
import math

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

		self.COLL_AXES = self._create_collection("AXES")

		for plane in ["xy", "xz", "yz"]:
			self._create_plane(plane, size=size)
			self._C.object.data.materials.append( self._bg_material )
			self.COLL_AXES.objects.link(self._C.object)
			self._C.scene.collection.objects.unlink(self._C.object)

	def _create_collection(self, name):
		col = self._D.collections.new(name)
		self._C.scene.collection.children.link(col)
		return col

	def _create_material_with_color(self, name, color):
		material = self._D.materials.new(name)
		material.use_nodes = True
		material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = color
		# material.diffuse_color = color
		return material

	def _create_text(self, TXT, name, scale=(0.3, 0.3, 0.3), to_coll=True):
	    curve = self._D.curves.new(type="FONT", name=name)
	    curve.body = TXT
	    curve_obj = self._D.objects.new(name, curve)

	    curve_obj.scale = scale
	    curve_obj.rotation_euler[0] = self.RAD90

	    self.COLL_AXES.objects.link(curve_obj)

	    mod = curve_obj.modifiers.new(name="solid", type="SOLIDIFY")
	    mod.thickness = 0.1

	    return curve_obj

	def _add_3d_surface(self):
		"""
		:param x, y, z: Matrix of surface vertices
		"""
		_COLL_SURFACE = self._create_collection("PLOT_SURFACE")
		MESH_NAME = "PlotSurface"
		VC_TYPE = "ShaderNodeVertexColor"

		x,y,z = self._loc_X, self._loc_Y, self._loc_Z

		LEN_X = len(x[0])
		LEN_Y = len(y[0])

		#TODO: coord z range <- cal by numpy, not work for Matrix form list
		max_z = z.max()
		min_z = z.min()

		verts = []
		faces = []
		vert_idcs = 0
		for i in range(LEN_X):
			for j in range(LEN_Y):
				vert = (x[i][j], y[i][j], z[i][j])
				verts.append(vert)

				if i < LEN_X - 1 and j < LEN_Y - 1:
					faces.append([vert_idcs, vert_idcs+1, vert_idcs+LEN_Y+1, vert_idcs+LEN_Y, vert_idcs])
				vert_idcs += 1

		mesh_data = self._D.meshes.new(MESH_NAME)

		mesh_data.from_pydata(verts, [], faces)
		mesh_obj = self._D.objects.new(mesh_data.name, mesh_data)

		## Using Vertex_Color
		vert_col_name = F'_For{MESH_NAME}'
		if mesh_data.vertex_colors.find(vert_col_name) == -1:
			mesh_data.vertex_colors.new(name = vert_col_name)

		bm = bmesh.new()
		bm.from_mesh(mesh_data)
		bm_vert_color = bm.loops.layers.color[vert_col_name]

		for bm_face in bm.faces:
			for bm_loop in bm_face.loops:
				coord_z = bm_loop.vert.co[2]
				coord_z_ration = (coord_z - min_z ) / max_z
				bm_loop[bm_vert_color] = self._get_value_between_two_colors(coord_z_ration) + [1.]
		bm.to_mesh(mesh_data)
		bm.free()
		## End Vertex_Color Editing

		## Asign Vertex Color to Material via Node
		mat = self._D.materials.new(name = vert_col_name)
		mat.use_nodes = True
		vc = mat.node_tree.nodes.new(VC_TYPE)
		vc.layer_name = vert_col_name

		bsdf = mat.node_tree.nodes['Principled BSDF']
		mat.node_tree.links.new(vc.outputs[0], bsdf.inputs[0])
		## End Asign Material
		mesh_data.materials.append(mat)

		# self._C.collection.objects.link(mesh_obj)
		_COLL_SURFACE.objects.link(mesh_obj)
	def _add_3d_curve(self, thickness = 0.01, c=None):
		"""
		"""
		points = list(zip(self._loc_X, self._loc_Y, self._loc_Z))
		_COLL_CURVE = self._create_collection("PLOT_LINE")

		_material = self._create_material_with_color("_ForPlot", self._C2COLOR.get(c))

		curve_data = self._D.curves.new("_plot", type = "CURVE")
		curve_data.dimensions = '3D'
		curve_data.resolution_u = 20
		curve_data.render_resolution_u = 32
		curve_data.fill_mode = 'FULL'
		curve_data.extrude = thickness
		curve_data.bevel_depth = thickness
		curve_data.materials.append(_material)

		polyline = curve_data.splines.new("NURBS")
		polyline.points.add(len(points))
		for i, coord in enumerate(points):
			x, y, z = coord
			polyline.points[i].co = (x, y, z, 1)
		curve_obj = self._D.objects.new("_Plot", curve_data)
		
		# self._C.scene.collection.objects.link(curve_obj)
		_COLL_CURVE.objects.link(curve_obj)

	def _add_scatters(self, marker_size: float=0.05, marker:str = 'o', c:str=None):
		"""
		:param points: scatter data points
		:param size: marker size
		:param marker: o | ^ | #
		:param c: color of markers
		"""
		#TODO: create new material with color - c

		points = zip(self._loc_X, self._loc_Y, self._loc_Z)

		_COLL_SCATTER = self._create_collection("PLOT_SCATTERS")
		_mark_material = self._create_material_with_color("_ForMarker", self._C2COLOR.get(c))

		for point in points:
			# TODO: transform needed, maybe
			location = [ l * self.PLANE_SIZE for l in point]
			self._add_data_marker(point, size = marker_size, marker = marker, c = c)
			# latest created active object
			_ao = self._C.object
			_ao.data.materials.append( _mark_material )
			_COLL_SCATTER.objects.link(_ao)
			self._C.scene.collection.objects.unlink(_ao)

	def _add_data_marker(self, loc, size: float=0.1, marker:str = None, c:str=None):
		if marker == '#': # Cube
			self._O.mesh.primitive_cube_add(size = size, location = loc)
		elif marker == '^': # Cone
			self._O.mesh.primitive_cone_add(radius1 = size, depth = size * 2, location = loc)
		else: # 'o' Sphere by default
			self._O.mesh.primitive_uv_sphere_add(radius = size,
											location = loc)

	def _create_plane(self, which : str ='xy', size :int=1):
		"""
		:param which: Which axes plane to create - xy | yz | xz.
		:param size: Size of the plane, 1 by default.
		:returns: None
		"""

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
										enter_editmode = False,
										location = _loc,
										rotation = _rot)
		self._C.object.name = F"Plane_{which}"
		self._C.object.modifiers.new(f'Plane_{which}', type = "WIREFRAME")

	def _remove_objects(self):
		self._O.object.select_all(action="SELECT")
		self._O.object.delete(use_global=False)
		for col in self._D.collections:
			self._D.collections.remove(col)

	def _get_value_between_two_colors(self, z_ratio:float):
		ar, ag, ab = 0., 0., 1.
		br, bg, bb = 1., 0., 0.

		R = z_ratio * 1 + 0
		G = z_ratio * 0 + 0
		B = z_ratio * -1 + 1
		return [R, G, B]
	def _normalize(self, loc):
		return (loc - self._lower_coord) / (self._upper_coord - self._lower_coord) * self.PLANE_SIZE
	def _preprocess_coordinate(self, X, Y, Z, check_dim = None):
		self._internal_X = np.array(X, dtype = np.float32)
		self._internal_Y = np.array(Y, dtype = np.float32)
		self._internal_Z = np.array(Z, dtype = np.float32)

		if check_dim:
			assert len(self._internal_X.shape) == check_dim
			assert len(self._internal_Y.shape) == check_dim 
			assert len(self._internal_Z.shape) == check_dim 

		self._lower_limit = min(self._internal_X.min(), self._internal_Y.min(), self._internal_Z.min())
		self._upper_limit = max(self._internal_X.max(), self._internal_Y.max(), self._internal_Z.max())
		# set origin range
		self._lower_coord = math.floor(self._lower_limit)
		self._upper_coord = math.ceil(self._upper_limit)

		# data transilation
		self._loc_X = self._normalize(self._internal_X)
		self._loc_Y = self._normalize(self._internal_Y)
		self._loc_Z = self._normalize(self._internal_Z)