import argparse
import tempfile
import subprocess

import matplotlib.pyplot as plt
import pandas as pd

import fireperf.log


DEFAULTS = {
    "form type": "helmholtz",
    "mesh type": "tri",
    "degree": 1,
}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", type=str)
    return parser.parse_args()


def parse_plotting_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("metadata_filename", type=str)
    parser.add_argument("output_dir", type=str)
    return parser.parse_args()


def do_warm_start(with_mpi=False):
    n_cores = 1 if not with_mpi else 2

    with tempfile.TemporaryDirectory() as tmpdir:
        do_experiment(cwd=tmpdir, n_cores=n_cores)


def do_experiment(*, form_type="helmholtz", mesh_type="tri", mesh_size=128, 
                  degree=1, repeats=5, log_fname=None, 
                  metadata_fname="metadata.csv", cwd=".", n_cores=1):
    # If log_fname is not specified then create a randomly named file in the 
    # current directory.
    if log_fname is None:
        logfile = tempfile.NamedTemporaryFile(suffix=".txt", prefix="log", 
                                              dir=cwd, delete=False)
        log_fname = logfile.name

    cmd = ["assemble-form", log_fname, metadata_fname, form_type, mesh_type, str(mesh_size), str(degree),
           str(repeats)]

    if n_cores > 1:
        cmd = ["mpirun", "-np", str(n_cores), "--bind-to", "hwthread"] + cmd

    print(" ".join(cmd))
    subprocess.run(cmd, cwd=cwd)

def plot_runtime_vs_dof(output_fname, metadata_fname, *, form_type=DEFAULTS["form type"], mesh_type=DEFAULTS["mesh type"], degree=DEFAULTS["degree"], use_log_xscale=True):
    """Produce a single plot."""
    df = pd.read_csv(metadata_fname)
    df = df[(df.form == form_type) & (df.mesh == mesh_type) 
            & (df.degree == degree)]

    dofs = df.dof
    times = fireperf.log.parse_stage_times("Assemble", df.filename)

    plt.plot(dofs, times)
    plt.scatter(dofs, times, color="k", marker="x")

    plt.xlabel("DoF")
    plt.ylabel("Time (s)")
    plt.yscale("log")
    plt.title(_get_plot_title(df))

    if use_log_xscale:
        plt.xscale("log")

    plt.tight_layout()
    plt.savefig(output_fname)
    plt.clf()


def plot_throughput_vs_dof(output_fname, metadata_fname, use_log_xscale=True, **kwargs):
    df = pd.read_csv(metadata_fname)

    form_type = kwargs.get("form_type", DEFAULTS["form type"])
    mesh_type = kwargs.get("mesh_type", DEFAULTS["mesh type"])
    degree = kwargs.get("degree", DEFAULTS["degree"])

    df = df[(df.form == form_type)
            & (df.mesh == mesh_type) 
            & (df.degree == degree)]

    dofs = df.dof
    times = fireperf.log.parse_stage_times("Assemble", df.filename)

    throughputs = [dof/time for dof, time in zip(dofs, times)]

    plt.plot(dofs, throughputs)
    plt.scatter(dofs, throughputs, color="k", marker="x")

    plt.xlabel("DoF")
    plt.ylabel("Throughput (DoF/s)")
    plt.yscale("log")
    plt.title(_get_plot_title(df))

    if use_log_xscale:
        plt.xscale("log")

    plt.tight_layout()
    plt.savefig(output_fname)
    plt.clf()


def _get_plot_title(df):
    """Return a string containing all of the constant columns 
       of the DataFrame."""
    const_cols = {}
    for col in df.columns:
        if df[col].nunique() == 1:
            const_cols[col] = df[col][0]

    return str(const_cols)
