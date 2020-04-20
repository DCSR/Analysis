"""
This file contains all procedures called for the Test Area Tab

Index:

self.fig1_2L_PR()

self.TwoLeverFig()

self.matPlotEventRecord()

self.bin_HD_Records()

self.bin_HD_10SecCount()

self.load_2L_PR_Files()

"""
import model

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


def fig1_2L_PR(fig, recordList):
    """
    This function was written in a separate branch to draw a figure  the 2L-PR-HD paper

    "Load 2L-PR Files loads four specific files.
    This function uses the first three files and assumes that
    File 1: 8_H383_Mar_10.str  - 1L-FR - 20 injection max
    File 2: 8_H383_Mar_10.str  - 1L-HD - 3h session
    File 3: 8_H383_Mar_10.str  - 2L-FR-HD 4h session

    A radio button (showOn_tkCanvas) controls whether the figure is drawn to a canvas or to a separate window
    that can be saved as a prn file.
    
    """
    print("fig_2L_PR() called in TestArea")
    

    gs = gridspec.GridSpec(nrows = 30, ncols= 1)

    max_x_scale = 360
    xLabels = ['0','30','60','90','120','150','180','210','240','270','300','330','360','390']

    # Spacing of each subplot 
    eventRecord0 = fig.add_subplot(gs[0,0],label="1")  # row [0] and col [0]]
    cocGraph0 = fig.add_subplot(gs[2:8,0],label='2')   # rows 2 - 7, col 0
    eventRecord1 = fig.add_subplot(gs[10,0],label="3")  # row [10] and col [0]]
    cocGraph1 = fig.add_subplot(gs[12:18,0],label='4')   # rows 2 - 7, col 0
    eventRecord2 = fig.add_subplot(gs[20,0],label="5")  # row [10] and col [0]]
    accessLine = fig.add_subplot(gs[21,0],label="5")  # row [11] and col [0]]
    eventRecordL2 = fig.add_subplot(gs[22,0],label="5")  # row [12] and col [0]]
    cocGraph2 = fig.add_subplot(gs[24:30,0],label='6')   # rows 2 - 7, col 0

    # *** Top ***
    
    injNum = 0
    injTimeList = []       
    record0 = recordList[0]
    for pairs in record0.datalist:
        if pairs[1] == 'P':                     
            injNum = injNum + 1
            injTimeList.append(pairs[0]/60000)  # Min
    eventRecord0.axes.get_yaxis().set_visible(False)
    eventRecord0.axes.get_xaxis().set_ticklabels([])           # suppress tick labels
    eventRecord0.axes.get_yaxis().set_ticklabels([])
    eventRecord0.text(-0.05,0.0, 'FR1', ha = 'center', transform=eventRecord0.transAxes, color = 'black')
    eventRecord0.set_xlim(0,max_x_scale)
    eventRecord0.xaxis.set_major_locator(MaxNLocator(7))       # six major intervals
    eventRecord0.xaxis.set_minor_locator(AutoMinorLocator(4))  # 5 ticks per interval
    eventRecord0.spines['left'].set_color('none')
    eventRecord0.spines['left'].set_position(('axes', -0.02))
    eventRecord0.spines['top'].set_color('none')
    eventRecord0.spines['right'].set_color('none')
    eventRecord0.set_ylim(0.01, 1)
    eventRecord0.eventplot(injTimeList,lineoffsets = 0, linelengths=1.5, colors = "black")
    # ***********  Cocaine Concentration curve **********************
    cocGraph0.patch.set_facecolor("none")
    cocGraph0.spines['left'].set_position(('axes', -0.02))
    cocGraph0.spines['top'].set_color('none')
    cocGraph0.spines['right'].set_color('none')
    #cocGraph0.set_xlabel('Session Time (min)', fontsize = 12)
    #cocGraph0.xaxis.labelpad = 20
    cocGraph0.set_ylabel('Cocaine', fontsize = 12)
    #cocGraph0.yaxis.labelpad = 15
    cocGraph0.set_xscale("linear")
    cocGraph0.set_yscale("linear")
    cocGraph0.set_xlim(0, max_x_scale*60000)
    cocGraph0.xaxis.set_major_locator(ticker.LinearLocator(int(max_x_scale/30)+1))
    cocGraph0.yaxis.set_major_locator(MaxNLocator(6))       # five major intervals
    cocGraph0.yaxis.set_minor_locator(AutoMinorLocator(4))  # 5 ticks per interval       
    cocGraph0.set_xticklabels(xLabels) 
    cocGraph0.set_ylim(0, 25)
    
    resolution = 5  # seconds
    cocConcXYList = model.calculateCocConc(record0.datalist,record0.cocConc, record0.pumpSpeed, resolution)
    # cocConcXYList returns a list of [time,conc].
    # The following separates these into two equal length lists to be plotted
    cocConcList = []
    timeList = []
    for i in range(len(cocConcXYList)):
        timeList.append(cocConcXYList[i][0])       # essentially a list in 5 sec intervals           
        cocConcList.append(cocConcXYList[i][1])
        
    cocConcLine = Line2D(timeList,cocConcList, color = 'black', ls = 'solid')
    cocGraph0.text(0.85,0.5, '1L-FR1 (20 inj max)', ha = 'center', transform=cocGraph0.transAxes, fontsize = 14)
    cocGraph0.add_line(cocConcLine)

    # *** Middle ***
    injNum = 0
    injTimeList = []       
    record1 = recordList[1]
    for pairs in record1.datalist:
        if pairs[1] == 'P':                     
            injNum = injNum + 1
            injTimeList.append(pairs[0]/60000)  # Min
    eventRecord1.axes.get_yaxis().set_visible(False)
    eventRecord1.axes.get_xaxis().set_ticklabels([])           # suppress tick labels
    eventRecord1.axes.get_yaxis().set_ticklabels([])
    eventRecord1.text(-0.05,0.0, 'HD', ha = 'center', transform=eventRecord1.transAxes, color = 'black')
    eventRecord1.set_xlim(0,max_x_scale)
    eventRecord1.xaxis.set_major_locator(MaxNLocator(7))       # six major intervals
    eventRecord1.xaxis.set_minor_locator(AutoMinorLocator(4))  # 5 ticks per interval
    eventRecord1.spines['left'].set_color('none')
    eventRecord1.spines['left'].set_position(('axes', -0.02))
    eventRecord1.spines['top'].set_color('none')
    eventRecord1.spines['right'].set_color('none')
    eventRecord1.set_ylim(0.01, 1)
    eventRecord1.eventplot(injTimeList,lineoffsets = 0, linelengths=1.5, colors = "black")
   
    # ***********  Cocaine Concentration curve **********************
    cocGraph1.patch.set_facecolor("none")
    cocGraph1.spines['left'].set_position(('axes', -0.02))
    cocGraph1.spines['top'].set_color('none')
    cocGraph1.spines['right'].set_color('none')
    #cocGraph1.set_xlabel('Session Time (min)', fontsize = 12)
    #cocGraph1.xaxis.labelpad = 20
    cocGraph1.set_ylabel('Cocaine', fontsize = 12)
    #cocGraph1.yaxis.labelpad = 15
    cocGraph1.set_xscale("linear")
    cocGraph1.set_yscale("linear")
    cocGraph1.set_xlim(0, max_x_scale*60000)
    cocGraph1.xaxis.set_major_locator(ticker.LinearLocator(int(max_x_scale/30)+1))
    cocGraph1.yaxis.set_major_locator(MaxNLocator(6))       # five major intervals
    cocGraph1.yaxis.set_minor_locator(AutoMinorLocator(4))  # 5 ticks per interval       
    cocGraph1.set_xticklabels(xLabels) 
    cocGraph1.set_ylim(0, 25)
   
    resolution = 5  # seconds
    cocConcXYList = model.calculateCocConc(record1.datalist,record1.cocConc, record1.pumpSpeed, resolution)
    # cocConcXYList returns a list of [time,conc].
    # The following separates these into two equal length lists to be plotted
    cocConcList = []
    timeList = []
    for i in range(len(cocConcXYList)):
        timeList.append(cocConcXYList[i][0])       # essentially a list in 5 sec intervals           
        cocConcList.append(cocConcXYList[i][1])
        
    cocConcLine = Line2D(timeList,cocConcList, color = 'black', ls = 'solid')
    cocGraph1.text(0.85,0.5, '1L-HD (3h)', ha = 'center', transform=cocGraph1.transAxes, fontsize = 14)
    cocGraph1.add_line(cocConcLine)

    # *** Bottom ***
    injNum = 0
    injTimeList = []       
    record2 = recordList[2]
    for pairs in record2.datalist:
        if pairs[1] == 'J':                    
            injNum = injNum + 1
            injTimeList.append(pairs[0]/60000)  # Min
    eventRecord2.axes.get_yaxis().set_visible(False)
    eventRecord2.axes.get_xaxis().set_ticklabels([])           # suppress tick labels
    eventRecord2.axes.get_yaxis().set_ticklabels([])
    eventRecord2.text(-0.05,0.0, 'FR1', ha = 'center', transform=eventRecord2.transAxes, color = 'black')
    eventRecord2.set_xlim(0,max_x_scale)
    eventRecord2.xaxis.set_major_locator(MaxNLocator(7))       # six major intervals
    eventRecord2.xaxis.set_minor_locator(AutoMinorLocator(4))  # 5 ticks per interval
    eventRecord2.spines['left'].set_color('none')
    eventRecord2.spines['left'].set_position(('axes', -0.02))
    eventRecord2.spines['top'].set_color('none')
    eventRecord2.spines['right'].set_color('none')
    eventRecord2.set_ylim(0.01, 1)
    eventRecord2.eventplot(injTimeList,lineoffsets = 0, linelengths=1.5, colors = "black")


    # Access ["=","."], "Lever 1")
    # ["-",","], "Lever 2")

    accessList = [0]
    timeList = [0]
    access = False
    record2 = recordList[2]
    for pairs in record2.datalist:
        if pairs[1] == ',':
            #draw horizontal line to timestamp then draw vertical line up
            timeList.append(pairs[0]/60000)  # Min
            accessList.append(access)
            access = True
            timeList.append(pairs[0]/60000)  # Min
            accessList.append(access)
        elif pairs[1] == '-':
            #draw horizontal line to timestamp then draw vertical line down
            timeList.append(pairs[0]/60000)  # Min
            accessList.append(access)
            access = False
            timeList.append(pairs[0]/60000)  # Min
            accessList.append(access)
        elif pairs[1] == 'E':    # End of session
            timeList.append(pairs[0]/60000)  # Min
            accessList.append(access)
            access = False
            timeList.append(pairs[0]/60000)  # Min
            accessList.append(access)
            
    accessLine.axes.get_yaxis().set_visible(False)
    accessLine.axes.get_xaxis().set_ticklabels([])           # suppress tick labels
    accessLine.axes.get_yaxis().set_ticklabels([])
    accessLine.text(-0.05,0.0, 'Access', ha = 'center', transform=accessLine.transAxes, color = 'black')
    accessLine.set_xlim(0,max_x_scale)
    accessLine.xaxis.set_major_locator(MaxNLocator(7))       # six major intervals
    accessLine.xaxis.set_minor_locator(AutoMinorLocator(4))  # 5 ticks per interval
    accessLine.spines['left'].set_color('none')
    accessLine.spines['left'].set_position(('axes', -0.02))
    accessLine.spines['top'].set_color('none')
    accessLine.spines['right'].set_color('none')
    accessLine.set_ylim(0, 1)
    accessLine.set_xlim(0,360)
    accessL1 = Line2D(timeList,accessList, color = 'black', ls = 'solid')
    accessLine.add_line(accessL1)

    injNum = 0
    injTimeList = []       
    record2 = recordList[2]
    for pairs in record2.datalist:
        if pairs[1] == 'P':                    
            injNum = injNum + 1
            injTimeList.append(pairs[0]/60000)  # Min
    eventRecordL2.axes.get_yaxis().set_visible(False)
    eventRecordL2.axes.get_xaxis().set_ticklabels([])           # suppress tick labels
    eventRecordL2.axes.get_yaxis().set_ticklabels([])
    eventRecordL2.text(-0.05,0.0, 'HD', ha = 'center', transform=eventRecordL2.transAxes, color = 'black')
    eventRecordL2.set_xlim(0,max_x_scale)
    eventRecordL2.xaxis.set_major_locator(MaxNLocator(7))       # six major intervals
    eventRecordL2.xaxis.set_minor_locator(AutoMinorLocator(4))  # 5 ticks per interval
    eventRecordL2.spines['left'].set_color('none')
    eventRecordL2.spines['left'].set_position(('axes', -0.02))
    eventRecordL2.spines['top'].set_color('none')
    eventRecordL2.spines['right'].set_color('none')
    eventRecordL2.set_ylim(0.01, 1)
    eventRecordL2.eventplot(injTimeList,lineoffsets = 0, linelengths=1.5, colors = "black")
   
    # ***********  Cocaine Concentration curve **********************
    cocGraph2.patch.set_facecolor("none")
    cocGraph2.spines['left'].set_position(('axes', -0.02))
    cocGraph2.spines['top'].set_color('none')
    cocGraph2.spines['right'].set_color('none')
    cocGraph2.set_xlabel('Session Time (min)', fontsize = 12)
    #cocGraph2.xaxis.labelpad = 20
    cocGraph2.set_ylabel('Cocaine', fontsize = 12)
    #cocGraph2.yaxis.labelpad = 15
    cocGraph2.set_xscale("linear")
    cocGraph2.set_yscale("linear")
    cocGraph2.set_xlim(0, max_x_scale*60000)
    cocGraph2.xaxis.set_major_locator(ticker.LinearLocator(int(max_x_scale/30)+1))
    cocGraph2.yaxis.set_major_locator(MaxNLocator(6))       # five major intervals
    cocGraph2.yaxis.set_minor_locator(AutoMinorLocator(4))  # 5 ticks per interval
    cocGraph2.set_xticklabels(xLabels) 
    cocGraph2.set_ylim(0, 25)
    
    resolution = 5  # seconds
    cocConcXYList = model.calculateCocConc(record2.datalist,record2.cocConc, record2.pumpSpeed, resolution)
    # cocConcXYList returns a list of [time,conc].
    # The following separates these into two equal length lists to be plotted
    cocConcList = []
    timeList = []
    for i in range(len(cocConcXYList)):
        timeList.append(cocConcXYList[i][0])       # essentially a list in 5 sec intervals           
        cocConcList.append(cocConcXYList[i][1])
        
    cocConcLine = Line2D(timeList,cocConcList, color = 'black', ls = 'solid')
    cocGraph2.text(0.85,0.5, '2L-FR1-HD (4h)', ha = 'center', transform=cocGraph2.transAxes, fontsize = 14)
    cocGraph2.add_line(cocConcLine)
    
    # if (self.showOn_tkCanvas.get()):
    #    self.testArea_MatPlot_Canvas.draw()
    # else:
    #    plt.show()


