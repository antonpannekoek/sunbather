# FAQ

## How do I create Parker wind profiles?

Add the parameters of the planet/star system to the *$SUNBATHER_PROJECT_PATH/planets.txt* file. Make sure the SED you specify in _planets.txt_ is present in the _$CLOUDY_PATH/data/SED/_ folder in the right format (see Glossary). Then, to calculate the isothermal Parker profile, use the `run()` function of the `construct_parker` module. To calculate the nonisothermal temperature profile, use the `run()` function of the `convergeT_parker` module. See the Glossary for explicit examples. 

## How do I choose the composition of the atmosphere?

The composition usually has to be specified at two stages:  

1. When creating the (isothermal) Parker wind profiles with the `construct_parker` module: You can choose to use a pure H/He composition (which uses `p-winds` standalone) by specifying the hydrogen fraction by number with the `fraction_hydrogen` argument. You can also choose an arbitrary composition that includes metal species (which uses `p-winds` and `Cloudy` in tandem) with the `z` and `zelem` arguments. In this case, `z` specifies a metallicity relative to solar and is thus a scaling factor for all metal species. `zelem` can be used to scale the abundance of individual elements. It takes a dictionary format, for example `zelem={"Na":3, "Mg+":10, "Fe+2":0.5, "K":0}`. Note that `z` and `zelem` can be used together and are **multiplicative**. In the `construct_parker` module, the composition only affects the wind structure through the mean molecular weight. Therefore, using `z` and `zelem` is only needed for (highly) supersolar metallicities; using `fraction_hydrogen=0.9` will usually suffice for a solar composition atmosphere.

