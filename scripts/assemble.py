import argparse
import cProfile
import pstats 

import matplotlib.pyplot as plt
import pandas as pd

from firedrake import *
from firedrake.petsc import PETSc
import fireperf.form
import fireperf.log
import fireperf.mesh
from fireperf import metadata


def assemble_form():
    args = _parse_args()

    m = fireperf.mesh.make_mesh(args.mesh_type, args.mesh_size)
    V = FunctionSpace(m, "CG", degree=args.degree)
    form = fireperf.form.make_form(args.form_type, V)

    if args.use_action:
        form = action(form, Function(V))

    if args.verbose:
        PETSc.Sys.Print(f"DoF: {V.dim()}")

    # Do a warm start and save the resulting tensor to prevent reallocation
    # in future.
    out = assemble(form)

    # Do the main run.
    if args.profiler == "petsc":
        PETSc.Log.begin()

        for _ in range(args.repeats):
            with PETSc.Log.Stage("Assemble"):
                assemble(form, tensor=out)

        PETSc.Log.view(PETSc.Viewer.ASCII(args.fout))
    elif args.profiler == "cprofile":
        pr = cProfile.Profile()
        pr.enable()

        for _ in range(args.repeats):
            assemble(form, tensor=out)

        pr.disable()
        pstats.Stats(pr).dump_stats(args.fout)
    else:
        raise AssertionError


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("form_type", type=str, 
                        choices=fireperf.form.FORM_TYPES)
    parser.add_argument("mesh_type", type=str, 
                        choices=fireperf.mesh.MESH_TYPES)
    parser.add_argument("mesh_size", type=int)
    parser.add_argument("degree", type=int)
    parser.add_argument("repeats", type=int)
    parser.add_argument("-o", dest="fout", type=str, default="assemble.out")
    parser.add_argument("-v", dest="verbose", action="store_true")
    parser.add_argument("--use-action", action="store_true")
    parser.add_argument("--profiler", type=str, default="petsc",
                        choices=["petsc", "cprofile"])
    return parser.parse_args()


if __name__ == "__main__":
    assemble_form()