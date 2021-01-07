"""Run the code and plot the output."""

import pickle
import re
import subprocess

import matplotlib.pyplot as plt
import numpy as np


MESH_SIZES = np.logspace(3, 10, num=6, base=2, dtype=np.int)
N_REPEATS = 5


def parse_dof(stdout):
    pattern = r"Degrees-of-freedom: (\d+)"
    match = re.search(pattern, stdout)
    return int(match.group(1))


def parse_time(stdout):
    pattern = r"Wall-clock time: (.+) seconds"
    match = re.search(pattern, stdout)
    return float(match.group(1))


def checkout_pyop2_branch(branch_name):
    cmd = ["git", "-C", "/home/connor/projects/improve-firedrake-scaling/firedrake/src/PyOP2", "checkout", branch_name]
    subprocess.run(cmd, check=True)


def run(branch_name):
    checkout_pyop2_branch(branch_name)

    dofs = []
    times = []
    for mesh_size in MESH_SIZES:
        cmd = ["python", "solve.py", str(mesh_size)]
        print(" ".join(cmd))

        _dofs = []
        _times = []
        for _ in range(N_REPEATS):
            stdout = subprocess.check_output(cmd, universal_newlines=True)
            _dofs.append(parse_dof(stdout))
            _times.append(parse_time(stdout))
        dofs.append(sum(_dofs) / N_REPEATS)
        times.append(sum(_times) / N_REPEATS)
    throughputs = [dof/time for dof, time in zip(dofs, times)]

    data = {"dofs": dofs, "times": times, "throughputs": throughputs}
    with open(f"{branch_name}.pkl", "wb") as f:
        pickle.dump(data, f)


def main():
    run("test-without-kernel-cache")
    run("test-with-kernel-cache")


if __name__ == "__main__":
    main()
