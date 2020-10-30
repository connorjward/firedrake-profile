from firedrake import *


def tri(n_repeats):
    return SquareMesh(n_repeats, n_repeats, 1)


def quad(n_repeats):
    return SquareMesh(n_repeats, n_repeats, 1, quadrilateral=True)


def tet(n_repeats):
    return CubeMesh(n_repeats, n_repeats, n_repeats, 1)


def hex(n_repeats):
    mesh2d = make_quad(n_repeats)
    return ExtrudedMesh(mesh2d, n_repeats)


def to_pvd(mesh, fname):
    outfile = File(fname)
    outfile.write(mesh)

