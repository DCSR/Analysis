   def loadZimmerFile(self):
        selected = self.fileChoice.get()    
        aFileName = "/Users/daveroberts/Dropbox/Programming/Python/Analysis101/TH_ BAZ15-033.txt"
        #             /Users/daveroberts/Dropbox/Programming/Python/Analysis101/TH_BAZ15-033.txt  
        aFileName = filedialog.askopenfilename()
        print(aFileName)
        self.recordList[selected] = self.getZimmerFile(self.recordList[selected],aFileName)
        self.recordList[selected].extractStatsFromList()
        print(self.recordList[selected])
        self.fileNameList[selected].set(self.recordList[selected].fileName)
        
        
    def getZimmerFile(self,aDataRecord,aFileName):
    
        """
        A data record is passed in (which may or may not be empty). It is reset
        then filled with data from a chosen file and returned.
 
        Notes: 
        Uses the D: field to discriminate an FR1 file from a TH file.
        If it is an FR1 file it substitutes a pump time of 5 sec - probably wrong...
        If it is a TH file it uses the array of pumptimes.
        The pump times are preassigned and NOT read from the datafile

        To Do: Because values of zero throw errors in log functions, every log function needs
           to check and handle such data, or (perhaps in the interim) the data file should substitute
           0.00001 for any zero value (as often happens in the last consumption bin)
        
        Parsing the injections listed in Q: into bins matches the totals listed in H: 

        Codes for Zimmer files
    
        A = Active responses
        B = Infusions
        C = Inactive responses
      * D = List for pump times   
      * H = Number of infusions per 10 minute bin
      * I = Number of ResponsconsumptionListes per 10 minute bin
      * J = Number of Inactive responses per 10 minute bin

        M = Session duration (minutes)
      * N = 10 min counter
      * P = Time that pump, cue lights, and tone are on  
        Q = Time (in seconds) of each infusion
        R = Time (in seconds) of each response
        S = Each infusion duration (in centiseconds)
        U = Time out (seconds)
        W = Weight of animal - ignore
        X = Subscript for Q array - ignore
        Y = Subscript for R array - ignore
 
       * = used in TH file
    
       """
        # empty dataRecord
        aDataRecord.fileName = "Zimmer test"
        aDataRecord.numberOfL1Responses = 0
        aDataRecord.numberOfL2Responses = 0
        aDataRecord.numberOfInfusions = 0
        aDataRecord.totalPumpDuration = 0
        #   Check these assumptions
        #   These are values provided by Brandon (I think)
        #   MUSC: 2.73 mg/ml * 0.0000176 mls/mSec = 0.000048048 mg/mSec
        #   WAKE: 5 mg/ml * 0.000025 = 0.000125 mg/mSec 
        aDataRecord.cocConc = 2.73
        aDataRecord.pumpSpeed = 0.0176
        aDataRecord.averagePumpTime = 0.0
        # For comparison:
        # WakePumpTimes = [3.162,1.780,1.000,0.562,0.316,0.188,0.100,0.056,0.031,0.018,0.010,0.0056]
        aDataRecord.TH_PumpTimes = [8.175,4.597,2.585,1.454,0.818,0.460,0.259,0.145,0.082,0.046,0.026,0.0146]
        aDataRecord.priceList = []
        aDataRecord.consumptionList = []
        aDataRecord.deltaList = []
        aDataRecord.notes = "Zimmer file"
        """
          A: and B: contain the number of active responses and infusions respectively. These should be
          the same, but they are not. So, as a first pass, this analysis uses the injection data only.
          That is, the program uses the timestamps for the infusions and counts it as a pump time and
          a response time. 
        """
        sectionStartIdentfier = "Q:"
        sectionEndIdentifier = "R:"
        directory = os.path.split(aFileName)[0]
        fileName = os.path.split(aFileName)[1]
        # print(fileName)
        aDataRecord.fileName = fileName
        tempList = []
        # print("Looking for section preceded by "+sectionStartIdentfier+" in "+fileName+"\n")
        dataPoints = 0
        lineNumber = 0
        sectionIdentified = False
        FR1_File = False
        with open(aFileName) as myOpenFile:    # aFileName is complete string passed to procedure
            for line in myOpenFile:            # This runs through the file one line at a time
                lineNumber = lineNumber + 1            # count the lines
                if "D:       0.000" in line:   # This is used to descriminate between FR1 and TH files.
                    FR1_File = True            
                elif sectionStartIdentfier in line:  # if it finds "Q:" then it knows that it is in the right section of the datafile
                    sectionIdentified = True           
                    # print("Infusion data ('Q:') begins at line ", lineNumber)
                elif (sectionIdentified):   # If True, it should be in the right section and trying to parse the data 
                    if line[0] == " ":      # Looks for an indented section of text by checking that the first character is a space. 
                        numberList = line.split()               # splits the line up into a "list" of text values (turned into numbers later)
                        for dataNumber in numberList:           # goes through each "number" in the list (they are actually strings)
                            if dataNumber.find(".") > 0:        # It ignores "numbers" that doesn't have a decimal point - i.e. the 1st number
                                data = float(dataNumber)        # Convert the text value into a float (number with a decimal value)
                                time = int(data*1000)           # time in mSec
                                pair = [time, "P"]              # Cteate a timestamp pair: "Pump On" timestamp
                                tempList.append(pair)           # Add to list
                                pair = [time, "L"]              # Lever response timestamp
                                tempList.append(pair)
                                blockNum = int(time/600000)
                                if FR1_File:
                                    time = time+5000            # Pump Off time stamp. 
                                else:
                                    time = time+(aDataRecord.TH_PumpTimes[blockNum]*1000)   # Get pump duration from pump time array
                                pair = [time, "p"]
                                tempList.append(pair)
                                dataPoints = dataPoints + 1     # Count number of data points                     
                    elif sectionEndIdentifier in line:          # Look for end of section i.e. "R:"
                        sectionIdentified = False
            myOpenFile.close()
            print("Found", dataPoints,"dataPoints in Zimmer file:", fileName)
            aDataRecord.datalist = tempList

    
            """
            There are two ways to calculate cocaine consumption during the bins.
      
            Option 1 assumes that timestamp data stream contained all the information,
            such as the beginning and end of each Block ("B","b") and pump interval ("P","p").
            This would tie the analysis directly to the data and would be able to handle situations in
            which the interval length was changed (eg. 10 to 5 or 12 min) or the pumptimes were altered.

            Option 2. Unfortunately, not all datastreams contain this information. The "work around" is to calculate
            everything using only the pump start times. The duration of each infusion is calculated from the
            pumptime list which is assigned when the datastream is loaded. This option assumes that the pumptime list
            is accurate and that the bin length is always 10 min.

            """

            pumpStarttime = 0
            blockNum = -1 
            pumpOn = False
            leverTotal = 0       
            pumpTimeList = [0,0,0,0,0,0,0,0,0,0,0,0]     #Temp list of 12 pairs: price and total pump time
            aDataRecord.responseList = [0,0,0,0,0,0,0,0,0,0,0,0]
            aDataRecord.consumptionList = [0,0,0,0,0,0,0,0,0,0,0,0]
            aDataRecord.priceList = [0,0,0,0,0,0,0,0,0,0,0,0]
            for pairs in aDataRecord.datalist:              # Fill pumpTimeList and responseList
                if pairs[1] == 'P':
                    time = pairs[0]
                    blockNum = int(time/600000)
                    aDataRecord.responseList[blockNum] = aDataRecord.responseList[blockNum] + 1  # inc Bin_responses
                    leverTotal = leverTotal + 1                          # using pump for responses
                    duration = aDataRecord.TH_PumpTimes[blockNum]
                    pumpTimeList[blockNum] = pumpTimeList[blockNum] + duration                     
            mgPerSec = aDataRecord.cocConc * aDataRecord.pumpSpeed
            for i in range(12):
                aDataRecord.consumptionList[i] = pumpTimeList[i] * mgPerSec
            
            for i in range(12):
                # dosePerResponse = pumptime(mSec) * mg/ml * ml/sec)
                dosePerResponse = aDataRecord.TH_PumpTimes[i] * aDataRecord.cocConc * aDataRecord.pumpSpeed
                price = round(1/dosePerResponse,2)
                aDataRecord.priceList[i] = price

            return aDataRecord         
