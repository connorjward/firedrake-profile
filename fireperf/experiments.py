import argparse
import tempfile
import subprocess


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-o", "--output-dir", type=str, default=".")

    return parser.parse_args()


def do_warm_start(with_mpi=False):
    n_cores = 1 if not with_mpi else 2

    with tempfile.TemporaryDirectory() as tmpdir:
        do_experiment(cwd=tmpdir, n_cores=n_cores)


def do_experiment(*, form_type="helmholtz", mesh_type="tri", mesh_size=128, 
                  degree=1, repeats=5, log_fname=None, 
                  metadata_fname="metadata.csv", cwd=".", n_cores=1):
    # If log_fname is not specified then create a randomly named file in the 
    # current directory.
    if log_fname is None:
        logfile = tempfile.NamedTemporaryFile(suffix=".txt", prefix="log", 
                                              dir=cwd, delete=False)
        log_fname = logfile.name

    cmd = ["assemble-form", form_type, mesh_type, str(mesh_size), str(degree),
           str(repeats), log_fname, metadata_fname]

    if n_cores > 1:
        cmd = ["mpirun", "-np", str(n_cores), "--bind-to", "hwthread"] + cmd

    print(" ".join(cmd))
    subprocess.run(cmd, cwd=cwd)
