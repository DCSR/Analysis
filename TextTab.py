
import tkinter as tk

def summaryText(aTextBox,aRecord):
    """
    Prints a summary
    Note that if you tell Python to print a class (like DataRecod) it
    will default to the string __str__() defined in the class structure.
    In this case, see DataModel.py -> DatRecord 

    """
    aTextBox.insert("1.0",aRecord)
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
    aTextBox.insert(tk.END,"First inj = "+str(round(timeFirstInjection/1000,1))+" sec ("+str(round(timeFirstInjection/60000,0))+" min)\n")
    aTextBox.insert(tk.END,"Last inj  = "+str(round(timeLastInjection/ 1000,1))+" sec ("+str(round(timeLastInjection/ 60000,0))+" min)\n")
    aTextBox.insert(tk.END,"Total of "+str(numIntervals)+" intervals = "+str(round(totalIntervals/ 1000,1))+" sec, ("+str(round(totalIntervals/60000,0))+" min)\n")
    meanInterval = totalIntervals/numIntervals
    aTextBox.insert(tk.END,"Mean interval = "+str(round(meanInterval/1000,1))+" sec, ("+str(round(meanInterval/60000,2))+" min)\n")
    aTextBox.insert(tk.END,"Rate (inj/hr) = "+str(round(60/(meanInterval/60000),3))+"\n")
    aTextBox.insert(tk.END,"***************************\n")


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
