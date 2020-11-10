"""
"""

import argparse
import subprocess


FORM_TYPES = ["mass", "helmholtz"]
MESH_TYPES = ["tri", "quad", "tet", "hex"]
MESH_REFINEMENT_LEVELS = range(1, 6)
DEGREES = range(1, 4)
N_REPEATS = 5


parser = argparse.ArgumentParser()
parser.add_argument("--output-dir", default=".", type=str)
args = parser.parse_args()

# Run the tests.
for form_type in FORM_TYPES:
    for mesh_type in MESH_TYPES:
        for mesh_refinement_level in MESH_REFINEMENT_LEVELS:
            for degree in DEGREES:
                log_fname = (f"{form_type}_{mesh_type}_"
                             f"{mesh_refinement_level}_{degree}.txt")
                meta_fname = "metadata.csv"

                cmd = ["python", "assemble.py",
                       "-o", f"{args.output_dir}/{log_fname}",
                       "--meta", f"{args.output_dir}/{meta_fname}",
                       "--form", form_type,
                       "--mesh", mesh_type,
                       "--mesh-refinement-level", str(mesh_refinement_level),
                       "--degree", str(degree),
                       "--repeats", str(N_REPEATS)]

                print(" ".join(cmd))
                subprocess.run(cmd, check=True)
