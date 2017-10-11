"""
Notes Oct 8 prior to commit

count_

Lever             One      Two
----------------------------------
Lever Down          L       J
Lever Up            l       j
Start_Block_Char    B       A
End_Block_Char      b       a     = IBI
Insert Lever        =       -
Retract Lever       .       ,
StartTrial          T
EndTrial            t
PumpOn              P
PumpOff             p
StimOn              S
StimOff             s
StartSession            G
EndSession              E

"""


def get_time_list_for_code(letter_code, aList):
    ''' (letter, list) -> list

    Return a list of times corresponding to the letter_code.

    A timestamp is a pair of integer (time) and charcter (letter_code).
    The timestamp can be a list of lists or a list of tuples

    >>> find_code('B',[(1000, 'B'),(2000,'P'),(3000,'B')])
    [1000, 3000]
    '''
    return_list = []
    
    for timestamp in aList:
        if timestamp[1] == letter_code:
            return_list.append(timestamp[0])

    return return_list

def count_char(letter_code, aList):
    ''' (letter, list) -> int
        Returns the number of times a letter_code occurs in a list.
    '''
    count = 0
    for timestamp in aList:
        if timestamp[1] == letter_code:
            count = count + 1
    return count
    
def pump_durations(aList):
    ''' (list) -> list
        Returns the total time a pump was on
    '''
    durations = []
    duration = 0
    pumpOn = False
    block_index = -1
    for timestamp in aList:           
        if timestamp[1] == 'b':     # end of block
           durations.append(duration)  # Add
           block_index = block_index + 1
           duration = 0
        if timestamp[1] == 'P':
            pumpStartTime = timestamp[0]
            pumpOn = True
        if timestamp[1] == 'p':
            if pumpOn:
                duration = duration + (timestamp[0] - pumpStartTime)
                pumpOn = False
    return durations    


def pump_durations_per_block(aList):
    pass


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
    response_count = count_char('L',aList)
    print('Number of Responses: ', response_count)    
    injection_count = count_char('P',aList)
    print('Number of injections:', injection_count)
    durations_list = pump_durations(aList)
    print("Durations List:", durations_list)
    block_count = count_char('B',aList)
    print('Number of Blocks:', block_count)
    times = get_time_list_for_code('B', aList)    
    print('Block start times: ',times)
    


