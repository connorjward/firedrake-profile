import matplotlib.pyplot as plt
import pandas as pd

import logparser


META_FNAME = "/home/connor/data/firedrake-profile/metadata.csv"

df = pd.read_csv(META_FNAME)

times = []
for filename in df.filename:
    with open(filename) as f:
        log = f.read()
    stages = logparser.parse_stages(log)
    times.append(stages["Assemble"].group("time"))

plt.plot(df.dof, times)
plt.scatter(df.dof, times, color="k", marker="x")
plt.savefig("figure")
