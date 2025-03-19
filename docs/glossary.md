# Glossary
This page is a glossary that provides additional information on various modules/classes/functionalities included in `sunbather`. We also refer to "Hazy", which is the official documentation of `Cloudy` and can be found in your *$CLOUDY_PATH/docs/* folder. 

## The `sunbather` modules:

### The `tools` module
This module contains many basic functions and classes that are used by the other `sunbather` modules, and can also be used when postprocessing/analyzing `sunbather` output. Specifically, the `Sim` class is the main way to work with `Cloudy`'s output and plot the atmospheric structure, perform radiative transfer calculations, and more. You can create a `Sim` object by passing the full path to the `Cloudy` output files (e.g., see the `RT` module section below).


### The `construct_parker` module
This module is used to create Parker wind profiles. The module can make pure H/He profiles, in which case it is basically a wrapper around the [`p-winds` code](https://github.com/ladsantos/p-winds) (dos Santos et al. 2022). The code can however also make Parker wind profiles for an arbitrary composition (e.g. at a given scaled solar metallicity), which is much more computationally expensive, because it then iteratively runs `p-winds` and `Cloudy`. In this mode, `Cloudy` is used to obtain the mean molecular weight structure of the atmosphere for the given composition, which `p-winds` uses to calculate the density and velocity structure. 

The main function to use in the module is the `run()` function, which takes a single value or list of mass-loss rates and temperatures, and calculates a single/grid of isothermal Parker wind models.

Example use: 

```python
from sunbather import construct_parker
import numpy as np

mdots = np.arange(10, 12, 0.1) #log10 of the mass-loss rate
temps = np.arange(6000, 10000, 200)

construct_parker.run("HD209458b", pdir="10x_solar", mdot=mdots, temp=temps, z=10, cores=8)
```

This creates a grid of isothermal Parker wind profiles for the planet HD209458b (must be defined in *planets.txt*) with a 10x solar metallicity composition. The atmospheric structures are saved as .txt files in *$SUNBATHER_PROJECT_PATH/parker_profiles/HD209458b/10x_solar/*. 8 models are calculated in parallel (speeds up computation time if your machine has multiple CPU cores available).


### The `convergeT_parker` module
This module is used to run Parker wind profiles through `Cloudy` to (iteratively) solve for a non-isothermal temperature structure. Additionally, the "converged" simulation can then be postprocessed with the `RT` module in order to make transmission spectra. This module is basically a convenience wrapper which sets up the necessary folder structure and input arguments for the `solveT` module that actually performs the iterative scheme described in Linssen et al. (2022; 2024).

The main function to use in the module is the `run()` function, which takes a single value or list of mass-loss rates and temperatures, and calculates a single/grid of Parker wind models.

Example use:

```python
from sunbather import convergeT_parker
import numpy as np

mdots = np.arange(10, 12, 0.1) #log10 of the mass-loss rate
temps = np.arange(6000, 10000, 200)

convergeT_parker.run("HD209458b", pdir="10x_solar", workingdir="10x_solar", mdot=mdots, temp=temps, z=10, cores=8)
```

This simulates a grid of Parker wind models for the planet HD209458b (must be defined in *planets.txt*) with a 10x solar metallicity composition. All of the isothermal Parker wind profiles (i.e., the atmospheric density and velocity profiles) must have been calculated with the `sunbather.construct_parker` module before. This function saves the simulation as `Cloudy` output files in the */$SUNBATHER_PROJECT_PATH/sims/1D/HD209458b/10x_solar/parker_T_Mdot/* folders. These can then be read into Python using `sunbather`'s `tools.Sim` class.


### The `solveT` module
This module contains the iterative scheme described in Linssen et al. (2022; 2024) to solve for a nonisothermal temperature structure of a given atmospheric profile. It is called by `sunbather.convergeT_parker`. As long as you're simulating Parker wind profiles (and not some other custom profile), you do not need to access this module.


### The `RT` module
This module contains functions to perform radiative transfer calculations of the planet transmission spectrum.

The main function that you can use from this module is the `FinFout()` function, which calculates the transmission spectrum, given a `Sim` object, a wavelength array, and a list of atomic species to include in the calculations.

Example use:

```python
from sunbather import tools, RT
import numpy as np
import matplotlib.pyplot as plt

simulation = tools.Sim(tools.get_sunbather_project_path()+"/sims/1D/HD209458b/solar/parker_8000_11.000/converged")
wavs = np.linspace(10830, 10836, 1000)
trans_spec, _, _ = RT.FinFout(simulation, wavs, "He")

plt.plot(wavs, trans_spec)
```


## The *\$SUNBATHER_PROJECT_PATH*
This is the directory on your machine where all Parker wind profiles and `Cloudy` simulations are saved. You can choose any location and name you like, as long as it doesn't contain any spaces. The full path to this directory must be set as your `$SUNBATHER_PROJECT_PATH` environmental variable (see installation instructions). The reason `sunbather` uses a project path is to keep all output from simulations (i.e. user-specific files) separate from the source code. Internally and in Python, the path is returned by the `tools.get_sunbather_project_path()` function.


## The _planets.txt_ file
This file stores the bulk parameters of the planets that are simulated. A template of this file is provided in the */sunbather/src/sunbather/data/workingdir/* directory, but you must copy it to your *$SUNBATHER_PROJECT_PATH* in order for it to work (or execute the `sunbather.firstrun()` function that copies it for you). Every time you want to simulate a new planet/star system, you must add a line to this file with its parameters. You can add comments at the end of the line with a # (for example referencing where the values are from). The first column specifies the "name", which is a tag for this system that cannot contain spaces and is used for the `plname` argument of the `construct_parker.run()` and `convergeT_parker.run()` functions, as well as for the `tools.Planet` class to access the system parameters in Python. The second column specifies the "full name", which can be any string you like and can be used e.g. when plotting results. The third column is the radius of the planet in Jupiter radii (7.1492e9 cm). The fourth column is the radius of the star in solar radii (6.9634e10 cm). The fifth column is the semi-major axis of the system in AU (1.49597871e13 cm). The sixth column is the mass of the planet in Jupiter masses (1.898e30 g). The seventh column is the mass of the star in solar masses (1.9891e33 g). The eighth column is the transit impact parameter (dimensionless, 0 is across the center of the stellar disk, 1 is grazing the stellar limb). The ninth column is the name of the stellar SED - see "Stellar SED handling" below in this glossary.


## Stellar SED handling
When running `sunbather`, the spectral energy distribution (SED) of the host star has to be available to `Cloudy`, which looks for it in its *$CLOUDY_PATH/data/SED/* folder. Therefore, every SED you want to use has be **copied to that folder, and requires a specific format**: the first column must be wavelengths in units of Å and the second column must be the lambda*F_lambda flux **at a distance of 1 AU** in units of erg s-1 cm-2. Additionally, on the first line, after the first flux value, the following keywords must appear: "units angstrom nuFnu". In the */sunbather/stellar_SEDs/* folder, we have provided the MUSCLES SEDs in the correct format. Even though `Cloudy` in principle supports other units, `sunbather` doesn't, so please stick to the units as described. Normalization of the flux to the planet orbital distance is done automatically by *sunbather* based on the semi-major axis value given in the *planets.txt* file.
