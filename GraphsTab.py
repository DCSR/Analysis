"""
This file contains all the precedures called from the GraphsTab

There are several ways to graph stuff. Much of what is in this files draws to a ttk canvas,
in this case self.graphCanvas.

The other way is to use matplotlib.  

Index: (alphabetical)

cocaineModel()         OK

cumulativeRecord()     OK

eventRecords()         OK

eventRecordsIntA()     OK

histogram()            OK

pumpDurationIntA()     OK

timeStamps()           OK


"""

import GraphLib
import model
import ListLib

def cocaineModel(aCanvas,aRecord,max_x_scale,resolution = 60, aColor = "blue", clear = True, max_y_scale = 20):
    if clear:
        aCanvas.delete('all')
    x_zero = 75
    y_zero = 350
    x_pixel_width = 500 #700
    y_pixel_height = 150 #200
    x_divisions = 12
    y_divisions = 4
    if (max_x_scale == 10) or (max_x_scale == 30): x_divisions = 10
    GraphLib.eventRecord(aCanvas, x_zero+5, 185, x_pixel_width, max_x_scale, aRecord.datalist, ["P"], "")
    GraphLib.drawXaxis(aCanvas, x_zero, y_zero, x_pixel_width, max_x_scale, x_divisions, color = "black")
    GraphLib.drawYaxis(aCanvas, x_zero, y_zero, y_pixel_height, max_y_scale, y_divisions, True, color = "black")
    x_scaler = x_pixel_width / (max_x_scale*60*1000)
    y_scaler = y_pixel_height / max_y_scale
    cocConcXYList = model.calculateCocConc(aRecord.datalist,aRecord.cocConc,aRecord.pumpSpeed,resolution)
    # print(modelList)
    x = x_zero
    y = y_zero
    totalConc = 0
    totalRecords = 0
    startAverageTime = 10 * 60000    # 10 min
    endAverageTime = 180 * 60000     # 120 min
    for pairs in cocConcXYList:
        if pairs[0] >= startAverageTime:
            if pairs[0] < endAverageTime:
                totalRecords = totalRecords + 1
                totalConc = totalConc + pairs[1]
        concentration = round(pairs[1],2)
        newX = x_zero + pairs[0] * x_scaler // 1
        newY = y_zero - concentration * y_scaler // 1
        aCanvas.create_line(x, y, newX, newY, fill= aColor)
        # aCanvas.create_oval(newX-2, newY-2, newX+2, newY+2, fill=aColor)
        x = newX
        y = newY
    aCanvas.create_text(300, 400, fill = "blue", text = aRecord.fileName)
    """
    dose = 2.8*aRecord.cocConc * aRecord.pumpSpeed
    tempStr = "Duration (2.8 sec) * Pump Speed ("+str(aRecord.pumpSpeed)+" ml/sec) * cocConc ("+str(aRecord.cocConc)+" mg/ml) = Unit Dose "+ str(round(dose,3))+" mg/inj"
    aCanvas.create_text(300, 450, fill = "blue", text = tempStr)
    """
    averageConc = round((totalConc/totalRecords),3)
    # draw average line
    X1 = x_zero + (startAverageTime * x_scaler) // 1
    Y  = y_zero-((averageConc) * y_scaler) // 1
    X2 = x_zero + (endAverageTime * x_scaler) // 1
    # aCanvas.create_line(X1, Y, X2, Y, fill= "red")
    # tempStr = "Average Conc (10-180 min): "+str(averageConc)
    # aCanvas.create_text(500, Y, fill = "red", text = tempStr)


def cumulativeRecord(aCanvas,aRecord,showBPVar,max_x_scale,max_y_scale):
    aCanvas.delete('all')
    # graphCanvas is 800 x 600
    x_zero = 50
    y_zero = 550
    x_pixel_width = 700                               
    y_pixel_height = 500
    x_divisions = 12
    if (max_x_scale == 10) or (max_x_scale == 30): x_divisions = 10
    y_divisions = 10
    aTitle = aRecord.fileName
    GraphLib.drawXaxis(aCanvas, x_zero, y_zero, x_pixel_width, max_x_scale, x_divisions)
    GraphLib.drawYaxis(aCanvas, x_zero, y_zero, y_pixel_height, max_y_scale, y_divisions, True)
    GraphLib.cumRecord(aCanvas, x_zero, y_zero, x_pixel_width, y_pixel_height, max_x_scale, max_y_scale, \
        aRecord.datalist,showBPVar, aTitle)


def eventRecords(aCanvas,aRecordList,max_x_scale):
    # graphCanvas is 800 x 600
    aCanvas.delete('all')
    x_zero = 50
    x_pixel_width = 700
    x_divisions = 12
    if (max_x_scale == 10) or (max_x_scale == 30): x_divisions = 10
    GraphLib.drawXaxis(aCanvas, x_zero, 550, x_pixel_width, max_x_scale, x_divisions)
    y_zero = 30
    box = 0
    # eventRecord(aCanvas, x_zero, y_zero, x_pixel_width, max_x_scale, datalist, charList, aLabel)
    # aTitle = aRecord.fileName
    for record in aRecordList:
        y_zero = y_zero + 40
        box = box + 1
        aTitle = "Box "+str(box)
        GraphLib.eventRecord(aCanvas, x_zero, y_zero, x_pixel_width, max_x_scale, record.datalist, ["P"], aTitle)

