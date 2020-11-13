import argparse
from itertools import product

import matplotlib.pyplot as plt
import pandas as pd

from fireperf.log import LogParser


def plot_runtime(ax, dofs, times):
    _plot_dofs(ax, dofs, times)

    ax.set_ylabel("Time (s)")
    ax.set_yscale("log")


def plot_throughput(ax, dofs, times):
    t_max = times[-1]
    speedups = [time / t_max for time in times]

    _plot_dofs(ax, dofs, speedups)

    ax.set_ylabel("Parallel efficiency")
    ax.set_xscale("log")


def _plot_dofs(ax, dofs, ys):
    ax.plot(dofs, ys)
    ax.scatter(dofs, ys, color="k", marker="x")

    ax.set_xscale("log")
    ax.invert_xaxis()
    ax.set_xlabel("DoF")
