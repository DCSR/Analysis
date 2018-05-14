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
        Button2 = ttk.Button(self.buttonFrame,text="Draw on tk Canvas",command=lambda arg = 1: self.drawOnCanvas(arg))
        Button2.grid(column = 0, row = 1)
        Button3 = ttk.Button(self.buttonFrame,text="Draw using pyplot",command=lambda arg = 1: self.drawUsingPyplot(arg))
        Button3.grid(column = 0, row = 2)
        Button4 = ttk.Button(self.buttonFrame,text="tutorial",command=lambda arg = 1: self.tutorial(arg))
        Button4.grid(column = 0, row = 3)
        Button5 = ttk.Button(self.buttonFrame,text="saveFigure2()",command=lambda arg = 1: self.saveFigure2(arg))
        Button5.grid(column = 0, row = 4)
               
        # Canvas Frame
        self.graphFrame = ttk.Frame(self.root,borderwidth=5, relief="sunken")
        self.graphFrame.grid(column = 1, row = 0, rowspan = 5)
        
        self.figure = Figure(figsize=(4,3), dpi=80)

        self.graphCanvas = FigureCanvasTkAgg(self.figure, master=self.graphFrame)
        self.graphCanvas.get_tk_widget().grid(column=0, row=0, padx = 20, pady = 20)
        
        # Date Time Frame 
        self.dateTimeFrame = ttk.Frame(self.root,borderwidth=5, relief="sunken")
        self.dateTimeFrame.grid(column = 0, row = 6, columnspan = 2)
        self.timeStringVar = StringVar()
        timeLabel = ttk.Label(self.dateTimeFrame, textvariable = self.timeStringVar)
        timeLabel.grid(column = 0, row = 0, sticky = (E))

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
        Procedure to learn how to use Figure and Line2d to do the same thing as pyplot.


        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot([1, 2, 3, 4], [10, 20, 25, 30], color='lightblue', linewidth=3)
        ax.scatter([0.3, 3.8, 1.2, 2.5], [11, 25, 9, 26], color='darkgreen', marker='^')
        ax.set_xlim(0.5, 4.5)
        plt.show()
       
        """

        x = np.arange(1,22,1)   # [1..21]

        y = [5879.4, 2591.1, 2593.0, 2414.1, 2688.2, 2994.0, 3084.2, 3140.4, 3267.9, 3485.5, 3650.1, \
                3647.6, 3888.2, 3929.7, 4209.8, 4378.4, 4552.4, 4854.1, 5375.1, 5828.3, 6027.6]

        ySEM = [712.1, 315.2, 220.1, 208.3, 196.3, 135.8, 172.8, 186.1, 180.9, 177.6, 196.5, 200.4, \
                196.3, 193.7, 200.9, 252.0, 263.8, 309.6, 547.5, 616.1, 618.3]
        
        aSubPlot = self.figure.add_subplot(111)
        aSubPlot.set_xlim(0,22)
        aSubPlot.set_ylim(0, 7500)
        aSubPlot.set_title('One Plot - two lines')
        aSubPlot.set_xlabel('X axis label')        # Axis Labels aren't visible - don't know why
        aSubPlot.set_ylabel('Y label')
        xLabels = ['1','','3','','5','','7','','9','','11','','13','','15','','17','','19','','21']
        aSubPlot.set_xticks([1,3,5,7,9,11,13,15,17,19,21])
        aSubPlot.errorbar(x,y,ySEM)         # This works!
        
        #aLine = Line2D(x,y, color = 'red') # This works
        #aSubPlot.add_line(aLine)

        #aSubPlot.plot(x,y, color = 'blue')   # This works!

        aSubPlot.scatter([5,10,15,20],[3000,4000,5000,6000], color = 'red')  #This works

        self.figure.tight_layout()
        self.graphCanvas.draw()

    def drawUsingPyplot(self,arg):
        """
        Draws Figure 2 for 2L-PR paper.
        Data are from "Figure 2.xlsx".
        y is a list of pumptimes from 26 rats. Data are averages across the four days with the highest breakpoints.
        """
        x = np.arange(1,22,1)   # [1..21]
        
        y = [5879.4, 2591.1, 2593.0, 2414.1, 2688.2, 2994.0, 3084.2, 3140.4, 3267.9, 3485.5, 3650.1, \
                       3647.6, 3888.2, 3929.7, 4209.8, 4378.4, 4552.4, 4854.1, 5375.1, 5828.3, 6027.6]

        ySEM = [712.1, 315.2, 220.1, 208.3, 196.3, 135.8, 172.8, 186.1, 180.9, 177.6, 196.5, 200.4, \
                196.3, 193.7, 200.9, 252.0, 263.8, 309.6, 547.5, 616.1, 618.3]

        fig, ax = plt.subplots()
       
        #ax.plot(x,y)    Simple Plot
        ax.errorbar(x, y, ySEM)
        # Pad margins so that markers don't get clipped by the axes
        # plt.margins(0.2)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.15)
        plt.title('Figure 2')
        plt.ylabel('Pump Time', fontsize = 14)
        plt.xlabel('Trial Number', fontsize = 14)
        ax.set_xticks([1,3,5,7,9,11,13,15,17,19,21])
        
        plt.show()
           
    def tutorial(self,arg):
        #https://www.datacamp.com/community/tutorials/matplotlib-tutorial-python
        # Prepare the data
        x = np.linspace(0, 10, 100)
        # Plot the data
        plt.plot(x, x, label='linear')
        # Add a legend
        plt.legend()
        # Show the plot
        plt.show()

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
