"""Run the code and plot the output."""

import pickle
import re
import subprocess

import matplotlib.pyplot as plt
import numpy as np


MESH_SIZES = np.logspace(3, 8, num=6, base=2, dtype=np.int)
N_REPEATS = 3


def run(branch_name):
    with open(f"{branch_name}.pkl", "rb") as f:
        data = pickle.load(f)
    dofs = data["dofs"]
    times = data["times"]
    throughputs = data["throughputs"]

    plt.plot(times, throughputs, label=branch_name)
    plt.scatter(times, throughputs, color="k", marker="x")
    [plt.text(*pt) for pt in zip(times, throughputs, dofs)]



def main():
    run("test-without-kernel-cache")
    run("test-with-kernel-cache")

    plt.xlabel("Time")
    plt.ylabel("Throughput (DoF/s)")
    plt.xscale("log")
    plt.yscale("log")
    plt.grid(which="both")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"plot_compare_log.png")


if __name__ == "__main__":
    main()