2. When simulating Parker wind profiles with `Cloudy` to calculate the nonisothermal temperature profile (and population levels) with the `convergeT_parker` module: You can specify the composition with the `z` and `zelem` arguments as explained under point 1. The default is a solar composition, so `z=1`. If you want to simulate a pure H/He composition with `Cloudy`, you can pass `z=0` (and specify the He abundance through `zelem={"He":0.1}`. Contrary to point 1 however, in `convergeT_parker`, the metal content directly affects the thermal structure and XUV absorption, so we recommend using `z=1` even when you only make hydrogen and helium spectra.

## How do I calculate the transmission spectrum?

Create the Parker wind profile with `construct_parker.run()` and simulate it with `Cloudy` with `convergeT_parker.run()`. Then, load the `Cloudy` output in your Python script with the `tools.Sim` class (see FAQ below), and use the `RT.FinFout()` function to make the transit spectrum. At minimum, `RT.FinFout()` expects the `Sim` object, a wavelength array, and a list of species for which to calculate the spectrum. See the _sunbather/examples/fit_helium.ipynb_ notebook for an example.

## How do I simulate one planet with different stellar SEDs?

The safest way is to add another entry in the *$SUNBATHER_PROJECT_PATH/planets.txt* file, with the same parameter values, but a different planet "name" and "SEDname" (the "full name" can be the same). 

Alternatively and more prone to mistakes, the `construct_parker.run()` and `convergeT_parker.run()` functions also take the `sed_name` argument which allows you to specify a different name of the SED file without making a new entry in the _planets.txt_ file. In this case, it is **strongly advised** to use a different `pdir` and `workingdir` (in which you indicate the SED type) as well. 

## Why do I have to specify a `pdir` and a `workingdir`?

Generally, for one planet you may want to create Parker wind profiles with different temperatures, mass-loss rates, but also different atmospheric compositions. The `pdir` and `workingdir` arguments correspond to actual folders on your machine. Each folder groups together profiles with different $T$ and $\dot{M}$, so the `pdir` and `workingdir` effectively allow you to separate the profiles by composition. `pdir` corresponds to the folder where the Parker wind **structure** from the `construct_parker` module (i.e. density and velocity as a function of radius) is stored: *$SUNBATHER_PROJECT_PATH/parker_profiles/planetname/pdir/*, and `workingdir` corresponds to the folder where the `Cloudy` simulations from the `convergeT_parker` module are stored: *$SUNBATHER_PROJECT_PATH/sims/1D/planetname/dir/*.

For example, you can make one `pdir` which stores a grid of T/mdot profiles at a H/He ratio of 90/10, and another which stores a grid of profiles at a ratio of 99/01. The reason that the  `workingdir` argument is not the exact same as the `pdir` argument, is that you may want to create your Parker wind structure profile only once (in one `pdir` folder) but then run it multiple times with `Cloudy` while changing the abundance of one particular trace element (in multiple `workingdir` folders). The latter would usually not really change the atmospheric structure, but could produce a very different spectral feature.

## How do I read / plot the output of `Cloudy` in Python?

The `Sim` class in the `tools` module can be used to read in simulations by giving the full path to the simulation. `Cloudy` output is separated into different output files, which all have the same name but a different extension. The bulk structure of the atmosphere (including temperature and density) is stored in the ".ovr" file. The radiative heating and cooling rates as a function of radius are stored in the ".heat" and ".cool" files. The densities of different energy levels of different atomic/ionic species are stored in the ".den" file. These files are all read in as a Pandas dataframe and can be accessed as follows:

``` python
from sunbather import tools

mysimulation = tools.Sim(tools.get_sunbather_project_path()+"/sims/1D/planetname/dir/parker_T_Mdot/converged")

#to get the planet parameters of this simulation:
mysimulation.p.R #radius
mysimulation.p.Mstar #mass of host star

#to get Cloudy output
mysimulation.ovr.alt #radius grid of the following profiles:
mysimulation.ovr.rho #density profile
mysimulation.ovr.Te #temperature profile
mysimulation.ovr.v #velocity profile
mysimulation.cool.ctot #total radiative cooling
mysimulation.den['H[1]'] #density of ground-state atomic hydrogen
mysimulation.den['He[2]'] #density of the second (=metastable) level of helium
mysimulation.den['Fe+2[10]'] #density of the tenth energy level of Fe 2+
```

## Can I run a Parker wind profile through `Cloudy` while using the isothermal temperature profile?

Yes, you can pass `constant_temp=True` to `convergeT_parker.run()` to simulate the Parker wind profile without converging on a nonisothermal temperature structure. This will save a `Cloudy` simulation called "constantT" and the folder structure works the same way as for converged simulations: you again need to pass a `workingdir` where the simulation is saved, and you can in principle use the same directory that you use for converged profiles (but you will need to pass the `overwrite=True` flag if the converged nonisothermal simulation already exists - nothing will be overwritten in this case though!).

## I forgot to specify some species for which I want Cloudy output with the `save_sp` argument. Do I need to run `convergeT_parker.run()` again from scratch?

You can use the `tools.insertden_Cloudy_in()` function to add species to a (converged) `Cloudy` simulation file and run it again, without having to go through the temperature convergence scheme again. If you want to do this for a grid of Parker wind models, you will have to set up a loop over the correct filepaths yourself.

## Can I run an atmospheric profile other than an (isothermal) Parker wind?

You can "trick" the code into running an arbitrary outflow profile by saving your density and velocity profile in the expected file format in the *$SUNBATHER_PROJECT_PATH/parker_profiles/* folder. For example, you can create a simple density and velocity profile in Python:

``` python
from sunbather import tools
import numpy as np

p = tools.Planet('generic_planet') #make sure you add the parameters in planets.txt

r = np.linspace(1, 10, num=1000) * p.R #in cm
rho = 1e-15 / np.linspace(1, 10, num=1000)**3 #falls with r^3
v = 5e4 * np.linspace(1, 10, num=1000) #starts at 0.5km/s, increases linearly with r so that Mdot = 4 pi rho v r^2 is constant
mu = np.repeat(np.nan, 1000) #mu is not used by convergeT_parker.py

print("log(Mdot) =", np.log10(4*np.pi*r[0]**2*rho[0]*v[0]))

np.savetxt(tools.projectpath+'/parker_profiles/'+p.name+'/geometric/pprof_'+p.name+'_T=0_M=0.000.txt', np.column_stack((r, rho, v, mu)), delimiter='\t')
```

You can then solve the temperature structure of this profile as: 

```python
from sunbather import convergeT_parker

convergeT_parker.run("generic_planet", mdot=0, temp=0, pdir="geometric", workingdir="geometric")
```

Similarly, you could for example postprocess the density and velocity profile of an `ATES` simulation (Caldiroli et al. 2021) with `sunbather` to produce a transmission spectrum.

## How do I stop the simulation at the Roche radius / choose the maximum radius?

The `construct_parker` module always creates a profile up until 20 Rp and this can only be changed by editing the source code. 

The `convergeT_parker` module by default simulates the atmosphere with `Cloudy` up until 8 Rp and this can be changed with the `altmax` argument. 

The `RT.FinFout()` function by default makes a transit spectrum based on the full `Cloudy` simulation (so by default up until 8 Rp), but you can give an upper boundary in cm with the `cut_at` argument. For example, if you want to include only material up until the planet's Roche radius when making the transit spectrum, it generally doesn't hurt to leave `construct_parker` and `convergeT_parker` at the default values (unless the Roche radius is larger than 8 Rp, then make sure to pass a larger `altmax` to `convergeT_parker`), and just pass `cut_at=mysimulation.p.Rroche` to `RT.FinFout()`, where `mysimulation` is the `tools.Sim` object of your `Cloudy` simulation.
