
import tkinter as tk

import ListLib
                

def summaryText(aTextBox,aRecord):
    """
    Prints a summary
    Note that if you tell Python to print a class (like DataRecod) it
    will default to the string __str__() defined in the class structure.
    In this case, see DataModel.py -> DatRecord 

    """
    aTextBox.insert(tk.END,aRecord)
    timeFirstInjection = 0
    T1 = 0
    numInj = 0
    numIntervals = 0
    totalIntervals = 0
    sessionEnd = 0
    meanInterval = 0.0
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

        if pairs[1] == "E":
            sessionEnd = pairs[0] #finds session lengh

    timeLastInjection = T1

    aTextBox.insert(tk.END,"First inj = "+str(round(timeFirstInjection/1000,1))+" sec ("+str(round(timeFirstInjection/60000,0))+" min)\n")
    aTextBox.insert(tk.END,"Last inj  = "+str(round(timeLastInjection/ 1000,1))+" sec ("+str(round(timeLastInjection/ 60000,0))+" min)\n")
    aTextBox.insert(tk.END,"Total of "+str(numIntervals)+" intervals = "+str(round(totalIntervals/ 1000,1))+" sec, ("+str(round(totalIntervals/60000,0))+" min)\n")
    if numIntervals > 0:
        meanInterval = totalIntervals/numIntervals
        aTextBox.insert(tk.END,"Mean interval = "+str(round(meanInterval/1000,1))+" sec, ("+str(round(meanInterval/60000,2))+" min)\n")
        aTextBox.insert(tk.END,"Rate (inj/hr) = "+str(round(60/(meanInterval/60000),3))+"\n")
    else:
        aTextBox.insert(tk.END,"Mean interval = 0\n")
    if sessionEnd > 0:
        aTextBox.insert(tk.END,"session length (min) = "+str(round((sessionEnd/60000),0))+"\n") #bug being generated here
    else:
        aTextBox.insert(tk.END,"session length (min) = 0\n")
    aTextBox.insert(tk.END,"***************************\n")

##    aString = "Total Pump Duration = {0:6d} mSec \n".format(totalPumpDuration)
##                aTextBox.insert(tk.END,aString)


# work on adding injection times

def injectionTimesText(aTextBox, aRecord):
    
        injection = 0
        previousInjTime = 0
        aTextBox.insert(tk.END,"Inj Duration   Time (sec)   Time (min) Interval (sec)\n")
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
                    aTextBox.insert(tk.END,tempString+"\n")
                
        aTextBox.insert(tk.END,"Number of injections: "+str(injection)+"\n")

#work on adding dose report

##def matPlotEventRecord(self):
##    aCanvas = self.testArea_MatPlot_Canvas
##    aFigure = self.matPlotTestFigure
##    aRecord = self.recordList[self.fileChoice.get()]
##    startTime = self.startTimeScale.get()
##    endTime = self.endTimeScale.get()
##    ta.matPlotEventRecord(aCanvas,aFigure,aRecord,startTime,endTime)

# this function points to self.startTimesScale.get and self.endTimeScale.get which
# lives within matPlotEventRecord(self)
# placing that func above now

##self.startTimeVar = IntVar()                     # Associated with startTimeScale, initialized to zero       
##self.endTimeVar = IntVar()                         # Associated with endTimeScale, initialized to 360
##self.drugConcStr = StringVar(value="5.0")
##self.weightStr = StringVar(value="350")


