#
# #! Tech with Tim
# class Iter:
#     def __init__(self, n):

#         self.n = n

#     def __iter__(self):
#         print("iter")
#         self.current = -1
#         return self

#     def __next__(self):
#         print("next - test ooo")
#         self.current += 1

#         if self.current >= self.n:
#             raise StopIteration

#         return self.current


# x = Iter(5)
# itr = iter(x)
# print(next(itr))
# print(next(itr))
# for i in itr:
#     print(i)


#! Corey Schafer - example
# class MyRange:
#     def __init__(self, start, end):
#         self.value = start
#         self.end = end

#     def __iter__(self):
#         return self

#     def __next__

#! stack overflow example - edited
# s = "hello world"
# it = iter(s)
# print(next(it), "- nexter")
# print(next(it), " - nexter")
# print()
# for i in it:
#     print(i, "- breaker")
#     break
# print()
# for i in it:
#     print(i, "- for looper")
# # print(list(it))  # Doesn't start from the beginning


#! Fluent Python -  Example - edited
import collections

Card = collections.namedtuple("Card", ["rank", "suit"])


class AdrianDeck:
    ranks = [str(n) for n in range(2, 4)] + list("JQ")
    suits = "spades diamonds".split()

    def __init__(self):
        # self.current = -1
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    # def __len__(self):
    #     return len(self._cards)

    def __getitem__(self, position):
        print("get item")
        return self._cards[position]

    def __iter__(self):
        print("iter go!")
        self.current = -1
        return self

    def __next__(self):
        print("next")
        self.current += 1

        if self.current >= len(self._cards):
            raise StopIteration

        return self._cards[self.current]


deck = AdrianDeck()

print("START!!!!!!!!!!!!!!!!")
# it = iter(deck)
# print(it)
for i in deck:
    print(i)
# print(next(it))
# print(next(it))
# print(next(it))
# print(next(it))
# print(next(it))
