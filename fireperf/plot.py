import argparse

import matplotlib.pyplot as plt
import pandas as pd

import fireperf.log
from fireperf import DEFAULTS


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-o", "--output-file", type=str, default="figure.png")
    parser.add_argument("--metadata-file", type=str, default=DEFAULTS["metadata file"])

    return parser.parse_args()


def plot_runtime_vs_dof(output_fname, *, metadata_fname=DEFAULTS["metadata file"], form_type="helmholtz", mesh_type=DEFAULTS["mesh type"], degree=DEFAULTS["degree"], set_xlog=False):
    df = pd.read_csv(metadata_fname)

    df = df[(df.form == form_type) & (df.mesh == mesh_type) 
            & (df.degree == degree)]

    dofs = df.dof
    times = fireperf.log.parse_stage_times("Assemble", df.filename)

    fig, ax = plt.subplots()

    ax.plot(dofs, times)
    ax.scatter(dofs, times, color="k", marker="x")

    ax.set_xlabel("DoF")
    ax.set_ylabel("Time (s)")
    if set_xlog:
        ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_title(f"form: {form_type}, mesh: {mesh_type}, degree: {degree}")

    fig.tight_layout()
    plt.savefig(output_fname)


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

        #dofs = _get_total_dofs(filtered_df)
        dofs = filtered_df.mpi_size.unique()
        times = fireperf.log.parse_stage_times("Assemble", filtered_df.filename.unique())

        throughput = [dof/time for dof, time in zip(dofs, times)]

        fig, ax = plt.subplots()

        ax.plot(dofs, throughput)
        ax.scatter(dofs, throughput, color="k", marker="x")

        ax.set_title(f"form: {form_type}, mesh: {mesh_type}, degree: {degree}")
        ax.set_xlabel("DoF")
        #ax.invert_xaxis()
        #ax.set_xscale("log")
        ax.set_ylabel("Throughput (DoF/s)")

        fig.tight_layout()
        plt.savefig(f"throughput_{form_type}_{mesh_type}_{degree}.png")


def _get_average_dofs(df):
    dofs = []
    for fname in df.filename:
        dofs.append(df[df.filename == fname].dof.mean())
    return dofs


def _get_total_dofs(df):
    dofs = []
    for fname in df.filename:
        dofs.append(df[df.filename == fname].dof.sum())
    return dofs