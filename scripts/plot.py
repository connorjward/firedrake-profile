"""
???
"""

import argparse

import matplotlib.pyplot as plt
import pandas as pd

from fireperf import logparser, plotter


FIGSIZE = (12, 12)


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
                plotter.plot_runtime(ax, filtered_df.dof, times)
            elif args.type == "efficiency":
                plotter.plot_efficiency(ax,filtered_df.dof, times)
            else:
                raise AssertionError()

            ax.set_title("mesh: {mesh}, degree: {degree}"
                                .format(mesh=mesh_type, degree=degree))

    fig.tight_layout()
    plt.savefig(f"{args.output_dir}/{form_type}.png")
