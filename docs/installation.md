# Installing `sunbather`

You can install `sunbather` via `pip`, or compile it from source.

### Option 1: Installation with pip

Simply run the following command:

```bash
pip install sunbather
```

This will automatically check for the dependencies and request to install the missing ones. We recommend installing `sunbather` in a [virtual environment](https://realpython.com/python-virtual-environments-a-primer/).

### Option 2: compilation from source

Clone `sunbather` from Github using the following command:

```bash
git clone https://github.com/antonpannekoek/sunbather.git
```

...

## Post-installation steps

For `sunbather` to work, you need a `Cloudy` installation (`sunbather` currently only works with `Cloudy v23.01` or `Cloudy v17.02`, we recommend the use of the newer 23.01 version), as well as a "project directory" where the models will be saved, and the paths to these need to be set as system environmental variables. Furthermore, a *planets.txt* file that stores the bulk planetary parameters must be present in the project directory. This *planets.txt* file must obey a specific tabular format, and an example file comes with the `sunbather` installation. Finally, to perform simulations with `sunbather`, stellar SEDs are required in a specific tabular format. The `sunbather` installation comes with a set of SEDs from the MUSCLES survey. These and/or any other SED files must be placed inside the */c23.01/data/SED/* folder. 

#### Option 1: If you don't have `Cloudy` yet (or don't mind a second installation):
`sunbather` provides an easy way to install `Cloudy v23.01`. Simply open a Python environment and run the following commands:

```python
import sunbather
sunbather.firstrun()
```

This will install `Cloudy` into the `sunbather` root directory. It will automatically set the path variable for you. It will also prompt you to enter a project directory. It then copies the template *planets.txt* file supplied by `sunbather` into your project directory. It then also copies the SED files into the `Cloudy` directory.

#### Option 2: If you already have a `Cloudy` installation:
The path to the `Cloudy` installation must be set as the `$CLOUDY_PATH` environmental variable, and if you are using version 17.02 instead of 23.01, you should also set the `$CLOUDY_VERSION` environmental variable to `"17.02"`. Your project directory must be stored in the `$SUNBATHER_PROJECT_PATH` environmental variable. The easiest solution is to add these variables to your `~/.bashrc` or `~/.zsh` file:

```bash
export CLOUDY_PATH="/full/path/to/c23.01/"
export SUNBATHER_PROJECT_PATH="/full/path/to/project_folder/"
```

Then, copy the */sunbather/src/sunbather/data/workingdir/planets.txt* file into your project directory. Also, if you want to make use of the MUSCLES stellar SEDs, copy the contents of the *sunbather/src/sunbather/data/stellar_SEDs/* folder into the */c23.01/data/SED/* folder.

#### Option 3: If you don't have `Cloudy` yet but prefer to manually install it:
Complete `Cloudy` download and installation instructions can be found [here](https://gitlab.nublado.org/cloudy/cloudy/-/wikis/home). In short, for most Unix systems, the steps are as follows:

1. Go to the [v23 download page](https://data.nublado.org/cloudy_releases/c23/) and download the "c23.01.tar.gz" file (or go to the [v17 download page](https://data.nublado.org/cloudy_releases/c17/old/) and  download the "c17.02.tar.gz" file).
2. Extract it in a location where you want to install _Cloudy_.
3. `cd` into the _/c23.01/source/_ or _/c17.02/source/_ folder and compile the code by running `make`.
4. Quickly test the _Cloudy_ installation: in the source folder, run `./cloudy.exe`, type "test" and hit return twice. It should print "Cloudy exited OK" at the end.

If you have trouble installing _Cloudy_, we refer to the download instructions linked above, as well as the _Cloudy_ [help forum](https://cloudyastrophysics.groups.io/g/Main/topics).

After installation, follow the steps above under Option 2. 

## Testing your `sunbather` installation

...



## Getting started with `sunbather`

1. To get familiar with `sunbather`, we recommend you go through the Jupyter notebooks in the */sunbather/examples/* folder, where example use cases (such as creating atmospheric profiles, calculating transmission spectra and fitting observational data) are worked out and explained. 
2. For more details on how to use the code, check out the Glossary and FAQ pages. We specifically recommend you read the glossary sections "The _planets.txt_ file" and "Stellar SED handling". 