# Python code to merge dict using
# (|) and (|=) operators

dict1 = {"a": 10, "b": 5, "c": 3}
dict2 = {"d": 6, "c": 4, "b": 8}


print()
dict3 = dict1 | dict2
print("Merging dict2 to dict1 (i.e., dict1|dict2) : ")
print(dict3)

dict4 = dict2 | dict1
print("\nMerging dict1 to dict2 (i.e., dict2|dict1) : ")
print(dict4)

dict1 |= dict2

print("\nMerging dict2 to dict1 and Updating dict1 : ")
print("dict1 : ", dict1)
print("dict2 : ", dict2)

print()
