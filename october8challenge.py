#function sum of digits (text)
    #set total to 0
    #for each character in the first 100 characters of text
        #if character is a digit (0-9)
            #convert character to integer
            #add it to total
        #end if
    #end for

    #return total
#end function
def sum_of_digits(text):
    total = 0
    for char in text[:100]:
        if char.isdigit():
            total += int(char)
    return total
print(sum_of_digits("abc13498!!"))
print(sum_of_digits("!#@$%^&*()"))
print(sum_of_digits("no digits!"))
print(sum_of_digits("~~__{}}|||>><<??"))
