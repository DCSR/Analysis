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
        Button1 = ttk.Button(self.buttonFrame,text="Clear tk Canvas",command=lambda arg = 1: self.clearCanvas(arg))
        Button1.grid(column = 0, row = 0)
        Button2 = ttk.Button(self.buttonFrame,text="Fig 2 with tk",command=lambda arg = 1: self.fig2OnCanvas(arg))
        Button2.grid(column = 0, row = 1)
        Button3 = ttk.Button(self.buttonFrame,text="save tk Fig 2",command=lambda arg = 1: self.saveFigure2(arg))
        Button3.grid(column = 0, row = 2)
        Button4 = ttk.Button(self.buttonFrame,text="Figure 2",command=lambda arg = 1: self.figure2(arg))
        Button4.grid(column = 0, row = 3)
        Button5 = ttk.Button(self.buttonFrame,text="Figure 3",command=lambda arg = 1: self.figure3(arg))
        Button5.grid(column = 0, row = 4)
        Button6 = ttk.Button(self.buttonFrame,text="Figure 4 Rev",command=lambda arg = 1: self.figure4Rev(arg))
        Button6.grid(column = 0, row = 5)
        Button7 = ttk.Button(self.buttonFrame,text="Figure 4",command=lambda arg = 1: self.figure4(arg))
        Button7.grid(column = 0, row = 6)
        Button8 = ttk.Button(self.buttonFrame,text="Split axis test",command=lambda arg = 1: self.test(arg))
        Button8.grid(column = 0, row = 7)
               
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

    # ******************* Figure 4 Rev ************************

    def figure4Rev(self,arg):
        """
        Figure for 2L-PR manuscript using pyplot.
        Uses data Means and SEMs from Figure4 Means.xlxs

        Note that, with shorter sessions, it appears that the lever might have been held
        down for a brief period when the lever was being withdrawn. This resulted in a small
        amount of holddown time showing up in the bin after the final one. For example, if
        session lenght was 4 sec, some times showed up in bin 5. 

        Including the X+1 data yields the correct totals for the session. But those bins were
        excluded from the graph.

        """
        # ***********  Data from "Figure4 Means.xlxs"  ******************
        
        y180 = [9.3, 287.8, 326.0, 290.0, 220.1, 168.7, 129.5, 86.6, 80.5, 65.3, \
                62.7, 54.0, 56.1, 54.3, 50.7, 62.3, 53.1, 51.9, 44.3, 43.3, \
                39.7, 45.5, 37.1, 23.3, 22.9, 26.6, 30.2, 26.8, 20.0, 22.6, \
                23.4, 25.7, 21.3, 21.3, 21.0, 18.4, 16.3, 14.8, 14.1, 13.3, \
                13.4, 13.6, 13.9, 15.5, 13.8, 14.7, 17.6, 17.9, 20.7, 18.7, \
                15.9, 13.2, 16.5, 16.1, 13.9, 15.8, 14.3, 14.2, 12.1, 16.4, \
                12.4, 9.4, 9.4, 13.1, 7.2, 9.2, 10.2, 9.8, 9.7, 7.7, \
                8.6, 8.8, 8.8, 7.8, 11.2, 7.0, 4.1, 8.1, 6.6, 8.8, \
                9.4, 9.2, 8.0, 6.7, 6.6, 7.4, 6.1, 7.8, 7.8, 7.2, \
                6.0, 10.0, 8.3, 8.4, 7.9, 5.5, 4.1, 3.0, 5.3, 6.6, \
                8.9, 9.4, 7.8, 6.6, 6.5, 5.4, 4.7, 8.4, 8.2, 13.2, \
                10.4, 8.7, 8.1, 8.2, 9.6, 9.9, 9.3, 9.6, 13.0, 12.4, \
                10.1, 6.9, 13.2, 15.4, 11.4, 10.5, 10.3, 8.5, 9.5, 8.0, \
                10.2, 10.7, 10.6, 12.7, 8.9, 11.9, 6.4, 7.6, 7.0, 5.5, \
                6.9, 11.2, 10.3, 7.2, 7.8, 8.4, 5.0, 4.4, 7.7, 4.7, \
                8.0, 7.6, 13.9, 11.8, 10.2, 10.3, 8.2, 6.3, 7.0, 7.4, \
                7.6, 8.8, 7.8, 6.7, 5.7, 5.0, 5.4, 7.4, 6.2, 5.6, \
                10.8, 9.5, 5.1, 7.8, 9.8, 8.2, 9.6, 10.8, 10.8, 11.2]

        
        y180SEM = [4.9, 57.3, 47.1, 46.2, 50.7, 41.0, 31.3, 25.8, 21.6, 17.9, \
                   14.5, 12.0, 12.1, 11.7, 10.2, 10.7, 13.3, 13.0, 11.0, 11.0, \
                   10.7, 12.6, 12.0, 4.9, 4.9, 4.6, 4.9, 5.5, 4.2, 5.1, \
                   6.4, 6.9, 5.7, 4.9, 4.9, 5.2, 5.1, 4.9, 3.9, 4.4, \
                   5.0, 5.5, 4.9, 3.1, 3.7, 3.6, 4.5, 4.2, 5.3, 4.7, \
                   3.0, 2.0, 4.4, 3.9, 4.1, 5.5, 5.2, 4.5, 3.2, 3.7, \
                   3.6, 3.0, 2.8, 2.6, 2.3, 3.7, 3.2, 3.6, 4.3, 2.8, \
                   2.9, 2.7, 2.5, 3.3, 3.2, 2.2, 1.6, 2.4, 2.6, 3.1, \
                   2.9, 2.6, 3.1, 2.0, 3.0, 2.3, 2.0, 2.5, 3.2, 2.4, \
                   2.3, 4.5, 3.2, 3.5, 2.6, 2.4, 1.4, 1.2, 2.0, 1.8, \
                   2.3, 2.5, 2.3, 1.9, 2.6, 2.9, 2.6, 2.4, 2.5, 3.6, \
                   3.1, 1.9, 1.8, 2.5, 3.1, 2.3, 3.8, 3.6, 2.7, 3.1, \
                   3.1, 2.4, 3.8, 3.3, 2.9, 3.3, 2.5, 2.7, 2.4, 1.7, \
                   3.1, 2.6, 2.9, 3.5, 1.7, 3.3, 1.6, 1.8, 2.6, 1.4, \
                   2.3, 3.7, 3.9, 3.7, 4.2, 2.6, 1.8, 1.6, 2.4, 1.8, \
                   2.8, 2.1, 3.7, 2.5, 1.9, 2.7, 3.3, 2.4, 2.7, 3.0, \
                   3.6, 4.3, 3.4, 2.4, 1.7, 2.0, 1.7, 2.7, 2.2, 2.7, \
                   4.7, 3.4, 2.0, 2.8, 4.1, 2.5, 2.8, 2.2, 3.2, 2.6]


        
        y120 = []
        y120SEM = []
        
        y60 = []
        y60SEM = []

        y30 = []
        y30SEM = []

        y15 = []
        y15SEM = []

        y8 = []
        y8SEM = []

        y4 = []
        y4SEM = []

        y2 = []
        y2SEM = []

        y1 = [0.198]
        y1SEM = [0.089]

        # ******* Various X axes ****** 
        x180 = np.arange(1,181,1)          # 180 data points
        x120 = np.arange(1,121,1)          
        x60 = np.arange(1,61,1)            
        x30 = np.arange(1,31,1)            
        x15 = np.arange(1,16,1)            
        x8 = np.arange(1,9,1)             
        x4 = np.arange(1,5,1)             
        x2 = [1,2]
        x1 = [1]

        fig, ax1 = plt.subplots()

        myMarkersize = 1
        myLinewidth = 1

        print(len(x180), len(y180), len(y180SEM))
        
        ax1.errorbar(x180, y180, y180SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                     color = 'black', ecolor = 'none', label = "180 sec")
        """
        ax1.errorbar(x120, y120, y120SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                     color = 'red', ecolor = 'none', label = "120 sec")
        ax1.errorbar(x60, y60, y60SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                   color = 'orange', ecolor = 'none', label = "60 sec")
        ax1.errorbar(x30, y30, y30SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                   color = 'slategray', ecolor = 'none', label = "30 sec")
        ax1.errorbar(x15, y15, y15SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                   color = 'darkblue', ecolor = 'none', label = "15 sec")
        ax1.errorbar(x8, y8, y8SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                   color = 'olive', ecolor = 'none', label = "8 sec")
        ax1.errorbar(x4, y4, y4SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                     color = 'blue', ecolor = 'none', label = "4 sec")
        ax1.errorbar(x2, y2, y2SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                     color = 'plum', ecolor = 'none', label = "2 sec")
        ax1.errorbar(x1, y1, y1SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                     color = 'lime', ecolor = 'none', label = "1 sec")
        """

        #plt.title('Figure 4')
        plt.margins(0.1)    # Pad margins so that markers don't get clipped by the axes       
        plt.subplots_adjust(bottom = 0.15)  # Tweak spacing to prevent clipping of tick-labels
        
        # ****  top spine  ****
        ax1.spines['top'].set_color('red')
        ax1.spines['top'].set_position(('axes', 1.02))    # Offset the axis 0.02 to left of zero
                        
        # ****** x Axis *********
        ax1.spines['bottom'].set_color('blue')        
        plt.xlabel('Access Period (1 second bins)', fontsize = 14)
        ax1.set_xlim(0, 180)         
        majorLocator = MultipleLocator(30)
        ax1.xaxis.set_major_locator(majorLocator)
        ax1.spines['bottom'].set_position(('axes', -0.02))   # Offset X axis down 0.02        
        ax1.spines['bottom'].set_bounds(0, 180)              # Only draw spine between the y-ticks
        
        # ****** Left Axis *******
        ax1.spines['left'].set_color('blue')
        plt.ylabel('Pump duration (sec)', fontsize = 14)        
        ax1.set_ylim(0, 1000.0)      
        majorLocator = MultipleLocator(100.0)
        ax1.yaxis.set_major_locator(majorLocator)
        ax1.spines['left'].set_position(('axes', 0.0))    # Offset the axis 0.02 to left of zero

        # ****** Right Axis *******
        ax1.spines['right'].set_color('red')

        # ****** Inset Figure ******

        ax2 = plt.axes([.35, .3, .5, .5], facecolor = 'none')   #
        ax2.spines['top'].set_color('none')
        ax2.spines['right'].set_color('none')        
        # X axis
        ax2.spines['bottom'].set_position(('axes', -0.02))   # Offset X axis down 0.02 
        majorLocator = MultipleLocator(3)
        ax2.xaxis.set_major_locator(majorLocator)
        ax2.set_xlim(0, 15)
        # Y Axis       
        ax2.set_ylim(0, 1000.0)  

        ax2.errorbar(x180, y180, y180SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                     color = 'black', ecolor = 'black', label = "180 sec")
        """
        ax2.errorbar(x120, y120, y120SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                     color = 'red', ecolor = 'red', label = "120 sec")
        ax2.errorbar(x60, y60, y60SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                   color = 'orange', ecolor = 'orange', label = "60 sec")
        ax2.errorbar(x30, y30, y30SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                   color = 'slategray', ecolor = 'slategray', label = "30 sec")
        ax2.errorbar(x15, y15, y15SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                   color = 'darkblue', ecolor = 'darkblue', label = "15 sec")
        ax2.errorbar(x8, y8, y8SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                   color = 'olive', ecolor = 'olive', label = "8 sec")
        ax2.errorbar(x4, y4, y4SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                     color = 'blue', ecolor = 'blue', label = "4 sec")
        ax2.errorbar(x2, y2, y2SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                     color = 'plum', ecolor = 'plum', label = "2 sec")
        ax2.errorbar(x1, y1, y1SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                     color = 'lime', ecolor = 'lime', label = "1 sec")
        """

        plt.title('Inset Title', fontsize = 10)

        legend = ax1.legend(loc='upper right', shadow=True)
        #ax1.spines['left'].set_color('none')
        #ax1.set_xticklabels(xLabels, rotation= 270.0)  # Or rotation = "vertical'
        plt.show()   




    # *******************  Figure 4 ***************************

    def figure4(self,arg):
        """
        Figure for 2L-PR manuscript using pyplot.
        Uses data Means and SEMs from Figure4 Means.xlxs

        Note that, with shorter sessions, it appears that the lever might have been held
        down for a brief period when the lever was being withdrawn. This resulted in a small
        amount of holddown time showing up in the bin after the final one. For example, if
        session lenght was 4 sec, some times showed up in bin 5. 

        Including the X+1 data yields the correct totals for the session. But those bins were
        excluded from the graph.

        """
        # ***********  Data from "Figure4 Means.xlxs"  ******************
        
        y180 = [0.156, 5.002, 5.716, 5.103, 3.920, 2.991, 2.342, 1.618, 1.469, 1.214, \
                1.125, 0.981, 1.025, 0.981, 0.909, 1.098, 0.969, 0.915, 0.821, 0.784, \
                0.731, 0.838, 0.668, 0.396, 0.405, 0.440, 0.515, 0.480, 0.348, 0.400, \
                0.431, 0.458, 0.380, 0.368, 0.369, 0.322, 0.279, 0.267, 0.255, 0.230, \
                0.237, 0.241, 0.244, 0.265, 0.260, 0.259, 0.319, 0.324, 0.365, 0.342, \
                0.275, 0.235, 0.307, 0.291, 0.254, 0.279, 0.259, 0.250, 0.218, 0.274, \
                0.220, 0.168, 0.166, 0.229, 0.127, 0.165, 0.173, 0.163, 0.166, 0.140, \
                0.139, 0.143, 0.155, 0.149, 0.189, 0.114, 0.072, 0.140, 0.129, 0.146, \
                0.151, 0.153, 0.146, 0.117, 0.112, 0.124, 0.105, 0.136, 0.153, 0.132, \
                0.103, 0.191, 0.148, 0.140, 0.131, 0.097, 0.068, 0.051, 0.091, 0.117, \
                0.152, 0.164, 0.132, 0.115, 0.112, 0.076, 0.073, 0.136, 0.146, 0.215, \
                0.179, 0.143, 0.133, 0.133, 0.163, 0.165, 0.144, 0.156, 0.209, 0.207, \
                0.163, 0.116, 0.236, 0.266, 0.206, 0.201, 0.173, 0.141, 0.165, 0.139, \
                0.167, 0.184, 0.185, 0.227, 0.147, 0.200, 0.110, 0.126, 0.120, 0.095, \
                0.112, 0.180, 0.171, 0.125, 0.138, 0.144, 0.094, 0.077, 0.126, 0.085, \
                0.141, 0.137, 0.226, 0.207, 0.185, 0.195, 0.151, 0.116, 0.129, 0.131, \
                0.136, 0.156, 0.133, 0.121, 0.099, 0.089, 0.100, 0.139, 0.106, 0.093, \
                0.176, 0.164, 0.099, 0.132, 0.168, 0.138, 0.157, 0.189, 0.197, 0.212]
        y180SEM = [0.078, 1.001, 0.809, 0.773, 0.924, 0.796, 0.647, 0.536, 0.453, 0.373, \
                   0.302, 0.252, 0.239, 0.223, 0.188, 0.199, 0.233, 0.225, 0.205, 0.208, \
                   0.200, 0.235, 0.219, 0.081, 0.094, 0.073, 0.090, 0.102, 0.072, 0.089, \
                   0.113, 0.125, 0.099, 0.082, 0.085, 0.093, 0.088, 0.090, 0.073, 0.077, \
                   0.092, 0.098, 0.088, 0.052, 0.068, 0.062, 0.087, 0.077, 0.091, 0.090, \
                   0.053, 0.042, 0.085, 0.078, 0.084, 0.101, 0.096, 0.082, 0.062, 0.057, \
                   0.066, 0.056, 0.051, 0.050, 0.041, 0.066, 0.054, 0.065, 0.078, 0.051, \
                   0.042, 0.041, 0.048, 0.063, 0.056, 0.036, 0.030, 0.045, 0.056, 0.050, \
                   0.041, 0.045, 0.056, 0.040, 0.051, 0.037, 0.034, 0.047, 0.075, 0.049, \
                   0.041, 0.087, 0.059, 0.058, 0.046, 0.044, 0.021, 0.019, 0.035, 0.034, \
                   0.040, 0.043, 0.037, 0.033, 0.043, 0.040, 0.037, 0.040, 0.048, 0.059, \
                   0.058, 0.026, 0.026, 0.038, 0.053, 0.034, 0.052, 0.052, 0.038, 0.051, \
                   0.044, 0.039, 0.077, 0.062, 0.059, 0.071, 0.044, 0.044, 0.039, 0.034, \
                   0.045, 0.045, 0.052, 0.062, 0.028, 0.057, 0.027, 0.033, 0.043, 0.023, \
                   0.036, 0.057, 0.064, 0.058, 0.068, 0.044, 0.038, 0.027, 0.033, 0.034, \
                   0.053, 0.038, 0.056, 0.046, 0.044, 0.060, 0.065, 0.046, 0.051, 0.055, \
                   0.065, 0.079, 0.060, 0.046, 0.030, 0.038, 0.034, 0.054, 0.039, 0.043, \
                   0.077, 0.059, 0.047, 0.050, 0.071, 0.042, 0.042, 0.039, 0.060, 0.059]
        
        y120 = [0.149, 4.245, 5.366, 3.633, 2.455, 1.695, 1.234, 1.216, 1.228, 1.468, \
                1.198, 1.115, 1.116, 1.051, 1.158, 1.026, 0.902, 0.726, 0.742, 0.652, \
                0.683, 0.589, 0.511, 0.514, 0.526, 0.566, 0.644, 0.683, 0.526, 0.536, \
                0.482, 0.491, 0.326, 0.452, 0.282, 0.319, 0.342, 0.276, 0.301, 0.415, \
                0.448, 0.346, 0.300, 0.257, 0.269, 0.235, 0.166, 0.207, 0.195, 0.233, \
                0.165, 0.200, 0.163, 0.118, 0.216, 0.260, 0.173, 0.263, 0.211, 0.147, \
                0.169, 0.224, 0.139, 0.149, 0.194, 0.217, 0.168, 0.123, 0.157, 0.184, \
                0.231, 0.164, 0.212, 0.154, 0.237, 0.182, 0.154, 0.186, 0.176, 0.073, \
                0.129, 0.112, 0.109, 0.121, 0.107, 0.098, 0.117, 0.134, 0.197, 0.162, \
                0.102, 0.079, 0.085, 0.124, 0.191, 0.197, 0.178, 0.183, 0.143, 0.164, \
                0.089, 0.089, 0.166, 0.145, 0.100, 0.147, 0.188, 0.215, 0.195, 0.085, \
                0.163, 0.142, 0.173, 0.085, 0.143, 0.112, 0.167, 0.078, 0.098, 0.091]
        y120SEM = [0.071, 1.086, 0.732, 0.512, 0.492, 0.369, 0.272, 0.262, 0.295, 0.295, \
                   0.274, 0.298, 0.290, 0.262, 0.259, 0.225, 0.233, 0.196, 0.171, 0.145, \
                   0.186, 0.170, 0.125, 0.141, 0.152, 0.105, 0.209, 0.210, 0.119, 0.137, \
                   0.126, 0.123, 0.081, 0.136, 0.089, 0.097, 0.062, 0.067, 0.106, 0.135, \
                   0.159, 0.118, 0.078, 0.060, 0.061, 0.087, 0.091, 0.080, 0.047, 0.076, \
                   0.075, 0.051, 0.057, 0.049, 0.065, 0.088, 0.044, 0.070, 0.050, 0.047, \
                   0.044, 0.050, 0.051, 0.063, 0.047, 0.054, 0.047, 0.042, 0.037, 0.058, \
                   0.071, 0.062, 0.045, 0.043, 0.052, 0.042, 0.060, 0.060, 0.068, 0.025, \
                   0.046, 0.037, 0.039, 0.057, 0.047, 0.040, 0.047, 0.049, 0.070, 0.062, \
                   0.042, 0.027, 0.029, 0.047, 0.045, 0.079, 0.075, 0.069, 0.050, 0.066, \
                   0.028, 0.038, 0.071, 0.063, 0.044, 0.048, 0.061, 0.042, 0.053, 0.048, \
                   0.062, 0.043, 0.040, 0.031, 0.058, 0.047, 0.071, 0.026, 0.060, 0.081]
        
        y60 = [0.162, 5.485, 6.665, 5.105, 3.636, 2.444, 1.757, 1.543, 1.312, 1.029, \
               1.086, 0.951, 0.819, 0.815, 0.817, 0.834, 0.796, 0.659, 0.604, 0.614, \
               0.618, 0.627, 0.613, 0.537, 0.534, 0.316, 0.273, 0.388, 0.386, 0.351, \
               0.465, 0.430, 0.336, 0.451, 0.289, 0.241, 0.305, 0.326, 0.276, 0.317, \
               0.286, 0.266, 0.291, 0.276, 0.177, 0.199, 0.190, 0.209, 0.205, 0.136, \
               0.136, 0.218, 0.288, 0.231, 0.240, 0.198, 0.238, 0.244, 0.247, 0.301]
        y60SEM = [0.087, 0.931, 1.140, 1.087, 0.802, 0.574, 0.412, 0.429, 0.398, 0.336, \
                  0.414, 0.440, 0.296, 0.243, 0.255, 0.258, 0.299, 0.260, 0.281, 0.213, \
                  0.175, 0.247, 0.273, 0.167, 0.145, 0.103, 0.087, 0.097, 0.086, 0.101, \
                  0.144, 0.100, 0.083, 0.128, 0.109, 0.082, 0.091, 0.098, 0.064, 0.040, \
                  0.053, 0.066, 0.063, 0.075, 0.053, 0.044, 0.064, 0.090, 0.067, 0.046, \
                  0.032, 0.067, 0.065, 0.079, 0.076, 0.067, 0.111, 0.109, 0.135, 0.122]

        y30 = [0.221, 5.686, 6.157, 4.430, 3.302, 2.823, 2.449, 2.446, 2.088, 1.824, \
               1.788, 1.586, 1.334, 1.040, 0.925, 0.900, 0.814, 0.787, 0.875, 0.873, \
               0.836, 0.845, 0.729, 0.647, 0.645, 0.570, 0.384, 0.372, 0.484, 0.486]
        y30SEM = [0.105, 0.964, 1.402, 1.064, 0.812, 0.746, 0.712, 0.697, 0.659, 0.618, \
                  0.505, 0.375, 0.262, 0.214, 0.269, 0.322, 0.277, 0.200, 0.223, 0.227, \
                  0.335, 0.248, 0.245, 0.171, 0.242, 0.162, 0.098, 0.116, 0.142, 0.199]

        y15 = [0.223, 5.564, 6.022, 4.626, 4.252, 3.711, 3.303, 2.997, 2.583, 2.385, \
               2.192, 1.579, 1.218, 1.073, 0.992]
        y15SEM = [0.102, 1.106, 1.041, 0.786, 0.890, 0.898, 0.785, 0.719, 0.715, 0.639, \
                  0.640, 0.399, 0.351, 0.356, 0.395]

        y8 = [0.227, 5.836, 6.825, 5.358, 4.232, 3.437, 3.162, 2.488]
        y8SEM = [0.102, 1.331, 1.022, 0.618, 0.684, 0.612, 0.616, 0.566]

        y4 = [0.273, 6.816, 8.401, 6.878]
        y4SEM = [0.141, 1.477, 1.405, 1.229]

        y2 = [0.302, 6.083]
        y2SEM = [0.151, 1.468]

        y1 = [0.198]
        y1SEM = [0.089]

        # ******* Various X axes ****** 
        x180 = np.arange(1,181,1)          # 180 data points
        x120 = np.arange(1,121,1)          
        x60 = np.arange(1,61,1)            
        x30 = np.arange(1,31,1)            
        x15 = np.arange(1,16,1)            
        x8 = np.arange(1,9,1)             
        x4 = np.arange(1,5,1)             
        x2 = [1,2]
        x1 = [1]

        fig, ax1 = plt.subplots()

        myMarkersize = 1
        myLinewidth = 1
        
        ax1.errorbar(x180, y180, y180SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                     color = 'black', ecolor = 'none', label = "180 sec")
        ax1.errorbar(x120, y120, y120SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                     color = 'red', ecolor = 'none', label = "120 sec")
        ax1.errorbar(x60, y60, y60SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                   color = 'orange', ecolor = 'none', label = "60 sec")
        ax1.errorbar(x30, y30, y30SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                   color = 'slategray', ecolor = 'none', label = "30 sec")
        ax1.errorbar(x15, y15, y15SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                   color = 'darkblue', ecolor = 'none', label = "15 sec")
        ax1.errorbar(x8, y8, y8SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                   color = 'olive', ecolor = 'none', label = "8 sec")
        ax1.errorbar(x4, y4, y4SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                     color = 'blue', ecolor = 'none', label = "4 sec")
        ax1.errorbar(x2, y2, y2SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                     color = 'plum', ecolor = 'none', label = "2 sec")
        ax1.errorbar(x1, y1, y1SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                     color = 'lime', ecolor = 'none', label = "1 sec")

        #plt.title('Figure 4')
        plt.margins(0.1)    # Pad margins so that markers don't get clipped by the axes       
        plt.subplots_adjust(bottom = 0.15)  # Tweak spacing to prevent clipping of tick-labels
        
        # ****  top spine  ****
        ax1.spines['top'].set_color('red')
        ax1.spines['top'].set_position(('axes', 1.02))    # Offset the axis 0.02 to left of zero
                        
        # ****** x Axis *********
        ax1.spines['bottom'].set_color('blue')        
        plt.xlabel('Access Period (1 second bins)', fontsize = 14)
        ax1.set_xlim(0, 180)         
        majorLocator = MultipleLocator(30)
        ax1.xaxis.set_major_locator(majorLocator)
        ax1.spines['bottom'].set_position(('axes', -0.02))   # Offset X axis down 0.02        
        ax1.spines['bottom'].set_bounds(0, 180)              # Only draw spine between the y-ticks
        
        # ****** Left Axis *******
        ax1.spines['left'].set_color('blue')
        plt.ylabel('Pump duration (sec)', fontsize = 14)        
        ax1.set_ylim(0, 10.0)      
        majorLocator = MultipleLocator(1.0)
        ax1.yaxis.set_major_locator(majorLocator)
        ax1.spines['left'].set_position(('axes', 0.0))    # Offset the axis 0.02 to left of zero

        # ****** Right Axis *******
        ax1.spines['right'].set_color('red')

        # ****** Inset Figure ******

        ax2 = plt.axes([.35, .3, .5, .5], facecolor = 'none')   #
        ax2.spines['top'].set_color('none')
        ax2.spines['right'].set_color('none')        
        # X axis
        ax2.spines['bottom'].set_position(('axes', -0.02))   # Offset X axis down 0.02 
        majorLocator = MultipleLocator(3)
        ax2.xaxis.set_major_locator(majorLocator)
        ax2.set_xlim(0, 15)
        # Y Axis       
        ax2.set_ylim(0, 10.0)  

        ax2.errorbar(x180, y180, y180SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                     color = 'black', ecolor = 'black', label = "180 sec")
        ax2.errorbar(x120, y120, y120SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                     color = 'red', ecolor = 'red', label = "120 sec")
        ax2.errorbar(x60, y60, y60SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                   color = 'orange', ecolor = 'orange', label = "60 sec")
        ax2.errorbar(x30, y30, y30SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                   color = 'slategray', ecolor = 'slategray', label = "30 sec")
        ax2.errorbar(x15, y15, y15SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                   color = 'darkblue', ecolor = 'darkblue', label = "15 sec")
        ax2.errorbar(x8, y8, y8SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                   color = 'olive', ecolor = 'olive', label = "8 sec")
        ax2.errorbar(x4, y4, y4SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                     color = 'blue', ecolor = 'blue', label = "4 sec")
        ax2.errorbar(x2, y2, y2SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                     color = 'plum', ecolor = 'plum', label = "2 sec")
        ax2.errorbar(x1, y1, y1SEM, marker = 'o', markersize = myMarkersize, linewidth = myLinewidth, \
                     color = 'lime', ecolor = 'lime', label = "1 sec")

        plt.title('Inset Title', fontsize = 10)

        legend = ax1.legend(loc='upper right', shadow=True)
        #ax1.spines['left'].set_color('none')
        #ax1.set_xticklabels(xLabels, rotation= 270.0)  # Or rotation = "vertical'
        plt.show()

    def test(self,arg):
            x = np.linspace(0,10,100)
            x[75:] = np.linspace(40,42.5,25)

            y = np.sin(x)

            # Two plots that share the Y axis
            f,(ax,ax2) = plt.subplots(1,2,sharey=True, facecolor='w')

            # plot the same data on both axes
            ax.plot(x, y)
            ax2.plot(x, y)

            ax.set_xlim(0,7.5)
            ax2.set_xlim(40,42.5)

            # hide the spines between ax and ax2
            ax.spines['right'].set_visible(False)
            ax2.spines['left'].set_visible(False)
            ax.yaxis.tick_left()
            ax.tick_params(labelright=False)
            ax2.yaxis.tick_right()

            # This looks pretty good, and was fairly painless, but you can get that
            # cut-out diagonal lines look with just a bit more work. The important
            # thing to know here is that in axes coordinates, which are always
            # between 0-1, spine endpoints are at these locations (0,0), (0,1),
            # (1,0), and (1,1).  Thus, we just need to put the diagonals in the
            # appropriate corners of each of our axes, and so long as we use the
            # right transform and disable clipping.

            d = .015 # how big to make the diagonal lines in axes coordinates
            # arguments to pass plot, just so we don't keep repeating them
            kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
            ax.plot((1-d,1+d), (-d,+d), **kwargs)
            ax.plot((1-d,1+d),(1-d,1+d), **kwargs)

            kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
            ax2.plot((-d,+d), (1-d,1+d), **kwargs)
            ax2.plot((-d,+d), (-d,+d), **kwargs)

            # What's cool about this is that now if we vary the distance between
            # ax and ax2 via f.subplots_adjust(hspace=...) or plt.subplot_tool(),
            # the diagonal lines will move accordingly, and stay right at the tips
            # of the spines they are 'breaking'

            # Move the whole plot around
            pos1 = ax.get_position() # get the original position
            # add aomething (eg. 0.2) to any of the four coordinates 
            pos2 = [pos1.x0, pos1.y0,  pos1.width, pos1.height] 
            ax.set_position(pos2) # set a new position


            ax.spines['left'].set_position(('axes', -0.1))

            plt.show()

    def clearCanvas(self,arg):
        print("clearFigure")
        self.figure.clf()
        self.graphCanvas.draw()
        

    def fig2OnCanvas(self,arg):
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
        
        # Don't know what tick padding is - nor how to change it
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

    def figure2(self,arg):
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
        N = [26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 25, 24, 24, 22, 20, 19, 15, 13, 8, 7, 7]

        dose = []
        for pumptime in y:
            mg = (pumptime/1000) * 5.0 * 0.025  # pumptime(mSec) * mg/ml * ml/sec)
            dose.append(mg)

        doseSEM = []
        for SEM in ySEM:
            mg = (SEM/1000) * 5.0 * 0.025  # pumptime(mSec) * mg/ml * ml/sec)
            doseSEM.append(mg)
        
        #print(len(x), len(y), len(ySEM), len(xLabels), len(dose), len(N), len(doseSEM))

        fig, ax1 = plt.subplots()

        ax1.spines['top'].set_color('none')
        ax1.spines['bottom'].set_color('blue')
        ax1.spines['left'].set_color('blue')
        ax1.spines['right'].set_color('none')
                 
        ax1.errorbar(x, dose, doseSEM, marker = 'o', color = 'black', ecolor = 'red')
        plt.margins(0.1)    # Pad margins so that markers don't get clipped by the axes       
        plt.subplots_adjust(bottom = 0.15)  # Tweak spacing to prevent clipping of tick-labels
        plt.title('Figure 2')

        # ****** Top spine ******
        ax1.spines['top'].set_position(('axes', 1.02))    # Offset the axis 0.02 to left of zero
        #ax1.spines['top'].set_color('none')
        
        # ****** x Axis *********
        plt.xlabel('Trial Response Ratio', fontsize = 14)
        ax1.set_xlim(0, 24)         
        majorLocator = MultipleLocator(1)
        ax1.xaxis.set_major_locator(majorLocator)
        ax1.spines['bottom'].set_position(('axes', -0.02))  # Offset X axis down 0.02        
        ax1.spines['bottom'].set_bounds(1, 23)              # Only draw spine between the y-ticks
        
        # ****** Left Axis *******
        plt.ylabel('Dose (mg)', fontsize = 14)        
        ax1.set_ylim(0, 1.0)      
        majorLocator = MultipleLocator(0.25)
        ax1.yaxis.set_major_locator(majorLocator)
        ax1.spines['left'].set_position(('axes', 0.0))    # Offset the axis 0.02 to left of zero

        #ax1.spines['left'].set_color('none')
        ax1.set_xticklabels(xLabels, rotation= 270.0)  # Or rotation = "vertical'

        # ************* Survival Curve ***************************
        ax2 = ax1.twinx()
        ax2.spines['top'].set_color('red')
        ax2.spines['bottom'].set_color('none')
        ax2.spines['left'].set_color('none')
        ax2.spines['right'].set_color('red')
        
        ax2.plot(x, N, color= 'blue')       # Simple Plot - no SEMs
        ax2.set_ylabel('Nunber of Subjects Reaching Ratio', fontsize = 14)  
        ax2.set_ylim(0, 30)
        ax2.spines['right'].set_position(('axes', 1.0))    # Offset the axis 0.02 to the right

        #ax.text(0.1, 0.1, 'test text', horizontalalignment='center', \
        #verticalalignment='center', transform=ax.transAxes)
        
        plt.show()
           
    def figure3(self,arg):
        """
        Draw figure 3 for 2L-PR paper
        Effect of access time (1 - 180 sec) on Breakpoint and cocaine intake
        """
        
        #**************  Data from Figure3_Final.xlxs ***********************
        x = [1,2,4,8,15,30,60,120,180]
        BP = [8.41, 12.26, 15.67, 16.31, 16.77, 17.09, 17.31, 16.89, 17.49]
        BP_SEM = [0.99, 1.18, 1.40, 0.87, 1.03, 1.10, 1.24, 1.32, 1.34]

        Intake = [0.12, 1.12, 3.23, 4.29, 5.80, 6.52, 6.72, 8.13, 8.99]
        Intake_SEM = [0.06, 0.26, 0.54, 0.42, 0.97, 1.15, 0.93, 1.17, 1.01] 
        
        #************** Break Point Plot ************************************
        """
        '1','2','4','6','9','12','15','20','25','32','40','50','62','77','95','118',
        '145','178','219','268','328','402', '492', '603'
        """
        
        BP_labels = ['15','20','25','32','40','50','62','77','95','118','145','178','219','268','328','402', '492']  # 603...
       
        fig, ax1 = plt.subplots()
        ax1.errorbar(x, BP, BP_SEM, marker = 'o', color = 'black', ecolor = 'red')
        ax1.spines['top'].set_color('black')
        ax1.spines['bottom'].set_color('black')
        ax1.spines['left'].set_color('black')
        ax1.spines['right'].set_color('none')

        # ***** X-axis *******
        plt.xlabel('Trial Duration (sec)', fontsize = 14)       
        ax1.set_xlim(0, 182)
        majorLocator = MultipleLocator(30)
        ax1.xaxis.set_major_locator(majorLocator)

        # ***** Left axis *****
        plt.ylabel('Final Ratio', fontsize = 14)        
        ax1.set_ylim(7, 20)
        ax1.spines['left'].set_position(('axes', - 0.02))    # Offset the axis 0.02 to the left
        majorLocator = MultipleLocator(1)
        ax1.yaxis.set_major_locator(majorLocator)
        ax1.set_yticklabels(BP_labels, rotation= 0.0)  # Or rotation = "vertical'
        
        # ************* 
        ax2 = ax1.twinx()
        ax2.spines['top'].set_color('none')
        ax2.spines['bottom'].set_color('none')
        ax2.spines['left'].set_color('none')
        ax2.spines['right'].set_color('black')
        ax2.errorbar(x, Intake, Intake_SEM, marker = 'o', color = 'blue', ecolor = 'blue')
        ax2.set_ylabel('Cocaine Intake (mg)', fontsize = 14)  
        ax2.set_ylim(0, 12)
        ax2.spines['right'].set_position(('axes', 1.02))    # Offset the axis 0.02 to the right

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
