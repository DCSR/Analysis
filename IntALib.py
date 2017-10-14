import ListLib


def sort_to_bins(pump_timelist):
    ''' (letter, list) -> int
        >>> get_pump_timelist[(900, 'P'),(2500,'p')])
       [100, 1000, 500]
        
    '''
    count = 0
    for timestamp in aList:
        if timestamp[1] == letter_code:
            count = count + 1
    return count
    
def get_pump_timelist(aList):
    ''' (list) -> list
        From a datalist (of timestamps), returns a list of
        times and durations for the pump using the Pump On ("P")
        and Pump Off ("p") characters. 

        A timestamp is a pair of integer (time) and charcter (letter_code).
        The timestamp can be a list of lists or a list of tuples

        Could convert all times to block times. 


        
    '''
    pump_timelist = []
    duration = 0
    pumpOn = False
    block_index = -1
    for timestamp in aList:
        if timestamp[1] == 'B':
            block_start_time = timestamp[0]
        if timestamp[1] == 'P':
            pumpStartTime = timestamp[0]
            pumpOn = True
        if timestamp[1] == 'p':
            if pumpOn:
                duration = timestamp[0] - pumpStartTime
                pumpOn = False
                block_time = pumpStartTime - block_start_time
                pump_timelist.append([block_time, duration])               
    return pump_timelist    



def get_pumptimes_per_bin(pump_timelist, bin_size = 5000):
    ''' (list) -> (list)
        From a pump_timelist, returns a list of cummulative pump durations
        per one second bins.
        >>> get_pumptime_per_bin([(1900, 2600])  # (start_time, duration)
        [0,100,1000,1000,500]
    '''
    durations_per_bin = []

    # calculate number of bins required and initialize list
    access_period = 1000*60*5  # 5 minutes
    number_of_bins = access_period // bin_size
    for bin in range(number_of_bins):
        durations_per_bin.append(0)

    for pair in pump_timelist:    # step through list
        start_time = pair[0]
        duration = pair[1]
        bin_num = pair[0]//bin_size
        remaining_bin_time = ((bin_num+1) * bin_size) - start_time
        # If the duration fits within one bin then add it to that bin and you are done
        if duration < remaining_bin_time:     # done
            durations_per_bin[bin_num] = durations_per_bin[bin_num] + duration
        # But if the pump duration spans two or more bins then..
        # split the duration into consecutive bins
        else:                                 
            durations_per_bin[bin_num] = durations_per_bin[bin_num] + remaining_bin_time
            duration = duration - remaining_bin_time
            bin_num = bin_num + 1
            while duration > 0:
                if duration > bin_size:
                    durations_per_bin[bin_num] = durations_per_bin[bin_num] + 1000                    
                    duration = duration - 1000
                    bin_num = bin_num + 1
                else:
                    durations_per_bin[bin_num] = durations_per_bin[bin_num] + duration
                    duration = 0  
    return durations_per_bin



if __name__ == '__main__':
    #import doctest
    #doctest.testmod(verbose=True)    

    aList = []
    aFile = open('IntA_Example_File.dat','r')
    for line in  aFile:
        pair = line.split()
        pair[0] = int(pair[0])
        aList.append(pair)
    aFile.close()
    # aList = [(1900, 'P'),(5000,'p')]
    injection_count = ListLib.count_char('P',aList)
    print('Number of injections:', injection_count)
    times = ListLib.get_time_list_for_code('P', aList)    
    print('Pump start times: ',times)    
    pump_timelist = get_pump_timelist(aList)
    print("pump_timeiist:", pump_timelist)
    pumptimes_per_bin = get_pumptimes_per_bin(pump_timelist, bin_size = 10000)
    print('pumptimes_per_bin = ', pumptimes_per_bin)


    


