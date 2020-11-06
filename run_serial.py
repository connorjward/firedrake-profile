"""
"""

import subprocess

import numpy as np


FORM_TYPES = ["mass", "helmholtz"]
MESH_TYPES = ["tri", "quad", "tet", "hex"]
DEGREES = range(1, 4)
N_REPEATS = 5


def get_mesh_sizes(mesh_type):
    if mesh_type in ["tri", "quad"]:
        return np.linspace(100, 750, 10, dtype=np.int)
    else:
        return np.linspace(20, 60, 10, dtype=np.int)


for form_type in FORM_TYPES:
    for mesh_type in MESH_TYPES:
        for mesh_size in get_mesh_sizes(mesh_type):
            for degree in DEGREES:
                cmd = ["python", "assemble.py",
                    "--form", form_type,
                    "--mesh", mesh_type,
                    "--mesh-size", str(mesh_size),
                    "--degree", str(degree),
                    "--repeats", str(N_REPEATS)]

                print(" ".join(cmd))

                subprocess.run(cmd, check=True)
