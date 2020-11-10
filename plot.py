"""
???
"""

import argparse

import matplotlib.pyplot as plt
import pandas as pd

from fireperf import logparser


FIGSIZE = (12, 12)


def plot_runtime(ax, dofs, times):
    ax.plot(dofs, times)
    ax.scatter(dofs, times, color="k", marker="x")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.invert_xaxis()
    ax.set_ylabel("Time (s)")


def plot_efficiency(ax, dof, times):
    t_max = times[-1]
    speedups = [time / t_max for time in times]

    ax.plot(dof, speedups)
    ax.scatter(dof, speedups, color="k", marker="x")

    ax.set_xscale("log")
    ax.invert_xaxis()
    ax.set_ylabel("Parallel efficiency")


parser = argparse.ArgumentParser()
parser.add_argument("--type", default="runtime", type=str, 
                    choices=["runtime", "efficiency"])
parser.add_argument("--data-dir", default=".", type=str,
                    help="Location of the data files.")
parser.add_argument("--output-dir", default=".", type=str,
                    help="Location where the produced figures will be kept.")
args = parser.parse_args()

try:
    df = pd.read_csv(f"{args.data_dir}/metadata.csv")
except FileNotFoundError:
    print("The metadata file could not be found. Make sure you specify the "
          "correct data directory.")
    exit(1)

form_types = df.form.unique()
mesh_types = df.mesh.unique()
degrees = df.degree.unique()

for form_type in form_types:
    # Create the figure.
    fig, axs = plt.subplots(len(mesh_types), len(degrees), figsize=FIGSIZE)
    fig.suptitle(form_type)

    for i, mesh_type in enumerate(mesh_types):
        for j, degree in enumerate(degrees):
            # Filter the data.
            filtered_df = df[(df.form == form_type) 
                             & (df.mesh == mesh_type) 
                             & (df.degree == degree)]

            times = []
            for filename in filtered_df.filename:
                with open(f"{args.data_dir}/{filename}") as f:
                    log = f.read()
                stages = logparser.parse_stages(log)
                times.append(float(stages["Assemble"].group("time")))

            ax = axs[i, j]

            if args.type == "runtime":
                plot_runtime(ax, filtered_df.dof, times)
            elif args.type == "efficiency":
                plot_efficiency(ax,filtered_df.dof, times)
            else:
                raise AssertionError()

            ax.set_title("mesh: {mesh}, degree: {degree}"
                                .format(mesh=mesh_type, degree=degree))
            ax.set_xlabel("DoF")

    fig.tight_layout()
    plt.savefig(f"{args.output_dir}/{form_type}.png")
