
# defaultdict - when dictionary key is called that is not already there, it creates that key with the default value
# dict.setdefault() - checks if the key is in the dictionary, if not it adds that key with the default value
# dict.get() - checks if the key is in the dictionary, if not it returns that key with the default value


from collections import defaultdict


# from collections import defaultdict

# s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
# d = defaultdict(list)
# for k, v in s:
#     d[k].append(v)

# print(sorted(d.items()))



# mydict = {'george': 16, 'amber': 19}
# print(list(mydict.keys())[list(mydict.values()).index(16)])




# car = {
#   "brand": "Ford",
#   "model": "Mustang",
#   "year": 1964
# }

# car.setdefault("model", "Bronco")

# # print(f"{x=}")
# print(f"{car=}")


message = 'It was a bright cold day in April, and the clocks were striking thirteen.'


count = defaultdict(int)



for character in message:
  # count.setdefault(character, 0)
  count[character] = count[character] + 1

print(count)









