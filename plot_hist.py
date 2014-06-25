#!/usr/bin/env python
desc="""Plot histogram
"""
epilog="""Author:
l.p.pryszcz@gmail.com

Barcelona, 29/11/2012
"""

import argparse, os, sys
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

def histplot(ax, x, handle, categories, title, xlab, ylab, log):
    """
    """
    #fig = plt.figure()
    #ax = fig.add_subplot(111)
    if log:
    	ax.set_yscale('log')
    # the histogram of the data
    n, bins, patches = ax.hist(x, categories, normed=0, facecolor='green', alpha=0.75)

    # hist uses np.histogram under the hood to create 'n' and 'bins'.
    # np.histogram returns the bin edges, so there will be 50 probability
    # density values in n, 51 bin edges in bins and 50 patches.  To get
    # everything lined up, we'll compute the bin centers
    #bincenters = 0.5*(bins[1:]+bins[:-1])
    # add a 'best fit' line for the normal PDF
    #y = mlab.normpdf( bincenters, mu, sigma)
    #l = ax.plot(bincenters, y, 'r--', linewidth=1)
    #title+'\nmean=%.2f; stdev=%.2f' % (np.mean(x),np.std(x)), \
    ax.set_title(title)
    #ax.set_title('mean=%.2f,stdev=%.2f' % (np.mean(x),np.std(x)))
    #ax.set_xlim(40, 160)
    #ax.set_ylim(0, 0.03)
    #plt.text(60, .025, r'mean=%.2f,stdev=%.2f' % (np.mean(x),np.std(x)))
    ax.grid(True)
 
def plot_hist(handle, out, cols, names, bins, title, xlab, ylab, log, vmax, vmin, \
              verbose, dlimit=1):
    """
    """
    if verbose:
        sys.stderr.write( "Parsing data...\n" )
    x = [[] for i in range(len(cols))]
    for l in handle:
        try:
            ldata = l[:-1].split('\t')
            for i, col in enumerate(cols):
                if col>=len(ldata) or not ldata[col]:
                    continue
                v=float(ldata[col])
                if vmin<v<vmax:
                    x[i].append(v)
        except:
            sys.stderr.write("[Error] Cannot parse line: %s\n" % ",".join(l.split('\t')))
    if verbose:
        sys.stderr.write( " %s values loaded.\n" % len(x) )
    #define number of rows and columns
    ncol = nrow = int(np.sqrt(len(cols)))
    if ncol*nrow < len(cols):
        ncol += 1
    if ncol*nrow < len(cols):
        nrow += 1
    if verbose:
        sys.stderr.write(" %s columns x %s rows\n"%(ncol, nrow))
    #start figure
    fig = plt.figure()
    #http://matplotlib.org/users/customizing.html
    #mpl.rcParams['figure.subplot.wspace'] = 0.3
    mpl.rcParams['figure.subplot.hspace'] = 0.5
    mpl.rcParams['axes.titlesize'] = 8
    mpl.rcParams['axes.labelsize'] = 6
    mpl.rcParams['xtick.labelsize'] = 5
    mpl.rcParams['ytick.labelsize'] = 5
    #add subplots
    for i, data in enumerate(x):
        ax = fig.add_subplot(nrow, ncol, i+1)
        if len(cols)==1 and title:
            ax.set_title(title)
        name = ""
        if names:
            name = names[i]
        if len(data)<dlimit:
            sys.stderr.write("[WARNING] Only %s data points for: %s\n"%(len(data), name))
            continue
        histplot(ax, data, handle, bins, name, xlab, ylab, log)

        if i+1>len(cols)-nrow:
            ax.set_xlabel(xlab)
        if not i%nrow:
            ax.set_ylabel(ylab)

    if type(out) is file and out.name=='<stdout>':
    	plt.show()
    else:
        fpath = out #handle.name+".png"
        fformat = fpath.split('.')[-1] 
        plt.savefig(fpath, dpi=300, format=fformat, orientation='landscape', transparent=False)
        sys.stderr.write("Figure written to: %s\n" % fpath)
    
    
def main():
    
    usage   = "%(prog)s [options] -v" 
    parser  = argparse.ArgumentParser( usage=usage,description=desc,epilog=epilog )
  
    parser.add_argument("-v", "--verbose", default=False, action="store_true", help="verbose")    
    parser.add_argument('--version', action='version', version='1.0')
    parser.add_argument("-i", "--input",   default=sys.stdin, type=file,
                        help="input           [stdin]")
    parser.add_argument("-o", "--output",  default=sys.stdout, 
                        help="input           [stdout]")
    parser.add_argument("-b", "--bins",    default=100, type=int,
                        help="number of bins  [%(default)s]")
    parser.add_argument("-c", "--col",     default=[0], nargs="+", type=int,
                        help="columns to use  [%(default)s]")
    parser.add_argument("-n", "--names",   default="", nargs="+", 
                        help="column names    [%(default)s]")
    parser.add_argument("-t", "--title",   default="Histogram", 
                        help="histogram title [%(default)s]")
    parser.add_argument("-x", "--xlab",    default="", 
                        help="x-axis label    [%(default)s]")
    parser.add_argument("-y", "--ylab",    default="", 
                        help="y-axis label    [%(default)s]")
    parser.add_argument("--log",           default=False, action="store_true",
                        help="log scale       [%(default)s]")
    parser.add_argument("--max",           default=float('inf'), type=float,
                        help="max value       [%(default)s]")
    parser.add_argument("--min",           default=float('-inf'), type=float,
                        help="min value       [%(default)s]")

    o = parser.parse_args()
    if o.verbose:
        sys.stderr.write( "Options: %s\n" % str(o) )

    plot_hist(o.input, o.output, o.col, o.names, o.bins, o.title, o.xlab, o.ylab, o.log, \
              o.max, o.min, o.verbose)
              
if __name__=='__main__': 
    t0  = datetime.now()
    main()
    dt  = datetime.now()-t0
    sys.stderr.write( "#Time elapsed: %s\n" % dt )