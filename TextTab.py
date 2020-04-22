
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