##self.textButtonFrame = Frame(self.textTab, borderwidth=5, relief="sunken")
##self.textButtonFrame.grid(column = 0, row = 0, sticky=N)
##
##self.textBox = Text(self.textTab, width=100, height=43)
##self.textBox.grid(column = 1, row = 0, rowspan = 2)
##        
##cleartextButton = Button(self.textButtonFrame, text="Clear", command= lambda: \
##                              self.clearText()).grid(row=0,column=0,columnspan = 2,sticky=N)
##summarytextButton = Button(self.textButtonFrame, text="Summary", command= lambda: \
##                              self.summaryText()).grid(row=1,column=0,columnspan = 2,sticky=N)
##injectionTimesButton = Button(self.textButtonFrame, text="Injection Times", command= lambda: \
##                              self.injectionTimesText()).grid(row=2,column=0,columnspan = 2,sticky=N)        
##
##pyPlotEventButton = Button(self.textButtonFrame, text="PyPlot Event Record", command= lambda: \
##                              self.pyPlotEventRecord()).grid(row=3,column=0,columnspan=2,sticky=N)
##
##doseReportButton = Button(self.textButtonFrame, text="Dose Report", command= lambda: \
##                              self.doseReport()).grid(row=4,column=0,columnspan = 2,sticky=N)
##
##self.startTimeLabel = Label(self.textButtonFrame, text = "T1").grid(row=5,column=0,sticky=W)        
##
##self.startTimeScale = Scale(self.textButtonFrame, orient=HORIZONTAL, length=100, resolution = 5, \
##                                  from_=0, to=360, variable = self.startTimeVar)
##self.startTimeScale.grid(row=5,column=1)
##self.startTimeScale.set(0)
##
##self.endTimeLabel = Label(self.textButtonFrame, text = "T2").grid(row=6,column=0,sticky=W) 
##
##self.endTimeScale = Scale(self.textButtonFrame, orient=HORIZONTAL, length=100, resolution = 5, \
##                                  from_=0, to=360, variable = self.endTimeVar)
##self.endTimeScale.grid(row=6,column=1)
##self.endTimeScale.set(360)
##        
##concentrationLabel = Label(self.textButtonFrame, text="Conc (mg/ml)")
##concentrationLabel.grid(row = 7, column = 0)
##        
##self.concentrationEntry = Entry(self.textButtonFrame, width=6,textvariable = self.drugConcStr)
##self.concentrationEntry.grid(row = 7, column = 1)
##
##weightLabel = Label(self.textButtonFrame, text="Body weight (gms)")
##weightLabel.grid(row = 8, column = 0)
##
##self.weightEntry = Entry(self.textButtonFrame, width=6,textvariable = self.weightStr)
##self.weightEntry.grid(row = 8, column = 1)
##
##intA_text_button = Button(self.textButtonFrame, text="IntA", command= lambda: \
##                              self.intA_text()).grid(row = 9,column = 0, columnspan = 2,sticky=N)
##TH_text_button = Button(self.textButtonFrame, text="Threshold (TH)", command= lambda: \
##                              self.threshold_text()).grid(row = 10,column = 0, columnspan = 2,sticky=N)
##


def doseReport(aTextBox, aRecord, aStartTimeScale, aEndTimeScale, aConcentrationEntry, aWeightEntry):

##        an.startTimeVar = tk.IntVar()                        # Associated with startTimeScale, initialized to zero       
##        an.endTimeVar = tk.IntVar()                          # Associated with endTimeScale, initialized to 360
##        an.drugConcStr = tk.StringVar(value="5.0")
##        an.weightStr = tk.StringVar(value="350")

        
        
        pumpOn = False
        injections = 0
        totalPumpDuration = 0
        lastTime = 0
        time1 = aStartTimeScale
        time2 = aEndTimeScale
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
        aTextBox.insert(tk.END,aString)

        try:
            conc = float(aConcentrationEntry)
            weight = int(aWeightEntry)         # in grams
            aString = "Drug Concentration = {0:5.3f} mg/ml\nWeight = {1:3d} grams \n".format(conc,weight)            
        except ValueError:
            aString = "Error getting Conc and/or Body weight \n"
        aTextBox.insert(tk.END,aString)

        if injections > 0:
                aString = "Total Pump Duration = {0:6d} mSec \n".format(totalPumpDuration)
                aTextBox.insert(tk.END,aString)
                averagePumpTime = round(totalPumpDuration / injections,2)
                aString = "Average Pump Time = {0:5.3f} mSec \n".format(averagePumpTime)
                aTextBox.insert(tk.END,aString)
                totalDose = (totalPumpDuration/1000) * conc * 0.025  # pumptime(mSec) * mg/ml * ml/sec)
                totalDosePerKg = totalDose/(weight/1000)
                aString = "Total Dose = {0:5.3f} mg;  {1:5.3f} mg/kg \n".format(totalDose, totalDosePerKg)
                aTextBox.insert(tk.END,aString)
                averageDose = (totalDose / injections)
                averageDosePerKg = averageDose / (weight/1000)
                aString = "Average Dose = {0:5.3f} mg;  {1:5.3f} mg/kg \n".format(averageDose, averageDosePerKg)
                aTextBox.insert(tk.END,aString)

        
        aTextBox.insert(tk.END,"********************************\n")

