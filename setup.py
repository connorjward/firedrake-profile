from distutils.core import setup
from glob import glob


setup(name="fireperf",
      version="0.0.1",
      description="Tools for profiling Firedrake performance",
      author="Connor Ward",
      author_email="c.ward20@imperial.ac.uk",
      packages=["fireperf"],
      scripts=glob("scripts/*"))
