import argparse

import matplotlib.pyplot as plt
import pandas as pd
from firedrake import *
from firedrake.petsc import PETSc

import fireperf.form
import fireperf.log
import fireperf.mesh


def assemble_form():

    def parse_args():
        parser = argparse.ArgumentParser()
        parser.add_argument("output_fname", type=str)
        parser.add_argument("metadata_fname", type=str)
        parser.add_argument("form_type", type=str, 
                            choices=fireperf.form.FORM_TYPES)
        parser.add_argument("mesh_type", type=str, 
                            choices=fireperf.mesh.MESH_TYPES)
        parser.add_argument("mesh_size", type=int)
        parser.add_argument("degree", type=int)
        parser.add_argument("repeats", type=int)
        parser.add_argument("--use-action", action="store_true")
        return parser.parse_args()


    args = parse_args()

    m = fireperf.mesh.make_mesh(args.mesh_type, args.mesh_size)
    V = FunctionSpace(m, "CG", degree=args.degree)
    form = fireperf.form.make_form(args.form_type, V)

    if args.use_action:
        form = action(form, Function(V))

    # Do a warm start and save the resulting tensor to prevent reallocation
    # in future.
    out = assemble(form)

    # Start profiling.
    PETSc.Log.begin()

    # Do main run.
    for _ in range(args.repeats):
        with PETSc.Log.Stage("Assemble"):
            assemble(form, tensor=out)

    # Save the output.
    fireperf.log.write(args.output_fname)
    fireperf.log.write_metadata(args.metadata_fname, args.output_fname,
                                args.form_type, args.mesh_type, args.degree,
                                V.dof_count)
