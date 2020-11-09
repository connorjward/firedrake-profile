import glob
import re

import matplotlib.pyplot as plt

import logparser


FORM_TYPE = "mass"
MESH_TYPE = "tri"
DEGREE = 1

pattern = "{form}_{mesh}_{degree}_*.txt".format(form=FORM_TYPE, mesh=MESH_TYPE, degree=DEGREE)

filenames = glob.glob(pattern)

dofs = []
times = []

for filename in filenames:
    match = re.fullmatch(r"(\w+)_(\w+)_(\d+)_(?P<dof>\d+).txt", filename)
    dofs.append(match.group("dof"))

    with open(filename) as f:
        log = f.read()
    stages = logparser.parse_stages(log)
    times.append(stages[-1].group("time"))

plt.plot(dofs, times)
plt.scatter(dofs, times, color="k", marker="x")
plt.savefig(pattern + ".png")
