"""Run the code and plot the output."""

import os
import re
import subprocess

import matplotlib.pyplot as plt
import numpy as np


PROJECT_DIR = os.path.expandvars("$HOME/projects/improve-strong-scaling")

MESH_SIZES = np.logspace(3, 10, num=10, base=2, dtype=np.int)
N_REPEATS = 3


def checkout_repo(branch_id, git_dir="."):
    cmd = "git -C {} checkout {}".format(git_dir, branch_id)
    subprocess.run(cmd.split(), check=True)


def checkout_firedrake(branch_id="master"):
    git_dir = "{}/firedrake/src/firedrake".format(PROJECT_DIR)
    checkout_repo(branch_id, git_dir)


def checkout_pyop2(branch_id="master"):
    git_dir = "{}/firedrake/src/PyOP2".format(PROJECT_DIR)
    checkout_repo(branch_id, git_dir)


def checkout_old_firedrake():
    branch_id = "f2232f48"
    checkout_firedrake(branch_id)


def checkout_old_pyop2():
    branch_id = "36529246"
    checkout_pyop2(branch_id)


def parse_dof(stdout):
    pattern = r"Degrees-of-freedom: (\d+)"
    match = re.search(pattern, stdout)
    return int(match.group(1))


def parse_time(stdout):
    pattern = r"Wall-clock time: (.+) seconds"
    match = re.search(pattern, stdout)
    return float(match.group(1))


def do_measurement():
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

    throughputs = [dof / time for dof, time in zip(dofs, times)]

    plt.plot(times, throughputs)
    plt.scatter(times, throughputs, color="k", marker="x")
    [plt.text(*pt) for pt in zip(times, throughputs, dofs)]


def main():
    checkout_old_firedrake()
    checkout_old_pyop2()
    do_measurement()

    checkout_firedrake()
    checkout_pyop2()
    do_measurement()

    plt.xlabel("Time")
    plt.ylabel("Throughput (DoF/s)")
    plt.xscale("log")
    plt.yscale("log")
    plt.grid(which="both")
    plt.tight_layout()
    plt.savefig("comparison.png")


if __name__ == "__main__":
    main()
