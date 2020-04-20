
"""
April 15, 2020

Move Test Model and Axes Example to GraphsTab.py

Rename "Test Area" to 2L-PR

"""

from tkinter import *
from tkinter.ttk import Notebook
from tkinter import filedialog
from datetime import datetime
import DataModel as dm
import GraphsTab as gt
import TestArea as ta
import stream01
import math
import os
import GraphLib
import model
import Examples
import numpy as np
import ListLib

from scipy.optimize import curve_fit
from scipy.stats.stats import pearsonr

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.lines import Line2D
from matplotlib.figure import Figure
import matplotlib.patches as patches
import matplotlib.lines as lines
from matplotlib import gridspec
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, MaxNLocator, FormatStrFormatter, AutoMinorLocator)
import matplotlib.ticker as ticker

"""
Models, Views and Controllers (MCV) design: keep the representation of the data separate
from the parts of the program that the user interacts with.

View: displays information to the user (Graphical User Interface (tkinter and graphs)

Models: store and retrieve data from databases and files.
Controllers: convert user input into calls on functions that manipulate data
"""

def main(argv=None):
    if argv is None:
        argv = sys.argv
    gui = myGUI()
    gui.go()
    return 0


class myGUI(object):
    def __init__(self):
        """
        This object controls all aspects of the Graphical User Interface:
        It uses the Tk tookkit imported from tkinter.
        "root" is the base level; all other frames and widgets are in relation to "root".

        Note that widgets can be called from Tk or ttk. Here the default is to Tk widgets. 

        """
        self.version = "Analysis"
        self.root = Tk()
        self.root.title(self.version)
        canvas_width = 800
        canvas_height = 600
        self.initialDir = ""
        if (os.name == "posix"):
            self.initialDir = "/Users/daveroberts/Documents"
        else:
            self.initialDir = "C:/"
        print("Initial Directory:", self.initialDir)

        # **********************************************************************
        # *********   Variables and Lists associated with the View     *********
        # **********************************************************************
        
        #Construct ten empty dataRecords
        self.record0 = dm.DataRecord([],"empty")   #Data Record defined in DataModel.py      
        self.record1 = dm.DataRecord([],"empty")
        self.record2 = dm.DataRecord([],"empty")
        self.record3 = dm.DataRecord([],"empty")
        self.record4 = dm.DataRecord([],"empty")
        self.record5 = dm.DataRecord([],"empty")
        self.record6 = dm.DataRecord([],"empty")
        self.record7 = dm.DataRecord([],"empty")
        self.record8 = dm.DataRecord([],"empty")
        self.record9 = dm.DataRecord([],"empty")
        
        # Create a list of these dataRecords so that one can be "selected" with self.fileChoice.get()
        self.recordList = [self.record0,self.record1,self.record2,self.record3,self.record4, \
                           self.record5,self.record6,self.record7,self.record8,self.record9]

        # Header row
        self.showOn_tkCanvas = BooleanVar(value = True) # Either tk Canvas or pyplot
        self.clockTimeStringVar = StringVar(value="0:00:00")
        
        self.fileChoice = IntVar(value=0)
        self.fileName0 = StringVar(value = self.recordList[0].fileName)
        self.fileName1 = StringVar(value = self.recordList[1].fileName)
        self.fileName2 = StringVar(value = self.recordList[2].fileName)
        self.fileName3 = StringVar(value = self.recordList[3].fileName)
        self.fileName4 = StringVar(value = self.recordList[4].fileName)
        self.fileName5 = StringVar(value = self.recordList[5].fileName)
        self.fileName6 = StringVar(value = self.recordList[6].fileName)
        self.fileName7 = StringVar(value = self.recordList[7].fileName)
        self.fileName8 = StringVar(value = self.recordList[8].fileName)
        self.fileName9 = StringVar(value = self.recordList[9].fileName)
        
        self.fileNameList = [self.fileName0,self.fileName1,self.fileName2,self.fileName3,self.fileName4,\
                             self.fileName5,self.fileName6,self.fileName7,self.fileName8,self.fileName9]

        # Graphs Tab
        self.showBPVar = BooleanVar(value = True)
        self.max_x_scale = IntVar(value=360)
        self.max_y_scale = IntVar(value=500)

        # Threshold stuff
        self.printReportVar = BooleanVar(value = True)
        self.pumpTimes = IntVar()                           # Use OMNI or M0 pumptimes
        self.pumpTimes.set(0)                               # Default to OMNI pumptimes
        self.logXVar = BooleanVar(value = True) 
        self.logYVar = BooleanVar(value = True)
        self.showPmaxLine = BooleanVar(value = True)
        self.showOmaxLine = BooleanVar(value = True)
        self.manualCurveFitVar = BooleanVar(value = False)
        self.QzeroVar = DoubleVar()                         # Qzero
        self.alphaVar = DoubleVar()                         # alpha
        self.k_Var = DoubleVar(value=3.0)                   # k 
        self.rangeBegin = IntVar()                          # First Point
        self.rangeBegin.set(1)
        self.rangeEnd = IntVar()                            # Last Point
        self.rangeEnd.set(11)
        self.responseCurveVar = BooleanVar(value = True)    # Show Response Curve
        self.respMax = IntVar()
        self.respMax.set(200)
        self.average_TH_FilesVar = BooleanVar(value=False)  # Not associated with widget

        # Text Tab
        self.startTimeVar = IntVar()                        # Associated with startTimeScale, initialized to zero       
        self.endTimeVar = IntVar()                          # Associated with endTimeScale, initialized to 360
        self.drugConcStr = StringVar(value="5.0")
        self.weightStr = StringVar(value="350")

        # Test Area Tab
        self.leverCount = IntVar()                          # Associated with L1Button & L2Button
        self.leverCount.set(2)      

        # ******************************************************************************
        # **************************         Root Frame            *********************
        # ******************************************************************************
        
        self.rootFrame = Frame(self.root, borderwidth=2, relief="sunken")
        self.rootFrame.grid(column = 0, row = 0)
        headerFrame= Frame(self.root,borderwidth=2, relief="sunken")
        headerFrame.grid(row=0,column=0,sticky=EW)
        fileSelectorFrame = Frame(self.root, borderwidth=2, relief="sunken")
        fileSelectorFrame.grid(row=1,column=0,sticky=NSEW)        
        noteBookFrame = Frame(self.root, borderwidth=2, relief="sunken")
        noteBookFrame.grid(row=2,column=0)
        myNotebook = Notebook(noteBookFrame)
        self.graphTab = Frame(myNotebook)
        self.thresholdTab = Frame(myNotebook)
        self.textTab = Frame(myNotebook)
        self.testAreaTab = Frame(myNotebook)
        myNotebook.add(self.graphTab,text = "Graphs")
        myNotebook.add(self.thresholdTab,text = "Threshold")
        myNotebook.add(self.textTab,text = "Text")
        myNotebook.add(self.testAreaTab,text = "Test Area")
        myNotebook.grid(row=0,column=0)

        # **************      Header Row    ******************      
        openFilesButton = Button(headerFrame, text="Open Files", command= lambda: self.openWakeFiles("")).grid(row=0,column=0, sticky=W)        
        spacer1Label = Label(headerFrame, text="               ").grid(row=0,column=1)
        clockTimeLabel = Label(headerFrame, textvariable = self.clockTimeStringVar).grid(row = 0, column=2)
        spacer2Label = Label(headerFrame, text="               ").grid(row=0,column=3)
        loadTestButton1 = Button(headerFrame, text="1L_PR.str", command= lambda: \
                              self.openWakeFiles("1L_PR.str")).grid(row=0,column=4,sticky=N, padx = 20)
        loadTestButton2 = Button(headerFrame, text="TH_FEATHER.dat", command= lambda: \
                              self.openWakeFiles("TH_FEATHER.dat")).grid(row=0,column=5,sticky=N, padx = 20)
        loadTestButton3 = Button(headerFrame, text="TH_OMNI1.str", command= lambda: \
                              self.openWakeFiles("TH_OMNI1.str")).grid(row=0,column=6,sticky=N, padx = 20)
        loadTestButton4 = Button(headerFrame, text="2L-PR-HD1.str", command= lambda: \
                              self.openWakeFiles("2L-PR-HD1.str")).grid(row=0,column=7,sticky=N, padx = 20)
        
        spacer2Label = Label(headerFrame, text="                    ").grid(row = 0,column = 8)
        canvasButton = Radiobutton(headerFrame, text = "tk Canvas", variable = self.showOn_tkCanvas, value = 1).grid(row = 0, column = 9, sticky = E)
        pyplotButton = Radiobutton(headerFrame, text = "pyplot ", variable = self.showOn_tkCanvas, value = 0).grid(row = 0, column = 10, sticky = E)

        #*************** FileSelectorFrame stuff ****************
        padding = 20
        radiobutton1 = Radiobutton(fileSelectorFrame, textvariable = self.fileName0, variable = self.fileChoice, \
                                   value = 0, command =lambda: self.selectList()).grid(column=0, row=2, padx=padding)
        radiobutton2 = Radiobutton(fileSelectorFrame, textvariable = self.fileName1, variable = self.fileChoice, \
                                   value = 1, command =lambda: self.selectList()).grid(column=1, row=2,padx=padding)
        radiobutton3 = Radiobutton(fileSelectorFrame, textvariable = self.fileName2, variable = self.fileChoice, \
                                   value = 2, command =lambda: self.selectList()).grid(column=2, row=2,padx=padding)
        radiobutton4 = Radiobutton(fileSelectorFrame, textvariable = self.fileName3, variable = self.fileChoice, \
                                   value = 3, command =lambda: self.selectList()).grid(column=3, row=2,padx=padding)
        radiobutton5 = Radiobutton(fileSelectorFrame, textvariable = self.fileName4, variable = self.fileChoice, \
                                   value = 4, command =lambda: self.selectList()).grid(column=4, row=2,padx=padding)
        radiobutton6 = Radiobutton(fileSelectorFrame, textvariable = self.fileName5, variable = self.fileChoice, \
                                   value = 5, command =lambda: self.selectList()).grid(column=0, row=3,padx=padding)
        radiobutton7 = Radiobutton(fileSelectorFrame, textvariable = self.fileName6, variable = self.fileChoice, \
                                   value = 6, command =lambda: self.selectList()).grid(column=1, row=3,padx=padding)
        radiobutton8 = Radiobutton(fileSelectorFrame, textvariable = self.fileName7, variable = self.fileChoice, \
                                   value = 7, command =lambda: self.selectList()).grid(column=2, row=3,padx=padding)
        radiobutton9 = Radiobutton(fileSelectorFrame, textvariable = self.fileName8, variable = self.fileChoice, \
                                   value = 8, command =lambda: self.selectList()).grid(column=3, row=3,padx=padding)
        radiobutton10 = Radiobutton(fileSelectorFrame, textvariable = self.fileName9, variable = self.fileChoice, \
                                   value = 9, command =lambda: self.selectList()).grid(column=4, row=3,padx=padding)


        # *************************************************************
        # **************        Graph Tab     *************************
        # *************************************************************
        
        self.columnFrame = Frame(self.graphTab, borderwidth=2, relief="sunken")
        self.columnFrame.grid(column = 0, row = 0, columnspan= 1, sticky=NS)
        
        self.graphButtonFrame = Frame(self.columnFrame, borderwidth=2, relief="sunken")
        self.graphButtonFrame.grid(column = 0, row = 0, sticky=N)
        clearCanvasButton = Button(self.graphButtonFrame, text="Clear", command= lambda: \
                            self.clearGraphTabCanvas()).grid(row=0,column=0,sticky=N)
        cumRecButton = Button(self.graphButtonFrame, text="cumulativeRecord()", command= lambda: \
            self.cumulativeRecord()).grid(row=2,column=0,sticky=N)
        showBPButton = Checkbutton(self.graphButtonFrame, text = "show BP", variable = self.showBPVar, onvalue = True, offvalue = False, \
            command= lambda:self.cumulativeRecord()).grid(row = 3,column=0)
        eventRecButton = Button(self.graphButtonFrame, text="eventRecords()", command= lambda: \
                              self.eventRecords()).grid(row=4,column=0,sticky=N)
        timeStampButton = Button(self.graphButtonFrame, text="timeStamps()", command= lambda: \
                              self.timeStamps()).grid(row=5,column=0,sticky=N)       
        modelButton = Button(self.graphButtonFrame, text="cocaineModel()", command= lambda: \
                              self.cocaineModel()).grid(row=6,column=0,sticky=N)
        histogramButton = Button(self.graphButtonFrame, text="histogram()", command= lambda: \
                              self.histogram()).grid(row=7,column=0,sticky=N)

        # ******  IntA Frame ************
        self.graph_IntA_frame = Frame(self.columnFrame, borderwidth=2, relief="sunken")
        self.graph_IntA_frame.grid(column = 0, row = 1)
        IntA_frame_lable = Label(self.graph_IntA_frame, text = "IntA").grid(row = 0, column=0)
        IntA_event_button = Button(self.graph_IntA_frame, text="eventRecordsIntA()", command= lambda: \
            self.eventRecordsIntA()).grid(row=1,column=0,sticky=N)
        IntA_durations_button = Button(self.graph_IntA_frame, text="pumpDurationsIntA()", command= lambda: \
            self.pumpDurationsIntA()).grid(row=2,column=0,sticky=N)        
        IntA_histogram_block_Button = Button(self.graph_IntA_frame, text="Histogram (blocks)", command= lambda: \
            self.IntAHistogram_blocks()).grid(row=3,column=0,sticky=N)
        IntA_histogram_all_Button = Button(self.graph_IntA_frame, text="Histogram (All)", command= lambda: \
            self.IntAHistogram_all()).grid(row=4,column=0,sticky=N)

        # ******  2L - PR Frame *********
        self.graph_2LPR_frame = Frame(self.columnFrame, borderwidth=2, relief="sunken")
        self.graph_2LPR_frame.grid(column = 0, row = 2)
        TwoLever_frame_lable = Label(self.graph_2LPR_frame, text = "2L-PR").grid(row = 0, column=0)
        TwoLever_CR_button = Button(self.graph_2LPR_frame, text="Cum Rec", command= lambda: \
            self.TwoLeverCR()).grid(row=1,column=0,sticky=N)
        TwoLever_Test2_button = Button(self.graph_2LPR_frame, text="Test 1", command= lambda: \
            self.TwoLeverGraphTest1()).grid(row=2,column=0,sticky=N)

        # ******  Example Frame *********
        self.graph_example_frame = Frame(self.columnFrame, borderwidth=2, relief="sunken")
        self.graph_example_frame.grid(column = 0, row = 3)
        example_frame_lable = Label(self.graph_example_frame, text = "Examples").grid(row = 0, column=0)
        model_example_button = Button(self.graph_example_frame, text="Test Model", command= lambda: \
                self.testModel()).grid(row=1,column=0,sticky=N)
        axes_example_button = Button(self.graph_example_frame, text="Axes", command= lambda: \
                              self.test()).grid(row=2,column=0,sticky=N)

        # ******* Y axis frame *********
        self.graph_YaxisRadioButtonFrame = Frame(self.columnFrame, borderwidth=2, relief="sunken")
        self.graph_YaxisRadioButtonFrame.grid(column = 0, row = 4)
        y_axisButtonLabel = Label(self.graph_YaxisRadioButtonFrame, text = "Y axis").grid(row = 0, column=0)
        y_scaleRadiobutton250 = Radiobutton(self.graph_YaxisRadioButtonFrame, text="250", variable=self.max_y_scale, value=250)
        y_scaleRadiobutton250.grid(column = 0, row = 1)
        y_scaleRadiobutton500 = Radiobutton(self.graph_YaxisRadioButtonFrame, text="500", variable=self.max_y_scale, value=500)
        y_scaleRadiobutton500.grid(column = 0, row = 2)
        y_scaleRadiobutton1000 = Radiobutton(self.graph_YaxisRadioButtonFrame, text="1000", variable=self.max_y_scale, value=1000)
        y_scaleRadiobutton1000.grid(column = 0, row = 3)
        y_scaleRadiobutton1500 = Radiobutton(self.graph_YaxisRadioButtonFrame, text="1500", variable=self.max_y_scale, value=1500)
        y_scaleRadiobutton1500.grid(column = 0, row = 4)
        
        # *************************************
        
        self.graph_XaxisRadioButtonFrame = Frame(self.graphTab, borderwidth=2, relief="sunken")
        self.graph_XaxisRadioButtonFrame.grid(column = 1, row = 1, sticky=EW)
        x_axisButtonLabel = Label(self.graph_XaxisRadioButtonFrame, text = "X axis").grid(row = 0, column=0)

        x_scaleRadiobutton10 = Radiobutton(self.graph_XaxisRadioButtonFrame, text="10", variable=self.max_x_scale, value=10)
        x_scaleRadiobutton10.grid(column = 1, row = 0)
        x_scaleRadiobutton30 = Radiobutton(self.graph_XaxisRadioButtonFrame, text="30", variable=self.max_x_scale, value=30)
        x_scaleRadiobutton30.grid(column = 2, row = 0)
        x_scaleRadiobutton60 = Radiobutton(self.graph_XaxisRadioButtonFrame, text="60", variable=self.max_x_scale, value=60)
        x_scaleRadiobutton60.grid(column = 3, row = 0)
        x_scaleRadiobutton120 = Radiobutton(self.graph_XaxisRadioButtonFrame, text="120", variable=self.max_x_scale, value=120)
        x_scaleRadiobutton120.grid(column = 4, row = 0)
        x_scaleRadiobutton180 = Radiobutton(self.graph_XaxisRadioButtonFrame, text="180", variable=self.max_x_scale, value=180)
        x_scaleRadiobutton180.grid(column = 5, row = 0)
        x_scaleRadiobutton360 = Radiobutton(self.graph_XaxisRadioButtonFrame, text="360", variable=self.max_x_scale, value=360)
        x_scaleRadiobutton360.grid(column = 6, row = 0)
        x_scaleRadiobutton720 = Radiobutton(self.graph_XaxisRadioButtonFrame, text="720", variable=self.max_x_scale, value=720)
        x_scaleRadiobutton720.grid(column = 7, row = 0)
        
        self.graphCanvasFrame = Frame(self.graphTab, borderwidth=2, relief="sunken")
        self.graphCanvasFrame.grid(column = 1, row = 0)
        self.graphCanvas = Canvas(self.graphCanvasFrame, width = canvas_width, height = canvas_height)
        self.graphCanvas.grid(row=0,column=0)
        self.graphCanvas.create_text(100,10,text = "Graph Canvas")


        # *****************************************************************
        # **************        Threshold Tab     *************************
        # *****************************************************************

        # Two subframes:        
        #
        # Column 0
        # thresholdButtonFrame
        #       lots of widgets
        #       Draw Demand Curve/ Clear Canvas/ OMNI vs M0 etc 
        #   drawThresholdFrame
        #       more widgets
        #       Qzero / alpha / k
        #       firstPointFrame
        #          1 2 3 4
        #          9 10 11 12
        #       Save Figure
        #       testStuff2() testStuff3()
        #       responseButtonFrame
        #          Show Response Curve
        #           25 50 100 200
        #
        # Column 1
        # TH_FigureFrame    - tk container
        #      self.tkCanvas     - drawing space for things loke event records
        #      self.matPlotCanvas - container for the MatPlotLib Figure
        #      self.figure       - the thing that axes and lines are drawn on

        self.thresholdButtonFrame = Frame(self.thresholdTab, borderwidth=2, relief="sunken")
        self.thresholdButtonFrame.grid(column = 0, row = 0, sticky=N)

        self.thresholdFigureFrame = Frame(self.thresholdTab, borderwidth=2, relief="sunken")
        self.thresholdFigureFrame.grid(column = 1, row = 0, sticky=N)


        #************** Threshold Button Frame *****
        
        clearTHCanvasButton = Button(self.thresholdButtonFrame, text="Clear Canvas", \
                                     command = lambda: self.clearFigure()).grid(row=0,column=0, columnspan = 2, sticky = EW)
        thresholdButton = Button(self.thresholdButtonFrame, text="Draw Demand Curve", command= lambda: \
                                 self.drawThreshold()).grid(row=1,column=0,columnspan = 2)
        CreateReportButton = Checkbutton(self.thresholdButtonFrame, text = "Print Report", variable = self.printReportVar, \
                                 onvalue = True, offvalue = False).grid(row = 2, column = 0, sticky = W)
        pumpTimeLabel = Label(self.thresholdButtonFrame, text = "Pump Times").grid(row=3,column=0,sticky=W)
        pumpTimesOMNI = Radiobutton(self.thresholdButtonFrame, text = "OMNI", variable = self.pumpTimes, value = 0).grid(row =4,column = 0, sticky = W)
        pumpTimesM0 = Radiobutton(self.thresholdButtonFrame, text = "M0 ", variable = self.pumpTimes, value = 1).grid(row = 5,column = 0, sticky = W)

        # **********  k slider *********************
        self.kFrame = Frame(self.thresholdButtonFrame, borderwidth=2, relief="sunken")
        self.kFrame.grid(row = 6, column = 0, columnspan=2, sticky=EW)
        k_Label = Label(self.kFrame, text = "k = ").grid(row=0,column=0,sticky=W)
        self.scale_k = Scale(self.kFrame, orient=HORIZONTAL, length=150, resolution = 0.1, \
                                 from_= 0.0, to = 9.9, variable = self.k_Var)
        self.scale_k.grid(row=0,column=1, columnspan = 1,stick = W)

        # ********* Log Buttons ******************
        logLogXCheckButton = Checkbutton(self.thresholdButtonFrame, text = "Log X", variable = self.logXVar, \
                                        onvalue = True, offvalue = False).grid(row = 7, column = 0, sticky = W)
        logLogYCheckButton = Checkbutton(self.thresholdButtonFrame, text = "Log Y", variable = self.logYVar, \
                                        onvalue = True, offvalue = False).grid(row = 8, column = 0, sticky = W)        
        showPmaxCheckButton = Checkbutton(self.thresholdButtonFrame, text = "Show Pmax line", variable = self.showPmaxLine, \
                                        onvalue = True, offvalue = False).grid(row = 9, column = 0, stick = W)
        showOmaxCheckButton = Checkbutton(self.thresholdButtonFrame, text = "Show Omax line", variable = self.showOmaxLine, \
                                        onvalue = True, offvalue = False).grid(row = 10, column = 0, sticky = W)

        # ********* Start / Stop Buttons ********
        self.startStopFrame = Frame(self.thresholdButtonFrame, borderwidth=2, relief="sunken")
        self.startStopFrame.grid(row = 11, column = 0, columnspan=2, sticky=EW)
        
        self.firstPointFrame = Frame(self.startStopFrame, borderwidth=2, relief="sunken")
        self.firstPointFrame.grid(row = 0, column = 0, sticky=W)
        
        rangeBeginLable = Label(self.firstPointFrame, text="First Point").grid(row=0,column=0, sticky=N)
        cumRecButton1 = Radiobutton(self.firstPointFrame, text = "1   ", variable= self.rangeBegin, value = 0).grid(row=1,column=0)
        cumRecButton2 = Radiobutton(self.firstPointFrame, text = "2  ", variable=  self.rangeBegin, value = 1).grid(row=2,column=0)
        cumRecButton3 = Radiobutton(self.firstPointFrame, text = "3  ", variable=  self.rangeBegin, value = 2).grid(row=3,column=0)
        cumRecButton4 = Radiobutton(self.firstPointFrame, text = "4  ", variable=  self.rangeBegin, value = 3).grid(row=4,column=0)

        self.lastPointFrame = Frame(self.startStopFrame, borderwidth=2, relief="sunken")
        self.lastPointFrame.grid(row = 0, column = 1, sticky=E)
        
        rangeEndLable = Label(self.lastPointFrame, text="Last Point").grid(row=0,column=0, sticky=N)
        cumRecButton1 = Radiobutton(self.lastPointFrame, text = "9   ", variable= self.rangeEnd, value = 8).grid(row=1,column=0)
        cumRecButton2 = Radiobutton(self.lastPointFrame, text = "10  ", variable= self.rangeEnd, value = 9).grid(row=2,column=0)
        cumRecButton3 = Radiobutton(self.lastPointFrame, text = "11  ", variable= self.rangeEnd, value = 10).grid(row=3,column=0)
        cumRecButton4 = Radiobutton(self.lastPointFrame, text = "12  ", variable= self.rangeEnd, value = 11).grid(row=4,column=0)

        # Responses Curve ***********************
        responseButtonFrame = Frame(self.thresholdButtonFrame, borderwidth=2, relief="sunken")
        responseButtonFrame.grid(row = 12, column = 0, sticky = EW)
        responseCurveCheckButton = Checkbutton(responseButtonFrame, text = "Show Response Curve", variable = self.responseCurveVar, \
                                        onvalue = True, offvalue = False).grid(row = 0, column = 0, columnspan = 2)
        respMaxLable = Label(responseButtonFrame, text="Responses (Y Scale)").grid(row=1,column = 0, columnspan = 2, sticky=(N))
        respMaxButton1 = Radiobutton(responseButtonFrame, text = "25   ", variable=self.respMax, value = 25).grid(row=2,column=0)
        respMaxButton2 = Radiobutton(responseButtonFrame, text = "50   ", variable=self.respMax, value = 50).grid(row=3,column=0)
        respMaxButton3 = Radiobutton(responseButtonFrame, text = "100   ", variable=self.respMax, value = 100).grid(row=2,column=1)
        respMaxButton4 = Radiobutton(responseButtonFrame, text = "200   ", variable=self.respMax, value = 200).grid(row=3,column=1)

        
        test2Button = Button(self.thresholdButtonFrame, text="Save Figure.png", command= lambda: \
                             self.save_TH_Figure()).grid(row=13,column=0,sticky=S)
        test3Button = Button(self.thresholdButtonFrame, text="testStuff2()", command= lambda: \
                             self.testStuff2()).grid(row=14,column=0,sticky=S)
        test4Button = Button(self.thresholdButtonFrame, text="testStuff3()", command = lambda: \
                             self.testStuff3()).grid(row=15,column=0,sticky=N)

        #************* drawThresholdFrame within thresholdButtonFrame ********       
        self.manualFrame = Frame(self.thresholdButtonFrame, borderwidth=2, relief="sunken")
        self.manualFrame.grid(row = 16, column = 0, columnspan = 1, sticky = EW)
                
        curveFitCheckButton = Checkbutton(self.manualFrame, text = "Manual Curve Fit", \
                    variable = self.manualCurveFitVar, onvalue = True, \
                    offvalue = False).grid(row = 0, column = 0, columnspan = 2, stick=W)

        self.QzeroLabel = Label(self.manualFrame, text = "Qzero").grid(row=1,column=0,sticky=EW)
        self.alphaLabel = Label(self.manualFrame, text = "alpha").grid(row=1,column=1,sticky=EW)        
        self.scale_Q_zero = Scale(self.manualFrame, orient=HORIZONTAL, length=150, resolution = 0.05, \
                                  from_=0.25, to=5.0, variable = self.QzeroVar)
        self.scale_Q_zero.grid(row=2,column=0, columnspan = 1)
        self.scale_Q_zero.set(1.0)
        self.scale_alpha = Scale(self.manualFrame, orient=HORIZONTAL, length=150, resolution = 0.00025, \
                                 from_= 0.0005, to = 0.02, variable = self.alphaVar)
        self.scale_alpha.grid(row=2,column=1, columnspan = 1)
        self.scale_alpha.set(0.005)
        

        #****************

        # TH_FigureFrame    - tk container (a Frame)
        #      self.matPlotFigure              - the thing that axes and lines are drawn on        
        #      self.threshold_matPlot_Canvas    - container for the MatPlotLib Figure
        #                                       - This is the thing that gets redrawn after things are changed.

        self.matPlotFigure = Figure(figsize=(7,8), dpi=80)
        
        self.threshold_matPlot_Canvas = FigureCanvasTkAgg(self.matPlotFigure, master=self.thresholdFigureFrame)
        self.threshold_matPlot_Canvas.get_tk_widget().grid(row=0,column=0)

        #*************** Text Tab *****************
         
        self.textButtonFrame = Frame(self.textTab, borderwidth=5, relief="sunken")
        self.textButtonFrame.grid(column = 0, row = 0, sticky=N)

        self.textBox = Text(self.textTab, width=100, height=43)
        self.textBox.grid(column = 1, row = 0, rowspan = 2)
        
        cleartextButton = Button(self.textButtonFrame, text="Clear", command= lambda: \
                              self.clearText()).grid(row=0,column=0,columnspan = 2,sticky=N)
        summarytextButton = Button(self.textButtonFrame, text="Summary", command= lambda: \
                              self.summaryText()).grid(row=1,column=0,columnspan = 2,sticky=N)
        injectionTimesButton = Button(self.textButtonFrame, text="Injection Times", command= lambda: \
                              self.injectionTimesText()).grid(row=2,column=0,columnspan = 2,sticky=N)        

        pyPlotEventButton = Button(self.textButtonFrame, text="PyPlot Event Record", command= lambda: \
                              self.pyPlotEventRecord()).grid(row=3,column=0,columnspan=2,sticky=N)

        doseReportButton = Button(self.textButtonFrame, text="Dose Report", command= lambda: \
                              self.doseReport()).grid(row=4,column=0,columnspan = 2,sticky=N)

        self.startTimeLabel = Label(self.textButtonFrame, text = "T1").grid(row=5,column=0,sticky=W)        

        self.startTimeScale = Scale(self.textButtonFrame, orient=HORIZONTAL, length=100, resolution = 5, \
                                  from_=0, to=360, variable = self.startTimeVar)
        self.startTimeScale.grid(row=5,column=1)
        self.startTimeScale.set(0)

        self.endTimeLabel = Label(self.textButtonFrame, text = "T2").grid(row=6,column=0,sticky=W) 

        self.endTimeScale = Scale(self.textButtonFrame, orient=HORIZONTAL, length=100, resolution = 5, \
                                  from_=0, to=360, variable = self.endTimeVar)
        self.endTimeScale.grid(row=6,column=1)
        self.endTimeScale.set(360)
        
        concentrationLabel = Label(self.textButtonFrame, text="Conc (mg/ml)")
        concentrationLabel.grid(row = 7, column = 0)
        
        self.concentrationEntry = Entry(self.textButtonFrame, width=6,textvariable = self.drugConcStr)
        self.concentrationEntry.grid(row = 7, column = 1)

        weightLabel = Label(self.textButtonFrame, text="Body weight (gms)")
        weightLabel.grid(row = 8, column = 0)

        self.weightEntry = Entry(self.textButtonFrame, width=6,textvariable = self.weightStr)
        self.weightEntry.grid(row = 8, column = 1)

        intA_text_button = Button(self.textButtonFrame, text="IntA", command= lambda: \
                              self.intA_text()).grid(row = 9,column = 0, columnspan = 2,sticky=N)
        TH_text_button = Button(self.textButtonFrame, text="Threshold (TH)", command= lambda: \
                              self.threshold_text()).grid(row = 10,column = 0, columnspan = 2,sticky=N)

        #***************** 2L-PR stuff **************
        self.text_2LPR_Frame = Frame(self.textTab, borderwidth=5, relief="sunken")
        self.text_2LPR_Frame.grid(row = 8, column = 0, sticky=(N))
        
        TwoLeverTextButton = Button(self.text_2LPR_Frame, text="2L-PR Summary", command= lambda: \
                              self.TwoLeverTextReport()).grid(row=0,column=0,sticky=W)
        TestButton = Button(self.text_2LPR_Frame, text="TH Test", command= lambda: \
                              self.THTest()).grid(row=1,column=0,sticky=W)
        TwoLeverTest2Button = Button(self.text_2LPR_Frame, text="2L-PR Test2", command= lambda: \
                              self.TwoLeverTest2()).grid(row=3,column=0,sticky="W")
        testText1Button = Button(self.text_2LPR_Frame, text="Text Formatting Examples", command= lambda: \
                              self.testText1()).grid(row=4,column=0,columnspan = 2,sticky=N)

        #**************** Test Area Tab **************
        # Contains testAreaButtonFrame and testAreaFigureFrame
        #
        # testAreaFigureFrame    - tk container (a Frame)
        #      self.matPlotTestFigure              - the thing that axes and lines are drawn on        
        #      self.threshold_tk_Canvas         - drawing space for things like event records
        #      self.testArea_matPlot_Canvas    - container for the MatPlotLib Figure
        #                                       - This is the thing that gets redrawn after things are changed.

        self.testAreaButtonFrame = Frame(self.testAreaTab, borderwidth=5, relief="sunken")
        self.testAreaButtonFrame.grid(column = 0, row = 0, sticky=N)

        self.testAreaFigureFrame = Frame(self.testAreaTab, borderwidth=5, relief="sunken")
        self.testAreaFigureFrame.grid(column = 1, row = 0, sticky=N)
        
        self.matPlotTestFigure = Figure(figsize=(9,8), dpi=80)
        self.matPlotTestFigure.set_edgecolor("white")  #see help(colors)
        self.matPlotTestFigure.set_facecolor("white")  #Set whether the figure frame (background) is displayed or invisible
        self.matPlotTestFigure.set_frameon(True)
        
        self.testArea_MatPlot_Canvas = FigureCanvasTkAgg(self.matPlotTestFigure, master=self.testAreaFigureFrame)
        self.testArea_MatPlot_Canvas.get_tk_widget().grid(row=0,column=0)
        

        Button1 = Button(self.testAreaButtonFrame, text="fig1_2L_PR()", command= lambda: \
                              self.fig1_2L_PR()).grid(row=0,column=0,columnspan=2,sticky=N)
        Button2 = Button(self.testAreaButtonFrame, text="TwoLeverFig()", command= lambda: \
                              self.TwoLeverFig()).grid(row=1,column=0,columnspan=2,sticky=N)
        Button3 = Button(self.testAreaButtonFrame, text="MatPlot Event Record", command= lambda: \
                              self.matPlotEventRecord()).grid(row=3,column=0,columnspan=2, sticky=N)
        Button4 = Button(self.testAreaButtonFrame, text="bin_HD_Records()", command= lambda: \
                              self.bin_HD_Records()).grid(row=4,column=0,columnspan=2, sticky=N)
        Button5 = Button(self.testAreaButtonFrame, text="bin_HD_10SecCount()", command= lambda: \
                              self.bin_HD_10SecCount()).grid(row=5,column=0,columnspan=2, sticky=N)
        Button6 = Button(self.testAreaButtonFrame, text="Load 2L_PR Files", command= lambda: \
                              self.load_2L_PR_Files()).grid(row=6,column=0,columnspan=2,sticky=N)

        L1Button = Radiobutton(self.testAreaButtonFrame, text = "1L", variable = self.leverCount, value = 1).grid(row = 7, column = 0, sticky = E)
        L2Button = Radiobutton(self.testAreaButtonFrame, text = "2L", variable = self.leverCount, value = 2).grid(row = 8, column = 0, sticky = E)
        
        # Button5 = Button(self.testAreaButtonFrame, text="unused", command= lambda: \
        # self.someCommand()).grid(row=5,column=0,columnspan=2,sticky=N)

    # ***************   End of __init__(self)  *************************
   

    # **************   Procedures called from Graphs Tab  *************
    def clearGraphTabCanvas(self):
        self.graphCanvas.delete('all')
        
    def cumulativeRecord(self):
        aCanvas = self.graphCanvas
        aRecord = self.recordList[self.fileChoice.get()]
        showBP = self.showBPVar.get()
        max_x_scale = self.max_x_scale.get()
        max_y_scale = self.max_y_scale.get()    
        gt.cumulativeRecord(aCanvas,aRecord,showBP,max_x_scale,max_y_scale)

    def eventRecords(self):
        aCanvas = self.graphCanvas
        aRecordList = self.recordList
        max_x_scale = self.max_x_scale.get()
        gt.eventRecords(aCanvas,aRecordList,max_x_scale)

    def timeStamps(self):
        aCanvas = self.graphCanvas
        aRecord = self.recordList[self.fileChoice.get()]
        max_x_scale = self.max_x_scale.get()
        gt.timeStamps(aCanvas,aRecord,max_x_scale)

    def cocaineModel(self):
        aCanvas = self.graphCanvas
        aRecord = self.recordList[self.fileChoice.get()]
        max_x_scale = self.max_x_scale.get()
        gt.cocaineModel(aCanvas,aRecord,max_x_scale)

    def histogram(self):
        aCanvas = self.graphCanvas
        aRecord = self.recordList[self.fileChoice.get()]
        max_x_scale = self.max_x_scale.get()
        gt.histogram(aCanvas,aRecord,max_x_scale)

    def eventRecordsIntA(self):
        aCanvas = self.graphCanvas
        aRecord = self.recordList[self.fileChoice.get()]
        gt.eventRecordsIntA(aCanvas,aRecord)

    def pumpDurationsIntA(self):
        aCanvas = self.graphCanvas
        aRecord = self.recordList[self.fileChoice.get()]
        gt.pumpDurationsIntA(aCanvas,aRecord)

    # **************   Procedures called from Threshold Tab  *************


    # **************   Procedures called from Text Tab  *************
        
        
    # **************   Procedures called from Test Area Tab  *************

    def fig1_2L_PR(self):
        """
        This draws Figure 1 for the 2L-PR-HD paper.
        Most of the procedure is in testArea.py but the definition of the Figure is in Analysis

        Can't immediately figure out how to call "draw" or "show" for TestArea.py.
        Might not matter. 

        """
        if (self.showOn_tkCanvas.get()):
            fig = self.matPlotTestFigure    # Previously defined Figure containing matPlotCanvas
            fig.clf()
        else:
            fig = plt.figure(figsize=(6,6), dpi=150, constrained_layout = False)  # Newly instantaited pyplot figure
        recordList = self.recordList
        ta.fig1_2L_PR(fig,recordList)
        if (self.showOn_tkCanvas.get()):
            self.testArea_MatPlot_Canvas.draw()
        else:
            plt.show()

    def TwoLeverFig(self):
        """
        This draws figure for 2L data
        """
        if (self.showOn_tkCanvas.get()):
            fig = self.matPlotTestFigure    # Previously defined Figure containing matPlotCanvas
            fig.clf()
        else:
            fig = plt.figure(figsize=(6,6), dpi=150, constrained_layout = False)  # Newly instantaited pyplot figure
        levers = self.leverCount.get()
        print("Number of Levers =",levers)  # Defaults to Two Lever
        aRecord = self.recordList[self.fileChoice.get()] 
        max_x_scale = self.max_x_scale.get()
        max_y_scale = self.max_y_scale.get()
        
        ta.TwoLeverFig(fig, aRecord, levers,max_x_scale, max_y_scale)

        if (self.showOn_tkCanvas.get()):
            self.testArea_MatPlot_Canvas.draw()
        else:
            plt.show()
            fig.savefig('SavePDFTest.pdf')
        

        


    # *********************************************************************
    
       
    def save_TH_Figure(self):
        """
        None > save a "Figure.png" in current directory.
        This will overwrite current file. Rename if you want to keep it. 

        self.fig is defined in myGUI and used as a container in all pyplot plots.
        This procedure saves the current self.fig to Figure.png
        Changing the extension will change the format:  eg. ".pdf" 

        """
        print("Saving Figure.png")
        self.matPlotFigure.savefig('Figure.png')


    def openWakeFiles(self,filename):
        """
        The procedure will read Wake datafiles that originate either from OMNI (.str) or from the
        Feather system (.dat).  If a filename is passed to this procedure then it will be opened. This
        is how filename Speed Buttons are handled.
        If no filename ("") is passed, then a File Open Dialog is spawned. One or several files can
        be selected and loaded.
        """       
        fileList = []
        fPath = ""
        if filename == "":
            fileList = filedialog.askopenfilenames(initialdir=self.initialDir)
        else:
            fileList.append(filename)
        """
        filenum = 0
        for file in fileList:
            filenum = filenum + 1
            fName = file[file.rfind('/')+1:]
            fPath = file[0:file.rfind('/')+1]
            print('File ',str(filenum), file)
        self.initialDir = fPath
        print("Path =", self.initialDir)
        """
        selected = self.fileChoice.get()
        for fName in fileList:
            if (selected < 10):
                print("Selection number:",selected)                
                self.recordList[selected].datalist = []
                name = fName[fName.rfind('/')+1:]
                path = fName[0:fName.rfind('/')+1]
                self.initialDir = path
                # print('path =',path)
                self.recordList[selected].fileName = name
                self.fileNameList[selected].set(name)
                # OMNI pump times
                # self.recordList[selected].TH_PumpTimes = [3.162,1.780,1.000,0.562,0.316,0.188, \
                #                                         0.100,0.056,0.031,0.018,0.010,0.0056]
                self.recordList[selected].TH_PumpTimes = [3.160,2.000,1.260,0.790,0.500,0.320, \
                                                          0.200,0.130,0.080,0.050,0.030,0.020]
                self.recordList[selected].cocConc = 5.0
                self.recordList[selected].pumpSpeed = 0.025 # Wake default 0.1 mls/4 sec = 0.025 / sec 
                # textBox.insert('1.0', name+" opened \n\n")
                if fName.find(".str") > 0:
                    self.recordList[selected].datalist = stream01.read_str_file(fName)               
                elif fName.find(".dat") > 0:
                    aFile = open(fName,'r')
                    for line in  aFile:
                        pair = line.split()
                        pair[0] = int(pair[0])
                        self.recordList[selected].datalist.append(pair)
                    aFile.close()
                self.recordList[selected].extractStatsFromList()

                # ------------  fillLists ---------
                verbose = True
                pumpStarttime = 0
                blockNum = -1 
                pumpOn = False
                leverTotal = 0       
                pumpTimeList = [0,0,0,0,0,0,0,0,0,0,0,0]     #Temp list of 12 pairs: price and total pump time
                responseList = [0,0,0,0,0,0,0,0,0,0,0,0]
                """
                This procedure assumes the datafile if a Threshold file and fills the
                response and consumption lists accordingly - i.e. 12 bins.
                But a PR daatfile could have many more bins which could throw an error.
                So for now, if the bin number does not count higher than 11.

                Eventually, 

                """
                for pairs in self.recordList[selected].datalist:
                    if pairs[1] == 'B':
                        if blockNum < 11:
                            blockNum= blockNum + 1
                    elif pairs[1] == 'P':
                        pumpStartTime = pairs[0]
                        pumpOn = True
                        responseList[blockNum] = responseList[blockNum] + 1  # inc Bin_responses
                        leverTotal = leverTotal + 1                        # using pump for responses
                    elif pairs[1] == 'p':
                        if pumpOn:
                            duration = pairs[0]-pumpStartTime
                            if blockNum <= 12:
                                pumpTimeList[blockNum] = pumpTimeList[blockNum] + duration
                            pumpOn = False
                    # else no nothing
                # print("responseList = ", responseList)
                consumptionList = [0,0,0,0,0,0,0,0,0,0,0,0]
                mgPerSec = self.recordList[selected].cocConc * (self.recordList[selected].pumpSpeed * 0.001)
                if verbose:
                    print("Cocaine Conc (mg/ml):", self.recordList[selected].cocConc)
                    print("Pump Speed ( mls/msec):", self.recordList[selected].pumpSpeed)
                    print("cocaine mg/sec:", mgPerSec)
                for i in range(12):
                    consumptionList[i] = pumpTimeList[i] * mgPerSec
                    if consumptionList[i] == 0:
                        consumptionList[i] = 0.01  #so as not to have a zero value that would crash in a log function
                totalResp = 0
                totalIntake = 0
                for i in range(12):
                    totalResp = totalResp + responseList[i]
                    totalIntake = totalIntake + consumptionList[i]
                print('Total Intake = ',totalIntake,';  Total Responses = ',totalResp)
                priceList = []      
                for i in range(12):
                    # dosePerResponse = pumptime(mSec) * mg/ml * ml/sec)
                    dosePerResponse = self.recordList[selected].TH_PumpTimes[i] * \
                                      self.recordList[selected].cocConc * \
                                      (self.recordList[selected].pumpSpeed)
                    price = round(1/dosePerResponse,2)
                    priceList.append(price)
                self.recordList[selected].priceList = priceList
                self.recordList[selected].consumptionList = consumptionList
                self.recordList[selected].responseList = responseList

                # ------------- end fillLists -----------------
                print(self.recordList[selected])
                selected = selected + 1
            else:
                print("More files selected than spots available")
        print("Path =", self.initialDir)


        # **********************  The Controllers  ***********************************
        # Controllers converts user input into calls on functions that manipulate data
        # ****************************************************************************

    def pyPlotEventRecord(self):
        injNum = 0
        injTimeList = []
        
        aRecord = self.recordList[self.fileChoice.get()]
        for pairs in aRecord.datalist:
            if pairs[1] == 'P':                     
                injNum = injNum + 1
                injTimeList.append(pairs[0]/60000)  # Min

        plt.figure(figsize=(9,3))
        plt.subplot(111)
        plt.axis([-0.1,185,0.0,1.0])
        plt.eventplot(injTimeList,lineoffsets = 0, linelengths=1.5)
        plt.show()

    def matPlotEventRecord(self):
        self.matPlotTestFigure.clf()
        gs = gridspec.GridSpec(nrows = 10, ncols= 1)

        injNum = 0
        injTimeList = []
        
        aRecord = self.recordList[self.fileChoice.get()]
        for pairs in aRecord.datalist:
            if pairs[1] == 'P':                     
                injNum = injNum + 1
                injTimeList.append(pairs[0]/60000)  # Min

        self.eventRecord = self.matPlotTestFigure.add_subplot(gs[0,0],label="1")  # row [0] and col [0]]

        self.eventRecord.axes.get_yaxis().set_visible(False)
        
        self.eventRecord.set_ylabel('')
        self.eventRecord.set_yticklabels("")                 # Suppress tick labels
        self.eventRecord.set_xlabel('Time (minutes)')
        self.eventRecord.set_title('Event Records using MatPlotLib.eventplot')
        startTime = self.startTimeScale.get()
        endTime = self.endTimeScale.get()
        self.eventRecord.set_xlim(startTime, endTime) 
        self.eventRecord.set_ylim(0.01, 1)
        self.eventRecord.eventplot(injTimeList,lineoffsets = 0, linelengths=1.5)
        self.testArea_MatPlot_Canvas.draw()

    def bin_HD_Records(self):
        """
        To Do: Presently defaults to 30 second access period. Supply other options. 

        This graph can be rendered either to the tkinter canvas or to a pyplot window
        by selecting the appropriate radio button in the header row. The pyplot window
        can be used to save the graph to a *.prn file.

        This function uses the MatplotLib Object Oriented style. That is, it uses the Figure
        and Axes objects rather than the shorthand plt.* instruction set. 

        B, b = Start and stop of a drug lever block
        P, p = Pump on and off

        This has been checked against "L" and "l" (lever down and up) and it is within a few milliseconds.

        The first trial line is plotted at y = 20 and the subsequent trails are drawn below.
        
        
        """
        
        #from matplotlib.ticker import (MultipleLocator, MaxNLocator, FormatStrFormatter, AutoMinorLocator)

        if (self.showOn_tkCanvas.get()):
            fig = self.matPlotTestFigure                # Previously defined Figure containing matPlotCanvas
            fig.clf()
        else:
            fig = plt.figure(figsize=(9,8), dpi=80, constrained_layout = True)  # Newly instantaited pyplot figure

        ax1 = fig.add_subplot(111,label="1")
        ax1.set_position([0.15, 0.05, 0.7, 0.80])      # Modify this to resize or move it around the canvas

        ax1.text(0.5, 0.93, "Access Time (Seconds)", ha = 'center', fontsize = 14, transform = fig.transFigure)
        
        ax1.xaxis.set_ticks_position('top')             # Put x ticks and labels on the top
        ax1.spines['top'].set_color('black')
        ax1.spines['top'].set
        ax1.xaxis.set_major_locator(MaxNLocator(3))     # Number of x tick intervals
        ax1.xaxis.set_minor_locator(MaxNLocator(30))    # Number of minor tick intervals
        xLabels = ['0','10','20','30']                  # Manually set labels
        ax1.set_xticklabels(xLabels, fontsize = 16)     # and font size

        ax1.spines['top'].set_linewidth(1)              # 0.5 would be very thin
        # x ticks and labels
        ax1.tick_params(axis='x', colors='black', width=2, length = 8, labelcolor = 'black', direction = 'out')
        # minor
        ax1.tick_params(axis='x', which = 'minor', colors='black', width=1, length = 4, direction = 'in')

        ax1.set_yticks([])                              # Suppress tick labels with empty list
     
        ax1.spines['bottom'].set_color('none')          # Make bottom spine disappear
        ax1.spines['left'].set_color('none')            # Make left axis disapear
        ax1.spines['right'].set_color('none')           # Make right spine disapear
               
        ax1.set_xlim(0, 30000)                          # 30 seconds - data are in mSec 
        # Max number of trials
        maxTrials = 26
        ax1.set_ylim(0, maxTrials)                             # (Arbitrarily) graphs a maximum of 20 trials 

        pumpOnTime = 0
        pumpDuration = 0
        trialDuration = 0
        totalPumpTime = 0
        trial = 0
        
        firstLine = 24.5                                # Positioning of the first line
        height = 0.6                                    # Height of event line
        spacing = 1.4                                   # Spacing between lines

        x = [0]                                         # starting x and y coordinates
        y = [firstLine]
        lineY = firstLine                               # This is y value of the line which will change for each trial
        pumpOn = False
        aRecord = self.recordList[self.fileChoice.get()]
        
        for pairs in aRecord.datalist:
            #if len(blockEndList) < 8:                   
                #print(pairs)
                if pairs[1] == 'P':
                    x.append(pairs[0]-startTime)        # Store the x coordinate of pump going on in "bin" time
                    y.append(lineY)                     # Store the y coordinate of start time to 0
                    x.append(pairs[0]-startTime)        # Store the bin time again
                    y.append(lineY+height)              # Set value = 1, this produces an upward line
                    pumpOn = True
                    pumpOnTime = pairs[0]
                elif pairs[1] == 'p':                   # Pump goes off
                    if pumpOn:                          # This ignores "safety" instructions sent while pump is off
                        x.append(pairs[0]-startTime)    # Store the x coordinate of pump going off in "bin" time
                        y.append(lineY+height)          # Store the y coordinate of pump going off at high level
                        x.append(pairs[0]-startTime)    # Store the x coordinate again
                        y.append(lineY)                 # Store the y coordinate at low level - creating a downward line
                        pumpDuration = pairs[0]-pumpOnTime              # Calculate and store pumpDuration
                        trialDuration = trialDuration + pumpDuration
                        totalPumpTime = totalPumpTime + pumpDuration
                        pumpOn = False
                elif pairs[1] == 'B':                   # Drug access period starts
                    startTime = pairs[0]                # Get startTime
                    x = [0]                             # Reset x coordinate to start of line                    
                    lineY = firstLine-(trial*spacing)   # Calculate y coodinate for line - counting down from top
                    y = [lineY]                         # Assign y coordinate
                elif pairs[1] == 'b':                   # Drug access period ends
                    x.append(30000)                     # Assign x coordinate to draw line to end
                    if pumpOn == False:                 # Normally the pump is off
                        y.append(lineY)                 # so assign y coordinate to draw a line to the end
                    else:                               # But if the pump is ON
                        y.append(lineY+height)          # Draw a line to end in up position
                        x.append(30000)                 # Then draw a downward line at the very end
                        y.append(lineY)

                    line1 = Line2D(x,y, color = 'black', ls = 'solid', marker = 'None')
                    ax1.add_line(line1)

                    trial = trial + 1
                    
                    # ax1.transData means it will use the data coordinates
                    # Whereas fig.transFigure would use x/y coordinates based on the entire figure - see Title above
                    # Write trial number to left of line
                    ax1.text(-500, lineY, str(trial), ha = 'right', fontsize = 14, transform=ax1.transData)

                    # Write pump trialDuration to the right of the line
                    ax1.text(35000, lineY, str(trialDuration), ha = 'right', fontsize = 14, transform=ax1.transData)

                    trialDuration = 0

        ax1.text(35000, 26, 'mSec', ha = 'right', fontsize = 14, transform=ax1.transData)
                   
        #print("totalDownTime", totalPumpTime)

        ax1.set_ylabel('Trial Number', fontsize = 16)
        ax1.yaxis.labelpad = 35                  # Move label left or right
            
        if (self.showOn_tkCanvas.get()):
            self.testArea_MatPlot_Canvas.draw()
        else:
            plt.show()

    def bin_HD_10SecCount(self):
        """

        Addition to bin_HD_Records()        
        
        """

        xMax = 180000
        timeSampleSize = 10000                          # 10 sec
        xLabels = ['0','60','120','180']                # Manually set labels 

        #from matplotlib.ticker import (MultipleLocator, MaxNLocator, FormatStrFormatter, AutoMinorLocator)

        if (self.showOn_tkCanvas.get()):
            fig = self.matPlotTestFigure                # Previously defined Figure containing matPlotCanvas
            fig.clf()
        else:
            fig = plt.figure(figsize=(9,8), dpi=80, constrained_layout = True)  # Newly instantaited pyplot figure

        ax1 = fig.add_subplot(111,label="1")
        ax1.set_position([0.15, 0.05, 0.7, 0.80])      # Modify this to resize or move it around the canvas

        ax1.text(0.5, 0.93, "Access Time (Seconds)", ha = 'center', fontsize = 14, transform = fig.transFigure)
        
        ax1.xaxis.set_ticks_position('top')             # Put x ticks and labels on the top
        ax1.spines['top'].set_color('black')
        ax1.spines['top'].set
        ax1.xaxis.set_major_locator(MaxNLocator(3))     # Number of x tick intervals
        ax1.xaxis.set_minor_locator(MaxNLocator(30))    # Number of minor tick intervals

        ax1.set_xticklabels(xLabels, fontsize = 16)     # and font size

        ax1.spines['top'].set_linewidth(1)              # 0.5 would be very thin
        # x ticks and labels
        ax1.tick_params(axis='x', colors='black', width=2, length = 8, labelcolor = 'black', direction = 'out')
        # minor
        ax1.tick_params(axis='x', which = 'minor', colors='black', width=1, length = 4, direction = 'in')

        ax1.set_yticks([])                              # Suppress tick labels with empty list
     
        ax1.spines['bottom'].set_color('none')          # Make bottom spine disappear
        ax1.spines['left'].set_color('none')            # Make left axis disapear
        ax1.spines['right'].set_color('none')           # Make right spine disapear
               
        ax1.set_xlim(0, xMax)                          # 30 seconds - data are in mSec 
        # Max number of trials
        maxTrials = 26
        ax1.set_ylim(0, maxTrials)                             # (Arbitrarily) graphs a maximum of 20 trials 

        pumpOnTime = 0
        pumpDuration = 0
        trialDuration = 0
        totalPumpTime = 0
        trial = 0
        
        firstLine = 24.5                                # Positioning of the first line
        height = 0.6                                    # Height of event line
        spacing = 1.4                                   # Spacing between lines

        x = [0]                                         # starting x and y coordinates
        y = [firstLine]
        lineY = firstLine                               # This is y value of the line which will change for each trial
        pumpOn = False

        sampleTotal = 0
        sampleList = []

        

        aRecord = self.recordList[self.fileChoice.get()]

        testRecord = dm.DataRecord([],"empty")
        """
        Starts at 10 sec
        # bin time 1 sec for 1 sec
        # bin time 4 sec for 1/2 sec
        # bin time 9 sec for 2 sec
        bin time 15 sec for 2 sec 
        Ends at 30 sec
        """

        testRecord.datalist = [[10000, 'B'], \
                            [10500, 'P'], [11500, 'p'], \
                            [14000, 'P'], [14500, 'p'], \
                            [19000, 'P'], [21020, 'p'], \
                            [25000, 'P'], [27000, 'p'], \
                            [40000, 'b'], \
                            [60000, 'B'], \
                            [60500, 'P'], [61500, 'p'], \
                            [64000, 'P'], [64500, 'p'], \
                            [69000, 'P'], [71020, 'p'], \
                            [75000, 'P'], [77000, 'p'], \
                            [90000, 'b']] 
        
        for pairs in aRecord.datalist:
            #if len(blockEndList) < 8:                   
                #print(pairs)
                if pairs[1] == 'P':
                    pumpStartTime = pairs[0]-startTime  # Calculate time of pump going on in "bin" time
                    x.append(pumpStartTime)              # Store binStartTime as x coordinate 
                    y.append(lineY)                     # Store the y coordinate of start time to 0
                    x.append(pairs[0]-startTime)        # Store the bin time again
                    y.append(lineY+height)              # Set value = 1, this produces an upward line
                    pumpOn = True
                    pumpOnTime = pairs[0]
                elif pairs[1] == 'p':                   # Pump goes off
                    if pumpOn:                          # This ignores "safety" instructions sent while pump is off
                        pumpStopTime = pairs[0]-startTime  # Calculate time of pump going off in "bin" time
                        x.append(pumpStopTime)                      # Store binStopTime as x coordinate
                        # Store the x coordinate of pump going off in "bin" time
                        y.append(lineY+height)          # Store the y coordinate of pump going off at high level
                        x.append(pairs[0]-startTime)    # Store the x coordinate again
                        y.append(lineY)                 # Store the y coordinate at low level - creating a downward line
                        pumpDuration = pairs[0]-pumpOnTime              # Calculate and store pumpDuration
                        trialDuration = trialDuration + pumpDuration
                        totalPumpTime = totalPumpTime + pumpDuration
                        # changes to bin_HD_Records
                        if pumpStartTime < timeSampleSize:
                            if pumpStopTime < timeSampleSize:    # Add to total if withing time criteria
                                sampleTotal = sampleTotal + pumpDuration
                            else:
                                timeOver = pumpStopTime - timeSampleSize # Time past criteria
                                sampleTotal = sampleTotal + pumpDuration - timeOver                       
                        pumpOn = False
                elif pairs[1] == 'B':                   # Drug access period starts
                    startTime = pairs[0]                # Get startTime
                    x = [0]                             # Reset x coordinate to start of line                    
                    lineY = firstLine-(trial*spacing)   # Calculate y coodinate for line - counting down from top
                    y = [lineY]                         # Assign y coordinate
                elif pairs[1] == 'b':                   # Drug access period ends
                    x.append(xMax)                     # Assign x coordinate to draw line to end
                    if pumpOn == False:                 # Normally the pump is off
                        y.append(lineY)                 # so assign y coordinate to draw a line to the end
                    else:                               # But if the pump is ON
                        y.append(lineY+height)          # Draw a line to end in up position
                        x.append(xMax)                 # Then draw a downward line at the very end
                        y.append(lineY)

                    line1 = Line2D(x,y, color = 'black', ls = 'solid', marker = 'None')
                    ax1.add_line(line1)

                    sampleList.append(sampleTotal)
                    sampleTotal = 0

                    trial = trial + 1
                    
                    # ax1.transData means it will use the data coordinates
                    # Whereas fig.transFigure would use x/y coordinates based on the entire figure - see Title above
                    # Write trial number to left of line
                    ax1.text(-500, lineY, str(trial), ha = 'right', fontsize = 14, transform=ax1.transData)

                    # Write pump trialDuration to the right of the line
                    ax1.text(xMax+30000, lineY, str(trialDuration), ha = 'right', fontsize = 14, transform=ax1.transData)

                    trialDuration = 0


        if len(sampleList) > 0:
            print("Time Sample Size =", timeSampleSize, "First sample", sampleList[0])
        total = 0
        for i in range(len(sampleList)):
            total = total + sampleList[i]
        print('total:', total) 
        print(sampleList)
            

        # ax1.text(35000, 26, 'mSec', ha = 'right', fontsize = 14, transform=ax1.transData)
                   
        #print("totalDownTime", totalPumpTime)

        ax1.set_ylabel('Trial Number', fontsize = 16)
        ax1.yaxis.labelpad = 35                  # Move label left or right
            
        if (self.showOn_tkCanvas.get()):
            self.testArea_MatPlot_Canvas.draw()
        else:
            plt.show()

    def load_2L_PR_Files(self):
        """
        Load 4 files of subject H383
        8_H383_Mar_10.str  - 1L-FR
        8_H383_Mar_10.str  - 1L-HD
        8_H383_Mar_10.str  - 2L-FR-HD 
        8_H383_Mar_10.str  - 2L-PR-HD
        """
        self.fileChoice.set(0)        
        self.openWakeFiles("/Users/daveroberts/Documents/Two Lever PR/Raw Data/Final/H383/8_H383_Mar_10.str")
        self.fileChoice.set(1)        
        self.openWakeFiles("/Users/daveroberts/Documents/Two Lever PR/Raw Data/Final/H383/8_H383_Mar_11.str")
        self.fileChoice.set(2)        
        self.openWakeFiles("/Users/daveroberts/Documents/Two Lever PR/Raw Data/Final/H383/8_H383_Mar_21.str")
        self.fileChoice.set(3)        
        self.openWakeFiles("/Users/daveroberts/Documents/Two Lever PR/Raw Data/Final/H383/8_H383_Mar_27.str")
    

    def clearFigure(self):
        self.matPlotFigure.clf()
        self.threshold_matPlot_Canvas.draw()

    def testStuff2(self):
        print("testStuff3")

    def testStuff3(self):
        print("testStuff3")

    def drawThreshold(self):
        """
        TH_FigureFrame                   - tk Frame that will contain the Figure
        self.threshold_matPlot_Canvas    - container for the MatPlotLib Figure
                                         - This must be redrawn after things are changed
        self.matPlotFigure      - This is the Figure that axes and lines are drawn on
        """
        verbose = True

        def demandFunction(x,alpha):
            """
            Demand function described by Hursh
            

            y = np.e**(np.log10(Qzero)+k*(np.exp(-alpha*Qzero*x)-1))

            # Some day experiment with a different equation like:
            # y = Qzero * np.e**(-x * alpha)
            
            """
            
            Qzero = self.Qzero
            #k = self.k_Var.get()

            k = 4.19
            y = 10**(np.log10(Qzero)+k*(np.exp(-alpha*Qzero*x)-1))
                       
            return y 
        
        if (self.pumpTimes.get() == 0):
            pumpTimesString = "Using OMNI pumpTimes"
            TH_PumpTimes = [3.162,1.780,1.000,0.562,0.316,0.188, 0.100,0.056,0.031,0.017,0.010,0.0056]
        else:
            pumpTimesString = "Using Feather M0 pumpTimes"
            TH_PumpTimes = [3.160,2.000,1.260,0.790,0.500,0.320, 0.200,0.130,0.080,0.050,0.030,0.020]


        # Generate a price list based on which pump times were selected
        # This assumes a standard cocaine concentration of 5 mg/ml and a Razel pump with 5 RPM motor
        # The pump speed (0.025 ml/sec) was determined as an average across several pumps being
        # switched intermittently on a PR. Might be worth checking against the total fluid delivered
        # during a TH session.
        # Pump Speed was empirically determined. Razel tables show 0.0275 ml/sec
        priceList = []
        for i in range(12):
            dosePerResponse = TH_PumpTimes[i] * 5.0 * 0.025  # pumptime(mSec) * mg/ml * ml/sec)
            print(dosePerResponse)            
            price = round(1/dosePerResponse,2)
            priceList.append(price)

        print(priceList)

        # Retrieve the consumption and response lists from the selected dataRecord.
        # These lists are extracted from the datafile when initially opened.
        # Not that 0.01 is substituted for zero to avoid errors in log functions.

        aDataRecord = self.recordList[self.fileChoice.get()]
        datalist = aDataRecord.datalist    # Event record needs this.
        consumptionList = aDataRecord.consumptionList
        responseList = aDataRecord.responseList

        # ****************************************************************
        #
        #  SUBSTITUTIONS
        #
        # ****************************************************************
        # There is a very small discrepancy in how the mg/resp is calculated in Hursh's spreadsheet
        # Apparently Cody came up with the following mg/resp:
        mgPerRespList = [0.421,0.237,0.133,0.075, 0.041,0.024,0.013,0.0075,0.0041,0.0024,0.0013,0.000715]
        # I've estimated a 12th entry
        # This corresponds to the following pricelist from Hursh's spreadsheet.       
        priceList = [2.37,4.21,7.5,13.3,24.2,42.1,75,133.9,241.9,416.7,750,1398]

        # substitute the consumptionList that would be used by Steven
        for i in range(12):
            consumptionList[i] = responseList[i] * mgPerRespList[i]

        # *****************************************************************

        # Truncate the range of priceList and consumptionList according the radio button settings
        startRange = self.rangeBegin.get()
        endRange = self.rangeEnd.get()
        truncPriceList = []
        truncConsumptionList = []
        for t in range(startRange,endRange+1):    
            truncPriceList.append(priceList[t])
            truncConsumptionList.append(consumptionList[t])

        # Calculate Pmax as price with the highest response rate
        maxResp = max(responseList)
        binNum = 0
        for i in range(len(responseList)):
            if (responseList[i] == maxResp):
                binNum = i
        graphicalPmaxString = "Pmax (Graphically determine) = "+str(priceList[binNum])
        
        # Create list of injection times for event record
        injNum = 0
        injTimeList = []
        aRecord = self.recordList[self.fileChoice.get()]
        for pairs in aRecord.datalist:
            if pairs[1] == 'P':                     
                injNum = injNum + 1
                injTimeList.append(pairs[0]/60000)  # Min

        firstInjTime = injTimeList[0]              
        firstInjString = "First injection at {0:5.1f} min".format(firstInjTime)

        # Create a list to show the beginnings of each block
        blockNum = 0
        finishTime = 0
        blockTimeList = []
        for pairs in aRecord.datalist:
            if pairs[1] == 'B':                     
                blockNum = blockNum + 1
                blockTimeList.append(pairs[0]/60000)  # Min
            if pairs[1] == 'b':
                finishTime = pairs[0]/60000 + 10
                # The end of the (presumably) eleventh block plus ten minutes
                # It appears that the last block does not have a corresponding "b"                                                           
        finishTimeString = "Finish Time = {0:5.1f} (min)".format(finishTime)
        
        # Sometimes and animal won't start for an hour. One could erase this interval
        # by subtracting the time of the first injection from all times
        """
        adjustedTimeList = []
        for t in injTimeList:
            adjustedTimeList.append(t - firstInjTime)
        """

        # Create the beginnings of the graph
        # The user can control whether the graph is embedded into the program ...
        # Or pushed to a separate window with its own widgets.
        # The graph in the separate window can be saved as a separate publication quality .prn file
        if (self.showOn_tkCanvas.get()):
            fig = self.matPlotFigure    # Previously defined Figure containing matPlotCanvas
            fig.clf()
        else:
            fig = plt.figure(figsize=(6,6), dpi=80, constrained_layout = True)  # Newly instantaited pyplot figure

        # Patch is used to configure colors, lines etc.  
        fig.patch.set_facecolor("azure")
        fig.patch.set_edgecolor("blue")    
        fig.patch.set_linewidth(5.0)       # 0.5 would be very thin
        fig.set_frameon(True)              # Set whether the figure background is displayed or not
        # fig.suptitle("Threshold Title", fontsize = 16, x = 0.2, y = 0.94)
        # gridspec allows greater control over the positioning of plots
        from matplotlib import gridspec               
        gs = gridspec.GridSpec(nrows = 20, ncols= 1)

        # **************   EVENT RECORD **********************
        # Create a subplot for event record
        eventRecord = fig.add_subplot(gs[0,0],label="1")  # row [0] and col [0]]
        eventRecord.axes.get_yaxis().set_visible(False)
        
        eventRecord.text(0.5, 3, aDataRecord.fileName, ha = 'center', transform=eventRecord.transAxes, \
                fontsize=12, color='black')
        
        eventRecord.set_ylabel('')
        eventRecord.set_yticklabels("")                 # Suppress tick labels
        eventRecord.set_xlabel('Time (minutes)')
        eventRecord.spines["top"].set_color('none')
        eventRecord.spines["left"].set_color('none')
        eventRecord.spines["right"].set_color('none')
        startTime = 1                                  # could start from time of second bin
        eventRecord.set_xlim(startTime, finishTime) 
        eventRecord.set_ylim(0, 3)
        eventRecord.eventplot(injTimeList,lineoffsets = 0, linelengths=3)
        eventRecord.eventplot(blockTimeList,lineoffsets = 0, linelengths=5, color = 'red')

        # ************** DEMAND CURVE *************************

        # The k value is derived from the slider. Defaults to 3 (see definition on line 232)
        # Roberts thinks there is no justification for the function to have this parameter.

        k = self.scale_k.get()             
        kString = "Using k from slider = {0:4.1f}".format(k)

        # The manual curve fit checkbox allows users to play with k and alpha
        # If unchecked, it uses curvit to calculate alpha
        if (self.manualCurveFitVar.get() == True):

            # Override for now and use Steven's values:
            self.Qzero = 1.0
            QzeroString = "Qzero (mean of bins 1..3) = {0:6.3f}".format(self.Qzero)
            self.alpha = 0.00060899
            alphaString = "alpha (curve fit) = {0:7.5f}".format(self.alpha)
            k = 4.190
            kString = "Using k from Hursh = {0:4.3f}".format(k)

            """
            self.alpha = self.alphaVar.get()
            alphaString = "alpha (from slider) = {0:7.5f}".format(self.alpha)
            self.Qzero = self.QzeroVar.get()
            QzeroString = "Qzero (from slider) = {0:6.3f}".format(self.Qzero)
            """
        else:
            # Calculate Qzero as the average of the first three bins
            self.Qzero = (consumptionList[1]+consumptionList[2]+consumptionList[3])/3
            QzeroString = "Qzero (mean of bins 1..3) = {0:6.3f}".format(self.Qzero)
            # Fit the curve - find alpha
            param_bounds=([0.001],[0.02])
            fitParams, fitCovariances = curve_fit(demandFunction, truncPriceList, truncConsumptionList, bounds=param_bounds)
            self.alpha = fitParams[0]
            alphaString = "alpha (curve fit) = {0:7.5f}".format(self.alpha)
            #print (fitCovariances)

        # Create y values for best fit line
        fitLine = []
        Qzero = self.Qzero
        alpha = self.alpha       
        for x in truncPriceList:
            y = demandFunction(x,alpha)
            fitLine.append(y)

        # ****  Create the demand Curve Plot and set configurations ****  

        demandCurve = fig.add_subplot(gs[1:9,0],label="2")
        position = [0.15, 0.1, 0.70, 0.6]    # X1,Y1,X2,Y2 - lower left corner, top right corner
        demandCurve.set_position(position)        
        if (self.logXVar.get() == True):
            demandCurve.set_xscale("log")
        else:
            demandCurve.set_xscale("linear")
        if (self.logYVar.get() == True):
            demandCurve.set_yscale("log")
            yMax = 5
        else:
            demandCurve.set_yscale("linear")
            yMax = 2
        xMin = 1
        xMax = 1500
        yMin = 0.01
        yMax = 10.0
        demandCurve.set_xlim(xMin,xMax)
        demandCurve.set_ylim(yMin,yMax)            
        demandCurve.set_ylabel('Consumption', fontsize = 14)
        demandCurve.yaxis.labelpad = 15                             # Move label left or right
        demandCurve.set_xlabel('Price', fontsize = 14)
        demandCurve.plot(truncPriceList, fitLine, color ='red')     # Draw a loglog line 
        demandCurve.scatter(truncPriceList, truncConsumptionList)   # and a scatter plot

        # Calculate r as an indicator of goodness of fit
        r = pearsonr(truncPriceList,fitLine)
        rString = "r = {:.3f}, N = {}".format(r[0],len(truncPriceList))


        """
        Bentxley et al. (2013) offers the following formula for 1st derivative so presumably:
        slope = -alpha*Qzero*x*k*np.exp(-alpha*Qzero*x)
        equivalent to:
        slope = -alpha*Qzero*x*k*np.e**(-alpha*Qzero*x)
        """

        # If possible, calculate Pmax and Omax
        PmaxFound = False
        OmaxFound = False
        PmaxString = "Pmax not found"
        curveFitPmaxString = "Pmax not found"
        OmaxString = "Omax not found"
        for p in range(10,1500):
            if (PmaxFound != True):
                slope = -np.log(10**k) * Qzero * p * alpha * np.exp(-alpha * Qzero * p)
                """
                # Uncomment this section if you want to see it work
                if (slope < -0.98) and (slope > -1.02):
                            print(x, slope)
                """
                if slope < -1.0:
                    Pmax = p 
                    PmaxFound = True
                    curveFitPmaxString = "Pmax (curve fit) = {0:6.0f}".format(Pmax)
        if PmaxFound:
            OmaxFound = True
            Omax = demandFunction(Pmax,alpha)
            OmaxString = "Omax = {0:6.3f}".format(Omax)
            if self.showPmaxLine.get():
                x = [Pmax,Pmax]
                y = [yMin,Omax]
                pmaxLine = Line2D(x,y, color = 'green')
                PmaxString = "Pmax = {0:3.0f}  ".format(Pmax)
                demandCurve.add_line(pmaxLine)
                demandCurve.text(Pmax, Omax, PmaxString, ha = 'left', color = 'green',transform=demandCurve.transData)

        if self.showOmaxLine.get():
            if PmaxFound:
                x = [xMin,Pmax]
                y = [Omax,Omax]
                OmaxLine = Line2D(x,y, color = 'blue')
                demandCurve.add_line(OmaxLine)
                OmaxString = "Omax = {0:6.4f}".format(Omax)
                demandCurve.text(3, Omax - 0.05, OmaxString, ha = 'left', color = 'blue',transform=demandCurve.transData)
                
        """
                x = [1e0, 1e4]
                y = [Qzero,Qzero]
                QzeroLine = Line2D(x,y, color = 'blue')
                demandCurve.add_line(QzeroLine)
        """       
        
        # Show responses on second axis

        if (self.responseCurveVar.get() == True):
            respCurve = demandCurve.twinx()                  # create a 2nd axes that shares the same x-axis
            respCurve.set_position(position)
            respCurve.set_ylabel('Responses', fontsize = 14)
            respCurve.yaxis.labelpad = 20                    # Move label left or right
            respCurve.set_ylim(0,self.respMax.get())                        # Y axis from 0 to 250
            respCurve.plot(priceList,responseList, color = 'black')

        # Display stuff on screen
        demandCurve.text(0.05, 0.95, QzeroString, ha = 'left', transform=demandCurve.transAxes)
        demandCurve.text(0.05, 0.91, alphaString, ha = 'left', transform=demandCurve.transAxes)
        demandCurve.text(0.05, 0.87, kString, ha = 'left', transform=demandCurve.transAxes)
        demandCurve.text(0.65, 0.95, rString, ha = 'left', transform=demandCurve.transAxes)
       
        if (self.showOn_tkCanvas.get()):
            self.threshold_matPlot_Canvas.draw()
        else:
            plt.show()

        if (self.printReportVar.get()):
            print("********************************")
            print(pumpTimesString)
            print("Number of data points plotted = ",len(truncPriceList))
            print(firstInjString)
            print(finishTimeString)
            print(kString)
            print(QzeroString)            
            print(alphaString)
            print(graphicalPmaxString)
            print(curveFitPmaxString)
            print("priceList", priceList)
            tempString = "Consumption: "
            for i in range(len(consumptionList)):
                tempString = tempString+"{0:5.3f}, ".format(consumptionList[i])
            print(tempString)
            print("responses", responseList)
            tempString = "FitLine: "
            for i in range(len(fitLine)):
                tempString = tempString+"{0:5.3f}, ".format(fitLine[i])
            print(tempString)
            print("********************************")

    # *************** Two Lever ********************

    def TwoLeverCR(self):

            def draw_bar(x,y, pixel_height, width, color = "black"):
                self.graphCanvas.create_line(x, y, x, y-pixel_height, fill=color)
                self.graphCanvas.create_line(x, y-pixel_height, x+width, y - pixel_height, fill=color)
                self.graphCanvas.create_line(x+width, y-pixel_height, x+width, y, fill=color)
        
            self.graphCanvas.delete('all')
            # label = "TwoLever Cum Rec"
            # self.graphCanvas.create_text(300,200, text=label)
            aRecord = self.recordList[self.fileChoice.get()]
            # print(aRecord)
            # canvas is 800 x 600
            x_zero = 50
            y_zero = 400
            x_pixel_width = 700                               
            y_pixel_height = 350
            x_divisions = 12
            max_x_scale = self.max_x_scale.get()
            if (max_x_scale == 10) or (max_x_scale == 30): x_divisions = 10
            max_y_scale = self.max_y_scale.get()
            y_divisions = 10
            aTitle = aRecord.fileName
            # def cumRecord(aCanvas, x_zero, y_zero, x_pixel_width, y_pixel_height, max_x_scale, max_y_scale, datalist, aTitle, leverChar = 'L')
            self.graphCanvas.create_line(x_zero, y_zero, x_pixel_width, y_zero)
            GraphLib.drawYaxis(self.graphCanvas, x_zero, y_zero, y_pixel_height, max_y_scale, y_divisions, True)
            GraphLib.cumRecord(self.graphCanvas, x_zero, y_zero, x_pixel_width, y_pixel_height, max_x_scale, max_y_scale, \
                           aRecord.datalist, self.showBPVar.get(), aTitle, leverChar = 'J')
            # Get pump times
            binPumpTime = 0
            pumpStarttime = 0
            pumpOn = False     
            pumpTimeList = []
            for pairs in aRecord.datalist:
                if pairs[1] == 'B':  # Start of Drug Access
                    binStartTime = pairs[0]
                elif pairs[1] == 'P':
                    pumpStartTime = pairs[0]
                    pumpOn = True
                elif pairs[1] == 'p':
                    if pumpOn:
                        pumpDuration = pairs[0]-pumpStartTime
                        binPumpTime = binPumpTime + pumpDuration
                        pumpOn = False
                elif pairs[1] == 'b':   # End of Drug Access Period
                    dataPoint = [binStartTime,binPumpTime]
                    pumpTimeList.append(dataPoint)
                    binPumpTime = 0
            # print(pumpTimeList)
            # adapted from GraphLib.eventRecord()
            y_zero = 525
            x = x_zero
            y = y_zero
            scale_height = 90
            scale_max = 10000
            x_scaler = x_pixel_width / (max_x_scale*60*1000)
            for pairs in pumpTimeList:
                x = (x_zero + pairs[0] * x_scaler // 1)
                y = (pairs[1]/scale_max * scale_height) // 1
                draw_bar(x,y_zero,y,5)
                if pairs[1] == 0:
                    self.graphCanvas.create_text(x, y_zero-100, fill="blue", text = '*')                   
                # self.graphCanvas.create_line(x, y, newX, y)
                # self.graphCanvas.create_line(newX, y, newX, y-10)                        
                # x = newX
            GraphLib.drawXaxis(self.graphCanvas, x_zero, y_zero, x_pixel_width, max_x_scale, x_divisions)
            self.graphCanvas.create_text(400, y_zero+50, fill="blue", text = 'Session Time (min)')
            self.graphCanvas.create_text(200, y_zero+65, fill="blue", text = 'asterisk (*) indicates zero pump time during access period ')
            
    def TwoLeverGraphTest1(self):
            label = "TwoLeverGraphTest1"
            self.graphCanvas.delete('all')
            self.graphCanvas.create_text(300,200, text=label)


    def TwoLeverTextReport(self):
            """
            As of July 2018, all two lever PR files were collected through OMNI. Therefore
            the data analyzed here would have been read from an ".str" file through streamIO.read_str _file()
            Codes are as follows:               
                A, a = Start and stop of a PR lever block
                B, b = Start and stop of a drug lever block
                L, l = First lever down and up
                J, j = Second lever down and up
                =, . = First lever extend (=) and retract (.)
                -, , = Second lever extend (-) and retract (,)
                T, t = Start and stop of a trial
                S, s = Stimulus light on and off
                P, p = Pump on and off
                E    = End of session
                R    = Restart session

            It appears that the "j" (lever 
            
            Access to drug is defined by 'B' and 'b'
            Don't know what 'T' and 't' represent
        

            """
            self.textBox.insert(END,'\n****************************\n')
            self.textBox.insert(END,"Two Lever PR Summary for "+ self.recordList[self.fileChoice.get()].fileName+ '\n')

            printPumpTimes = True
            # PR Lever
            PR_accessStarts = 0
            PR_accessStops = 0
            PR_BinResponses = 0         # Responses in an access period           
            PR_LeverDownResponses = 0       
            PR_LeverUpResponses = 0
            PR_LeverDownTime = 0        # Time of each press
            PR_LeverDuration = 0        # Duration of each press
            PR_LeverTotalTime = 0       # Total of all presses
            PR_LeverDown = False           
           
            drugAccessStarts = 0        # Number of Drug access periods started          
            drugAccessStops = 0
            drugAccessStartTime = 0
            totalDrugAccessTime = 0
            drugLeverDownResponses = 0
            drugLeverUpResponses = 0
            drugLeverDownTime = 0
            drugLeverDown = False
            totalDrugLeverTime = 0
            minAccessTime = 10000000
            maxAccessTime = 0

            # Pump
            pumpStarts = 0
            pumpStops = 0
            pumpStartTime = 0
            pumpOn = False
            binPumpTime = 0
            totalPumpTime = 0

            finalRatio = 0
           
            # Total = 0       
            pumpTimeList = []
            responseList = []
            aRecord = self.recordList[self.fileChoice.get()]
            for pairs in aRecord.datalist:

                # PR lever block
                if pairs[1] == 'A': PR_accessStarts= PR_accessStarts + 1
                elif pairs[1] == 'a': PR_accessStops= PR_accessStops + 1
                elif pairs[1] == 'J':
                    PR_BinResponses = PR_BinResponses + 1
                    PR_LeverDownResponses = PR_LeverDownResponses + 1
                    PR_LeverDownTime = pairs[0]
                    PR_LeverDown = True
                elif pairs[1] == 'j':
                    PR_LeverUpResponses = PR_LeverUpResponses + 1
                    if PR_LeverDown:
                        PR_LeverDuration = pairs[0]-PR_LeverDownTime
                        PR_LeverTotalTime = PR_LeverTotalTime + PR_LeverDuration
                        PR_LeverDown = False
                                       
                # Drug access Block
                elif pairs[1] == 'B':  # Start of Drug Access - (also end of PR lever access)
                    drugAccessStarts = drugAccessStarts + 1
                    responseList.append(PR_BinResponses)   
                    PR_BinResponses = 0                       # Clear PR_BinResponses
                    drugAccessStartTime = pairs[0]
                elif pairs[1] == 'b':   # End of Drug Access Period
                    drugAccessStops = drugAccessStops + 1
                    pumpTimeList.append(binPumpTime)
                    binPumpTime = 0                           # Clear binPumpTime
                    binAccessTime = pairs[0]-drugAccessStartTime
                    #print(binAccessTime)
                    if binAccessTime < minAccessTime: minAccessTime = binAccessTime
                    if binAccessTime > maxAccessTime: maxAccessTime = binAccessTime
                    
                    totalDrugAccessTime = totalDrugAccessTime + binAccessTime
                    
                # Drug Lever Up/Down
                elif pairs[1] == 'L':
                    drugLeverDownResponses = drugLeverDownResponses + 1
                    drugLeverDownTime = pairs[0]
                    leverDown = True
                elif pairs[1] == 'l':
                    drugLeverUpResponses = drugLeverUpResponses + 1
                    if leverDown:
                        drugLeverDuration = pairs[0]-drugLeverDownTime
                        totalDrugLeverTime = totalDrugLeverTime + drugLeverDuration
                        leverDown = False

                # Pump On/Off    
                elif pairs[1] == 'P':
                    pumpStarts = pumpStarts + 1
                    pumpStartTime = pairs[0]
                    pumpOn = True
                elif pairs[1] == 'p':
                    # The program will try to stop the pump at the end of the session. This will ignore
                    # that command if pump is already off.
                    if pumpOn:
                        pumpStops = pumpStops +1                        
                        pumpDuration = pairs[0]-pumpStartTime
                        binPumpTime = binPumpTime + pumpDuration
                        totalPumpTime = totalPumpTime + pumpDuration
                        pumpOn = False
                                       
            responseList.append(PR_BinResponses)    # Non reinforced responses at the end of the session
            self.textBox.insert(END,'PR Access Intervals (Starts, Stops): '+str(PR_accessStarts)+', '+str(PR_accessStops)+'\n')
            self.textBox.insert(END,"Total PR Lever Down Responses = "+str(PR_LeverDownResponses)+'\n')
            self.textBox.insert(END,"Total PR Lever Up   Responses = "+str(PR_LeverUpResponses)+'\n')
            self.textBox.insert(END,"Total PR Lever Down Time = "+str(PR_LeverTotalTime)+'\n')
            if PR_LeverDownResponses > 0:
                PR_LeverAverage = int(PR_LeverTotalTime/PR_LeverDownResponses)
                self.textBox.insert(END,"Average PR Lever Down Time = "+str(PR_LeverAverage)+'\n\n')

            self.textBox.insert(END,"Drug Access Intervals (Starts, Stops): "+str(drugAccessStarts)+', '+str(drugAccessStops)+'\n')
            accessIntervalLength = int((totalDrugAccessTime/drugAccessStarts)/1000)
            self.textBox.insert(END,"Average Drug Access Interval = "+str(accessIntervalLength)+' seconds \n')
            self.textBox.insert(END,"Minimum Access Duration = "+str(minAccessTime)+'\n')
            self.textBox.insert(END,"Maximum Access Duration = "+str(maxAccessTime)+'\n')
            self.textBox.insert(END,"Total Drug Lever Down Responses = "+str(drugLeverDownResponses)+'\n')
            self.textBox.insert(END,"Total Drug Lever Up Responses = "+str(drugLeverUpResponses)+'\n')
            self.textBox.insert(END,"Total Drug Lever Down Time = "+str(totalDrugLeverTime)+'\n\n')


            self.textBox.insert(END,"Total Pump Starts = "+str(pumpStarts)+'\n')
            self.textBox.insert(END,"Total Pump Stops = "+str(pumpStops)+'\n')
            self.textBox.insert(END,"Total Pump Time = "+str(totalPumpTime)+'\n')
            if pumpStarts > 0:
                averagePumpDuration = int(totalPumpTime/pumpStarts)
                self.textBox.insert(END,"Average Pump Duration = "+str(averagePumpDuration)+'\n\n')


            if drugAccessStarts > 0:
                self.textBox.insert(END,"Final Ratio = "+str(responseList[drugAccessStarts-1])+'\n')

            if len(pumpTimeList) > 0:
                self.textBox.insert(END,"Pumptimes in each bin: \n")
                if printPumpTimes:
                    for i in range (len(pumpTimeList)):
                        self.textBox.insert(END,str(pumpTimeList[i])+'\n')
                    print(pumpTimeList)       
        
    def THTest(self):
            self.textBox.insert("1.0","THTest\n")

    def TwoLeverTest2(self):
            self.textBox.insert("1.0","TwoLeverTest2\n")

    # ************ End Two Lever *******************

    def testText1(self):
        Examples.showTextFormatExamples(self.textBox)

    def demandFunction(self, x, alpha, Qzero):
            k = 2
            y = np.e**(np.log(Qzero)+k*(np.exp(-alpha*Qzero*x)-1))
            return y

    def testFunction(self, x, k_value, alpha, Qzero):
            k = k_value
            y = np.exp(np.log(Qzero)+k*(np.exp(-alpha*Qzero*x)-1))
            return y       
        
  
 
    def testAxisExamples(self):
        """
         Test the drawLogYAxis() function with various parameters
        """ 
        aCanvas = self.thresholdCanvas
        x_zero = 100
        y_zero = 550
        x_pixel_width = 600
        y_pixel_height = 500
        x_startValue = 0.001
        y_startValue = 0.001
        x_logRange = 5
        y_logRange = 5
        x_caption = "Price (responses/mg cocaine)"
        y_caption = "Y"
        #leftLabel = True
        GraphLib.drawLog_X_Axis(aCanvas,x_zero,y_zero,x_pixel_width,x_startValue,x_logRange,x_caption, test = True)
        GraphLib.drawLog_Y_Axis(aCanvas,x_zero,y_zero,y_pixel_height,y_startValue,y_logRange,y_caption, test = True)       
        x_zero = 200
        y_zero = 450
        x_pixel_width = 500
        y_pixel_height = 400
        x_startValue = 0.01
        y_startValue = 0.01
        x_logRange = 5
        logRange = 5
        GraphLib.drawLog_X_Axis(aCanvas,x_zero,y_zero,x_pixel_width,x_startValue,x_logRange,x_caption, test = True)
        GraphLib.drawLog_Y_Axis(aCanvas, x_zero,y_zero,y_pixel_height,y_startValue,y_logRange, y_caption, test = True)
        x_zero = 300
        y_zero = 350
        x_pixel_width = 400
        y_pixel_height = 300
        x_startValue = 0.1
        y_startValue = 0.1
        x_logRange = 2
        y_logRange = 2
        GraphLib.drawLog_X_Axis(aCanvas,x_zero,y_zero,x_pixel_width,x_startValue,x_logRange,x_caption)
        GraphLib.drawLog_Y_Axis(aCanvas,x_zero+x_pixel_width,y_zero,y_pixel_height,y_startValue,y_logRange,y_caption, test = True, leftLabel=False)
               
    def injectionTimesText(self):
        aRecord = self.recordList[self.fileChoice.get()]
        injection = 0
        previousInjTime = 0
        self.textBox.insert(END,"Inj Duration   Time (sec)   Time (min) Interval (sec)\n")
        pumpOn = False
        for pairs in aRecord.datalist:
            if pairs[1] == 'P':
                pumpStartTime = pairs[0]
                injection = injection + 1
                secTime = pairs[0]/1000
                minTime = secTime/60
                interval = secTime - previousInjTime
                previousInjTime = secTime
                pumpOn = True
            if pairs[1] == 'p':
                if pumpOn:
                    pumpOn = False
                    duration = pairs[0]-pumpStartTime
                    if injection == 1:
                        tempString = "{0} {1:10.2f} {2:10.2f} {3:10.2f}".format(injection,duration,secTime,minTime,interval)
                    else:
                        tempString = "{0} {1:10.2f} {2:10.2f} {3:10.2f} {4:10.2f}".format(injection,duration,secTime,minTime,interval)
                    self.textBox.insert(END,tempString+"\n")
                
        self.textBox.insert(END,"Number of injections: "+str(injection)+"\n")

    def doseReport(self):
        aRecord = self.recordList[self.fileChoice.get()]
        pumpOn = False
        injections = 0
        totalPumpDuration = 0
        lastTime = 0
        time1 = self.startTimeScale.get()
        time2 = self.endTimeScale.get()
        for pairs in aRecord.datalist:
            if pairs[1] == 'P':
                minTime = pairs[0]/60000
                if (minTime >= time1) and (minTime < time2):
                    injections = injections + 1
                    pumpStartTime = pairs[0]
                    lastTime = pumpStartTime
                    pumpOn = True
            if pairs[1] == 'p':
                if pumpOn:
                    duration = pairs[0]-pumpStartTime
                    pumpOn = False
                    totalPumpDuration = totalPumpDuration + duration
                    
                    
        aString = "Injections between "+str(time1)+" and "+str(time2)+" minutes = "+str(injections)+"\n"
        self.textBox.insert(END,aString)

        try:
            conc = float(self.concentrationEntry.get())
            weight = int(self.weightEntry.get())         # in grams
            aString = "Drug Concentration = {0:5.3f} mg/ml\nWeight = {1:3d} grams \n".format(conc,weight)            
        except ValueError:
            aString = "Error getting Conc and/or Body weight \n"
        self.textBox.insert(END,aString)

        if injections > 0:
                aString = "Total Pump Duration = {0:6d} mSec \n".format(totalPumpDuration)
                self.textBox.insert(END,aString)
                averagePumpTime = round(totalPumpDuration / injections,2)
                aString = "Average Pump Time = {0:5.3f} mSec \n".format(averagePumpTime)
                self.textBox.insert(END,aString)
                totalDose = (totalPumpDuration/1000) * conc * 0.025  # pumptime(mSec) * mg/ml * ml/sec)
                totalDosePerKg = totalDose/(weight/1000)
                aString = "Total Dose = {0:5.3f} mg;  {1:5.3f} mg/kg \n".format(totalDose, totalDosePerKg)
                self.textBox.insert(END,aString)
                averageDose = (totalDose / injections)
                averageDosePerKg = averageDose / (weight/1000)
                aString = "Average Dose = {0:5.3f} mg;  {1:5.3f} mg/kg \n".format(averageDose, averageDosePerKg)
                self.textBox.insert(END,aString)

        
        self.textBox.insert(END,"********************************\n")

    def selectList(self):
        """
        Dummy function associated with radiobuttons that selects the filename textvariable.
        """
        # print("fileChoice: ", self.fileChoice.get())
        pass


    def clearTHCanvas(self):
        self.graphCanvas.delete('all')
        self.fig = plt.figure(clear=True)   # clear contents
       

    def threshold_text(self):
        aRecord = self.recordList[self.fileChoice.get()]
        aList = aRecord.datalist
        count = ListLib.count_char('L',aList)
        aString = 'Number of responses: '+str(count)
        self.textBox.insert(END,aString+"\n")
        
        count = ListLib.count_char('P',aList)
        aString = 'Number of injections: '+str(count)
        self.textBox.insert(END,aString+"\n")

        blockCount = ListLib.count_char('B',aList)
        aString = 'Number of blocks: '+str(blockCount)
        self.textBox.insert(END,aString+"\n")

        pump_count_list = ListLib.get_pump_count_per_block(aList)
        aString = 'Injections per block: '
        for item in pump_count_list:
            aString = aString + str(item) + ' '
        self.textBox.insert(END,aString+"\n")
        print(pump_count_list)

        for b in range (blockCount):    
            pump_duration_list = ListLib.get_pump_duration_list(aList, b)
            aString = 'Block '+str(b)+': '
            for i in range (len(pump_duration_list)):
                list_item = pump_duration_list[i]
                aString = aString + str(list_item[2]) + ' '
            self.textBox.insert(END,aString+"\n")
        #print("Block "+str(b), pump_duration_list)
        

    def intA_text(self):

        aRecord = self.recordList[self.fileChoice.get()]
        self.textBox.insert(END,aRecord.fileName+"\n")
        aList = aRecord.datalist

        count = ListLib.count_char('L',aList)
        aString = 'Number of Responses: '+str(count)
        self.textBox.insert(END,aString+"\n")

        count = ListLib.count_char('P',aList)
        aString = 'Number of Injections: '+str(count)
        self.textBox.insert(END,aString+"\n")

        count = ListLib.count_char('B',aList)
        aString = 'Number of Blocks: '+str(count)
        self.textBox.insert(END,aString+"\n")

        durations_list = ListLib.pump_durations_per_block(aList)
        print("Total durations per block:", durations_list)

        pump_duration_list = ListLib.get_pump_duration_list(aRecord.datalist, block = -1)
        print(pump_duration_list)     # prints a list of [pump_start_time, duration]  in mSec
        # pumptimes_per_bin = ListLib.get_pumptimes_per_bin(pump_timelist, bin_size = 5000)

        """
        # ***********************************************
        self.textBox.insert(END,"Total Pump Time (mSec): "+str(aRecord.totalPumpDuration)+"\n")
        self.textBox.insert(END,"Cummulative pump time per 5 second bin\n")
        aString = ""
        for t in range(len(pumptimes_per_bin)):
            aString = aString+str(pumptimes_per_bin[t])+' '
            #aString = aString + '{0:6d}'.format(pumptimes_per_bin[t])     
        self.textBox.insert(END,aString+"\n")
        total_pump_time = 0
        for t in range(len(pumptimes_per_bin)):
            total_pump_time = total_pump_time + pumptimes_per_bin[t]
        self.textBox.insert(END,"Total Pump Time (sum of bins): "+str(total_pump_time)+"\n")
        dose = (total_pump_time * 5 * 0.000025) / 0.33
        aString = "Total dose (mg/kg): {0:6.2f} mg/kg".format(dose)     # Format float to 2 decimal points in 6 character field
        self.textBox.insert(END, aString)
        """            
        
    def IntAHistogram_blocks(self):
        '''

        '''
        self.clearGraphTabCanvas()
        aRecord = self.recordList[self.fileChoice.get()]
        pump_total = 0
        for b in range (12):
            total_pump_time = 0
            pump_timelist = ListLib.get_pump_duration_list(aRecord.datalist, block = b)
            pumptimes_per_bin = ListLib.get_pumptimes_per_bin(pump_timelist, bin_size = 5000)
            for t in range(len(pumptimes_per_bin)):
                total_pump_time = total_pump_time + pumptimes_per_bin[t]
            pump_total = pump_total + total_pump_time
            y = (b*45)+50
            GraphLib.histogram(self.graphCanvas,pumptimes_per_bin, y_zero = y, y_pixel_height = 35, clear = False)
            self.graphCanvas.create_text(750, y, fill="blue", text = "Sum = "+str(total_pump_time))
            dose = (total_pump_time * 5 * 0.000025) / 0.33
            aString = "{0:6.2f} mg/kg".format(dose)     #eg. 4000 mSec * 5 mg/ml *0.000025 mls/mSec / 0.330 kg = 1.5 mg/kg
            self.graphCanvas.create_text(750, y + 12, fill="blue", text = aString)
        self.graphCanvas.create_text(750, y + 45, fill="blue", text = "Total "+str(pump_total))

    def IntAHistogram_all(self):
        self.clearGraphTabCanvas()
        aRecord = self.recordList[self.fileChoice.get()]
        pump_total = 0
        x_zero = 75
        y_zero = 550
        x_pixel_width = 600
        y_pixel_height = 400
        max_x_scale = 300
        max_y_scale = 20000
        x_divisions = 5
        y_divisions = 10
        labelLeft = True
        GraphLib.drawYaxis(self.graphCanvas, x_zero, y_zero, y_pixel_height, max_y_scale, y_divisions, labelLeft, \
                  format_int = True, color = "black")
        pump_duration_list = ListLib.get_pump_duration_list(aRecord.datalist, block = -1)
        pumptimes_per_bin = ListLib.get_pumptimes_per_bin(pump_duration_list, bin_size = 5000)
        for t in range(len(pumptimes_per_bin)):
                pump_total = pump_total + pumptimes_per_bin[t]
        GraphLib.histogram(self.graphCanvas,pumptimes_per_bin, y_zero = 550, y_pixel_height = 400, clear = False, \
                           max_y_scale = 20000, y_divisions = 4)

        self.graphCanvas.create_text(300, 100, fill="blue", text = "Total Pump Time: "+str(pump_total))
        dose = (pump_total * 5 * 0.000025) / 0.33
        aString = "Total: {0:6.2f} mg/kg".format(dose)     # Format float to 2 decimal points in 6 character field
        self.graphCanvas.create_text(300, 130, fill="blue", text = aString)        


    def testModel(self):
        WakePumpTimes = [3.162,1.780,1.000,0.562,0.316,0.188,0.100,0.056,0.031,0.018,0.010,0.0056]
        """
        This compares the same dose over 3 different time periods 5,25 and 50 sec
        It does this by changing the concentration, but perhpas it would be
        better to change the pump speed.

        eg. 5000 mSec * 4 mg/ml *0.000025 mls/mSec / 0.330 kg = 1.5 mg/kg
        # model.calculateCocConc defaults to bodyweight 0.330 

        """        
        # testRecord1  5 sec infusion
        testRecord1 = dm.DataRecord([],"5 sec") 
        testRecord1.datalist = [[10000, 'P'],[15000, 'p']]
        testRecord1.pumpSpeed = 0.025   # Wake default 0.1 mls/4 sec = 0.025 / sec
        testRecord1.cocConc = 4.0
        testRecord1.TH_PumpTimes = WakePumpTimes
        testRecord1.extractStatsFromList()
        duration = testRecord1.totalPumpDuration
        dose = (testRecord1.totalPumpDuration * testRecord1.cocConc * (testRecord1.pumpSpeed/1000)/0.330)
        print("testRecord1 Duration = {0}; Total Dose = {1:2.1f}".format(duration,dose))
        # testRecord2  50 sec infusion
        duration = 50
        testRecord2 = dm.DataRecord([],"50 sec") 
        testRecord2.datalist = [[10000, 'P'],[15000, 'p'], [15000, 'P'],[20000, 'p'], \
                                [20000, 'P'],[25000, 'p'], [25000, 'P'],[30000, 'p'], \
                                [30000, 'P'],[35000, 'p'], [35000, 'P'],[40000, 'p'], \
                                [40000, 'P'],[45000, 'p'], [45000, 'P'],[50000, 'p'], \
                                [50000, 'P'],[55000, 'p'], [55000, 'P'],[60000, 'p']]                          
        testRecord2.pumpSpeed = 0.025   # Wake default 0.1 mls/4 sec = 0.025 / sec
        testRecord2.cocConc = 4.0 / (duration / 5.0)
        testRecord2.TH_PumpTimes = WakePumpTimes
        testRecord2.extractStatsFromList()
        duration = testRecord2.totalPumpDuration
        dose = (testRecord2.totalPumpDuration * testRecord2.cocConc * (testRecord2.pumpSpeed/1000)/0.330)
        print("testRecord2 Duration = {0}; Total Dose = {1:2.1f}".format(duration,dose))
        # testRecord3  90 sec infusion
        duration = 90
        testRecord3 = dm.DataRecord([],"90 sec") 
        testRecord3.datalist = [[10000, 'P'],[15000, 'p'], [15000, 'P'],[20000, 'p'], \
                                [20000, 'P'],[25000, 'p'], [25000, 'P'],[30000, 'p'], \
                                [30000, 'P'],[35000, 'p'], [35000, 'P'],[40000, 'p'], \
                                [40000, 'P'],[45000, 'p'], [45000, 'P'],[50000, 'p'], \
                                [50000, 'P'],[55000, 'p'], [55000, 'P'],[60000, 'p'], \
                                [60000, 'P'],[65000, 'p'], [65000, 'P'],[70000, 'p'], \
                                [70000, 'P'],[75000, 'p'], [75000, 'P'],[80000, 'p'], \
                                [80000, 'P'],[85000, 'p'], [85000, 'P'],[90000, 'p'], \
                                [90000, 'P'],[95000, 'p'], [95000, 'P'],[100000, 'p']]
        testRecord3.pumpSpeed = 0.025   # Wake default 0.1 mls/4 sec = 0.025 / sec
        testRecord3.cocConc = 4.0 / (duration / 5.0)
        testRecord3.TH_PumpTimes = WakePumpTimes
        testRecord3.extractStatsFromList()
        duration = testRecord3.totalPumpDuration
        dose = (testRecord3.totalPumpDuration * testRecord3.cocConc * (testRecord3.pumpSpeed/1000)/0.330)
        print("testRecord3 Duration = {0}; Total Dose = {1:2.1f}".format(duration,dose))

        self.showModel(testRecord1, resolution = 5, aColor = "black", max_y_scale = 10)
        self.showModel(testRecord2, resolution = 5, aColor = "red", clear = False, max_y_scale = 10)
        self.showModel(testRecord3, resolution = 5, aColor = "blue", clear = False, max_y_scale = 10)

    def test(self):
        self.clearGraphTabCanvas()
        x_zero = 50
        y_zero = 550
        x_pixel_width = 700                               
        y_pixel_height = 500
        max_x_scale = self.max_x_scale.get()
        x_divisions = 12
        if (max_x_scale == 10) or (max_x_scale == 30): x_divisions = 10
        max_y_scale = self.max_y_scale.get()        
        y_divisions = 10
        GraphLib.drawXaxis(self.graphCanvas, x_zero, y_zero, x_pixel_width, max_x_scale, x_divisions, color = "red")
        offset = 0      
        GraphLib.drawYaxis(self.graphCanvas, x_zero, y_zero, y_pixel_height, max_y_scale, y_divisions, True, color = "blue")
        GraphLib.drawYaxis(self.graphCanvas, x_zero+x_pixel_width +10, y_zero, y_pixel_height, max_y_scale, y_divisions, False)

    # ******************** End Draw Threshold ***********

    def clearText(self):
        self.textBox.delete("1.0",END)

    def summaryText(self):
        # print(dataRecordList[self.fileChoice.get()])    # This will print to the Python Shell
        self.textBox.insert("1.0",self.recordList[self.fileChoice.get()])

        aRecord = self.recordList[self.fileChoice.get()]

        timeFirstInjection = 0
        T1 = 0
        numInj = 0
        numIntervals = 0
        totalIntervals = 0       
        for pairs in aRecord.datalist:
            if pairs[1] == "P":
                if numInj == 0: timeFirstInjection = pairs[0]
                numInj = numInj + 1
                T2 = pairs[0]
                if T1 > 0:
                    numIntervals = numIntervals + 1
                    interval = T2-T1
                    totalIntervals = totalIntervals + interval
                T1 = T2
        timeLastInjection = T1
        self.textBox.insert(END,"First inj = "+str(round(timeFirstInjection/1000,1))+" sec ("+str(round(timeFirstInjection/60000,0))+" min)\n")
        self.textBox.insert(END,"Last inj  = "+str(round(timeLastInjection/ 1000,1))+" sec ("+str(round(timeLastInjection/ 60000,0))+" min)\n")
        self.textBox.insert(END,"Total of "+str(numIntervals)+" intervals = "+str(round(totalIntervals/ 1000,1))+" sec, ("+str(round(totalIntervals/60000,0))+" min)\n")
        meanInterval = totalIntervals/numIntervals
        self.textBox.insert(END,"Mean interval = "+str(round(meanInterval/1000,1))+" sec, ("+str(round(meanInterval/60000,2))+" min)\n")
        self.textBox.insert(END,"Rate (inj/hr) = "+str(round(60/(meanInterval/60000),3))+"\n")
        self.textBox.insert(END,"***************************\n")

    def periodic_check(self):
        thisTime = datetime.now()
        self.clockTimeStringVar.set(thisTime.strftime("%H:%M:%S"))        
        self.root.after(100, self.periodic_check)               

    def go(self):
        self.root.after(100, self.periodic_check)
        self.root.mainloop()
        

if __name__ == "__main__":
    sys.exit(main())

