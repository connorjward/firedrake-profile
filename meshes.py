from firedrake import *


def make(type, size):
    if type == "tri":
        return _make_tri(size)
    elif type == "quad":
        return _make_quad(size)
    elif type == "tet":
        return _make_tet(size)
    elif type == "hex":
        return _make_hex(size)


def to_pvd(mesh, fname):
    outfile = File(fname)
    outfile.write(mesh)


def _make_tri(n_repeats):
    return SquareMesh(n_repeats, n_repeats, 1)


def _make_quad(n_repeats):
    return SquareMesh(n_repeats, n_repeats, 1, quadrilateral=True)


def _make_tet(n_repeats):
    return CubeMesh(n_repeats, n_repeats, n_repeats, 1)


def _make_hex(n_repeats):
    mesh2d = _make_quad(n_repeats)
    return ExtrudedMesh(mesh2d, n_repeats)
