#----------------------------------------------------------------------
#----------------------------------------------------------------------
#
# PySam.py
# By S. Crespi, Sep 2021
# Version 1.0
#
# The following is a collection of useful functions.
# To use them, simply copy this file where needed and add this line to
#  your code:
#   from PySam import *
#
# WARNING: 
#   At this stage, it is necessary to copy and paste this file to the
#    specific folder where is needed. This method (that sill be changed
#    in future updates) is extremaly version-sensitive. Please, always
#    check if you are using the most updated version.
#    
# Version note:
#  - v1.0: first functions added
#
#----------------------------------------------------------------------
#----------------------------------------------------------------------


#######################################################################


#----------------------------------------------------------------------
# 
#   resize_scatterplot(s,s1=10,s2=100,log=False,extrema=[])
#
# Rescale the size of a scatter plot points
#
# Parameters:  s : array_like
#                  Array to be scaled.
#              s1 : float
#                   Minimum value for the marker size
#              s2 : float
#                   Maximum value for the marker size
#              log : bool
#                    if False (default), the marker size scales as s
#                    if True, the marker size scales as log(s)
#              extrema : 2-elements array, optional
#                        Gives the range of s to rescale
# Returns:  array
#           Scaled markers size
#----------------------------------------------------------------------

def resize_scatterplot(s,s1=10,s2=100,log=False,extrema=[]):

    """
    Rescale the size of a scatter plot points
    """

    import numpy as np
    s = np.asarray(s)
    if extrema==[]: r1,r2 = min(s),max(s)
    else:
        try: r1,r2 = min(extrema),max(extrema)
        except: raise TypeError("extrema must be a list of two values")
    if not log:
        return s1+(s-r1)*(s2-s1)/(r2-r1)
    else:
        return resize_scatterplot(np.log10(s),s1=s1,s2=s2,extrema=[np.log10(r1),np.log10(r2)])


#######################################################################


#----------------------------------------------------------------------
#
#   get_colours_for_plot(Ncolors,cmap='gist_rainbow')
#
# Generate a discrete color palette for plots.
#
# Parameters:  Ncolors : int
#                        Number of colors.
#              cmap : string
#                     Colormap from the library pylab.
# Returns:  array
#           Array of RGBA tuples.
#
# Note:  a warning will be raised unless the following lines are
#         included in the main
#        >>> from matplotlib.axes._axes import _log as matplotlib_axes_logger
#        >>> matplotlib_axes_logger.setLevel('ERROR')
#----------------------------------------------------------------------

def get_colours_for_plot(Ncolors,cmap='gist_rainbow'):

    """
    Generate a discrete color palette for plots
    """

    import pylab
    cm = pylab.get_cmap(cmap)
    col=[cm(1.*i/(Ncolors-1)) for i in range(Ncolors)] # color will now be an RGBA tuple

    from matplotlib.axes._axes import _log as matplotlib_axes_logger
    matplotlib_axes_logger.setLevel('ERROR')
    return col


#######################################################################

#----------------------------------------------------------------------
#
#   get_xfit(x, log=False, d=0.05, N=1000)
#
# Generate an array that samples the x-coordinate
#
# Parameters:  x : array-like
#                  The x-values of the dataset.
#              log : bool, optional
#                    If True, sample the x-coordinate with logarithmic cadence. Default is False.
#              d : float, optional
#                  The fraction of the x-coordinate sampled beyond the range of x. Default is 0.05 (5%).
#              N : int, optional
#                  The lenght of the returned array. Default is 1000.
# Returns:  array
#           Array of x-coordinate.
#
#----------------------------------------------------------------------

def get_xfit(x, log=False, d=0.05, N=1000):

    """
    Generate an array that samples the x-coordinate
    """

    x1,x2 = min(x),max(x)
    if log:
        return get_xfit(np.log10(x), d=d, N=N)
    else:
        return np.linspace(x1-d*(x2-x1),x2+d*(x2-x1),N)