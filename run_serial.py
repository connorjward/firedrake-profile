"""
"""

import argparse
import datetime
import os
import subprocess

import numpy as np


FORM_TYPES = ["mass", "helmholtz"]
MESH_TYPES = ["tri", "quad", "tet", "hex"]
DEGREES = range(1, 4)
N_REPEATS = 5


parser = argparse.ArgumentParser()
parser.add_argument("base_dir", type=str)
args = parser.parse_args()


def get_mesh_sizes(mesh_type):
    """Return an appropriate array of mesh sizes so that all models
    have approximately the same range of DoFs."""

    # First the 2D case then the 3D one.
    if mesh_type in ["tri", "quad"]:
        return np.linspace(100, 750, 10, dtype=np.int)
    else:
        return np.linspace(20, 60, 10, dtype=np.int)


# Store the results in a time-stamped directory.
data_dir = (args.base_dir + "/" 
            + datetime.datetime.now().isoformat(timespec="seconds") + "/")
os.mkdir(data_dir)

# Run the tests.
for form_type in FORM_TYPES:
    for mesh_type in MESH_TYPES:
        for mesh_size in get_mesh_sizes(mesh_type):
            for degree in DEGREES:
                log_fname = ("{form}_{mesh}_{size}_{degree}.txt"
                             .format(form=form_type, mesh=mesh_type,
                                     size=mesh_size, degree=degree))
                meta_fname = "metadata.csv"

                cmd = ["python", "assemble.py",
                       "-o", data_dir + log_fname,
                       "--meta", data_dir + meta_fname,
                       "--form", form_type,
                       "--mesh", mesh_type,
                       "--mesh-size", str(mesh_size),
                       "--degree", str(degree),
                       "--repeats", str(N_REPEATS)]

                print(" ".join(cmd))
                subprocess.run(cmd, check=True)