##def matPlotEventRecord(self):
##    aCanvas = self.testArea_MatPlot_Canvas
##    aFigure = self.matPlotTestFigure
##    aRecord = self.recordList[self.fileChoice.get()]
##    startTime = self.startTimeScale.get()
##    endTime = self.endTimeScale.get()
##    ta.matPlotEventRecord(aCanvas,aFigure,aRecord,startTime,endTime)

### unchanged for ref


#prodecure called from the Text tab ref
##
##def summaryText(self):
##        aTextBox = self.textBox
##        aRecord = self.recordList[self.fileChoice.get()]       
##        tt.summaryText(aTextBox,aRecord)

##def injectionTimesText(self):
##        aRecord = self.recordList[self.fileChoice.get()]
##        injection = 0
##        previousInjTime = 0
##        self.textBox.insert(END,"Inj Duration   Time (sec)   Time (min) Interval (sec)\n")
##        pumpOn = False
##        for pairs in aRecord.datalist:
##            if pairs[1] == 'P':
##                pumpStartTime = pairs[0]
##                injection = injection + 1
##                secTime = pairs[0]/1000
##                minTime = secTime/60
##                interval = secTime - previousInjTime
##                previousInjTime = secTime
##                pumpOn = True
##            if pairs[1] == 'p':
##                if pumpOn:
##                    pumpOn = False
##                    duration = pairs[0]-pumpStartTime
##                    if injection == 1:
##                        tempString = "{0} {1:10.2f} {2:10.2f} {3:10.2f}".format(injection,duration,secTime,minTime,interval)
##                    else:
##                        tempString = "{0} {1:10.2f} {2:10.2f} {3:10.2f} {4:10.2f}".format(injection,duration,secTime,minTime,interval)
##                    self.textBox.insert(END,tempString+"\n")
##                
##        self.textBox.insert(END,"Number of injections: "+str(injection)+"\n")



def threshold_text(aTextBox, aRecord):
        
        aList = aRecord.datalist
        count = ListLib.count_char('L',aList)
        aString = 'Number of responses: '+str(count)
        aTextBox.insert(tk.END,aString+"\n")
        
        count = ListLib.count_char('P',aList)
        aString = 'Number of injections: '+str(count)
        aTextBox.insert(tk.END,aString+"\n")

        blockCount = ListLib.count_char('B',aList)
        aString = 'Number of blocks: '+str(blockCount)
        aTextBox.insert(tk.END,aString+"\n")

        pump_count_list = ListLib.get_pump_count_per_block(aList)
        aString = 'Injections per block: '
        for item in pump_count_list:
            aString = aString + str(item) + ' '
        aTextBox.insert(tk.END,aString+"\n")
        print(pump_count_list)

        pump_count_list = ListLib.get_pump_count_per_block(aList)
        aString = 'Injections per block vertical: '
        for item in pump_count_list:
            aString = aString + str(item) + ' \n'#SeaChange03012020 added \n to make list vertical, easing spreadsheet entry
        aTextBox.insert(tk.END,aString+"\n")
        print(pump_count_list)


        for b in range (blockCount):    
            pump_duration_list = ListLib.get_pump_duration_list(aList, b)
            aString = 'Block '+str(b)+': '
            for i in range (len(pump_duration_list)):
                list_item = pump_duration_list[i]
                aString = aString + str(list_item[2]) + ' '
            aTextBox.insert(tk.END,aString+"\n")
        #print("Block "+str(b), pump_duration_list)



