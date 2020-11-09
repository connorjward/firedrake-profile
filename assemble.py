"""
Script that assembles a matrix.
"""

import argparse

from firedrake import *
from firedrake.petsc import OptionsManager

from form import make_form
from mesh import make_mesh


parser = argparse.ArgumentParser()
parser.add_argument("-o", dest="log_file", default="log.txt", type=str)
parser.add_argument("--meta", dest="meta_file", default="metadata.csv", 
                    type=str, help="Location of the metadata file.")
parser.add_argument("--form", default="helmholtz", type=str)
parser.add_argument("--mesh", default="tri", type=str,
                    choices=["tri", "quad", "tet", "hex"])
parser.add_argument("--mesh-size", default=10, type=int)
parser.add_argument("--degree", default=1, type=int)
parser.add_argument("--repeats", default=1, type=int)
args = parser.parse_args()

# Enable PETSc logging.
PETSc.Log.begin()

with PETSc.Log.Stage("Make mesh"):
    mesh = make_mesh(args.mesh, args.mesh_size)

with PETSc.Log.Stage("Make function space"):
    V = FunctionSpace(mesh, "CG", degree=args.degree)

with PETSc.Log.Stage("Make form"):
    form = make_form(args.form, V)

# Do a warm start and save the resulting tensor to prevent reallocation
# in future.
with PETSc.Log.Stage("Assemble (warm start)"):
    out = assemble(form)

# Do main run.
for _ in range(args.repeats):
    with PETSc.Log.Stage("Assemble"):
        assemble(form, tensor=out)


# postprocessing
print("# cells: {}, DoF: {}".format(mesh.num_cells(), V.dof_count))


# Save the log output to a file.
PETSc.Log.view(PETSc.Viewer.ASCII(args.log_file))

# Save the metadata file, appending to the file if it already exists.
with open(args.meta_file, "a") as f:
    # Add a header if the file is empty.
    if f.tell() == 0:
        f.write("filename,dof\n")

    line = "{filename},{dof}\n".format(filename=args.log_file, dof=V.dof_count)
    f.write(line)