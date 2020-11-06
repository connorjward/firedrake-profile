import matplotlib.pyplot as plt
import pyop2.profiling
from firedrake import *

from problem import Problem


MESH_SIZE = 10
MESH_TYPE = "quad"

FORM_TYPE = "helmholtz"
DEGREE = 1

N_WARM_START_REPEATS = 1
N_REPEATS = 5


problem = Problem(MESH_TYPE, MESH_SIZE, DEGREE, FORM_TYPE)

# do warm starts
for _ in range(N_WARM_START_REPEATS):
    out = assemble(problem.form)

PETSc.Log.begin()
# do main run
for _ in range(N_REPEATS):
    with PETSc.Log.Stage("assemble"):
        assemble(problem.form, tensor=out)

# postprocessing
#PETSc.Log.view()
print("DoF: {}".format(problem.function_space.dof_count))
