import itertools as it

from mpi4py import MPI
import numpy as np

import fireperf.assemble
import fireperf.log


FORM_TYPES = fireperf.form.FORM_TYPES
MESH_TYPES = fireperf.mesh.MESH_TYPES_2D
MESH_SIZE = (2048, 2048)
DEGREE = 1
USE_ACTION = False
REPEATS = 5


# Do a warm start.
for _ in range(3):
    fireperf.assemble.assemble_form("helmholtz", "tri", (256, 256), 1, False, 5)

# Do the main run.
params = it.product(FORM_TYPES, MESH_TYPES)

for form_type, mesh_type in params:
    print(f"{MPI.COMM_WORLD.Get_size()} {form_type} {mesh_type}")

    dof = fireperf.assemble.assemble_form(form_type, mesh_type, MESH_SIZE, 
                                          DEGREE, USE_ACTION, REPEATS)

    log_fname = f"{form_type}_{mesh_type}_{dof}.txt"
    meta_fname = "metadata.csv"

    fireperf.log.write(log_fname)
    fireperf.log.write_metadata(meta_fname, log_fname, form_type, mesh_type,
                                DEGREE, dof)
