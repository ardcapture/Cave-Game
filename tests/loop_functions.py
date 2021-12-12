raw = 'asdfaa3fa!!!'
functions = [str.isalnum, str.isalpha, str.isdigit, str.islower,  str.isupper]  # list of functions

for fn in functions:     # iterate over list of functions, where the current function in the list is referred to as fn
    for ch in raw:       # for each character in the string raw
        if fn(ch):        
            print(str(fn), True)
            break