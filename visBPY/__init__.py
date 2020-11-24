from .plotAR import remove_objects, build_axes
import random

__all__ = ['build_axes', 'remove_objects', 'make_data_scatter']


def _rand_array(n):
    return [random.randint(0, 100) for _ in range(n)]


def make_data_scatter(N=10):
    return {"x": _rand_array(N), "y": _rand_array(N), "z": _rand_array(N)}