def injectionTimesTextMin(aTextBox, aRecord):#add this to analysis
        
        aTextBox.insert(tk.END,aRecord.fileName+"\n") #this adds rat id to output seachange03012020
        injection = 0
        previousInjTime = 0
        aTextBox.insert(tk.END,"Time of lever press (min)\n")
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
                        tempString = "{3:10.2f}".format(injection,duration,secTime,minTime,interval)
                    else:
                        tempString = "{3:10.2f}".format(injection,duration,secTime,minTime,interval)
                    aTextBox.insert(tk.END,tempString+ "\n")
                
        aTextBox.insert(tk.END,"Number of injections: "+str(injection)+"\n")

def intervalText(aTextBox, aRecord): #SeaChange03012020 added infusion intervals only

        
        aTextBox.insert(tk.END,aRecord.fileName+"\n") #this adds rat id to output seachange03012020
        injection = 0
        previousInjTime = 0
        aTextBox.insert(tk.END,"Interval (min)\nTime to first infusion -->")
        pumpOn = False
        for pairs in aRecord.datalist:
            if pairs[1] == 'P':
                pumpStartTime = pairs[0]
                injection = injection + 1
                secTime = pairs[0]/1000
                minTime = secTime/60
                interval = (secTime - previousInjTime)/60 #()/60 changes interval seconds to interval minutes seachange03012020
                previousInjTime = secTime
                pumpOn = True
            if pairs[1] == 'p':
                if pumpOn:
                    pumpOn = False
                    duration = pairs[0]-pumpStartTime
                    if injection == 1:
                        tempString = "{3:10.2f}".format(injection,duration,secTime,minTime,interval)
                    else:
                        tempString = "{4:10.2f}".format(injection,duration,secTime,minTime,interval)
                    aTextBox.insert(tk.END,tempString+"\n")
                
        aTextBox.insert(tk.END,"Number of injections: "+str(injection)+"\n")

def bintimeText(aTextBox, aRecord): #SeaChange03162020 added bin times only

        
        aTextBox.insert(tk.END,aRecord.fileName+"\n") #this adds rat id to output seachange03012020
        injection = 0
        previousInjTime = 0
        aTextBox.insert(tk.END,"Interval (min)\n Length of first infusion -->")
        pumpOn = False
        for pairs in aRecord.datalist:
            if pairs[1] == 'P':
                pumpStartTime = pairs[0]
                injection = injection + 1
                secTime = pairs[0]/1000
                minTime = secTime/60
                interval = (secTime - previousInjTime)/60 #()/60 changes interval seconds to interval minutes seachange03012020
                previousInjTime = secTime
                pumpOn = True
            if pairs[1] == 'p':
                if pumpOn:
                    pumpOn = False
                    duration = pairs[0]-pumpStartTime
                    if injection == 1:
                        tempString = "{1:10.2f}".format(injection,duration,secTime,minTime,interval)
                    else:
                        tempString = "{1:10.2f}".format(injection,duration,secTime,minTime,interval)
                    aTextBox.insert(tk.END,tempString+"\n")
                
        aTextBox.insert(tk.END,"Number of injections: "+str(injection)+"\n")
        
def injectionTimesText(aTextBox, aRecord):
        aRecord
        aTextBox.insert(tk.END,aRecord.fileName+"\n") #this adds rat id to output seachange03012020
        injection = 0
        previousInjTime = 0
        aTextBox.insert(tk.END,"Inj Duration   Time (sec)   Time (min) Interval (sec)\n")
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
                    aTextBox.insert(tk.END,tempString+"\n")
                
        aTextBox.insert(tk.END,"Number of injections: "+str(injection)+"\n")