def TwoLeverFig(fig,aRecord,levers,max_x_scale,max_y_scale):
    """
    To Do: select X axis limit from radio button.

    1L-PR uses L1 ("L") as PR lever
    1L-PR uses only one block ("B")

    2L-PR uses L2 ("J") as PR lever and L1 ("L") as HD lever
    2L_PR uses "B" to signal access to HD

    Resolutions:
    aRecord.datalist  - mSec 10800000 mSec in 180 minute session
    cumRecTimes - transforms all times into fractions of a minute so that it can be plotted in minutes
    binStartTimes     - fractions of a minute
    binStartTimesSec  - second

    testAreaFigureFrame    - tk container (a Frame)
    self.matPlotTestFigure          - the thing that axes and lines are drawn on        
    self.threshold_tk_Canvas        - drawing space for things like event records
    self.testArea_matPlot_Canvas    - container for the MatPlotLib Figure
                                    - This is the thing that gets redrawn after things are changed.
    """
    verbose = True    # local - couple to a global variable and checkbox?
    PR_lever_Char = 'J'
    if levers == 1:
         PR_lever_Char = 'L'
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

    showLabels = False

    aCumRecGraph = fig.add_subplot(gs[0:2,0:3],label="1")  # row [0,1] and col [0,1,2]  
    aBarGraph = fig.add_subplot(gs[2,0:3],label="2")       # row [2]   and col [0,1,2]
    aCocConcGraph = fig.add_subplot(gs[3,0:3],label='3')   # row [3]   and col [0,1,2]
    
    # Coc Conc graph in mSec so have to do the X axis labels maunally
    xLabels = ['0','30','60','90','120','150','180','210','240','270','300','330','360','390']
    
   
    if (showLabels):
        aCumRecGraph.set_title(aRecord.fileName)
        
    #aCumRecGraph.set_xlabel('Session Time (min)', fontsize = 12)
    aCumRecGraph.patch.set_facecolor("none")
    aCumRecGraph.spines['top'].set_color('none')
    aCumRecGraph.spines['right'].set_color('none')
    aCumRecGraph.set_ylabel('PR Lever Responses', fontsize = 12)
    #aCumRecGraph.yaxis.labelpad = 15
    aCumRecGraph.set_xscale("linear")
    aCumRecGraph.set_yscale("linear")
    aCumRecGraph.set_xlim(0, max_x_scale)  
    aCumRecGraph.set_ylim(0, max_y_scale)
    aCumRecGraph.xaxis.set_major_locator(MultipleLocator(30))       # 30 min intervals
    aCumRecGraph.spines['left'].set_position(('axes', -0.02))

    #aBarGraph.set_xlabel('Session Time (min)', fontsize = 12)
    
    aBarGraph.patch.set_facecolor("none")
    aBarGraph.spines['left'].set_position(('axes', -0.02))
    aBarGraph.spines['top'].set_color('none')
    aBarGraph.spines['right'].set_color('none')
    aBarGraph.set_ylabel('Dose (mg)', fontsize = 12)
    #aBarGraph.yaxis.labelpad = 15
    aBarGraph.set_xscale("linear")
    aBarGraph.set_yscale("linear")
    aBarGraph.set_xlim(0, max_x_scale)
    aBarGraph.set_ylim(0, 1.5)
    aBarGraph.xaxis.set_major_locator(MultipleLocator(30))       # 30 min intervals
    #aBarGraph.set_xticklabels(xLabels)                 # Suppress tick labels

    aCocConcGraph.patch.set_facecolor("none")
    aCocConcGraph.spines['left'].set_position(('axes', -0.02))
    aCocConcGraph.spines['top'].set_color('none')
    aCocConcGraph.spines['right'].set_color('none')
    aCocConcGraph.set_xlabel('Session Time (min)', fontsize = 12)
    #aCocConcGraph.xaxis.labelpad = 20
    aCocConcGraph.set_ylabel('Cocaine', fontsize = 12)
    #aCocConcGraph.yaxis.labelpad = 15
    aCocConcGraph.set_xscale("linear")
    aCocConcGraph.set_yscale("linear")
    aCocConcGraph.set_xlim(0, max_x_scale*60000)
    aCocConcGraph.xaxis.set_major_locator(ticker.LinearLocator(int(max_x_scale/30)+1))
    aCocConcGraph.set_xticklabels(xLabels) 
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
        if pairs[1] == PR_lever_Char:           # 1l = 'L'; 2L = 'J'
            trialResponses = trialResponses + 1
            respTotal = respTotal + 1
            adjustedRespTotal = respTotal - (resets * max_y_scale)
            if adjustedRespTotal == max_y_scale:
                resets = resets + 1
                adjustedRespTotal = 0
            x = pairs[0]/60000     # fraction of a min
            cumRecTimes.append(x)
            cumRecResp.append(adjustedRespTotal)       
        elif pairs[1] == 'B':                   # If 2L then "B" controls tick mark
            if levers == 2:
                binStartTime_mSec = pairs[0]                   
                finalRatio = trialResponses
                totalDrugBins = totalDrugBins + 1
                t = pairs[0]/1000    # in seconds
                binStartTimesSec.append(t)
                t = pairs[0]/60000   # fraction of a minute
                binStartTimes.append(t)
                tickPositionY.append(adjustedRespTotal)
        elif pairs[1] == 'P':                   # If 1L then "P" controls tick mark
            if levers == 1:
                binStartTime_mSec = pairs[0]                   
                finalRatio = trialResponses
                totalDrugBins = totalDrugBins + 1
                t = pairs[0]/1000    # in seconds
                binStartTimesSec.append(t)
                t = pairs[0]/60000   # fraction of a minute
                binStartTimes.append(t)
                tickPositionY.append(adjustedRespTotal)
            pumpStartTime = pairs[0]
            pumpOn = True
        elif pairs[1] == 'p':
            if pumpOn:
                pumpDuration = pairs[0]-pumpStartTime
                binPumpTime = binPumpTime + pumpDuration
                pumpOn = False
                if levers == 1:
                    trialResponses = 0
                    pumpTimeList.append(binPumpTime)                
                    binDose = (binPumpTime/1000) * 5.0 * 0.025  # pumptime(mSec) * mg/ml * ml/sec)
                    totalDose = totalDose + binDose
                    doseList.append(binDose)
                    #print(binStartTime,binDose)
                    binPumpTime = 0
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
        aTickMark = Line2D(tickMarkX, tickMarkY, color = "black")
        aTickMark.set_lw(1.0) 
        aCumRecGraph.add_line(aTickMark)                          

    # *********** Draw Bar chart of doses **************************
    """ binStartTimes are fractions of a minute.
        The problem was that the first bar was too thin because it was too close to the edge.
        Here, they are rounded up to an integer and shift 1 min which helps.
        There is still an issue that some of the bars are a slightly different width. 
        Perhaps this has to do with the size of the x scale
    """
    binStartTimesInt = []
    for num in binStartTimes:
        binStartTimesInt.append(round(num)+1)

    print("binStartTimes = ", binStartTimes)
    print("binStartTimesInt = ", binStartTimesInt)
    print("doseList =", doseList)
    print("pumpTimeList = ", pumpTimeList)        
    bar_width = 2.5     # The units correspond to X values, so will get skinny with high max_x_scale.

    aBarGraph.bar(binStartTimesInt,doseList,bar_width, color = "black")

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
        
    cocConcLine = Line2D(timeList,cocConcList, color = 'black', ls = 'solid')
    aCocConcGraph.add_line(cocConcLine)

    # ***********  Prediction of dose selected by cocaine levels
    # i.e. correlate binDose with the cocaine cencentration at time of the dose

    cocLevels = []
    for i in range(len(binStartTimes)):
        t = int(binStartTimesSec[i]/5)          # Get time corresponding to 5 sec bin in cocConcList
        cocLevel = cocConcList[t]
        #if verbose: print(t,cocLevel,doseList[i])
        cocLevels.append(cocLevel)              # Create a list of cocaine concentrations corresponding to binDose
    

    # **********   Create formated text strings ************************
    averageBinLength = (totalBinTime_mSec/totalDrugBins)/1000
    drugAccessLengthStr = "Access Period = {:.0f} sec".format(averageBinLength)
    totalDrugBinsStr = "Break Point = {}".format(totalDrugBins)
    finalRatioStr = "Final Ratio = {}".format(finalRatio)
    totalDoseStr = "Total Dose = {:.3f} mg".format(totalDose)
    rStr = ""
    # r = pearsonr(doseList,cocLevels)
    # print("r =",r)
    # rStr = "r = {:.3f}".format(r[0])
    if verbose:
        print(drugAccessLengthStr)
        print(totalDrugBinsStr)
        print(finalRatioStr)
        print(totalDoseStr)
        print(rStr)
    if (showLabels):
        self.matPlotTestFigure.text(0.1, 0.96, drugAccessLengthStr)
        self.matPlotTestFigure.text(0.1, 0.94, totalDrugBinsStr)
        self.matPlotTestFigure.text(0.1, 0.92, finalRatioStr)        
        self.matPlotTestFigure.text(0.1, 0.90, totalDoseStr)
        self.matPlotTestFigure.text(0.8, 0.18, rStr)

    # ********************************************************************

    





    
