'''
    Created on 2013-03-15
    
    template for paper plots
    
    @author: darp
'''
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Polygon
import pylab
import numpy as np
import numpy.numarray as na
import abc

class PaperPlotTemplate(object):
    '''
        abstract class with default values for plots
    '''
    __metaclass__ = abc.ABCMeta

    def __init__(self, params=dict()):
        self.__params = { #save figure in path
                        'path' : './',
                        'figsize' : (6,6), 
                        'fontsize' : 16,
                        'xlabel' : '',
                        'ylabel' : '',
                        'grid' : True,
                        'grid_linewidth' : 1.0,
                        # axis parameters
                        'xlim' : [0,100],
                        'ylim' : [0,100],
                        'xlog' : False,
                        'ylog' : False,
                        'axisbelow' : True,
                        'ticksize' : 14,
                        # legend parameters
                        'legend_scatterpoints' : 1,
                        'legend_location' : 4 }
        for key, val in params.items():
            self.__params[key] = val

        self.__functions = self._get_plotting_functions()
        self.__ax = None
        
    def __call__(self, filename=''):
        '''
            plot figure and save it optionally
            to a pdf file
        '''
        params = self.__params
        pylab.figure(figsize=params['figsize'])
        self.__ax = pylab.subplot(111)

        functions = self.__functions
        for function in functions:
            function()

        # set legend parameters
        if len(functions) > 1:
            pylab.legend( loc = params['legend_location'],
                        scatterpoints = params['legend_scatterpoints'] )
            pylab.rc('legend', **{'fontsize':params['fontsize']})

        # set labels
        pylab.ylabel( params['ylabel'], fontsize=params['fontsize'] )
        pylab.xlabel( params['xlabel'], fontsize=params['fontsize'] )

        self._set_axis_parameter()

        pylab.grid( params['grid'], linewidth=params['grid_linewidth'] )
        pylab.tight_layout()

        if filename != '' :
            self._save_plot( filename )
        else:
            pylab.show()

    @abc.abstractmethod
    def _get_plotting_functions( self ):
        '''
            this method has to be implemented by all subclasses. the method
            returns a list of functions which add plots to the figure.
        '''
        return

    def _set_axis_parameter( self ):
        # set axis to equal length
        params = self.__params
        ax_0 = self._get_axis()
        # set axis aspect 
        pylab.xlim(params['xlim'])
        pylab.ylim(params['ylim'])
        x0,x1 = ax_0.get_xlim()
        y0,y1 = ax_0.get_ylim()
        if params['xlog'] and params['ylog']:
            delta_x = float(np.log(x1)-np.log(x0))
            delta_y = float(np.log(y1)-np.log(y0))
        else:
            delta_x = float(x1 - x0)
            delta_y = float(y1 - y0)
        ax_0.set_aspect(delta_x/delta_y)
        # set tick size
        ax_0.tick_params(axis='both', labelsize=params['ticksize'])
        # set logarithmic scale
        if params['xlog']:
            pylab.xscale('log')
            if params['grid']:
                ax_0.xaxis.grid( True, which='both' )
        if params['ylog']:
            pylab.yscale('log')
            if params['grid']:
                ax_0.yaxis.grid( True, which='both' )
        # grid below bars and boxes
        ax_0.set_axisbelow(params['axisbelow'])

    def _get_axis( self ):
        return self.__ax

    def _save_plot( self, filename ):
        path = self.__params['path']
        savepath = '{}/{}'.format(path,filename)
        pp = PdfPages( savepath )
        pp.savefig()
        pp.close()

    def _plot_line( self, x, y, label, params=dict() ):
        fparams = { 'color' : 'black',
                    'linestyle' : 'solid',
                    'linewidth' : 2.0 }
        fparams.update( params )

        pylab.plot( x, y, 
                color = fparams['color'],
                linestyle = fparams['linestyle'],
                linewidth = fparams['linewidth'],
                label = label )

    def _plot_scatter( self, x, y, label, params=dict() ):
        fparams = { 'dotsize' : 30,
                    'color' : 'black' }
        fparams.update( params )
        pylab.scatter( x, y, 
                s = fparams['dotsize'],
                color = fparams['color'],
                label = label )

    def _plot_text( self, x, y, text, params=dict() ):
        fparams = { 'fontsize' : self.__params['fontsize'] }
        fparams.update( params )
        pylab.text( x, y, text, fontsize=fparams['fontsize'] )

    def _plot_bars( self, vals, text, xlabels, params=dict() ):
        fparams = { 'bar_width' : 0.5,
                    'facecolor' : '#BBBBBB',
                    'edgecolor' : '#000000' }
        fparams.update( params )

        bar_width = fparams['bar_width']
        xloc = np.array(range(len(vals))) + bar_width
        pylab.xticks( xloc )
        self.__ax.set_xticklabels( xlabels )
        pylab.bar( xloc, vals, 
                yerr=fparams['yerr'],
                width=bar_width, 
                facecolor=fparams['facecolor'],
                ecolor=fparams['edgecolor'],
                label=text,
                align='center')

    def _plot_boxplot( self, data, text, xlabels, params=dict() ):
        fparams = { 'color' : '#000000',
                    'facecolor' : '#FFFFFF',
                    'linewidth' : 2.0,
                    'alpha' : 1.0,
                    'notched_plot' : 0,
                    'show_outliers' : '' }
        fparams.update( params )
        self.__ax.set_xticklabels( xlabels )
        bp = pylab.boxplot( data, 
                            fparams['notched_plot'], 
                            fparams['show_outliers'] )

        # customize boxplot color and linewidth
        boxlines = bp['caps']
        for item in bp.values():
            pylab.setp(item, 
                    color=fparams['color'],
                    linewidth=fparams['linewidth'])

        numBoxes = len(bp['boxes'])
        medians = range(numBoxes)
        for i in range(numBoxes):
            box = bp['boxes'][i]
            boxX = []
            boxY = []
            for j in range(5):
                boxX.append(box.get_xdata()[j])
                boxY.append(box.get_ydata()[j])
            boxCoords = zip(boxX,boxY)

            boxPolygon = Polygon( boxCoords, 
                                facecolor=fparams['facecolor'], 
                                linewidth=fparams['linewidth'], 
                                alpha=fparams['alpha'] )
            self.__ax.add_patch(boxPolygon)
            # Now draw the median lines back over what we just filled in
            med = bp['medians'][i]
            medianX = []
            medianY = []
            for j in range(2):
                medianX.append(med.get_xdata()[j])
                medianY.append(med.get_ydata()[j])
                pylab.plot( medianX, medianY, fparams['color'] )
                medians[i] = medianY[0]

