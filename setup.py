from setuptools import setup


setup(name="fireperf",
      version="0.0.1",
      description="Tools for profiling Firedrake performance",
      author="Connor Ward",
      author_email="c.ward20@imperial.ac.uk",
      packages=["fireperf"],
      install_requires=["pandas"],
      entry_points={
            "console_scripts": [
                  "assemble-form = fireperf.scripts:assemble_form",
                  "plot-runtime = fireperf.scripts:plot_runtime",
                  "plot-throughput = fireperf.scripts:plot_throughput",
            ]
      })
