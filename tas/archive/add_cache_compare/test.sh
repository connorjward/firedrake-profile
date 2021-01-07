# Run without cache
git -C ~/projects/improve-firedrake-scaling/firedrake/src/PyOP2 checkout test-without-kernel-cache
python solve_petsc.py 16 | tee without-kernel-cache.txt

# Run with cache
git -C ~/projects/improve-firedrake-scaling/firedrake/src/PyOP2 checkout test-with-kernel-cache
python solve_petsc.py 16 | tee with-kernel-cache.txt