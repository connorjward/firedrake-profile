from firedrake import *


_MESHES_2D = ["tri", "quad"]
_MESHES_3D = ["tet", "hex"]

MESHES = _MESHES_2D + _MESHES_3D


def make_mesh(mesh_type, mesh_size):
    if mesh_type == "tri":
        return SquareMesh(*mesh_size, 1)
    if mesh_type == "quad":
        return SquareMesh(*mesh_size, 1, quadrilateral=True)
    if mesh_type == "tet":
        return CubeMesh(*mesh_size, 1)
    if mesh_type == "hex":
        mesh2d = SquareMesh(*mesh_size[:2], 1, quadrilateral=True)
        return ExtrudedMesh(mesh2d, mesh_size[2])
    raise AssertionError()


def is_2d(mesh_type):
    return mesh_type in _MESHES_2D


def is_3d(mesh_type):
    return mesh_type in _MESHES_3D