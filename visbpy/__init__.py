import bpy
from .basic import VisCore

class Axes(VisCore):
    SIZE = {
        "X": 1,
        "Y": 1,
        "Z": 1
    }
    def __init__(self, size:int=1):
        super().__init__(size)
        self._C.scene.cursor.location = [0, self.PLANE_SIZE, 0]

    def scatter(self, xs, ys, zs, c='r', marker='o'):
        self._preprocess_coordinate(xs, ys, zs)
        self._add_scatters(c=c, marker=marker)
    
    def plot(self, xs, ys, zs, c='r', thickness = 0.01):
        self._preprocess_coordinate(xs, ys, zs)
        self._add_3d_curve(c=c, thickness=thickness)
    
    def plot_surface(self, xs, ys, zs):
        self._preprocess_coordinate(xs, ys, zs, 2)
        self._add_3d_surface()

    def set_xlabel(self, label):
        COLL_XLABEL = self._create_collection("COLL_XLABEL")
        xlabel_obj = self._create_text(label, 'XLabel', to_coll=COLL_XLABEL)
        xlabel_obj.location = [self.PLANE_CENT, -0.1, 0]
        xlabel_obj.data.align_x = 'CENTER'
        xlabel_obj.rotation_euler[0] -= self.RAD90 / 4
    def set_ylabel(self, label):
        COLL_YLABEL = self._create_collection("COLL_YLABEL")
        ylabel_obj = self._create_text(label, 'YLabel', to_coll=COLL_YLABEL)
        ylabel_obj.location = [self.PLANE_SIZE + 0.1, self.PLANE_CENT, 0]
        ylabel_obj.data.align_x = 'CENTER'
        ylabel_obj.rotation_euler[2] = self.RAD90
        ylabel_obj.rotation_euler[0] = self.RAD90 * 3 / 4
    def set_zlabel(self, label):
        COLL_ZLABEL = self._create_collection("COLL_ZLABEL")
        zlabel_obj = self._create_text(label, 'ZLabel', to_coll=COLL_ZLABEL)
        zlabel_obj.location = [self.PLANE_SIZE, self.PLANE_SIZE, self.PLANE_CENT]
        # zlabel_obj.data.align_x = 'CENTER'
        zlabel_obj.rotation_euler[0] -= self.RAD90 / 4

