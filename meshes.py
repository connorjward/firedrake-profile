from firedrake import *


def tri(n_repeats):
    return SquareMesh(n_repeats, n_repeats, 1)


def quad(n_repeats):
    return SquareMesh(n_repeats, n_repeats, 1, quadrilateral=True)


def tet(n_repeats):
    mesh = SquareMesh(n_repeats, n_repeats, 1) 
    return ExtrudedMesh(mesh, n_repeats)


def hex(n_repeats):
    mesh = SquareMesh(n_repeats, n_repeats, 1, quadrilateral=True) 
    return ExtrudedMesh(mesh, n_repeats)


def to_pvd(mesh, fname):
    outfile = File(fname)
    outfile.write(mesh)

