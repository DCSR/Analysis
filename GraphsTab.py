"""
This file contains all the precedures called from the GraphsTab

Index:

drawCumulativeRecord()

drawEventRecords()

showModel()

timeStamps()


self.showHistogram(self.recordList[self.fileChoice.get()])

"""

import GraphLib
import model

def drawCumulativeRecord(aCanvas,aRecord,showBPVar,max_x_scale,max_y_scale):
    aCanvas.delete('all')
    # graphCanvas is 800 x 600
    x_zero = 50
    y_zero = 550
    x_pixel_width = 700                               
    y_pixel_height = 500
    x_divisions = 12
    #max_x_scale = self.max_x_scale.get()
    if (max_x_scale == 10) or (max_x_scale == 30): x_divisions = 10
    #max_y_scale = self.max_y_scale.get()
    y_divisions = 10
    aTitle = aRecord.fileName
    # def cumRecord(aCanvas, x_zero, y_zero, x_pixel_width, y_pixel_height, max_x_scale, max_y_scale, datalist, aTitle)
    GraphLib.drawXaxis(aCanvas, x_zero, y_zero, x_pixel_width, max_x_scale, x_divisions)
    GraphLib.drawYaxis(aCanvas, x_zero, y_zero, y_pixel_height, max_y_scale, y_divisions, True)
    GraphLib.cumRecord(aCanvas, x_zero, y_zero, x_pixel_width, y_pixel_height, max_x_scale, max_y_scale, \
        aRecord.datalist,showBPVar, aTitle)


def drawEventRecords(aCanvas,aRecordList,max_x_scale):
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

def showModel(aCanvas,aRecord,max_x_scale,resolution = 60, aColor = "blue", clear = True, max_y_scale = 25):
    if clear:
        aCanvas.delete('all')
    x_zero = 75
    y_zero = 350
    x_pixel_width = 700
    y_pixel_height = 200
    x_divisions = 12
    y_divisions = 5
    if (max_x_scale == 10) or (max_x_scale == 30): x_divisions = 10
    GraphLib.eventRecord(aCanvas, x_zero, 100, x_pixel_width, max_x_scale, aRecord.datalist, ["P"], "Test")
    GraphLib.drawXaxis(aCanvas, x_zero, y_zero, x_pixel_width, max_x_scale, x_divisions, color = "red")
    GraphLib.drawYaxis(aCanvas, x_zero, y_zero, y_pixel_height, max_y_scale, y_divisions, True, color = "blue")
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
        # self.graphCanvas.create_oval(newX-2, newY-2, newX+2, newY+2, fill=aColor)
        x = newX
        y = newY
    aCanvas.create_text(300, 400, fill = "blue", text = aRecord.fileName)
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
    aCanvas.create_line(X1, Y, X2, Y, fill= "red")
    tempStr = "Average Conc (10-180 min): "+str(averageConc)
    aCanvas.create_text(500, Y, fill = "red", text = tempStr)

    
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
