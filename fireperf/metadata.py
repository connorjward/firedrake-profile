from firedrake import COMM_WORLD


class Row:

    def __init__(self, filename, form_type, mesh_type, degree, dof):
        self.filename = filename
        self.form_type = form_type
        self.mesh_type = mesh_type
        self.degree = degree
        self.dof = dof
        self.n_cores = COMM_WORLD.Get_size()

    
    def __str__(self):
        return (f"{self.filename},{self.n_cores},{self.form_type},"
                f"{self.mesh_type},{self.degree},{self.dof}\n")


def write(filename, row):
    if COMM_WORLD.Get_rank() == 0:
        with open(filename, "a") as f:
            # Add a header if the file is empty.
            if f.tell() == 0:
                f.write("filename,n_cores,form,mesh,degree,dof\n")

            f.write(str(row))