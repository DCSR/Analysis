
"""
Definition of data structure

"""



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
        self.iniLine = ""

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

