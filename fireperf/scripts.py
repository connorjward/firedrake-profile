import argparse
import itertools as it

import matplotlib.pyplot as plt
import pandas as pd
from firedrake import *
from firedrake.petsc import PETSc
from mpi4py import MPI

import fireperf.form
import fireperf.log
import fireperf.mesh


def assemble_form():

    def parse_args():
        parser = argparse.ArgumentParser()
        parser.add_argument("form_type", type=str, 
                            choices=fireperf.form.FORM_TYPES)
        parser.add_argument("mesh_type", type=str, 
                            choices=fireperf.mesh.MESH_TYPES)
        parser.add_argument("mesh_size", type=int)
        parser.add_argument("degree", type=int)
        parser.add_argument("repeats", type=int)
        parser.add_argument("log_fname", type=str)
        parser.add_argument("metadata_fname", type=str)
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

    # Save the output if rank 0.
    if MPI.COMM_WORLD.Get_rank() == 0:
        fireperf.log.write(args.log_fname)
        fireperf.log.write_metadata(args.metadata_fname, args.log_fname,
                                    args.form_type, args.mesh_type, args.degree,
                                    V.dof_count)


def plot_runtime():
    df = pd.read_csv("metadata.csv")

    form_types = df.form.unique()
    mesh_types = df.mesh.unique()
    degrees = df.degree.unique()

    params = it.product(form_types, mesh_types, degrees)

    for form_type, mesh_type, degree in params:
        print(f"{form_type} {mesh_type} {degree}")

        filtered_df = df[(df.form == form_type) 
                        & (df.mesh == mesh_type) 
                        & (df.degree == degree)]

        dofs = filtered_df.dof
        times = fireperf.log.parse_stage_times("Assemble", filtered_df.filename)

        fig, ax = plt.subplots()

        ax.plot(dofs, times)
        ax.scatter(dofs, times, color="k", marker="x")

        ax.set_xscale("log")
        ax.invert_xaxis()
        ax.set_xlabel("DoF")
        ax.set_ylabel("Time (s)")
        ax.set_yscale("log")
        ax.set_title(f"form: {form_type}, mesh: {mesh_type}, degree: {degree}")

        fig.tight_layout()
        plt.savefig(f"{form_type}_{mesh_type}_{degree}.png")


def plot_throughput():
    df = pd.read_csv("metadata.csv")

    form_types = df.form.unique()
    mesh_types = df.mesh.unique()
    degrees = df.degree.unique()

    params = it.product(form_types, mesh_types, degrees)

    for form_type, mesh_type, degree in params:
        print(f"{form_type} {mesh_type} {degree}")

        filtered_df = df[(df.form == form_type) 
                        & (df.mesh == mesh_type) 
                        & (df.degree == degree)]

        dofs = filtered_df.dof
        times = fireperf.log.parse_stage_times("Assemble", filtered_df.filename)

        throughput = [dof/time for dof, time in zip(dofs, times)]

        fig, ax = plt.subplots()

        ax.plot(dofs, throughput)
        ax.scatter(dofs, throughput, color="k", marker="x")

        ax.set_title(f"form: {form_type}, mesh: {mesh_type}, degree: {degree}")
        ax.set_xlabel("DoF")
        ax.invert_xaxis()
        ax.set_xscale("log")
        ax.set_ylabel("Throughput (DoF/s)")

        fig.tight_layout()
        plt.savefig(f"throughput_{form_type}_{mesh_type}_{degree}.png")
