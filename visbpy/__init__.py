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
        self._C.scene.cursor.location = [0, 0, 0]

    def scatter(self, xs, ys, zs, c='r', marker='o'):
        self._preprocess_coordinate(xs, ys, zs)
        self._add_scatters(c=c, marker=marker)
    
    def plot(self, xs, ys, zs, c='r', thickness = 0.05):
        self._preprocess_coordinate(xs, ys, zs)
        self._add_3d_curve(c=c, thickness=thickness)
    
    def plot_surface(self, xs, ys, zs):
        self._preprocess_coordinate(xs, ys, zs, 2)
        self._add_3d_surface()
 