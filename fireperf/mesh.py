from firedrake import *


MESH_TYPES_2D = ["tri", "quad"]
MESH_TYPES_3D = ["tet", "hex"]

MESH_TYPES = MESH_TYPES_2D + MESH_TYPES_3D


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
    return mesh_type in MESH_TYPES_2D


def is_3d(mesh_type):
    return mesh_type in MESH_TYPES_3D