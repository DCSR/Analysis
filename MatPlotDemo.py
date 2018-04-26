"""
dapted from SimpleTkinterPlotApp.py

Adapted from /WorkGroup in Prep/Python-Tkinter-MatplotLib.py

Documentation:

At this point, I cannot get the pyplot API to behave properly (it will not
hand control back to IDLE. It would need to be reset. Including the plt.ion()
as suggested here: https://mail.python.org/pipermail/python-list/2009-October/556014.html
fixes the hang but causes another figure to displayed that and must be closed. Not ideal

Critical features:
    self.FigureFrame           - ttk container (a Frame)
    self.myFigure              - the thing that axes and lines are drawn on        
    self.matPlotCanvas         - This is the thing that gets redrawn after things in myFigureare changed.



Issues: Y axis label doesn't show up

"""

import matplotlib as mpl
mpl.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.lines import Line2D
from matplotlib.figure import Figure
import sys
import tkinter as tk
#from tkinter import *
import tkinter.ttk as ttk
from numpy import arange, sin, pi
from datetime import datetime, date, time

import MatPlotGraphs

def main(argv=None):
    if argv is None:
        argv = sys.argv
    gui = GuiClass()
    gui.go()
    return 0

class GuiClass(object):
    def __init__(self):

        self.root = tk.Tk()
        self.root.wm_title("SimpleTkinterPlotApp.py")

        # buttonFrame and two buttons       
        self.buttonFrame = ttk.Frame(self.root,borderwidth=5, relief="sunken")
        self.buttonFrame.grid(column = 0, row = 0)
        
        Button1 = ttk.Button(self.buttonFrame,text="Draw Demand Curve",command=lambda arg = 1: self.drawDemandCurve())
        Button1.grid(column = 0, row = 1)
        Button2 = ttk.Button(self.buttonFrame,text="Draw log-log Graph",command=lambda arg = 1: self.drawLogLogGraph())
        Button2.grid(column = 0, row = 2)
        Button3 = ttk.Button(self.buttonFrame,text="Draw SineGraph",command=lambda arg = 0: self.drawSineGraph(arg))
        Button3.grid(column = 0, row = 3)
        Button4 = ttk.Button(self.buttonFrame,text="Change Plot 1",command=lambda arg = 1: self.changePlot1(arg))
        Button4.grid(column = 1, row = 4)
        Button6 = ttk.Button(self.buttonFrame,text="Clear Plot 1",command=lambda arg = 1: self.clearPlot(arg))
        Button6.grid(column = 1, row = 5)       
        Button5 = ttk.Button(self.buttonFrame,text="Add Plot 2",command=lambda arg = 1: self.addPlot(arg))
        Button5.grid(column = 1, row = 6)
        Button6 = ttk.Button(self.buttonFrame,text="Clear Plot 2",command=lambda arg = 2: self.clearPlot(arg))
        Button6.grid(column = 1, row = 7)
        Button7 = ttk.Button(self.buttonFrame,text="Clear Figure",command=lambda arg = 1: self.clearFigure(arg))
        Button7.grid(column = 0, row = 8)
        Button8 = ttk.Button(self.buttonFrame,text="Add Axes",command=lambda arg = 1: self.addAxes(arg))
        Button8.grid(column = 0, row = 9)
        Button9 = ttk.Button(self.buttonFrame,text="Delete Axes",command=lambda arg = 1: self.deleteAxes(arg))
        Button9.grid(column = 0, row = 10)
        Button10 = ttk.Button(self.buttonFrame,text="Report",command=lambda arg = 1: self.report())
        Button10.grid(column = 0, row = 11)

               
        # Canvas Frame
        """
        self.FigureFrame                - ttk container (a Frame)
        self.myFigure              - the thing that axes and lines are drawn on        
        self.matPlotCanvas              - container for the MatPlotLib Figure
                                         - This is the thing that gets redrawn after things are changed.
        """
        self.figureFrame = ttk.Frame(self.root,borderwidth=5, relief="sunken")
        self.figureFrame.grid(column = 1, row = 0, rowspan = 5)

        # Create a Figure and set defaults             
        self.myFigure = Figure(figsize=(5,5), dpi=80, tight_layout = True)
        # At dpi=80, and figsize=(5,5) creates a 400 x 400 pixel figure.
        self.myFigure.set_facecolor("red")        
        self.matPlotCanvas = FigureCanvasTkAgg(self.myFigure, master=self.figureFrame)
        self.matPlotCanvas.get_tk_widget().grid(row=1,column=0)

        x = []  
        y = []
        
        self.line1 = Line2D(x,y, color = 'red')
        self.line2 = Line2D(x,y, color = 'blue')
      
        # Date Time Frame 
        self.dateTimeFrame = ttk.Frame(self.root,borderwidth=5, relief="sunken")
        self.dateTimeFrame.grid(column = 0, row = 6, columnspan = 2)
        self.timeStringVar = tk.StringVar()
        timeLabel = ttk.Label(self.dateTimeFrame, textvariable = self.timeStringVar)
        timeLabel.grid(column = 0, row = 0)


    def drawDemandCurve(self):
        """
        Example of a graph with two axes.
        The main graph is a loglog plot
        """
        x =  [2.53, 4.49, 8.0, 14.23, 25.32, 42.55, 80.0, 142.86, 258.06, 444.44, 800.0, 1428.57]
        y1 = [0.864, 0.690, 0.486, 0.286, 0.134, 0.048, 0.012, 0.003, 0.00069, 0.000262, 0.000171, 0.0001607]
        y2 = [1.58, 0.69, 1.13, 1.75, 1.50, 0.98, 0.804, 0.891, 0.325, 0.064, 0.09, 0.01]
        y3 = [4, 3, 9, 25, 38, 44, 64, 127, 83, 27, 65, 0]
        
        self.myFigure.clf()                             # this clears the Figure - i.e. clears previous subplot
        aGraph = self.myFigure.add_subplot(111)
        aGraph.set_title('Demand \n Second line')
        aGraph.set_xlabel('X axis label: fontsize = 16', fontsize = 16)      
        aGraph.set_ylabel('Y axis label: fontsize = 14', fontsize = 14)
        
        aGraph.set_xscale("log")
        aGraph.set_yscale("log")
        aGraph.set_xlim(1e0, 1e3)  # should be 1 to 100 
        aGraph.set_ylim(1e-4, 1e1) # 
        aGraph.loglog(x, y1, color ='red')
        aGraph.scatter(x, y2)
        """
        Add a second axis and line for y3
        """
        self.matPlotCanvas.draw()

    def drawLogLogGraph(self):
        self.myFigure.clf()
        x = [2.53, 4.00, 6.35, 10.13, 16.00, 25.00, 40.00, 61.54, 100.00, 160.00, 266.67, 400.00]
        y = [0.864, 0.690, 0.486, 0.286, 0.134, 0.048, 0.012, 0.003, 0.00069, 0.000262, 0.000171, 0.0001607]        
        aGraph = self.myFigure.add_subplot(111)
        aGraph.set_xscale("log")
        aGraph.set_yscale("log")
        aGraph.set_xlim(1e0, 1e3)  # 1 to 100 
        aGraph.set_ylim(1e-4, 1e0) # 0.0001 to 1
         
        self.testLine = Line2D(x,y, color = 'red')
        aGraph.add_line(self.testLine)

        self.matPlotCanvas.draw()

    def drawSineGraph(self,arg):
        """
        Example of drawing a new graph to myFigure 
        """
        self.myFigure.clf() 
        aGraph = self.myFigure.add_subplot(111)
        aGraph.set_xlim(0,1)
        aGraph.set_ylim(-1, 1)
        aGraph.set_title('First line of title\n Second line')
        aGraph.set_xlabel('X axis label: fontsize = 16', fontsize = 16)      
        aGraph.set_ylabel('Y axis label: fontsize = 14', fontsize = 14)

        x = arange(0.0,1.0,0.01)
        y = sin(3*pi*x)                 
        self.line1.set_data(x,y)
        print(aGraph)

        aGraph.add_line(self.line1)
        print(aGraph)
        
        aGraph.add_line(self.line2)
        print(aGraph)

        self.matPlotCanvas.draw()


    def changePlot1(self,arg):
        x = arange(0.0,1.0,0.01)
        y = sin(3*pi*x)*0.8     
        self.line1.set_data(x,y)          
        self.matPlotCanvas.draw()

    def addPlot(self,arg):
        x = arange(0.0,1.0,0.01)
        y = sin(3*pi*x)*0.4
        self.line2.set_data(x,y) 
        #self.aGraph.add_line(aLine)
          
        self.matPlotCanvas.draw()
        

    def clearPlot(self,arg):
        x = []
        y = []
        if arg == 1:
            self.line1.set_data(x,y)
        else:
            self.line2.set_data(x,y)
        self.matPlotCanvas.draw()
        

    def addAxes(self,arg):
        print("Add a pair of Axes")
        #rect is a 4-length sequence of [left, bottom, width, height] quantities.
        rect = [0.2,0.2,0.7,0.7]
        self.myFigure.add_axes(rect, label='axes2')
        self.matPlotCanvas.draw()

    def deleteAxes(self,arg):
        self.myFigure.delaxes(self.myFigure.axes[0])
        self.matPlotCanvas.draw()
        


    def clearFigure(self,arg):
        print("clearFigure")
        #self.myFigure.clf(keep_observers=False)
        self.myFigure.clf()
        self.matPlotCanvas.draw()

    def report(self):
        print("Report:")
        axes = self.myFigure.gca()
        print("Current Axes", axes)
        figure = self.myFigure.get_figure()
        print("Current Figure", figure)
        #print("graph1:", self.graph1)
        #print("line1:", self.line1)
        print("Axes:", self.myFigure.axes)
        print("DPI:", self.myFigure.get_dpi())
        print("size in inches:", self.myFigure.get_size_inches())

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
