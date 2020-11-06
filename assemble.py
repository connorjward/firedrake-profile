"""
Script that assembles a matrix.
"""

import argparse

from firedrake import *

from form import make_form
from mesh import make_mesh


parser = argparse.ArgumentParser()
parser.add_argument("--form", default="helmholtz", type=str)
parser.add_argument("--mesh", default="tri", type=str,
                    choices=["tri", "quad", "tet", "hex"])
parser.add_argument("--mesh-size", default=10, type=int)
parser.add_argument("--degree", default=1, type=int)
parser.add_argument("--repeats", default=1, type=int)
args = parser.parse_args()

mesh = make_mesh(args.mesh, args.mesh_size)
V = FunctionSpace(mesh, "CG", degree=args.degree)

form = make_form(args.form, V)

# Do a warm start and save the resulting tensor to prevent reallocation 
# in future.
out = assemble(form)

# Do main run.
PETSc.Log.begin()

for _ in range(args.repeats):
    with PETSc.Log.Stage("assemble"):
        assemble(form, tensor=out)

# postprocessing
PETSc.Log.view()
