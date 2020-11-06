"""
Module containing the Problem class.
"""

from firedrake import *

import forms


class Problem:
    """Class representing the variational problem."""

    def __init__(self, mesh_type, mesh_size, degree, form_type):
        self.mesh = Problem._init_mesh(mesh_type, mesh_size)
        self.function_space = Problem._init_function_space(self.mesh, degree, form_type)
        self.form = Problem._init_form(form_type, self.mesh, degree)


    @staticmethod
    def _init_mesh(mesh_type, size):
        if mesh_type == "tri":
            return SquareMesh(size, size, 1)
        if mesh_type == "quad":
            return SquareMesh(size, size, 1, quadrilateral=True)
        if mesh_type == "tet":
            return CubeMesh(size, size, size, 1)
        if mesh_type == "hex":
            mesh2d = SquareMesh(size, size, 1, quadrilateral=True)
            return ExtrudedMesh(mesh2d, size)
        raise AssertionError()

    
    @staticmethod
    def _init_function_space(mesh, degree, form_type):
        if form_type in ["mass", "helmholtz"]:
             return FunctionSpace(mesh, "CG", degree)
        if form_type in ["laplacian", "elasticity", "hyperelasticity", "holzapfel"]:
            return VectorFunctionSpace(mesh, "CG", degree) 
        raise AssertionError()


    @staticmethod
    def _init_form(form_type, mesh, degree):
        if form_type == "mass":
            return forms.mass(mesh, degree)
        if form_type == "helmholtz":
            return forms.helmholtz(mesh, degree)
        raise AssertionError()
