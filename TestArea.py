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
        
