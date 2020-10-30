import matplotlib.pyplot as plt
from firedrake import *

import forms
import meshes


MESH_SIZE = 10
MESH_TYPE = "tri"

FORM_TYPE = "mass"
DEGREE = 1

N_WARM_START_REPEATS = 1
N_REPEATS = 5


# create the mesh
if MESH_TYPE == "tri":
    mesh = meshes.tri(MESH_SIZE)
elif MESH_TYPE == "quad":
    mesh = meshes.quad(MESH_SIZE)
elif MESH_TYPE == "tet":
    mesh = meshes.tet(MESH_SIZE)
elif MESH_TYPE == "hex":
    mesh = meshes.hex(MESH_SIZE)
else:
    raise AssertionError

# generate the form
if FORM_TYPE == "mass":
    form = forms.mass(mesh, DEGREE)
elif FORM_TYPE == "helmholtz":
    form = forms.helmholtz(mesh, DEGREE)
else:
    raise AssertionError

# do warm starts
for _ in range(N_WARM_START_REPEATS):
    out = assemble(form)

# do main run
for _ in range(N_REPEATS):
    assemble(form, tensor=out)
