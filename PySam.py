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


#######################################################################


'''
NAME:
    binning (v1.1)
    
PURPOSE: 
    To bin a set of data with errors. Each bin will contain the
    weighted average of the data inside the bin.

CALLING SEQUENCE: 
    binning(filein, fileout, dt, t0=None, plot=False)

PARAMETERS: 
    filein  file, str
            File ot name of the file containing the data in a
            3-columns format (x-coordinate, y-coordinate, y-errors).
    fileout file, str
            File or name of the file where the binned data will be
            stored.
    dt      float
            Required width of the bin (x-coordinate).
    t0      float, optional
            Left boundary of the first bin. The default, None, uses
            the first time in the dataset as t0.
    plot    bool, optional
            If True, a plot with data and binned data is displayed.
            Default is False.

RETURN:

OUTPUT:
    fileout file containing the binned data

NOTES:

VERSIONS HISTORY:
    v1.0: first release
          (S.Crespi-Jul2018)
    v1.1: added "type error" for dt and t0 
          data are automatically sorted along the 0th column
          wrong standard error of the weighted mean -> fixed
          added possibility of plotting
          minor improvements
          (S.Crespi-Oct2022)
    

'''


def binning(filein,fileout,dt,t0=None,plot=False):

    from numpy import arange,power,loadtxt,asarray
    
    # Load data
    data = loadtxt(filein, float)
    data = data[data[:, 0].argsort()]
    t, f, ferr = data[:,0], data[:,1], data[:,2]

    # Type Errors
    if t0==None: t0 = t[0]*1
    elif type(t0)!=float and type(t0)!=int:
        print("\n\n Type Error: t0 must be a number\n\n")
        quit()
    if type(dt)!=float and type(dt)!=int:
        print("\n\n Type Error: t0 must be a number\n\n")
        quit()
    
    # Bin and write out the file
    Ts = arange(t0+dt/2.,t[-1]+dt/2.,dt)
    k = 0
    Nt = len(t)
    file = open(fileout,'w+')
    for T in Ts:
        tobin = []
        for j in range(k,Nt):
            if t[j] >= T+dt/2.:
                k = j*1
                break
            tobin.append([f[j],ferr[j]])
        if tobin==[]: continue
        tobin = asarray(tobin)

        w2 = power(tobin[:,1],-2.)
        y = sum(tobin[:,0]*w2)/sum(w2)
        yerr = power(sum(w2),-0.5)
        
        file.write("{} {} {}\n".format(T,y,yerr))
    file.close()

    if plot:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1,figsize=(12,8))
        ax.errorbar(t,f,yerr=ferr,color='k',marker='.',alpha=0.5,zorder=0,ls='none')
        binned = loadtxt(fileout)
        ax.errorbar(binned[:,0],binned[:,1],yerr=binned[:,2],color='r',marker='.',alpha=1,zorder=1,ls='none')
        plt.tight_layout()
        plt.show()
    
    return