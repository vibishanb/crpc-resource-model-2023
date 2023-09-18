
[![DOI](https://zenodo.org/badge/692395824.svg)](https://zenodo.org/badge/latestdoi/692395824)

## How to run
- You'll need all the packages listed in [requirements.txt](./requirements.txt).
	- If you use anaconda all the packages are installed by default
	- If you use vanilla python, do ``` pip install -r requirements.txt```

- If you plan to modify some parameters, keep the following in mind and change accordingly
	- EnvEq.py:
	 	- contains all the code for differential equations, solver call, non negative check, therapy functions, etc
		- fixed code, do not modify unless necessary
	- input.py
		- contains the fixed parameters used by the simulation
		- change parameters and output file paths here
		- some parameters might be changed in parallelizer.py
	- parallelizer.py
		- contains the code for parsing input.py file, parallelization and the parameter ranges to (parallel) loop over
		- might need to know some basic python to understand and modify parameters here
	- somefile.csv
		- these files are present for some simualtion runs
		- parallelizer.py loops over each row as input
		- rows can be added without any other changes but adding columns would require modifying parallelizer.py to be useful
- In order to run some the simulation in some pre-determined parameter space:
	- Ensure EnvEq.py, input.py and parallelizer.py are in the same directory.
	- Change parameter values as required in input.py
	- If needed, parameters over which simualations must be parallelized can be saved in a .csv file and passed through parallelizer.py.

See latest release notes for further details of repo contents. 
