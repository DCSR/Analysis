"""
This file contains all the precedures called from the GraphsTab

self.drawEventRecords()

self.timeStamps(self.recordList[self.fileChoice.get()])

self.showModel(self.recordList[self.fileChoice.get()])

self.showHistogram(self.recordList[self.fileChoice.get()])

"""

import GraphLib

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
    print("gt.drawEventRecords() called")
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
    




"""

def drawCumulativeRecord(aRecord,aCanvas):
    print("drawCumulativeRecord called")

"""
