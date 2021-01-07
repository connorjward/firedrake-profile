"""Run the code and plot the output."""

import re
import subprocess
import sys

import matplotlib.pyplot as plt
import numpy as np


MESH_SIZES = np.logspace(3, 10, num=10, base=2, dtype=np.int)
N_REPEATS = 5


def parse_dof(stdout):
    pattern = r"Degrees-of-freedom: (\d+)"
    match = re.search(pattern, stdout)
    return int(match.group(1))


def parse_time(stdout):
    pattern = r"Wall-clock time: (.+) seconds"
    match = re.search(pattern, stdout)
    return float(match.group(1))


def main():
    test = sys.argv[1]
    if test not in ["orig", "mod"]:
        raise AssertionError

    dofs = []
    times = []
    for mesh_size in MESH_SIZES:
        cmd = ["python", f"{test}.py", str(mesh_size)]
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

    plt.plot(times, throughputs)
    plt.scatter(times, throughputs, color="k", marker="x")
    [plt.text(*pt) for pt in zip(times, throughputs, dofs)]
    plt.xlabel("Time")
    plt.ylabel("Throughput (DoF/s)")
    plt.xscale("log")
    plt.yscale("log")
    plt.grid(which="both")
    plt.tight_layout()
    plt.savefig(f"{test}.png")


if __name__ == "__main__":
    main()