def eventRecordsIntA(aCanvas,aRecord):
    # graphCanvas is 800 x 600
    aCanvas.delete('all')
    x_zero = 75
    x_pixel_width = 600
    x_divisions = 12
    max_x_scale = 5
    x_divisions = 5
    GraphLib.drawXaxis(aCanvas, x_zero, 550, x_pixel_width, max_x_scale, x_divisions)
    y_zero = 50
    for block in range(12):
        aTitle = str(block+1)
        pump_timestamps = ListLib.get_pump_timestamps(aRecord.datalist,block)
        GraphLib.eventRecord(aCanvas, x_zero, y_zero, x_pixel_width, max_x_scale, pump_timestamps, ["P","p"], aTitle)
        y_zero = y_zero + 45


def histogram(aCanvas, aRecord,max_x_scale,clear = True):
    """
    Draws a histogram using the datalist from aRecord.

    To Do: There is another histogram procedure in GraphLib. Should be merged. 

    """
    def drawBar(aCanvas,x,y, pixelHeight, width, color = "black"):
        aCanvas.create_line(x, y, x, y-pixelHeight, fill=color)
        aCanvas.create_line(x, y-pixelHeight, x+width, y-pixelHeight, fill=color)
        aCanvas.create_line(x+width, y-pixelHeight, x+width, y, fill=color)    
    if clear:
        aCanvas.delete('all')          
    # Draw Event Record
    x_zero = 75
    y_zero = 100
    x_pixel_width = 700
    y_pixel_height = 200
    x_divisions = 12
    y_divisions = 5
    if (max_x_scale == 10) or (max_x_scale == 30): x_divisions = 10
    aCanvas.create_text(200, y_zero-50 , fill = "blue", text = aRecord.fileName)
    GraphLib.eventRecord(aCanvas, x_zero, y_zero, x_pixel_width, max_x_scale, aRecord.datalist, ["P"], "")
    # Populate bin array
    binSize = 1   # in minutes
    intervals = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    T1 = 0
    numInj = 0
    numIntervals = 0
    outOfRange = 0
    totalIntervals = 0
    for pairs in aRecord.datalist:
        if pairs[1] == "P":
            numInj = numInj + 1
            T2 = pairs[0]
            if T1 > 0:
                numIntervals = numIntervals + 1
                interval = round((T2-T1)/(binSize*60000),3)   # rounded to a minute with one decimal point
                totalIntervals = totalIntervals + interval
                index = int(interval)
                if index < len(intervals)-1:
                    intervals[index] = intervals[index]+1
                else:
                    outOfRange = outOfRange+1
            T1 = T2
    tempStr = "Number of Injections = "+str(numInj)
    aCanvas.create_text(450, y_zero-50, fill = "blue", text = tempStr)
    # print("Number of Inter-injection Intervals =",numIntervals)
    # print("Inter-injection Intervals = ",intervals)
    meanInterval = round(totalIntervals / numIntervals,3)
    x_zero = 75
    y_zero = 450
    x_pixel_width = 400
    y_pixel_height = 300 
    max_x_scale = 20
    max_y_scale = 20
    x_divisions = 20
    y_divisions = max_y_scale
    labelLeft = True
    GraphLib.drawXaxis(aCanvas, x_zero, y_zero, x_pixel_width, max_x_scale, x_divisions, color = "black")
    GraphLib.drawYaxis(aCanvas, x_zero, y_zero, y_pixel_height, max_y_scale, y_divisions, labelLeft, color = "black")
    # intervals = [0,1,2,3,4,5,6,5,4,3,2,1,0,0,0,0,0,0,0,1]  #Used for test without loading a file
    unitPixelHeight = int(y_pixel_height/y_divisions)
    width = int(x_pixel_width/len(intervals))
    for i in range(len(intervals)):           
        x = x_zero + (i*width)
        drawBar(aCanvas,x,y_zero,intervals[i]*unitPixelHeight,width)
    #Draw OutOfRange Bar
    x = x_zero + (len(intervals)*width) + 20
    drawBar(aCanvas,x,y_zero,outOfRange*unitPixelHeight,width)
    tempStr = "Mean interval (min) = "+ str(meanInterval)
    aCanvas.create_text(200, y_zero-y_pixel_height, fill = "red", text = tempStr)
    rate = round(60/meanInterval,3)
    tempStr = "Rate (inj/hr) = "+str(rate)
    aCanvas.create_text(450, y_zero-y_pixel_height, fill = "blue", text = tempStr)
    aCanvas.create_line(x_zero+int(width*meanInterval), y_zero, x_zero+int(width*meanInterval), y_zero-y_pixel_height+20, fill="red")
    tempStr = "Each Bin = "+str(binSize)+" minute"
    aCanvas.create_text(250, y_zero+50, fill = "blue", text = tempStr)

def pumpDurationsIntA(aCanvas,aRecord):
    aCanvas.delete('all')
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
    
def timeStamps(aCanvas,aRecord,max_x_scale):
    # graphCanvas is 800 x 600
    aCanvas.delete('all')
    x_zero = 100
    y_zero = 500
    x_pixel_width = 650
    x_divisions = 12
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
    GraphLib.eventRecord(aCanvas, x_zero, y_zero-130, x_pixel_width, max_x_scale, aRecord.datalist, ["T"], "T")
    GraphLib.eventRecord(aCanvas, x_zero, y_zero-100, x_pixel_width, max_x_scale, aRecord.datalist, ["F"], "Food Tray")
    GraphLib.eventRecord(aCanvas, x_zero, y_zero-70,  x_pixel_width, max_x_scale, aRecord.datalist, ["B","b"], "Access")
    GraphLib.eventRecord(aCanvas, x_zero, y_zero-50,  x_pixel_width, max_x_scale, aRecord.datalist, ["H","h"], "Houselight")
    GraphLib.eventRecord(aCanvas, x_zero, y_zero-30,  x_pixel_width, max_x_scale, aRecord.datalist, ["G","E"], "Session")
  



"""

def drawCumulativeRecord(aRecord,aCanvas):
    print("drawCumulativeRecord called")

"""
