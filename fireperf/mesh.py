from firedrake import *


BASE_N_CELLS_MESH2D = 100
BASE_N_CELLS_MESH3D = 20


def make_mesh(mesh_type, refinement_factor):
    if mesh_type in ["tri", "quad"]:
        n_cells = BASE_N_CELLS_MESH2D * refinement_factor
    else:
        n_cells = BASE_N_CELLS_MESH3D * refinement_factor

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