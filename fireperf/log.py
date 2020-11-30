"""
???
"""

import re

from firedrake import *
from firedrake.petsc import PETSc
#from mpi4py import MPI


class Pattern:
    scientific_notation = r"\d+.\d+e[+-]\d+"
    percent = r"\d+.\d+%"


class LogParser:

    def __init__(self, fname):
        with open(fname) as f:
            self._text = f.read()

        self._stages = []


    def parse_stages(self):
        """
        Return a list of matches corresponding to the 'Summary of Stages'
        section of the PETSc log output.
        """
        patterns = [r"\s+\d+:\s+(?P<name>.*):"]
        for prefix in ["time", "flop", "mess", "mess_len", "rdct"]:
            pattern = (r"\s+(?P<{prefix}>{sci_num})"
                        r"\s+(?P<{prefix}_percent>{percent})"
                        .format(prefix=prefix,
                                sci_num=Pattern.scientific_notation, 
                                percent=Pattern.percent))
            patterns.append(pattern)

        matches = re.finditer("".join(patterns), self._text)

        self._stages = [match.groupdict() for match in matches]

    
    def get_stage_time(self, stage_name):
        for stage in self._stages:
            if stage["name"] == stage_name:
                return float(stage["time"])
        raise KeyError


def parse_stage_times(stage_name, fnames):
    times = []
    for fname in fnames:
        parser = LogParser(fname)
        parser.parse_stages()
        times.append(parser.get_stage_time(stage_name))
    return times


def write(fname):
    PETSc.Log.view(PETSc.Viewer.ASCII(fname))


def write_metadata(meta_fname, log_fname, form_type, mesh_type, degree, dof):
    n_cores = COMM_WORLD.Get_size()
    total_dof = COMM_WORLD.allreduce(dof)

    if COMM_WORLD.Get_rank() == 0:
        with open(meta_fname, "a") as f:
            # Add a header if the file is empty.
            if f.tell() == 0:
                f.write("filename,n_cores,form,mesh,degree,dof\n")

            f.write(f"{log_fname},{n_cores},{form_type},"
                    f"{mesh_type},{degree},{total_dof}\n")
