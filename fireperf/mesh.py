from firedrake import *


MESH_SIZE = 10


def make_mesh(mesh_type, n_cells):
    if mesh_type == "tri":
        return SquareMesh(n_cells, n_cells, 1)
    if mesh_type == "quad":
        return SquareMesh(n_cells, n_cells, 1, quadrilateral=True)
    if mesh_type == "tet":
        return CubeMesh(n_cells, n_cells, n_cells, 1)
    if mesh_type == "hex":
        mesh2d = SquareMesh(n_cells, n_cells, 1, quadrilateral=True)
        return ExtrudedMesh(mesh2d, n_cells)
    raise AssertionError()