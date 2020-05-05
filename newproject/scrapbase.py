def filewrite(data,filenames):
    '''Writes the data from data into filenames, with each element being on a new line

    Args:
        data      (list): Contains each list of data to be written
        filenames (list): The names of the files to write the data to
    '''
    for i in range(len(filenames)):
        with open(filenames[i], "w") as file:
            for j in range(len(data[i])):
                file.write(data[i][j])
                file.write("\n")
    return 0

def arrayinstring(array,string):
    '''Returns a score based on whether the elements of an array occur in a string

    Desc: If all elements of an array are in a substring of string, it returns 1
    If all elements of an array are not in a substring of string, it returns -1
    If its mixed results, it returns a 0

    Args:
        array   (list)  : An array of strings that should be looked for in string
        string  (str)   : A string to be searched through

    Results:
        score   (int)   : A score determining whether the elements of an array were all in or not a substring
    '''
    score=0
    for requirements in array:
        if requirements in string:
            score+=1
        else:
            score-=1
    if score == len(array):
        score = 1
    elif score == -len(array):
        score = -1
    else:
        score = 0
    return score


def searchthrough(array,required,disallowed):
    '''Searches through an array for a first occurrence of not including certain substrings and including certain ones.
    Returns the length of the array if no match occurs

    Args:
        array       (list)  : Array to be searched through
        required    (list)  : Substrings to be (case insensitive) in array
        disallowed  (list)  : Substrings to be (case insensitive) not in array

    Out:
        index   (int)   : The index at which the match occurs

    Examples:
        >   searchthrough(["Greetings", "Hello", "Good Day"], "d d")
        >   2

        >   searchthrough(["FoOoOoOoOo", "BOOOOOO", "h"],"ooo")
        >   0
    '''
    j=0
    while j<len(array):
        if arrayinstring(required,str.lower(array[j]))==1 and arrayinstring(disallowed,str.lower(array[j])):
            index=j
            j=len(array)+1
        j+=1
    try:
        return index
    except:
        return j
