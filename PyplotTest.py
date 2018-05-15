"""
Adapted from SimplePlotTemplate.py

"""

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.lines import Line2D
from matplotlib.figure import Figure
import sys
from tkinter import *
import tkinter.ttk as ttk
from numpy import arange, sin, pi
from datetime import datetime, date, time
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
import mpl_toolkits.axisartist as AA
import numpy as np

def main(argv=None):
    if argv is None:
        argv = sys.argv
    gui = GuiClass()
    gui.go()
    return 0

class GuiClass(object):
    def __init__(self):

        self.root = Tk()
        self.root.wm_title("PyplotTest.py")

        # buttonFrame and two buttons       
        self.buttonFrame = ttk.Frame(self.root,borderwidth=5, relief="sunken")
        self.buttonFrame.grid(column = 0, row = 0)
        Button1 = ttk.Button(self.buttonFrame,text="Clear Canvas",command=lambda arg = 1: self.clearPlot(arg))
        Button1.grid(column = 0, row = 0)
        Button2 = ttk.Button(self.buttonFrame,text="Fig 2 with tk",command=lambda arg = 1: self.drawOnCanvas(arg))
        Button2.grid(column = 0, row = 1)
        Button3 = ttk.Button(self.buttonFrame,text="Fig 2 with plt",command=lambda arg = 1: self.drawUsingPyplot(arg))
        Button3.grid(column = 0, row = 2)
        Button4 = ttk.Button(self.buttonFrame,text="tutorial",command=lambda arg = 1: self.tutorial(arg))
        Button4.grid(column = 0, row = 3)
        Button5 = ttk.Button(self.buttonFrame,text="saveFigure2()",command=lambda arg = 1: self.saveFigure2(arg))
        Button5.grid(column = 0, row = 4)
        Button6 = ttk.Button(self.buttonFrame,text="plt in tk canvas",command=lambda arg = 1: self.testEmbedded(arg))
        Button6.grid(column = 0, row = 5)
               
        # Canvas Frame
        self.graphFrame = ttk.Frame(self.root,borderwidth=5, relief="sunken")
        self.graphFrame.grid(column = 1, row = 0, rowspan = 5)
        
        self.figure = Figure(figsize=(6,5), dpi=80)

        self.graphCanvas = FigureCanvasTkAgg(self.figure, master=self.graphFrame)
        self.graphCanvas.get_tk_widget().grid(column=0, row=0, padx = 20, pady = 20)
        
        # Date Time Frame 
        self.dateTimeFrame = ttk.Frame(self.root,borderwidth=5, relief="sunken")
        self.dateTimeFrame.grid(column = 0, row = 6, columnspan = 2)
        self.timeStringVar = StringVar()
        timeLabel = ttk.Label(self.dateTimeFrame, textvariable = self.timeStringVar)
        timeLabel.grid(column = 0, row = 0, sticky = (E))

    def testEmbedded(self,arg):
        print("testEmbedded()")
        # Generate some example data
        X = np.linspace(0, 2 * np.pi, 50)
        Y = np.sin(X)
        """
        ax = self.figure.add_axes([0, 0, 1, 1])
        ax.plot(X, Y)
        """
        self.graphCanvas.draw()

    def clearPlot(self,arg):
        """
        self.x = []
        self.y = []     
        self.line1.set_data(self.x,self.y)          
        self.graphCanvas.draw()
        """
        print("clearFigure")
        self.figure.clf()
        self.graphCanvas.draw()
        

    def drawOnCanvas(self,arg):
        """
        It might be possible to do everything without pyplot
        but it takes forever to figure out how to do the samllest things.

        I could not figure out how to have two x axes and show the Ns.
        

        """

        x = np.arange(1,24,1)   # [1..21]

        y = [5879.4, 2591.1, 2593.0, 2414.1, 2688.2, 2994.0, 3084.2, 3140.4, 3267.9, 3485.5, 3650.1, \
                3647.6, 3888.2, 3929.7, 4209.8, 4378.4, 4552.4, 4854.1, 5375.1, 5828.3, 6027.6, 5942.4, 6613.2]

        ySEM = [712.1, 315.2, 220.1, 208.3, 196.3, 135.8, 172.8, 186.1, 180.9, 177.6, 196.5, 200.4, \
                196.3, 193.7, 200.9, 252.0, 263.8, 309.6, 547.5, 616.1, 618.3, 886.1, 720.4]

        y2 = [1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1]
        
        aSubPlot = self.figure.add_subplot(111)
        print(aSubPlot)

        #aSubPlot.set_title('Figure 2')

        # Hide or reveal the right and top spines
        aSubPlot.spines['right'].set_visible(False)
        aSubPlot.spines['top'].set_visible(False)
        # ******  Bottom X axis  ******
        aSubPlot.set_xlim(1,24)
        aSubPlot.set_xlabel('Response Ratio', fontsize = 14)

        majorLocator = MultipleLocator(1)
        #majorLocator = matplotlib.ticker.MaxNLocator(nbins=21)
        aSubPlot.xaxis.set_major_locator(majorLocator)
        
        majorFormatter = FormatStrFormatter('%d')
        aSubPlot.xaxis.set_major_formatter(majorFormatter)
        
        #minorLocator = MultipleLocator(1)
        #aSubPlot.xaxis.set_tick_padding(5.0)  # Doesn't work
        #aSubPlot.xaxis.margins(0.05)
        #aSubPlot.xaxis.set_offset_position(1.0)
        
        # Don't know what tick padding is nor how to change it
        print("tick padding", aSubPlot.xaxis.get_tick_padding())

        # Don't know what a margin is; changing it deosn't seem to do anything
        aSubPlot.margins(10.0,10.0)
        print("margins", aSubPlot.margins())
        
        print("Xaxis", aSubPlot.xaxis)

        #aSubPlot.set_xticks([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],minor=True)
        aSubPlot.xaxis.set_ticks_position('bottom')        
        
        xLabels = ['0','1','2','4','6','9','12','15','20','25','32',\
                   '40','50','62','77','95','118','145','178','219','268','328','402', '492']  # 603...

        aSubPlot.set_xticklabels(xLabels, rotation= 270.0)  # Or rotation = "vertical'

        print("major tick labels", aSubPlot.xaxis.get_majorticklabels)

        secondXaxis = aSubPlot.twiny()
        secondXaxis.set_xlim(1,24)
        secondXaxis.set_xlabel('Ns', fontsize = 16)
        ax = secondXaxis.plot(x,y2)
        #ax.set_major_formatter(majorFormatter)
        #secondXaxis.set_ticks_position('top')
        #aSubPlot.xaxis.set_ticks_position('bottom')
        
        # ******  Y axis  ******
        aSubPlot.set_ylim(0, 7500)
        aSubPlot.spines['left'].set_bounds(2000, 6000)  # Only draw spine between the y-ticks
        aSubPlot.set_ylabel('Pump Time', fontsize = 14)
        aSubPlot.yaxis.set_ticks_position('left')

        # ****** Create Plot *****
        aSubPlot.errorbar(x,y,ySEM)         # This works!

        print(secondXaxis)

            
        """
        bbox = {'fc': '0.8', 'pad': 0}
        aSubPlot.text(2.0, 2.0, 'some text', {'ha': 'center', 'va': 'center', 'bbox': bbox}, rotation=45)
        """
        #aLine = Line2D(x,y, color = 'red') # This works
        #aSubPlot.add_line(aLine)

        #aSubPlot.plot(x,y, color = 'blue')   # This works!

        # aSubPlot.scatter([5,10,15,20],[3000,4000,5000,6000], color = 'red')  #This works

        self.figure.tight_layout()
        self.graphCanvas.draw()

    def drawUsingPyplot(self,arg):
        """
        Draws Figure 2 for 2L-PR paper.
        Data are from "Figure 2.xlsx".
        y is a list of pumptimes from 26 rats. Data are averages across the four days with the highest breakpoints.
        """
        x = np.arange(1,24,1)   # [1..23]

        y = [5879.4, 2591.1, 2593.0, 2414.1, 2688.2, 2994.0, 3084.2, 3140.4, 3267.9, 3485.5, 3650.1, \
                3647.6, 3888.2, 3929.7, 4209.8, 4378.4, 4552.4, 4854.1, 5375.1, 5828.3, 6027.6, 5942.4, 6613.2]

        ySEM = [712.1, 315.2, 220.1, 208.3, 196.3, 135.8, 172.8, 186.1, 180.9, 177.6, 196.5, 200.4, \
                196.3, 193.7, 200.9, 252.0, 263.8, 309.6, 547.5, 616.1, 618.3, 886.1, 720.4]

        xLabels = ['','', '1','2','4','6','9','12','15','20','25','32',\
                   '40','50','62','77','95','118','145','178','219','268','328','402', '492']  # 603...
        N = [26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 25, 24, 24, 22, 20, 19, 15, 13, 8,	7, 7]

        dose = []
        for pumptime in y:
            mg = (pumptime/1000) * 5.0 * 0.025  # pumptime(mSec) * mg/ml * ml/sec)
            dose.append(mg)

        doseSEM = []
        for SEM in ySEM:
            mg = (SEM/1000) * 5.0 * 0.025  # pumptime(mSec) * mg/ml * ml/sec)
            doseSEM.append(mg)
        
        print(len(x), len(y), len(ySEM), len(xLabels), len(dose), len(N), len(doseSEM))

        fig, ax = plt.subplots()
       
        #ax.plot(x,y)    Simple Plot
        ax.errorbar(x, dose, doseSEM, marker = 'o', color = 'black', ecolor = 'red')
        plt.margins(0.1)    # Pad margins so that markers don't get clipped by the axes       
        plt.subplots_adjust(bottom = 0.15)  # Tweak spacing to prevent clipping of tick-labels
        plt.title('Figure 2')
        plt.ylabel('Dose (mg)', fontsize = 14)
        plt.xlabel('Trial Response Ratio', fontsize = 14)
        majorLocator = MultipleLocator(1)
        ax.xaxis.set_major_locator(majorLocator)
        majorLocator = MultipleLocator(0.25)
        ax.yaxis.set_major_locator(majorLocator)
        ax.set_xlim(0, 24)
        ax.set_ylim(0, 1.0)
        ax.set_xticklabels(xLabels, rotation= 270.0)  # Or rotation = "vertical'
        
        ax2 = ax.twinx()
        ax2.set_ylabel('Nunber of Subjects Reaching Ratio', fontsize = 14)  
        ax2.plot(x, N, color= 'blue')
        ax2.set_ylim(0, 30)

        #ax.text(0.1, 0.1, 'test text', horizontalalignment='center', \
        #verticalalignment='center', transform=ax.transAxes)
        
        plt.show()
           
    def tutorial(self,arg):
        #https://www.datacamp.com/community/tutorials/matplotlib-tutorial-python
        ax1 = self.figure.add_subplot(131)
        ax2 = self.figure.add_subplot(132)
        ax3 = self.figure.add_subplot(133)

        x = [1,2,3,4]
        y = [4,5,5,4]

        ax1.bar([1,2,3],[3,4,5])
        # ax1.axis["x"].set_axis_direction("left")  Doesn't work as per tutorial
        # ax1.xaxis.set_axis_direction("left")               "
        """
        ax2.barh([0.5,1,2.5],[0,1,2])
        ax2.axhline(0.45)
        ax1.axvline(0.65)
        ax3.scatter(x,y)
        ax3.set(title="ax3", xlabel="ax3 x label", ylabel="ax3 y label")
        """
        ax1

        self.graphCanvas.draw()

    def saveFigure2(self, arg):
        print("Saving Figure2.png")
        self.figure.savefig('Figure2.png')

    def periodic_check(self):
        # http://docs.python.org/dev/library/datetime.html#strftime-strptime-behavior
        time = datetime.now()
        self.timeStringVar.set(time.strftime("%B %d -- %H:%M:%S"))        
        self.root.after(100, self.periodic_check)

    def go(self):
        self.root.after(100, self.periodic_check)
        self.root.mainloop()

if __name__ == "__main__":
    sys.exit(main())  
