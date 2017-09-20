def find_code(letter_code, aList):
    ''' (list) -> list

    Return a list of timeStamps corresponding to the letter_code.

    A timestamp is a pair of code and time.
    The timestamp can be a list of lists or a list of tuples

    >>> find_code('L',[('L',1000),('P',2000),('L',3000)])
    [('L', 1000), ('L', 3000)]
    >>> find_code('L',[['L',1000],['P',2000],['L',3000]])
    [['L', 1000], ['L', 3000]]
    

    '''
    return_list = []
    
    for timestamp in aList:
        if timestamp[0] == letter_code:
            return_list.append(timestamp)

    return return_list




if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
