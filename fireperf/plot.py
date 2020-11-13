import argparse
from itertools import product

import matplotlib.pyplot as plt
import pandas as pd

from logparser import LogParser


def plot_runtime(ax, dofs, times):
    _plot_dofs(ax, dofs, times)

    ax.set_ylabel("Time (s)")
    ax.set_yscale("log")


def plot_throughput(ax, dofs, times):
    t_max = times[-1]
    speedups = [time / t_max for time in times]

    _plot_dofs(ax, dofs, speedups)

    ax.set_ylabel("Parallel efficiency")
    ax.set_xscale("log")


def _plot_dofs(ax, dofs, ys):
    ax.plot(dofs, ys)
    ax.scatter(dofs, ys, color="k", marker="x")

    ax.set_xscale("log")
    ax.invert_xaxis()
    ax.set_xlabel("DoF")


def _parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", default="runtime", type=str, 
                        choices=["runtime", "efficiency"])
    parser.add_argument("--data-dir", default=".", type=str,
                        help="Location of the data files.")
    parser.add_argument("--output-dir", default=".", type=str,
                        help="Location where the produced figures will be kept.")
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_command_line()

    try:
        df = pd.read_csv(f"{args.data_dir}/metadata.csv")
    except FileNotFoundError:
        print("The metadata file could not be found. Make sure you specify the "
            "correct data directory.")
        exit(1)

    forms = df.form.unique()
    meshes = df.mesh.unique()
    degrees = df.degree.unique()

    for form, mesh, degree in product(forms, meshes, degrees):
        # Filter the data.
        filtered_df = df[(df.form == form) 
                         & (df.mesh == mesh) 
                         & (df.degree == degree)]

        times = []
        for filename in filtered_df.filename:
            log = LogParser(f"{args.data_dir}/{filename}")
            stages = log.parse_stages()
            times.append(float(stages["Assemble"].group("time")))

        fig, ax = plt.subplots()

        if args.type == "runtime":
            plot_runtime(ax, filtered_df.dof, times)
        elif args.type == "throughput":
            plot_throughput(ax,filtered_df.dof, times)
        else:
            raise AssertionError()

        ax.set_title(f"form: {form}, mesh: {mesh}, degree: {degree}")

        fig.tight_layout()
        plt.savefig(f"{args.output_dir}/{form}_{mesh}_{degree}.png")
