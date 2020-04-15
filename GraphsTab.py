"""
This file contains all the precedures called from the GraphsTab


"""

import GraphLib

def drawCumulativeRecord(aRecord,aCanvas,showBPVar,max_x_scale = 120,max_y_scale=500):
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


"""

def drawCumulativeRecord(aRecord,aCanvas):
    print("drawCumulativeRecord called")

"""
