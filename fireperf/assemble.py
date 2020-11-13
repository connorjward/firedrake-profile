"""
Script that assembles a matrix.
"""

import argparse
from itertools import product

from firedrake import *

import fireperf
from fireperf.form import make_form
from fireperf.mesh import make_mesh


def assemble_form(form_type, mesh_type, mesh_size, degree, use_action, repeats):
    if ((fireperf.mesh.is_2d(mesh_type) and len(mesh_size) != 2)
            or (fireperf.mesh.is_3d(mesh_type) and len(mesh_size) != 3)):
        raise AssertionError()

    mesh = make_mesh(mesh_type, mesh_size)
    V = FunctionSpace(mesh, "CG", degree=degree)

    if use_action:
        two_form = make_form(form_type, V)
        form = action(two_form, Function(V))
    else:
        form = make_form(form_type, V)

    # Do a warm start and save the resulting tensor to prevent reallocation
    # in future.
    out = assemble(form)


    # Do main run.
    for _ in range(repeats):
        with PETSc.Log.Stage("Assemble"):
            assemble(form, tensor=out)
