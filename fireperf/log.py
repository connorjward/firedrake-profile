"""
???
"""

import re

from firedrake.petsc import PETSc
from mpi4py import MPI


class Pattern:
    scientific_notation = r"\d+.\d+e[+-]\d+"
    percent = r"\d+.\d+%"


class LogParser:

    def __init__(self, fname):
        with open(fname) as f:
            self._text = f.read()


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
        return {match.group("name"): match for match in matches}


def write(fname):
    PETSc.Log.view(PETSc.Viewer.ASCII(fname))


def write_metadata(meta_fname, log_fname, form_type, mesh_type, degree, dof):
    # Save the file, appending if it already exists.
    with open(meta_fname, "a") as f:
        # Add a header if the file is empty.
        if f.tell() == 0:
            f.write("filename,np,form,mesh,degree,dof\n")

        np = MPI.COMM_WORLD.Get_size()

        f.write(f"{log_fname},{np},{form_type},{mesh_type},{degree},{dof}\n")

