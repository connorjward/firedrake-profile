"""Run the code and plot the output."""

import pickle
import re
import subprocess

import matplotlib.pyplot as plt
import numpy as np


MESH_SIZES = np.logspace(3, 8, num=6, base=2, dtype=np.int)
N_REPEATS = 3


def plot(branch_name):
    with open(f"{branch_name}.pkl", "rb") as f:
        data = pickle.load(f)
    dofs = data["dofs"]
    times = data["times"]

    plt.plot(dofs, times, label=branch_name)
    plt.scatter(dofs, times, color="k", marker="x")

def main():
    plot("test-without-kernel-cache")
    plot("test-with-kernel-cache")

    plt.xlabel("DoF")
    plt.ylabel("Time (s)")
    #plt.xscale("log")
    #plt.yscale("log")
    plt.grid(which="both")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"compare_linear.png")



if __name__ == "__main__":
    main()
