import subprocess


N_PROCESSORS = 2


cmd = ["mpirun", "-np", str(N_PROCESSORS),  
       "--bind-to", "hwthread", 
       "--map-by", "hwthread", 
       "python", "assemble.py"]

subprocess.run(cmd, stdout=True, check=True)