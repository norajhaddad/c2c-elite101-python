#function capital_indexes(s):
    #create an empty list called indices

    #for each index i and character ch in s (using enumerate):
        #if ch is an uppercase letter:
            #add i to indices
    #return indices
def capital_indexes(s): #s is parameter name- string that'll be passed into function when called
    indices = [] #sets the empty list
    for i, ch in enumerate(s): #starts loop- vars i and ch will hold character at position- enumerate loops through and gives index + item
        if ch.isupper():
            indices.append(i) #add it to empty list if character is uppercase
    return indices
print(capital_indexes("HeLlo"))
print(capital_indexes("heelloo"))
print(capital_indexes("HELLOOO"))
