

# dicty01 = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'X', 8: 'X', 9: 'X', 10: 'X', 11: 'X', 12: 'X', 13: 'X', 14: 'X', 15: 'X'}

# # listydicty01 = list(dicty01.keys())

# # print("listydicty01", listydicty01)

# for i in list(dicty01.keys())[3:5]:
#     print(i, dicty01[i])



from itertools import chain, groupby
from operator import itemgetter

data1 = {'r': (2, 2, 2), 'e': 4, 'h': 2, 'k': 4}
data2 = {'r': (20, 20, 20), 'e': 5, 'y': 2, 'h': 2}
data3 = {'r': (10, 10, 10), 'e': 5, 'y': 2, 'h': 2}

get_key, get_val = itemgetter(0), itemgetter(1)
merged_data = sorted(chain(data1.items(), data2.items(), data3.items()), key=get_key)

output = {k: max(map(get_val, g)) for k, g in groupby(merged_data, key=get_key)}

print(output)
