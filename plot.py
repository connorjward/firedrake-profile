"""
???
"""

import argparse

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd

import logparser


FORM_TYPES = ["mass", "helmholtz"]
MESH_TYPES = ["tri", "quad", "tet", "hex"]
DEGREES = range(1, 3)


def plot_runtime(ax, dofs, times):
    ax.plot(dofs, times)
    ax.scatter(dofs, times, color="k", marker="x")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.invert_xaxis()


def plot_speedup(ax, dof, times):
    t_max = times[-1]
    speedups = [time / t_max for time in times]

    ax.plot(dof, speedups)
    ax.scatter(dof, speedups, color="k", marker="x")

    ax.set_xscale("log")
    ax.invert_xaxis()


parser = argparse.ArgumentParser()
parser.add_argument("metadata_file", type=str, 
                    help="Location of the metadata file.")
parser.add_argument("--type", default="time", type=str, 
                    choices=["time", "speedup"])
parser.add_argument("--output-dir", default=".", type=str)
args = parser.parse_args()

df = pd.read_csv(args.metadata_file)

for form_type in FORM_TYPES:
    # Create the figure.
    fig, axs = plt.subplots(len(MESH_TYPES), len(DEGREES), figsize=(10, 14))
    fig.suptitle(form_type)

    for i, mesh_type in enumerate(MESH_TYPES):
        for j, degree in enumerate(DEGREES):
            # Filter the data.
            filtered_df = df[(df.form == form_type) 
                             & (df.mesh == mesh_type) 
                             & (df.degree == degree)]

            times = []
            for filename in filtered_df.filename:
                with open(filename) as f:
                    log = f.read()
                stages = logparser.parse_stages(log)
                times.append(float(stages["Assemble"].group("time")))

            ax = axs[i, j]

            if args.type == "time":
                plot_runtime(ax, filtered_df.dof, times)
                ax.set_ylabel("Time (s)")
            elif args.type == "speedup":
                plot_speedup(ax,filtered_df.dof, times)
                ax.set_ylabel("S")
            else:
                raise AssertionError()

            ax.set_title("mesh: {mesh}, degree: {degree}"
                                .format(mesh=mesh_type, degree=degree))
            ax.set_xlabel("DoF")

    fig.tight_layout()
    plt.savefig("{dir}/{form_type}.png".format(dir=args.output_dir, 
                                               form_type=form_type))