class LinePlotExample(PaperPlotTemplate):

    def __init__( self ):
        params = dict()
        params['xlim'] = [0,5]
        params['ylim'] = [0,20]
        params['xlabel'] = 'Irgend Ne Kagge Uffe X Achse'
        params['ylabel'] = 'Irgend Nen Schmarn Uffe Y Achse'
        PaperPlotTemplate.__init__( self, params )

    def _get_plotting_functions( self ):
        functions = list()
        functions.append( self.__plot_scatter1 )
        functions.append( self.__plot_line1 )
        functions.append( self.__plot_line2 )
        functions.append( self.__plot_text1 )
        return functions

    def __plot_text1( self ):
        x,y = 2.2,10
        text = 'Ein Text'
        self._plot_text( x, y, text )

    def __plot_scatter1( self ):
        x = np.linspace(0,10,100)
        y = x**2 + 3
        m = (y + np.random.randn(1,100)*3)[0]
        params = { 'color' : 'gray' }
        label = 'Irgendwelche Punkte'
        self._plot_scatter( x, m, label, params )

    def __plot_line1( self ):
        x = np.linspace(0,10,100)
        y = x**2 + 3
        self._plot_line( x, y, 'Krasse Line' )

    def __plot_line2( self ):
        x = np.linspace(0,10,100)
        y = x**2 + 10
        params = { 'linestyle' : '--' }
        self._plot_line( x, y, 'Krasse Line 2', params )


class BarPlotExample(PaperPlotTemplate):

    def __init__( self ):
        params = dict()
        params['xlim'] = [0,5]
        params['ylim'] = [0,50]
        params['xlabel'] = 'Krasse X-Achse'
        params['ylabel'] = 'Krasse Y-Achse'
        params['legend_location'] = 2
        PaperPlotTemplate.__init__( self, params )

    def _get_plotting_functions( self ):
        functions = list()
        functions.append( self.__plot_line1 )
        functions.append( self.__plot_bars1 )
        return functions
    
    def __plot_bars1( self ):
        bars = np.array([10,20,30,25,40])
        text = 'Irgendnen Barplot'
        xlabels = ['P','E','N','I','S']
        self._plot_bars( bars, text, xlabels ) 

    def __plot_line1( self ):
        x = [0,1,2,3,4,5,6]
        y = np.ones(len(x))*4
        params = { 'color' : 'red' }
        label = 'Threshold'
        self._plot_line( x, y, label, params )


class BoxPlotExample( PaperPlotTemplate ):

    def __init__( self ):
        params = dict()
        params['xlim'] = [0,4]
        params['ylim'] = [1,1000]
        params['ylog'] = True
        params['grid_linewidth'] = 1.5
        params['xlabel'] = 'Krasse X-Achse'
        params['ylabel'] = 'Krasse Y-Achse'
        PaperPlotTemplate.__init__( self, params )

    def _get_plotting_functions( self ):
        functions = list()
        functions.append( self.__plot_boxplot1 )
        return functions

    def __plot_boxplot1( self ):
        data = self.__fake_boxplot_data()
        label = 'My Boxes'
        xlabels = ['A','L','F']
        self._plot_boxplot( data, label, xlabels )

    def __fake_boxplot_data( self ):
        spread = pylab.rand(50) * 100
        center = pylab.ones(25) * 50
        flier_high = pylab.rand(10) * 100 + 100
        flier_low = pylab.rand(10) * -100
        data = pylab.concatenate( (spread, center, flier_high, flier_low), 0 )

        spread = pylab.rand(50) * 100
        center = pylab.ones(25) * 40
        flier_high = pylab.rand(10) * 100 + 100
        flier_low = pylab.rand(10) * -100
        d2 = pylab.concatenate( (spread, center, flier_high, flier_low), 0 )
        data.shape = (-1, 1)
        d2.shape = (-1, 1)
        data = [ data, d2, d2[::2,0] ]

        return data
        

if __name__ == '__main__':
    linePlot = LinePlotExample()
    linePlot()
    barPlot = BarPlotExample()
    barPlot()
    boxPlot = BoxPlotExample()
    boxPlot()
