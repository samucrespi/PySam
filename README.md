
# PySam.py
### By S. Crespi, Sep 2021
#### Version 1.0

The following is a collection of useful functions.
To use them, simply copy this file where needed and add this line to your code:

```
from PySam import *
```

or 

```
import PySam as PS
```

**WARNING**: 
At this stage, it is necessary to copy and paste this file to the specific folder where is needed. This method (that will be changed in future updates) is extremely version-sensitive. Please, always check if you are using the most updated version.

------

**Version note**:
 - *v1.0*: first functions added

------
------

## List of all the Functions Available

**resize_scatterplot<i>(s, s1=10, s2=100, log=False, extrema=[])</i>**
 - Rescale the size of a scatter plot points
 
**get_colours_for_plot<i>(Ncolors, cmap='gist_rainbow')</i>**
 - Generate a discrete color palette for plots

**get_xfit<i>(x, log=False, d=0.05, N=1000)</i>**
 - Generate an array that samples the x-coordinate

**binning<i>(filein, fileout, dt, t0=None, plot=False)</i>**

------
## License

Copyright 2021-2022 Samuele Crespi and contributors.
