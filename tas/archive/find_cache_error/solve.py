from firedrake import *  # noqa: F403
from mpi4py import MPI
import math,sys,time
import numpy as np
seed = int(sys.argv[1])
#========;
#  Mesh  ;
#========;

rank = MPI.COMM_WORLD.Get_rank()
size = MPI.COMM_WORLD.Get_size()
if rank == 0:
  print("Discretization: CG1 on %d MPI processes" % (size))
mesh = UnitSquareMesh(seed,seed)
Q = FunctionSpace(mesh,'CG',1)
Q2 = FunctionSpace(mesh,'CG',4)
D0 = FunctionSpace(mesh,'DG',0)
u = TrialFunction(Q)
v = TestFunction(Q)
u_h = Function(Q)
u_bc = Function(Q)
with u_h.dat.vec as u_h_vec:
  dof = u_h_vec.getSize()
if rank == 0:
  print("\tDegrees-of-freedom: %d" % dof)

#==================;
#  Exact solution  ;
#==================;
x = SpatialCoordinate(Q.mesh())
f = interpolate(8*math.pi*math.pi*sin(2*x[0]*math.pi)*sin(2*x[1]*math.pi),Q)
u_bc = interpolate(sin(2*x[0]*math.pi)*sin(2*x[1]*math.pi),Q)
u_exact = interpolate(sin(2*x[0]*math.pi)*sin(2*x[1]*math.pi),Q2)

#=======================;
#  Boundary conditions  ;
#=======================;
bcs = DirichletBC(Q,Constant(0.0),(1,2,3,4))

#=============;
#  Weak form  ;
#=============;
a = inner(grad(u),grad(v))*dx
L = f*v*dx

#=====================;
#  Solver parameters  ;
#=====================;
solver_params = {
  'ksp_type': 'cg',
  'pc_type': 'hypre',
  'ksp_converged_reason': None,
  'ksp_rtol': '1e-7'
}

#=================;
#  Solve problem  ;
#=================;
for _ in range(1000):
  initialTime = time.time()
  solve(a == L, u_h, bcs, solver_parameters=solver_params)
  TotalTime = time.time() - initialTime

#================;
#  Compute info  ;
#================;
L2_error = errornorm(u_exact,u_h,'L2')
dofsec = dof/TotalTime
doa = np.multiply(np.log10(L2_error),-1.0)
doasec = doa/TotalTime
if rank == 0:
  print("\tWall-clock time:  %1.3e seconds" % TotalTime)
  print("\tL2 error norm: %1.3e" % L2_error)
  print("\tDigits of accuracy:  %1.3e" % doa)
  print("\tDoA/s:  %1.3e" % doasec)
  print("\tDoF/s:  %1.3e" % dofsec)

#outfile = File("poisson.pvd")
#outfile.write(u_bc,u_h)
