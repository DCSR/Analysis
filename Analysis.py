
# adapted from Dropbox/SelfAdministration/Analysis/Analysis102.py
from tkinter import *
from tkinter.ttk import Notebook
from tkinter import filedialog
from datetime import datetime
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
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.lines import Line2D
from matplotlib.figure import Figure
from matplotlib import gridspec
import matplotlib.pyplot as plt

"""
Models, Views and Controllers (MCV) design: keep the representation of the data separate
from the parts of the program that the user interacts with.
Models: store and retrieve data from import osdatabases and files. 
View: displays information to the user (eg. a graph)
Controllers: convert user input into calls on functions that manipulate data
"""

def main(argv=None):
    if argv is None:
        argv = sys.argv
    gui = myGUI()
    gui.go()
    return 0

# ********************* The Model **********************


class DataRecord:
    def __init__(self, datalist, fileName):
        self.fileName = fileName
        self.datalist = datalist
        self.numberOfL1Responses = 0
        self.numberOfL2Responses = 0
        self.numberOfInfusions = 0
        self.totalPumpDuration = 0        
        self.cocConc = 0.0
        self.pumpSpeed = 0.0
        self.averagePumpTime = 0.0
        self.TH_PumpTimes = []
        self.priceList = []
        self.consumptionList = []
        self.responseList = []
        self.deltaList = []
        self.notes = "test"

    def __str__(self):
        """
            Returns a string of values inside object that is used when the print command is called
        """
        consumptionStr = ""
        for i in range(0,len(self.consumptionList)):
            consumptionStr = consumptionStr + "{:.3f}, ".format(self.consumptionList[i])

        priceStr = ""
        for i in range(0,len(self.priceList)):
            priceStr = priceStr + "{:.2f}, ".format(self.priceList[i])

        responseStr = ""
        for i in range(0,len(self.responseList)):
            responseStr = responseStr + "{}, ".format(self.responseList[i])
                
        s = "Filename: "+self.fileName+ \
        "\nNotes: "+self.notes+ \
        "\nLever 1 Responses: "+str(self.numberOfL1Responses)+ \
        "\nLever 2 Responses: "+str(self.numberOfL2Responses)+ \
        "\nInfusions: "+str(self.numberOfInfusions)+ \
        "\nTotal Pump Time (mSec): "+str(self.totalPumpDuration)+ \
        "\nAverage Pump Time (mSec): "+str(round(self.averagePumpTime,4))+ \
        "\nPump Speed (ml/sec): "+str(self.pumpSpeed)+" ml/Sec\n"
        
        """
        "\nPumpTimes = "+str(self.TH_PumpTimes) + \
        "\nPriceList = " + priceStr + \
        "\nConsumptionList = " + consumptionStr + \
        "\nResponseList = " + responseStr +"\n"
        "\nDelta List: "+str(self.deltaList)+
        """
        #"\n============================\n"
        
        return s

    def extractStatsFromList(self):
        self.numberOfL1Responses = 0
        self.numberOfL2Responses = 0
        self.numberOfInfusions = 0
        self.totalPumpDuration = 0
        leverOut = True
        pumpOn = False
        lastTime = 0
        self.deltaList = []
        delta = 0
        for pairs in self.datalist:                   
            if pairs[1] == 'L':
                self.numberOfL1Responses = self.numberOfL1Responses + 1
            if pairs[1] == 'J':
                self.numberOfL2Responses = self.numberOfL2Responses + 1               
            if ((pairs[1] == 'P') and (leverOut == True)) :
                self.numberOfInfusions = self.numberOfInfusions + 1
                pumpStartTime = pairs[0]
                delta = pumpStartTime - lastTime
                self.deltaList.append(round(delta/(1000*60)))
                lastTime = pumpStartTime
                pumpOn = True
            if pairs[1] == 'p':
                if pumpOn:
                    duration = pairs[0]-pumpStartTime
                    pumpOn = False
                    self.totalPumpDuration = self.totalPumpDuration + duration
            if self.numberOfInfusions > 0:
                self.averagePumpTime = round(self.totalPumpDuration / self.numberOfInfusions,2)


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

        #Construct ten empty dataRecords
        self.record0 = DataRecord([],"empty")         
        self.record1 = DataRecord([],"empty")
        self.record2 = DataRecord([],"empty")
        self.record3 = DataRecord([],"empty")
        self.record4 = DataRecord([],"empty")
        self.record5 = DataRecord([],"empty")
        self.record6 = DataRecord([],"empty")
        self.record7 = DataRecord([],"empty")
        self.record8 = DataRecord([],"empty")
        self.record9 = DataRecord([],"empty")
        
        # Create a list of these dataRecords so that one can be "selected" with self.fileChoice.get()
        self.recordList = [self.record0,self.record1,self.record2,self.record3,self.record4, \
                           self.record5,self.record6,self.record7,self.record8,self.record9]

        # *************   The Model - vaiables, lists and files *********
        self.clockTimeStringVar = StringVar(value="0:00:00")
        self.max_x_scale = IntVar(value=360)
        self.max_y_scale = IntVar(value=500)
        self.neumaierDose = IntVar(value=2)
        # self.max_x_scale.set(120)
        
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

        # Threshold tab
        self.respMax = IntVar()
        self.respMax.set(200)
        self.rangeEnd = IntVar()
        self.rangeEnd.set(11)
        self.rangeBegin = IntVar()
        self.rangeBegin.set(1)
        self.average_TH_FilesVar = BooleanVar(value=False)
        self.pumpTimes = IntVar()
        self.pumpTimes.set(0)

        #*************  The View ************       

        #************* Root Frame
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
        myNotebook.add(self.thresholdTab,text = "Threshold")
        myNotebook.add(self.graphTab,text = "Graphs")      
        myNotebook.add(self.textTab,text = "Text")
        myNotebook.add(self.testAreaTab,text = "Test Area")
        myNotebook.grid(row=0,column=0)

        #**************Header Row ******************
        openFileButton = Button(headerFrame, text="Open File", command= lambda: self.openWakeFile("")).grid(row=0,column=0, sticky=W)
        spacer1Label = Label(headerFrame, text="               ").grid(row=0,column=1)
        clockTimeLabel = Label(headerFrame, textvariable = self.clockTimeStringVar).grid(row = 0, column=2)
        spacer2Label = Label(headerFrame, text="               ").grid(row=0,column=3)
        openFilesButton = Button(headerFrame, text="Open Files", command= lambda: self.openWakeFiles("")).grid(row=0,column=4, sticky=W)
        
        loadTestButton1 = Button(headerFrame, text="TH_OMNI_test.str", command= lambda: \
                              self.openWakeFiles("TH_OMNI_test.str")).grid(row=0,column=5,sticky=N, padx = 20)
        """
        loadTestButton2 = Button(headerFrame, text="TH_FEATHER_test.dat", command= lambda: \
                              self.openWakeFile("TH_FEATHER_test.dat")).grid(row=0,column=5,sticky=N, padx = 20)
        loadTestButton3 = Button(headerFrame, text="3_H886_Jul_4.str", command= lambda: \
                              self.openWakeFile("3_H886_Jul_4.str")).grid(row=0,column=6,sticky=N, padx = 20)
        loadTestButton4 = Button(headerFrame, text="8_H383_Mar_23.str", command= lambda: \
                              self.openWakeFile("8_H383_Mar_23.str")).grid(row=0,column=7,sticky=N, padx = 20)
        """

        #************** Graph Tab ******************
        self.columnFrame = Frame(self.graphTab, borderwidth=2, relief="sunken")
        self.columnFrame.grid(column = 0, row = 0, columnspan= 1, sticky=NS)
        
        self.graphButtonFrame = Frame(self.columnFrame, borderwidth=2, relief="sunken")
        self.graphButtonFrame.grid(column = 0, row = 0, sticky=N)
        clearCanvasButton = Button(self.graphButtonFrame, text="Clear", command= lambda: \
                              self.clearGraphTabCanvas()).grid(row=0,column=0,sticky=N)
        cumRecButton = Button(self.graphButtonFrame, text="Cum Rec", command= lambda: \
                              self.drawCumulativeRecord(self.recordList[self.fileChoice.get()])).grid(row=2,column=0,sticky=N)
        self.showBPVar = BooleanVar(value = True)      
        showBPButton = Checkbutton(self.graphButtonFrame, text = "show BP", variable = self.showBPVar, onvalue = True, offvalue = False, \
                                   command= lambda: self.drawCumulativeRecord(self.recordList[self.fileChoice.get()]))
        showBPButton.grid(row = 3,column=0)      
        eventRecButton = Button(self.graphButtonFrame, text="Event Rec", command= lambda: \
                              self.drawEventRecords()).grid(row=4,column=0,sticky=N)
        timeStampButton = Button(self.graphButtonFrame, text="Timestamps", command= lambda: \
                              self.timeStamps(self.recordList[self.fileChoice.get()])).grid(row=5,column=0,sticky=N)
        modelButton = Button(self.graphButtonFrame, text="Model Coc", command= lambda: \
                              self.showModel(self.recordList[self.fileChoice.get()])).grid(row=6,column=0,sticky=N)
        histogramButton = Button(self.graphButtonFrame, text="Histogram", command= lambda: \
                              self.showHistogram(self.recordList[self.fileChoice.get()])).grid(row=7,column=0,sticky=N)

        self.graph_YaxisRadioButtonFrame = Frame(self.columnFrame, borderwidth=2, relief="sunken")
        self.graph_YaxisRadioButtonFrame.grid(column = 0, row = 1)
        y_axisButtonLabel = Label(self.graph_YaxisRadioButtonFrame, text = "Y axis").grid(row = 0, column=0)
        y_scaleRadiobutton250 = Radiobutton(self.graph_YaxisRadioButtonFrame, text="250", variable=self.max_y_scale, value=250)
        y_scaleRadiobutton250.grid(column = 0, row = 1)
        y_scaleRadiobutton500 = Radiobutton(self.graph_YaxisRadioButtonFrame, text="500", variable=self.max_y_scale, value=500)
        y_scaleRadiobutton500.grid(column = 0, row = 2)
        y_scaleRadiobutton1000 = Radiobutton(self.graph_YaxisRadioButtonFrame, text="1000", variable=self.max_y_scale, value=1000)
        y_scaleRadiobutton1000.grid(column = 0, row = 3)
        y_scaleRadiobutton1500 = Radiobutton(self.graph_YaxisRadioButtonFrame, text="1500", variable=self.max_y_scale, value=1500)
        y_scaleRadiobutton1500.grid(column = 0, row = 4)

        # ******  IntA Frame ************

        self.graph_IntA_frame = Frame(self.columnFrame, borderwidth=2, relief="sunken")
        self.graph_IntA_frame.grid(column = 0, row = 2)
        IntA_frame_lable = Label(self.graph_IntA_frame, text = "IntA").grid(row = 0, column=0)
        IntA_event_button = Button(self.graph_IntA_frame, text="Event records", command= lambda: \
            self.IntA_event_records()).grid(row=1,column=0,sticky=N)
        IntA_durations_button = Button(self.graph_IntA_frame, text="Pump durations", command= lambda: \
            self.IntA_durations()).grid(row=2,column=0,sticky=N)        
        IntA_histogram_block_Button = Button(self.graph_IntA_frame, text="Histogram (blocks)", command= lambda: \
            self.IntAHistogram_blocks()).grid(row=3,column=0,sticky=N)
        IntA_histogram_all_Button = Button(self.graph_IntA_frame, text="Histogram (All)", command= lambda: \
            self.IntAHistogram_all()).grid(row=4,column=0,sticky=N)


        # ******  2L - PR Frame *********

        self.graph_2LPR_frame = Frame(self.columnFrame, borderwidth=2, relief="sunken")
        self.graph_2LPR_frame.grid(column = 0, row = 3)
        TwoLever_frame_lable = Label(self.graph_2LPR_frame, text = "2L-PR").grid(row = 0, column=0)
        TwoLever_CR_button = Button(self.graph_2LPR_frame, text="Cum Rec", command= lambda: \
            self.TwoLeverCR()).grid(row=1,column=0,sticky=N)
        TwoLever_Test1_button = Button(self.graph_2LPR_frame, text="Test 1", command= lambda: \
            self.TwoLeverGraphTest1()).grid(row=2,column=0,sticky=N)
        TwoLever_Test2_button = Button(self.graph_2LPR_frame, text="Test 2", command= lambda: \
            self.TwoLeverGraphTest2()).grid(row=3,column=0,sticky=N)

        # ******  Example Frame *********

        self.graph_example_frame = Frame(self.columnFrame, borderwidth=2, relief="sunken")
        self.graph_example_frame.grid(column = 0, row = 4)
        example_frame_lable = Label(self.graph_example_frame, text = "Examples").grid(row = 0, column=0)
        model_example_button = Button(self.graph_example_frame, text="Test Model", command= lambda: \
                self.testModel()).grid(row=1,column=0,sticky=N)
        axes_example_button = Button(self.graph_example_frame, text="Axes", command= lambda: \
                              self.test()).grid(row=2,column=0,sticky=N)
        
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
                

        #************** Threshold Tab **************
        # Two subframes:        
        #
        # thresholdButtonFrame 
        #      drawThresholdFrame
        #
        #
        #
        #
        #      responseButtonFrame
        # TH_FigureFrame    - tk container
        #      self.tkCanvas     - drawing space for things loke event records
        #      self.matPlotCanvas - container for the MatPlotLib Figure
        #      self.figure       - the thing that axes and lines are drawn on

        self.thresholdButtonFrame = Frame(self.thresholdTab, borderwidth=2, relief="sunken")
        self.thresholdButtonFrame.grid(column = 0, row = 0, sticky=N)

        self.thresholdFigureFrame = Frame(self.thresholdTab, borderwidth=2, relief="sunken")
        self.thresholdFigureFrame.grid(column = 1, row = 0, sticky=N)


        #************** Threshold Button Frame *****

        thresholdButton = Button(self.thresholdButtonFrame, text="Draw Demand Curve", command= lambda: \
                                 self.drawThreshold()).grid(row = 0, column = 0, columnspan = 2)
        
        clearTHCanvasButton = Button(self.thresholdButtonFrame, text="Clear Canvas", \
                                     command = lambda: self.clearFigure()).grid(row=1,column=0, columnspan = 2, sticky = EW)

        pumpTimesOMNI = Radiobutton(self.thresholdButtonFrame, text = "OMNI", variable = self.pumpTimes, value = 0).grid(row = 2,column = 0, sticky = W)
        cumRecButton2 = Radiobutton(self.thresholdButtonFrame, text = "M0 ", variable = self.pumpTimes, value = 1).grid(row = 2,column = 1, sticky = W)

        responseLabel = Label(self.thresholdButtonFrame, text="Draw Response Curve").grid(row = 3, column = 0, sticky = EW)

        self.logXVar = BooleanVar(value = True)      
        logLogCheckButton = Checkbutton(self.thresholdButtonFrame, text = "Log X", variable = self.logXVar, \
                                        onvalue = True, offvalue = False).grid(row = 4, column = 0, sticky = W)
        self.logYVar = BooleanVar(value = True)      
        logLogCheckButton = Checkbutton(self.thresholdButtonFrame, text = "Log Y", variable = self.logYVar, \
                                        onvalue = True, offvalue = False).grid(row = 4, column = 1)

        self.showPmaxLine = BooleanVar(value = True)      
        showPmaxCheckButton = Checkbutton(self.thresholdButtonFrame, text = "Pmax line", variable = self.showPmaxLine, \
                                        onvalue = True, offvalue = False).grid(row = 5, column = 0, stick = W)
        self.showOmaxLine = BooleanVar(value = True)
        showOmaxCheckButton = Checkbutton(self.thresholdButtonFrame, text = "Omax line", variable = self.showOmaxLine, \
                                        onvalue = True, offvalue = False).grid(row = 5, column = 1, sticky = W)




        #self.average_TH_FilesCheckButton = Checkbutton(self.ThresholdButtonFrame, text = "Average Files", \
        #        variable = self.average_TH_FilesVar, onvalue = True, offvalue = False).grid(row = 1, column = 0, columnspan = 2, sticky=W)


        #Contains:..

        #************* "drawThresholdFrame within thresholdButtonFrame ********       
        self.drawThresholdFrame = Frame(self.thresholdButtonFrame, borderwidth=2, relief="sunken")
        self.drawThresholdFrame.grid(row = 6, column = 0, columnspan = 2, sticky = EW)

        self.manualCurveFitVar = BooleanVar(value = True)
        curveFitCheckButton = Checkbutton(self.drawThresholdFrame, text = "Manual Curve Fit", \
                    variable = self.manualCurveFitVar, onvalue = True, \
                    offvalue = False).grid(row = 4, column = 0, columnspan = 2, stick=W)
                
        self.QzeroVar = DoubleVar()
        self.QzeroLabel = Label(self.drawThresholdFrame, text = "Qzero").grid(row=8,column=0,columnspan = 2,sticky=EW)
        self.scale_Q_zero = Scale(self.drawThresholdFrame, orient=HORIZONTAL, length=200, resolution = 0.05, \
                                  from_=0.25, to=5.0, variable = self.QzeroVar)
        self.scale_Q_zero.set(1.0)
        self.scale_Q_zero.grid(row=9,column=0, columnspan = 2)

        self.alphaVar = DoubleVar()
        self.alphaLabel = Label(self.drawThresholdFrame, text = "alpha").grid(row=10,column=0,columnspan = 2,sticky=EW)
        self.scale_alpha = Scale(self.drawThresholdFrame, orient=HORIZONTAL, length=200, resolution = 0.00025, \
                                 from_= 0.0005, to = 0.02, variable = self.alphaVar)
        self.scale_alpha.set(0.005)
        self.scale_alpha.grid(row=11,column=0, columnspan = 2)

        self.k_Var = DoubleVar()
        self.k_Label = Label(self.drawThresholdFrame, text = "k").grid(row=12,column=0,columnspan = 2,sticky=EW)
        self.scale_k = Scale(self.drawThresholdFrame, orient=HORIZONTAL, length=200, resolution = 0.1, \
                                 from_= 0.0, to = 9.9, variable = self.k_Var)
        self.scale_k.set(5.0)
        self.scale_k.grid(row=13,column=0, columnspan = 2)
    
        self.startStopFrame = Frame(self.thresholdButtonFrame, borderwidth=2, relief="sunken")
        self.startStopFrame.grid(columnspan=2, row = 9, column = 0)
        
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

        self.responseButtonFrame = Frame(self.thresholdButtonFrame, borderwidth=2, relief="sunken")
        self.responseButtonFrame.grid(row = 50, column = 0, sticky = EW)

        self.responseCurveVar = BooleanVar(value = True)
        self.responseCurveCheckButton = Checkbutton(self.responseButtonFrame, text = "Show Response Curve", variable = self.responseCurveVar, \
                                        onvalue = True, offvalue = False).grid(row = 0, column = 0, columnspan = 2)
        
        respMaxLable = Label(self.responseButtonFrame, text="Response Max").grid(row=1,column = 0, sticky=(N))
        respMaxButton1 = Radiobutton(self.responseButtonFrame, text = "25   ", variable=self.respMax, value = 25).grid(row=2,column=0)
        respMaxButton2 = Radiobutton(self.responseButtonFrame, text = "50   ", variable=self.respMax, value = 50).grid(row=3,column=0)
        respMaxButton3 = Radiobutton(self.responseButtonFrame, text = "100   ", variable=self.respMax, value = 100).grid(row=2,column=1)
        respMaxButton4 = Radiobutton(self.responseButtonFrame, text = "200   ", variable=self.respMax, value = 200).grid(row=3,column=1)


        test1Button = Button(self.thresholdButtonFrame, text="Test Pmax calc", command= lambda: \
                              self.testPmaxCalc()).grid(row=19,column=0,sticky=S)
        test2Button = Button(self.thresholdButtonFrame, text="Save Figure.png", command= lambda: \
                             self.save_TH_Figure()).grid(row=20,column=0,sticky=S)
        test3Button = Button(self.thresholdButtonFrame, text="testStuff2()", command= lambda: \
                             self.testStuff2()).grid(row=21,column=0,sticky=S)
        test4Button = Button(self.thresholdButtonFrame, text="testStuff3()", command = lambda: \
                             self.testStuff3()).grid(row=23,column=0,sticky=N)

        #****************

        # TH_FigureFrame    - tk container (a Frame)
        #      self.matPlotFigure              - the thing that axes and lines are drawn on        
        #      self.threshold_tk_Canvas         - drawing space for things like event records
        #      self.threshold_matPlot_Canvas    - container for the MatPlotLib Figure
        #                                       - This is the thing that gets redrawn after things are changed.

        self.matPlotFigure = Figure(figsize=(7,7), dpi=80)
        self.matPlotFigure.set_edgecolor("white")  #see help(colors)
        self.matPlotFigure.set_facecolor("white")
        #Set whether the figure frame (background) is displayed or invisible
        self.matPlotFigure.set_frameon(True)
        
        self.threshold_tk_Canvas = Canvas(self.thresholdFigureFrame, width = 600, height = 100)
        self.threshold_tk_Canvas.grid(row=0,column=0)
        self.threshold_tk_Canvas.create_text(300,10,text = "Threshold Canvas")

        self.threshold_matPlot_Canvas = FigureCanvasTkAgg(self.matPlotFigure, master=self.thresholdFigureFrame)
        self.threshold_matPlot_Canvas.get_tk_widget().grid(row=1,column=0)

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
        self.startTimeVar = IntVar()
        self.startTimeScale = Scale(self.textButtonFrame, orient=HORIZONTAL, length=100, resolution = 5, \
                                  from_=0, to=360, variable = self.startTimeVar)
        self.startTimeScale.grid(row=5,column=1)
        self.startTimeScale.set(0)

        self.endTimeLabel = Label(self.textButtonFrame, text = "T2").grid(row=6,column=0,sticky=W) 
        self.endTimeVar = IntVar()
        self.endTimeScale = Scale(self.textButtonFrame, orient=HORIZONTAL, length=100, resolution = 5, \
                                  from_=0, to=360, variable = self.endTimeVar)
        self.endTimeScale.grid(row=6,column=1)
        self.endTimeScale.set(360)
        
        concentrationLabel = Label(self.textButtonFrame, text="Conc (mg/ml)")
        concentrationLabel.grid(row = 7, column = 0)
        self.drugConcStr = StringVar(value="5.0")
        self.concentrationEntry = Entry(self.textButtonFrame, width=6,textvariable=self.drugConcStr)
        self.concentrationEntry.grid(row = 7, column = 1)

        weightLabel = Label(self.textButtonFrame, text="Body weight (gms)")
        weightLabel.grid(row = 8, column = 0)
        self.weightStr = StringVar(value="350")
        self.weightEntry = Entry(self.textButtonFrame, width=6,textvariable=self.weightStr)
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
        TwoLeverTest1Button = Button(self.text_2LPR_Frame, text="2L-PR Test1", command= lambda: \
                              self.TwoLeverTest1()).grid(row=1,column=0,sticky=W)
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
        
        Button1 = Button(self.testAreaButtonFrame, text="doublePlotTest()", command= lambda: \
                              self.doublePlotTest()).grid(row=0,column=0,columnspan=2,sticky=N)
        Button2 = Button(self.testAreaButtonFrame, text="1_H406_Apr_27.str", command= lambda: \
                              self.openWakeFile("1_H406_Apr_27.str")).grid(row=1,column=0,columnspan=2,sticky=N)
        Button3 = Button(self.testAreaButtonFrame, text="Save Test Tab Figure", command= lambda: \
                              self.saveTestFigure()).grid(row=2,column=0,columnspan=2,sticky=N)
        Button4 = Button(self.testAreaButtonFrame, text="MatPlot Event Record", command= lambda: \
                              self.matPlotEventRecord()).grid(row=4,column=0,columnspan=2, sticky=N)




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

        # *************  The Controllers  **********

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

        self.testArea_MatPlot_Canvas.draw()
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

    def doublePlotTest(self):
        """
        Resolutions:
        aRecord.datalist  - mSec 10800000 mSec in 180 minute session
        cumRecTimes - transforms all times into fractions of a minute so that it can be plotted in minutes
        binStartTimes     - fractions of a minute
        binStartTimesSec  - second
        """
        verbose = True    # local - couple to a global variable and checkbox?
        
        max_x_scale = self.max_x_scale.get()
        max_y_scale = self.max_y_scale.get()

        self.matPlotTestFigure.clf()

        gs = gridspec.GridSpec(nrows = 4, ncols= 3)
        """
        For positioning graphs see:
        https://matplotlib.org/tutorials/intermediate/gridspec.html?highlight=gridspec

        GridSpec defines how the figures fits into the space.
        Here we define a 4 row x 3 col space. The top figure uses a 2row and 3 cols 
        and the bottom two graphs use 1 row and 3 columns. 

        uses numpy two dimensional indexing for a 3x3 array
        >>> x = np.arange(10)
        >>> x
        array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        >>> x[0:2]
        array([0, 1])
        >>> x[0:3]
        array([0, 1, 2])
        """

        aCumRecGraph = self.matPlotTestFigure.add_subplot(gs[0:2,0:3],label="1")  # row [0,1] and col [0,1,2]  
        aBarGraph = self.matPlotTestFigure.add_subplot(gs[2,0:3],label="2")       # row [2]   and col [0,1,2]
        aCocConcGraph = self.matPlotTestFigure.add_subplot(gs[3,0:3],label='3')   # row [3]   and col [0,1,2]

        aRecord = self.recordList[self.fileChoice.get()]        
        aCumRecGraph.set_title(aRecord.fileName)
        aCumRecGraph.set_xlabel('Session Time (min)', fontsize = 12)      
        aCumRecGraph.set_ylabel('Access Lever Responses', fontsize = 12)       
        aCumRecGraph.set_xscale("linear")
        aCumRecGraph.set_yscale("linear")
        aCumRecGraph.set_xlim(0, max_x_scale)  
        aCumRecGraph.set_ylim(0, max_y_scale)

        #aBarGraph.set_xlabel('Session Time (min)', fontsize = 12)      
        aBarGraph.set_ylabel('Dose mg', fontsize = 12)       
        aBarGraph.set_xscale("linear")
        aBarGraph.set_yscale("linear")
        aBarGraph.set_xlim(0, max_x_scale)
        aBarGraph.set_xticklabels("")                 # Suppress tick labels
        aBarGraph.set_ylim(0, 1.5)

        #aCocConcGraph.set_xlabel('Session Time (min)', fontsize = 12)      
        aCocConcGraph.set_ylabel('Cocaine', fontsize = 12)       
        aCocConcGraph.set_xscale("linear")
        aCocConcGraph.set_yscale("linear")
        aCocConcGraph.set_xlim(0, max_x_scale*60000)
        aCocConcGraph.set_xticklabels("")              # Suppress tick labels (because it is in mSec)
        aCocConcGraph.set_ylim(0, 25)

        # make an array of x in fractions of a min.
        # make an array of y - total responses.
        pumpOn = False
        cumRecTimes = []
        cumRecResp = []
        totalDrugBins = 0
        resets = 0
        respTotal = 0
        binPumpTime = 0
        totalDose = 0
        binStartTime = 0        
        binStartTime_mSec = 0
        binEndTime_mSec = 0
        totalBinTime_mSec = 0
        binStartTimes = []
        binStartTimesSec = []
        tickPositionY = [] 
        doseList = []
        pumpTimeList = []
        finalRatio = 0
        trialResponses = 0
        adjustedRespTotal = 0


        # ************   Cummulative Record  *************************

        for pairs in aRecord.datalist:
            if pairs[1] == 'J':                     # Access leverChar = 'J'
                trialResponses = trialResponses + 1
                respTotal = respTotal + 1
                adjustedRespTotal = respTotal - (resets * max_y_scale)
                if adjustedRespTotal == max_y_scale:
                    resets = resets + 1
                    adjustedRespTotal = 0
                x = pairs[0]/60000     # fraction of a min
                cumRecTimes.append(x)
                cumRecResp.append(adjustedRespTotal)       
            elif pairs[1] == 'B':                   # Start of Drug Access
                binStartTime_mSec = pairs[0]                   
                finalRatio = trialResponses
                totalDrugBins = totalDrugBins + 1
                t = pairs[0]/1000    # in seconds
                binStartTimesSec.append(t)
                t = pairs[0]/60000   # fraction of a minute
                binStartTimes.append(t)
                tickPositionY.append(adjustedRespTotal)
            elif pairs[1] == 'P':
                pumpStartTime = pairs[0]
                pumpOn = True
            elif pairs[1] == 'p':
                if pumpOn:
                    pumpDuration = pairs[0]-pumpStartTime
                    binPumpTime = binPumpTime + pumpDuration
                    pumpOn = False
            elif pairs[1] == 'b':   # End of Drug Access Period
                binEndTime_mSec = pairs[0]
                totalBinTime_mSec = totalBinTime_mSec + (binEndTime_mSec - binStartTime_mSec) 
                trialResponses = 0
                pumpTimeList.append(binPumpTime)                
                binDose = (binPumpTime/1000) * 5.0 * 0.025  # pumptime(mSec) * mg/ml * ml/sec)
                totalDose = totalDose + binDose
                doseList.append(binDose)
                #print(binStartTime,binDose)
                binPumpTime = 0

        aCumRec = Line2D(cumRecTimes,cumRecResp, color = 'black', ls = 'solid', drawstyle = 'steps')
        aCumRec.set_lw(1.0)                     # Example of setting and getting linewidth
        # print("line width =", aCumRec.get_linewidth())
        aCumRecGraph.add_line(aCumRec)

        # ********* Draw Ticks *********************

        for i in range(len(binStartTimes)):
            tickX = max_x_scale * 0.01  # make the tick mark proportional (1%) to the X axis length 
            tickY = max_y_scale * 0.02  # make the tick mark proportional (2%) to the Y axis length 
            tickMarkX = [binStartTimes[i], binStartTimes[i] + tickX]
            tickMarkY = [tickPositionY[i], tickPositionY[i] - tickY]
            aTickMark = Line2D(tickMarkX, tickMarkY, color = "red")
            aTickMark.set_lw(1.0) 
            aCumRecGraph.add_line(aTickMark)                          

        # *********** Draw Bar chart of doses **************************

        print("binStartTimes = ", binStartTimes)
        print("doseList =", doseList)
        print("pumpTimeList = ", pumpTimeList)        
        bar_width = 2.0     # The units correspond to Y values, so will get skinny with high max_y_scale.    
        aBarGraph.bar(binStartTimes,doseList,bar_width)

        # ***********  Cocaine Concentration curve **********************
        resolution = 5  # seconds  
        cocConcXYList = model.calculateCocConc(aRecord.datalist,aRecord.cocConc, aRecord.pumpSpeed, resolution)
        
        # cocConcXYList returns a list of [time,conc].
        # The following separates these into two equal length lists to be plotted
        cocConcList = []
        timeList = []
        for i in range(len(cocConcXYList)):
            timeList.append(cocConcXYList[i][0])       # essentially a list in 5 sec intervals           
            cocConcList.append(cocConcXYList[i][1])
            
        cocConcLine = Line2D(timeList,cocConcList, color = 'blue', ls = 'solid')
        aCocConcGraph.add_line(cocConcLine)

        # ***********  Prediction of dose selected by cocaine levels
        # i.e. correlate binDose with the cocaine cencentration at time of the dose

        cocLevels = []
        for i in range(len(binStartTimes)):
            t = int(binStartTimesSec[i]/5)          # Get time corresponding to 5 sec bin in cocConcList
            cocLevel = cocConcList[t]
            #if verbose: print(t,cocLevel,doseList[i])
            cocLevels.append(cocLevel)              # Create a list of cocaine concentrations corresponding to binDose

        r = pearsonr(doseList,cocLevels)
        print("r =",r)

        # **********   Create formated text strings ************************
        averageBinLength = (totalBinTime_mSec/totalDrugBins)/1000
        drugAccessLengthStr = "Access Period = {:.0f} sec".format(averageBinLength)
        totalDrugBinsStr = "Break Point = {}".format(totalDrugBins)
        finalRatioStr = "Final Ratio = {}".format(finalRatio)
        totalDoseStr = "Total Dose = {:.3f} mg".format(totalDose)
        rStr = "r = {:.3f}".format(r[0])
        if verbose:
            print(drugAccessLengthStr)
            print(totalDrugBinsStr)
            print(finalRatioStr)
            print(totalDoseStr)
            print(rStr)

        self.matPlotTestFigure.text(0.1, 0.92, drugAccessLengthStr)
        self.matPlotTestFigure.text(0.1, 0.90, totalDrugBinsStr)
        self.matPlotTestFigure.text(0.1, 0.88, finalRatioStr)        
        self.matPlotTestFigure.text(0.1, 0.86, totalDoseStr)
        self.matPlotTestFigure.text(0.8, 0.18, rStr)

        
        
        # ********************************************************************

        self.matPlotTestFigure.tight_layout()
        self.testArea_MatPlot_Canvas.draw()


    def clearFigure(self):
        print("placeholder()")
        self.threshold_tk_Canvas.delete('all')
        self.matPlotFigure.clf()
        self.threshold_matPlot_Canvas.draw()

    def testStuff2(self):
        print("testStuff2")

    def testStuff3(self):
        print("testStuff3")

    def save_TH_Figure(self):
        """
        None > save a "Figure.png" in current directory.
        The will overwrite current file. Rename if you want to keep it. 

        self.fig is defined in myGUI and used as a container in all pyplot plots.
        This procedure saves the current self.fig to Figure.png
        Changing the extension will change the format:  eg. ".pdf" 

        """
        print("Saving Figure.png")
        # Spawn an Info dialog box?
        self.matPlotFigure.savefig('Figure.png')

    def saveTestFigure(self):
        """
        Define a TestFigure coresponding to Test Tab
        """
        print("saveTestFigure()")


    def draw_TH_Curve(self, params, priceList):
        verbose = True
        if verbose: print("draw_TH_Curve()")
        
        Qzero = params[0]
        k = params[1]
        alpha = params[2]

        fitLine = []
        for x in priceList:
            y = np.e**(np.log10(Qzero)+k*(np.exp(-alpha*Qzero*x)-1))
            fitLine.append(y)
        if verbose: print("CurveFit y values for fitLine", fitLine)
        self.demandCurve = self.matPlotFigure.add_subplot(111)  # initialize a fig and a pair of axes
        self.demandCurve.set_xscale("log")
        self.demandCurve.set_yscale("log")
        self.demandCurve.set_ylabel('Consumption')
        self.demandCurve.set_xlabel('Price')
        self.demandCurve.set_title('Demand Curve\nFrom MatPlotLib')
        self.demandCurve.set_xlim(1, 3000)  # or (1e0, 1e4)
        self.demandCurve.set_ylim(0.01, 3) # 
        self.demandCurve.loglog(priceList, fitLine, color ='red')

        
        # self.demandCurve.scatter(priceList, consumptionList, color = "blue")
        """
        r = pearsonr(consumptionList,fitLine)
        label = "r = {:.3f}, N = {}".format(r[0],len(fitLine))
        self.threshold_tk_Canvas.create_text(300, 10, text=label)
        """


        """
        Bentxley et al. (2013) offers the following formula for 1st derivative so presumably:
        slope = -alpha*Qzero*x*k*np.exp(-alpha*Qzero*x)
        equivalent to:
        slope = -alpha*Qzero*x*k*np.e**(-alpha*Qzero*x)
        """            
        if self.showPmaxLine.get():
            PmaxFound = False
            for x in range(10,1500):
                if (PmaxFound != True):
                    slope = -self.alpha*self.Qzero*x*self.k*np.exp(-self.alpha*self.Qzero*x)
                    if verbose:
                        if (slope < -0.98) and (slope > -1.02):
                            print(x, slope)
                    if slope < -1.0:
                        Pmax = x 
                        PmaxFound = True
            if PmaxFound:
                print(Pmax)
                x = [Pmax,Pmax]
                y = [0.001,3.0]
                pmaxLine = Line2D(x,y, color = 'green')
                self.demandCurve.add_line(pmaxLine)

        """
        # instantiate a second axes that shares the same x-axis as self.demandCurve
        self.responsePlot = self.demandCurve.twinx()
        self.responsePlot.set_ylabel('Responses')
        self.responsePlot.set_ylim(0,250)
        responseLine = Line2D(priceList,responseList, color = 'black')
        self.responsePlot.add_line(responseLine)
        """
        self.threshold_matPlot_Canvas.draw()
        
        
        

    def drawThreshold(self):
        """
        started life as testMatPlotFit()

         #consumptionList = [1.58, 0.69, 1.13, 1.75, 1.50, 0.98, 0.804, 0.891, 0.325, 0.064, 0.09, 0.01]
        """
        verbose = True
        
        MIN_X_SCALE = 0.1
        MAX_X_SCALE = 3000
        MIN_Y_SCALE = 0.001
        MAX_Y_SCALE = 3

        self.Qzero = 1.0       #Set some default
        self.k = self.scale_k.get()
        print("k =",self.k)

        def demandFunction(x,alpha):
            Qzero = self.Qzero
            k = self.k
            y = np.e**(np.log10(Qzero)+k*(np.exp(-alpha*Qzero*x)-1)) 
            return y

        selectedPumpTimesValues = self.pumpTimes.get()
        
        if (selectedPumpTimesValues == 0):
            if verbose: print("Using OMNI pumpTimes")
            TH_PumpTimes = [3.162,1.780,1.000,0.562,0.316,0.188, 0.100,0.056,0.031,0.018,0.010,0.0056]
        else:
            if verbose: print("Using Feather M0 pumpTimes")
            TH_PumpTimes = [3.160,2.000,1.260,0.790,0.500,0.320, 0.200,0.130,0.080,0.050,0.030,0.020]

        priceList = []
        for i in range(12):
            dosePerResponse = TH_PumpTimes[i] * 5.0 * 0.025  # pumptime(mSec) * mg/ml * ml/sec)
            price = round(1/dosePerResponse,2)
            priceList.append(price)
        print("priceList",priceList)

        useMultipleFiles = self.average_TH_FilesVar.get()
        if (useMultipleFiles == True):
            print("Averaging multiple files")
            datalist = []        # Empty - so will not draw an event record
            consumptionList = []
            responseList = []
            # consumptionList = self.getConsumptionList()
            # responseList = self.getResponseList()
        else:
            if verbose: print("Using an individual file")
            aDataRecord = self.recordList[self.fileChoice.get()]
            datalist = aDataRecord.datalist    # Event record needs this.
            consumptionList = aDataRecord.consumptionList
            responseList = aDataRecord.responseList
        print(consumptionList)

        """
        Need to configure threshold_tk_canvas
        width = 600
        height =100
        eventRecord(aCanvas, x_zero, y_zero, x_pixel_width, max_x_scale, dataList, charList, aLabel):
        """
        x_zero = 150
        y_zero = 50
        x_pixel_width = 600
        max_x_scale = 1000

        GraphLib.eventRecord(self.threshold_tk_Canvas, 50, 50, 500, 120, datalist, ["P"], "")

        self.Qzero = (consumptionList[0]+consumptionList[1]+consumptionList[2])/3
        if verbose: print("Use first three bins to calculate Qzero =", self.Qzero)

        #***** Fit the curve - find alpha *******
        param_bounds=([0.001],[0.02])
        fitParams, fitCovariances = curve_fit(demandFunction, priceList, consumptionList, bounds=param_bounds)
        self.alpha = fitParams[0]
        aString = "scipy curve_fit returns alpha = {0:3f}".format(self.alpha)         
        if verbose: print (aString)
        #print (fitCovariances)
        
        #***** Draw Qzero **************
        """
        self.scale_Q_zero.set(Qzero)           
            if self.showOmaxLine.get():            
                x = [MIN_X_SCALE,MAX_X_SCALE]
                y = [Qzero,Qzero]
                #self.matPlotFigure.loglog(x, y, color ='red')
        """
      
        #***** Generate a curvefit line ******
        if verbose: print("Generating curvefit line with Qzero, alpha and k =", self.Qzero, self.alpha, self.k)

        # may want a smoother curve
        #x = np.arange(priceList[0],priceList[11], 0.1)
        #y = demandFunction(priceList,self.Qzero)
        
        TH_params = [self.Qzero,self.k,self.alpha]
        print(TH_params)
        
        self.draw_TH_Curve(TH_params, priceList)


    def load_2L_testFile(self):
        """
        Called from testAreaTab Button2
        """
        print("load_2L-testFile()")

        
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
    def TwoLeverGraphTest2(self):
            label = "TwoLeverGraphTest2"
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
        
    def TwoLeverTest1(self):
            self.textBox.insert("1.0","TwoLeverTest1\n")

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
        
  
    def drawThreshold_old(self):

        """
        Deprecated

        """
        from scipy.optimize import curve_fit
        from scipy.stats.stats import pearsonr

        selectedPumpTimesValues = self.pumpTimes.get()
        if (selectedPumpTimesValues == 0):
            print("OMNI pumpTimes")
            TH_PumpTimes = [3.162,1.780,1.000,0.562,0.316,0.188, 0.100,0.056,0.031,0.018,0.010,0.0056]
        else:
            print("Feather M0 pumpTimes")
            TH_PumpTimes = [3.160,2.000,1.260,0.790,0.500,0.320, 0.200,0.130,0.080,0.050,0.030,0.020]
        print("TH_PumpTimes:", TH_PumpTimes)

        priceList = []
        for i in range(12):
            dosePerResponse = TH_PumpTimes[i] * 5.0 * 0.025  # pumptime(mSec) * mg/ml * ml/sec)
            price = round(1/dosePerResponse,2)
            priceList.append(price)
        print("priceList",priceList)

        useMultipleFiles = self.average_TH_FilesVar.get()
        if (useMultipleFiles == True):
            print("Averaging multiple files")
            datalist = []        # Empty - so will not draw an event record
            consumptionList = []
            responseList = []
            # consumptionList = self.getConsumptionList()
            # responseList = self.getResponseList()
        else:
            print("Using an individual file")
            aDataRecord = self.recordList[self.fileChoice.get()]
            datalist = aDataRecord.datalist    # Event record needs this.
            consumptionList = aDataRecord.consumptionList
            responseList = aDataRecord.responseList

        # Test list generated with k = 2, Qzero = 1.0, alpha = 0.0035
        # but this doesn't 
        #consumptionList = [0.885, 0.8777, 0.865, 0.845, 0.815, 0.773, 0.710, 0.632, 0.524, 0.407, 0.288, 0.214]

        x_zero = 100
        y_zero = 500
        x_pixel_width = 600
        y_pixel_height = 400
        xLogScaler = 3.0
        yLogScaler = 2.0
        max_x_scale = 1000         # price 
        response_max_x_scale = 120 # minutes
        x_divisions = 10
        max_y_scale = 2
        response_max_y_scale = self.respMax.get()
        y_divisions = 5
        leftLabel = True
        drawSymbol = True
        drawLine = False
        startRange = self.rangeBegin.get()
        endRange = self.rangeEnd.get()
        aCanvas = self.thresholdCanvas
        color = "black"
        logX = self.logXVar.get()
        logY = self.logYVar.get()
        x_startValue = 1            # used for Log scale; non-log defaults to 0
        y_startValue = 0.01 
        x_logRange = 3              # 3 Orders of magnitude: 1-1000
        y_logRange = 3              # 3 Orders of magnitude: 0.01-10

        # k_value = math.log10(priceList[endRange]-priceList[startRange])
        # print("k_value",k_value)
        k_value = 4      # See issue 2 above

        x_caption = "Price (responses/mg cocaine)"
        y_caption = "Y"
        self.thresholdCanvas.delete('all')
        if logX : GraphLib.drawLog_X_Axis(aCanvas,x_zero,y_zero,x_pixel_width,x_startValue,x_logRange,x_caption)           
        else:     GraphLib.drawXaxis(aCanvas, x_zero, y_zero, x_pixel_width, max_x_scale, x_divisions, color)
        
        if logY:  GraphLib.drawLog_Y_Axis(aCanvas,x_zero,y_zero,y_pixel_height,y_startValue,y_logRange,y_caption)
        else:     GraphLib.drawYaxis(self.thresholdCanvas, x_zero,y_zero, y_pixel_height, max_y_scale, y_divisions,leftLabel)


        GraphLib.betaTestCurve(aCanvas,x_zero,y_zero,x_pixel_width,y_pixel_height, \
                               x_startValue, y_startValue, x_logRange, y_logRange, max_x_scale, max_y_scale, \
                               priceList, consumptionList, logX, logY, drawLine = False, color = "red")
        truncX = []
        truncY = []

        for t in range(startRange,endRange+1):    
            truncX.append(priceList[t])
            truncY.append(consumptionList[t])

        # Do this stuff if len(truncX) is > 0)
        # Else print message saying no file loaded
        """
            if self.curveFitVar.get():
            numpy_x_list = np.array(truncX)
            numpy_y_list = np.array(truncY)
            popt, pcov = curve_fit(self.demandFunction, numpy_x_list, numpy_y_list)
            alpha = popt[0]
            Qzero = popt[1]
            self.scale_alpha.set(alpha)
            self.scale_Q_zero.set(Qzero)
        else:            
            alpha = self.scale_alpha.get()
            Qzero = self.scale_Q_zero.get()
        """
        numpy_x_list = np.array(truncX)
        numpy_y_list = np.array(truncY)
        # setting k = 4 for everything

        if self.curveFitVar.get():
            popt, pcov = curve_fit(self.demandFunction, numpy_x_list, numpy_y_list)

            alpha = popt[0]
            Qzero = popt[1]
            self.scale_alpha.set(alpha)
            self.scale_Q_zero.set(Qzero)
            
        else:            
            alpha = self.scale_alpha.get()
            Qzero = self.scale_Q_zero.get()
            # popt, pcov = curve_fit(self.demandFunction, numpy_x_list, numpy_y_list)


        # Calculate the correlation using only the points in the truncated list
        fitLine = []
        for i in range(0,len(truncX)):
            y = self.demandFunction(truncX[i],alpha,Qzero)
            fitLine.append(y)
        r = pearsonr(truncY,fitLine)
        label = "r = {:.3f}, N = {}".format(r[0],len(truncX))
        self.thresholdCanvas.create_text(300, 100, text=label)
        GraphLib.betaTestCurve(aCanvas, x_zero, y_zero, x_pixel_width, y_pixel_height, \
                               x_startValue, y_startValue, x_logRange, y_logRange, max_x_scale, max_y_scale, \
                               truncX, fitLine, logX, logY, drawSymbol = False, color = "blue")
                               # priceList, consumptionList, logX, logY, drawLine = False, color = "red")
        
        """
        Look for Pmax
        Bentzley et al. (2013) offers a formula for 1st derivative of the demand curve
        This formula is used to iterate through the line looking for a slope = 1.  
            slope = -alpha*Qzero*x*k*np.exp(-alpha*Qzero*x)
        same as:
            slope = -alpha*Qzero*x*k*np.e**(-alpha*Qzero*x)
        """
        verbose = False
        PmaxFound = False
        for x in range(10,500):
            if (PmaxFound != True):
                slope = -alpha*Qzero*x*k_value*np.exp(-alpha*Qzero*x)
                if verbose: 
                    if (slope < -0.9): print("slope at ",x," = ", slope)                
                if slope < -1.0:
                    Pmax = x 
                    Omax = self.demandFunction(x,alpha,Qzero)
                    PmaxFound = True
        if (PmaxFound):
            if logX:
                x_scaler = x_pixel_width / x_logRange
                PmaxX = GraphLib.get_logX_PixelValue(x_zero, Pmax, x_scaler, x_startValue)
                #PmaxX = (x_zero + (math.log(Pmax,10)*x_scaler)) // 1
            else:
                x_scaler = (x_pixel_width / max_x_scale)
                PmaxX = (x_zero + (Pmax * x_scaler)) // 1
            if logY:
                y_scaler = y_pixel_height / y_logRange
                OmaxY = GraphLib.get_logY_PixelValue(y_zero, Omax, y_scaler, y_startValue)
            else:
                y_scaler = (y_pixel_height / max_y_scale)
                OmaxY = (y_zero - (Omax * y_scaler)) // 1
             
            if self.showPmaxLine.get():
                aCanvas.create_line(PmaxX,y_zero,PmaxX,OmaxY,fill="red")
            if self.showOmaxLine.get():
                aCanvas.create_line(x_zero,OmaxY,PmaxX,OmaxY,fill="blue")
                
            alphaStr = "{:.6f}".format(alpha)
            QzeroStr = "{:.3f}".format(Qzero)
            OmaxStr  = "{:.3f}".format(Omax)
            # startRange and endRange anjusted from array index (0..11) to a [1..12]
            aCanvas.create_text(500, 80, fill="blue", text="Analysis of points "+str(startRange+1)+" to "+str(endRange+1))
            aCanvas.create_text(500, 100, fill="blue", text="Pmax = "+str(Pmax))
            aCanvas.create_text(500, 120, fill="blue", text="Qzero = "+QzeroStr)
            aCanvas.create_text(500, 140, fill="blue", text="Omax = "+OmaxStr)
            aCanvas.create_text(500, 160, fill="blue", text="Alpha = "+alphaStr)
            aCanvas.create_text(500, 180, fill="blue", text="k = "+str(k_value))
        
        GraphLib.eventRecord(self.thresholdCanvas, x_zero+50, y_zero-450, x_pixel_width-50, 120, datalist, ["P"], "")
        
        if self.responseCurveVar.get():
            GraphLib.drawYaxis(self.thresholdCanvas, x_zero+x_pixel_width, y_zero, y_pixel_height, response_max_y_scale, y_divisions, False)
            GraphLib.betaTestCurve(aCanvas,x_zero,y_zero,x_pixel_width,y_pixel_height, \
                                   x_startValue, y_startValue, x_logRange, y_logRange, max_x_scale, response_max_y_scale, \
                                   priceList,responseList, logX, False, drawLine = True, color = "black")

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
       

    def testPmaxCalc(self):
        print("testPmaxCalc deprecated")
        
        
    def injectionTimesText(self):
        aRecord = self.recordList[self.fileChoice.get()]
        injection = 0
        previousInjTime = 0
        self.textBox.insert(END,"Inj  Time (sec) Time (min) interval (sec)\n")
        for pairs in aRecord.datalist:
            if pairs[1] == 'P':
                injection = injection + 1
                secTime = pairs[0]/1000
                minTime = secTime/60
                interval = secTime - previousInjTime
                if injection == 1:
                    tempString = "{0} {1:10.2f} {2:10.2f}".format(injection,secTime,minTime,interval)
                else:
                    tempString = "{0} {1:10.2f} {2:10.2f} {3:10.2f}".format(injection,secTime,minTime,interval)
                self.textBox.insert(END,tempString+"\n")
                previousInjTime = secTime
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
            

    def openWakeFile(self, fileName):      
        if fileName == '':
            fileName = filedialog.askopenfilename(initialdir=self.initialDir)
        # print(fileName)
        if len(fileName) > 0:
            selected = self.fileChoice.get()
            self.recordList[selected].datalist = []
            name = fileName[fileName.rfind('/')+1:]
            path = fileName[0:fileName.rfind('/')+1]
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
            if fileName.find(".str") > 0:
                self.recordList[selected].datalist = stream01.read_str_file(fileName)               
            elif fileName.find(".dat") > 0:
                aFile = open(fileName,'r')
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
        response and consumption lists according - i.e. 12 bins.
        But a PR daatfile could have many more bins which could throw an error.
        So for now, if the bin number will not count higher than 11.

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
        print("Path =", self.initialDir)
    

    def clearTHCanvas(self):
        self.graphCanvas.delete('all')
        self.fig = plt.figure(clear=True)   # clear contents

    def clearGraphTabCanvas(self):
        self.graphCanvas.delete('all')
                                   
    def drawCumulativeRecord(self,aRecord):
        self.clearGraphTabCanvas()
        # print(aRecord)
        # canvas is 800 x 600
        x_zero = 50
        y_zero = 550
        x_pixel_width = 700                               
        y_pixel_height = 500
        x_divisions = 12
        max_x_scale = self.max_x_scale.get()
        if (max_x_scale == 10) or (max_x_scale == 30): x_divisions = 10
        max_y_scale = self.max_y_scale.get()
        y_divisions = 10
        aTitle = aRecord.fileName
        # def cumRecord(aCanvas, x_zero, y_zero, x_pixel_width, y_pixel_height, max_x_scale, max_y_scale, datalist, aTitle)
        GraphLib.drawXaxis(self.graphCanvas, x_zero, y_zero, x_pixel_width, max_x_scale, x_divisions)
        GraphLib.drawYaxis(self.graphCanvas, x_zero, y_zero, y_pixel_height, max_y_scale, y_divisions, True)
        GraphLib.cumRecord(self.graphCanvas, x_zero, y_zero, x_pixel_width, y_pixel_height, max_x_scale, max_y_scale, \
                           aRecord.datalist, self.showBPVar.get(), aTitle)

    def drawEventRecords(self):
        # canvas is 800 x 600
        self.clearGraphTabCanvas()
        x_zero = 50
        x_pixel_width = 700
        x_divisions = 12
        max_x_scale = self.max_x_scale.get()
        if (max_x_scale == 10) or (max_x_scale == 30): x_divisions = 10
        GraphLib.drawXaxis(self.graphCanvas, x_zero, 550, x_pixel_width, max_x_scale, x_divisions)
        y_zero = 30
        box = 0
        # eventRecord(aCanvas, x_zero, y_zero, x_pixel_width, max_x_scale, datalist, charList, aLabel)
        # aTitle = aRecord.fileName
        for record in self.recordList:
            y_zero = y_zero + 40
            box = box + 1
            aTitle = "Box "+str(box)
            GraphLib.eventRecord(self.graphCanvas, x_zero, y_zero, x_pixel_width, max_x_scale, record.datalist, ["P"], aTitle)
        # print("event Records")

    def timeStamps(self,aRecord):
        self.clearGraphTabCanvas()
        aCanvas = self.graphCanvas
        x_zero = 100
        y_zero = 500
        x_pixel_width = 650
        x_divisions = 12
        max_x_scale = self.max_x_scale.get()
        if (max_x_scale == 10) or (max_x_scale == 30): x_divisions = 10
        GraphLib.drawXaxis(aCanvas, x_zero, y_zero, x_pixel_width, max_x_scale, x_divisions, color = "black")
        GraphLib.eventRecord(aCanvas, x_zero, y_zero-400, x_pixel_width, max_x_scale, aRecord.datalist, ["L"], "L1 active")       
        GraphLib.eventRecord(aCanvas, x_zero, y_zero-360, x_pixel_width, max_x_scale, aRecord.datalist, ["A","a"], "A a")
        GraphLib.eventRecord(aCanvas, x_zero, y_zero-340, x_pixel_width, max_x_scale, aRecord.datalist, [">"], "L1 inactive")
        GraphLib.eventRecord(aCanvas, x_zero, y_zero-310, x_pixel_width, max_x_scale, aRecord.datalist, ["J"], "L2 active")
        GraphLib.eventRecord(aCanvas, x_zero, y_zero-290, x_pixel_width, max_x_scale, aRecord.datalist, ["<"], "L2 inactive") 
        GraphLib.eventRecord(aCanvas, x_zero, y_zero-260, x_pixel_width, max_x_scale, aRecord.datalist, ["P","p"], "Pump")
        GraphLib.eventRecord(aCanvas, x_zero, y_zero-230, x_pixel_width, max_x_scale, aRecord.datalist, ["S","s"], "Stim 1")
        GraphLib.eventRecord(aCanvas, x_zero, y_zero-210, x_pixel_width, max_x_scale, aRecord.datalist, ["C","c"], "Stim 2")
        GraphLib.eventRecord(aCanvas, x_zero, y_zero-180, x_pixel_width, max_x_scale, aRecord.datalist, ["=","."], "Lever 1")
        GraphLib.eventRecord(aCanvas, x_zero, y_zero-160, x_pixel_width, max_x_scale, aRecord.datalist, ["-",","], "Lever 2")
        GraphLib.eventRecord(aCanvas, x_zero, y_zero-130,  x_pixel_width, max_x_scale, aRecord.datalist, ["T"], "T")
        GraphLib.eventRecord(aCanvas, x_zero, y_zero-100,  x_pixel_width, max_x_scale, aRecord.datalist, ["F"], "Food Tray")
        GraphLib.eventRecord(aCanvas, x_zero, y_zero-70,  x_pixel_width, max_x_scale, aRecord.datalist, ["B","b"], "Access")
        GraphLib.eventRecord(aCanvas, x_zero, y_zero-50,  x_pixel_width, max_x_scale, aRecord.datalist, ["H","h"], "Houselight")
        GraphLib.eventRecord(aCanvas, x_zero, y_zero-30,  x_pixel_width, max_x_scale, aRecord.datalist, ["G","E"], "Session")
        

    def threshold_text(self):
        aRecord = self.recordList[self.fileChoice.get()]
        aList = aRecord.datalist
        count = ListLib.count_char('L',aList)
        aString = 'Nunber of responses: '+str(count)
        self.textBox.insert(END,aString+"\n")
        
        count = ListLib.count_char('P',aList)
        aString = 'Nunber of injections: '+str(count)
        self.textBox.insert(END,aString+"\n")

        count = ListLib.count_char('B',aList)
        aString = 'Nunber of blocks: '+str(count)
        self.textBox.insert(END,aString+"\n")

        pump_count_list = ListLib.get_pump_count_per_block(aList)
        aString = 'Injections per block: '
        for item in pump_count_list:
            aString = aString + str(item) + ' '
        self.textBox.insert(END,aString+"\n")

        for b in range (12):    
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

    def IntA_event_records(self):
        # canvas is 800 x 600
        self.clearGraphTabCanvas()
        aRecord = self.recordList[self.fileChoice.get()]
        x_zero = 75
        x_pixel_width = 600
        x_divisions = 12
        max_x_scale = 5
        x_divisions = 5
        GraphLib.drawXaxis(self.graphCanvas, x_zero, 550, x_pixel_width, max_x_scale, x_divisions)
        y_zero = 50
        for block in range(12):
            aTitle = str(block+1)
            pump_timestamps = ListLib.get_pump_timestamps(aRecord.datalist,block)
            GraphLib.eventRecord(self.graphCanvas, x_zero, y_zero, x_pixel_width, max_x_scale, pump_timestamps, ["P","p"], aTitle)
            y_zero = y_zero + 45

    def IntA_durations(self):
        '''

        '''
        aCanvas = self.graphCanvas
        self.clearGraphTabCanvas()
        aRecord = self.recordList[self.fileChoice.get()]
        pump_timelist = ListLib.get_pump_duration_list(aRecord.datalist, -1)
        duration_list = []
        for data in pump_timelist:
            duration_list.append(data[2])
        x_zero = 75
        y_zero = 50
        x_pixel_width = 600
        x_divisions = 12
        max_x_scale = 5
        x_divisions = 5
        GraphLib.drawXaxis(aCanvas, x_zero, 550, x_pixel_width, max_x_scale, x_divisions)
        x_scaler = x_pixel_width / (max_x_scale*60*1000)
        y_zero = 50
        block = 0
        for block in range(12):
            x = x_zero
            y = y_zero
            aLabel = str(block+1)
            pump_timelist = ListLib.get_pump_duration_list(aRecord.datalist,block)
            aCanvas.create_text(x_zero-30, y_zero-5, fill="blue", text = aLabel) 
            for data in pump_timelist:
                newX = (x_zero + data[1] * x_scaler // 1)
                aCanvas.create_line(x, y, newX, y)
                height = int(data[2]/40)
                aCanvas.create_line(newX, y, newX, y-height)                        
                x = newX
            y_zero = y_zero + 45
            
        
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
        

    def showHistogram(self,aRecord, clear = True):
        """
        Draws a histogram using the datalist from aRecord.

        To Do: There is another histogram procedure in GraphLib. Should be merged. 

        """
        def drawBar(aCanvas,x,y, pixelHeight, width, color = "black"):
            aCanvas.create_line(x, y, x, y-pixelHeight, fill=color)
            aCanvas.create_line(x, y-pixelHeight, x+width, y-pixelHeight, fill=color)
            aCanvas.create_line(x+width, y-pixelHeight, x+width, y, fill=color)
        
        if clear:
            self.clearGraphTabCanvas()          
        # Draw Event Record
        x_zero = 75
        y_zero = 100
        x_pixel_width = 700
        y_pixel_height = 200
        x_divisions = 12
        y_divisions = 5
        max_x_scale = self.max_x_scale.get()
        if (max_x_scale == 10) or (max_x_scale == 30): x_divisions = 10
        self.graphCanvas.create_text(200, y_zero-50 , fill = "blue", text = aRecord.fileName)
        GraphLib.eventRecord(self.graphCanvas, x_zero, y_zero, x_pixel_width, max_x_scale, aRecord.datalist, ["P"], "")
        # Populate bin array
        binSize = 1   # in minutes
        intervals = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        T1 = 0
        numInj = 0
        numIntervals = 0
        outOfRange = 0
        for pairs in aRecord.datalist:
            if pairs[1] == "P":
                numInj = numInj + 1
                T2 = pairs[0]
                if T1 > 0:
                    numIntervals = numIntervals + 1
                    interval = round((T2-T1)/(binSize*60000),1)   # rounded to a minute with one decimal point
                    index = int(interval)
                    if index < len(intervals)-1:
                        intervals[index] = intervals[index]+1
                    else:
                        outOfRange = outOfRange+1
                T1 = T2
        tempStr = "Number of Injections = "+str(numInj)
        self.graphCanvas.create_text(450, y_zero-50, fill = "blue", text = tempStr)
        # print("Number of Inter-injection Intervals =",numIntervals)
        print("Inter-injection Intervals = ",intervals)
        x_zero = 75
        y_zero = 450
        x_pixel_width = 400
        y_pixel_height = 300 
        max_x_scale = 20
        max_y_scale = 20
        x_divisions = 20
        y_divisions = max_y_scale
        labelLeft = True
        GraphLib.drawXaxis(self.graphCanvas, x_zero, y_zero, x_pixel_width, max_x_scale, x_divisions, color = "black")
        GraphLib.drawYaxis(self.graphCanvas, x_zero, y_zero, y_pixel_height, max_y_scale, y_divisions, labelLeft, color = "black")
        # intervals = [0,1,2,3,4,5,6,5,4,3,2,1,0,0,0,0,0,0,0,1]  #Used for test without loading a file
        unitPixelHeight = int(y_pixel_height/y_divisions)
        width = int(x_pixel_width/len(intervals))
        for i in range(len(intervals)):           
            x = x_zero + (i*width)
            drawBar(self.graphCanvas,x,y_zero,intervals[i]*unitPixelHeight,width)
        #Draw OutOfRange Bar
        x = x_zero + (len(intervals)*width) + 20
        drawBar(self.graphCanvas,x,y_zero,outOfRange*unitPixelHeight,width)
        tempStr = "Each Bin = "+str(binSize)+" minute"
        self.graphCanvas.create_text(250, y_zero+50, fill = "blue", text = tempStr)
        

    def showModel(self,aRecord, resolution = 60, aColor = "blue", clear = True, max_y_scale = 25):
        if clear:
            self.clearGraphTabCanvas()
        x_zero = 75
        y_zero = 350
        x_pixel_width = 700
        y_pixel_height = 200
        x_divisions = 12
        y_divisions = 5
        max_x_scale = self.max_x_scale.get()
        if (max_x_scale == 10) or (max_x_scale == 30): x_divisions = 10
        # max_y_scale = self.max_y_scale.get()
        # max_y_scale = 25
        GraphLib.eventRecord(self.graphCanvas, x_zero, 100, x_pixel_width, max_x_scale, aRecord.datalist, ["P"], "Test")
        GraphLib.drawXaxis(self.graphCanvas, x_zero, y_zero, x_pixel_width, max_x_scale, x_divisions, color = "red")
        GraphLib.drawYaxis(self.graphCanvas, x_zero, y_zero, y_pixel_height, max_y_scale, y_divisions, True, color = "blue")
        x_scaler = x_pixel_width / (max_x_scale*60*1000)
        y_scaler = y_pixel_height / max_y_scale
        cocConcXYList = model.calculateCocConc(aRecord.datalist,aRecord.cocConc, aRecord.pumpSpeed, resolution)
        # print(modelList)
        x = x_zero
        y = y_zero
        totalConc = 0
        totalRecords = 0
        startAverageTime = 10 * 60000    # 10 min
        endAverageTime = 120 * 60000     # 120 min
        for pairs in cocConcXYList:
            if pairs[0] >= startAverageTime:
                if pairs[0] < endAverageTime:
                    totalRecords = totalRecords + 1
                    totalConc = totalConc + pairs[1]
            concentration = round(pairs[1],2)
            newX = x_zero + pairs[0] * x_scaler // 1
            newY = y_zero - concentration * y_scaler // 1
            self.graphCanvas.create_line(x, y, newX, newY, fill= aColor)
            # self.graphCanvas.create_oval(newX-2, newY-2, newX+2, newY+2, fill=aColor)
            x = newX
            y = newY
        self.graphCanvas.create_text(300, 400, fill = "blue", text = aRecord.fileName)
        """
        dose = 2.8*aRecord.cocConc * aRecord.pumpSpeed
        tempStr = "Duration (2.8 sec) * Pump Speed ("+str(aRecord.pumpSpeed)+" ml/sec) * cocConc ("+str(aRecord.cocConc)+" mg/ml) = Unit Dose "+ str(round(dose,3))+" mg/inj"
        self.graphCanvas.create_text(300, 450, fill = "blue", text = tempStr)
        """
        averageConc = round((totalConc/totalRecords),3)
        # draw average line
        X1 = x_zero + (startAverageTime * x_scaler) // 1
        Y  = y_zero-((averageConc) * y_scaler) // 1
        X2 = x_zero + (endAverageTime * x_scaler) // 1
        self.graphCanvas.create_line(X1, Y, X2, Y, fill= "red")
        tempStr = "Average Conc (10-120 min): "+str(averageConc)
        self.graphCanvas.create_text(500, Y, fill = "red", text = tempStr)
        

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
        testRecord1 = DataRecord([],"5 sec") 
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
        testRecord2 = DataRecord([],"50 sec") 
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
        testRecord3 = DataRecord([],"90 sec") 
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
        self.textBox.insert("1.0","***************************\n")

    def periodic_check(self):
        thisTime = datetime.now()
        self.clockTimeStringVar.set(thisTime.strftime("%H:%M:%S"))        
        self.root.after(100, self.periodic_check)               

    def go(self):
        self.root.after(100, self.periodic_check)
        self.root.mainloop()
        

if __name__ == "__main__":
    sys.exit(main())

