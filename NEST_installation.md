## NEST Installation (Python 2/3)
**Instruction for Ubuntu (+PyCharm)**

#### 1. Get standard configuration (with NumPy, SciPy, Matplotlib, iPython and GNU Scientific Library)
```bash
sudo apt-get install build-essential autoconf automake libtool libltdl7-dev libreadline6-dev libncurses5-dev libgsl0-dev python-all-dev python-numpy python-scipy python-matplotlib ipython gsl-bin libgsl0-dev libgsl0-dbg
```
or you can install them from websites 
[SciPy](http://www.scipy.org/install.html),
[Matplotlib](http://matplotlib.sourceforge.net),
[iPython](https://pypi.python.org/pypi/ipython#downloads),
[GSL](http://www.gnu.org/software/gsl/).

#### 2. NEST-2.12.0| [Download](http://www.nest-simulator.org/download/)
```bash
tar -xzvf nest-x.y.z.tar.gz                         #Unpack the tarball
mkdir nest-x.y.z-build                              #Create a build directory
cd nest-x.y.z-build                                 #Change to the build directory
../nest-x.y.z/configure --prefix=$HOME/opt/nest     #Configure NEST
```
You will see NEST Configuration Summary, where
```bash
C compiler          : gcc  
C compiler flags    : -W -Wall -pedantic -Wno-long-long -O2 -g -O2 -fopenmp  
C++ compiler        : g++  
C++ compiler flags  : -W -Wall -pedantic -Wno-long-long -O2 -fopenmp  
Python bindings     : Yes (Python 2.7: /usr/bin/python)
Use threading       : Yes (OpenMP)  
Use GSL             : Yes  
. . . . . .
```
Pay attention for **Python bindings**! It must be *YES* and include your Python version.

Continue installation:
```bash
make                # Compile by running
make install        # Install by running
make installcheck   # Check installation
```
If the test completed without any errors, go to the next steps, else try to fix them.

#### 3. PYTHONPATH
```bash
sudo gedit ~/.bashrc
```
Add all lines from ```<nest folder>/bin/nest_vars.sh``` to  ```.bashrc ``` and save.

After this run
```bash
source ~/.bashrc
```

then run python interpreter. Enter "import nest". If you see this message, installation completed, else try fix errors.

```bash
              -- N E S T --

  Copyright (C) 2004 The NEST Initiative
  Version 2.12.0 Jul 13 2017 12:43:12
```

#### 4. If you use PyCharm
> Settings -> Project:"title" -> ProjectStructure -> Add Content root -> choose "site-packages" from NEST folder. Mark as "Sources".
