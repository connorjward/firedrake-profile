"""
???
"""

import argparse

import matplotlib.pyplot as plt
import pandas as pd

import logparser


FORM_TYPES = ["mass", "helmholtz"]
MESH_TYPES = ["tri", "quad", "tet", "hex"]
DEGREES = range(1, 3)

parser = argparse.ArgumentParser()
parser.add_argument("metadata_file", type=str, 
                    help="Location of the metadata file.")
parser.add_argument("--output-dir", default=".", type=str)
args = parser.parse_args()

df = pd.read_csv(args.metadata_file)

for form_type in FORM_TYPES:
    for mesh_type in MESH_TYPES:
        for degree in DEGREES:
            # Filter the data.
            filtered_df = df[(df.form == form_type) 
                             & (df.mesh == mesh_type) 
                             & (df.degree == degree)]

            times = []
            for filename in filtered_df.filename:
                with open(filename) as f:
                    log = f.read()
                stages = logparser.parse_stages(log)
                times.append(stages["Assemble"].group("time"))

            fig, ax = plt.subplots()
            ax.plot(filtered_df.dof, times)
            ax.scatter(filtered_df.dof, times, color="k", marker="x")
            fig.tight_layout()
            plt.savefig("{dir}/{form_type}_{mesh_type}_{degree}.png"
                        .format(dir=args.output_dir, form_type=form_type, 
                                mesh_type=mesh_type, degree=degree))
