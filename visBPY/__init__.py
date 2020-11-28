from typing import Iterator
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

    def scatter(self, xs:Iterator[float], ys:Iterator[float], zs:Iterator[float], c:str='r', marker:str='o'):
        self._add_scatters(zip(xs, ys, zs), c=c, marker=marker)
    
    def plot(self, xs, ys, zs, c='r'):
        self._add_3d_curve(list( zip(xs, ys, zs) ), c=c)