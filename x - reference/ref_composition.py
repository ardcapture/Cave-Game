# Python Object Oriented Programming by Joe Marini course example
# Using composition to build complex objects

from dataclasses import dataclass


class Book:
    def __init__(self, title: str, price: float, author: tuple[str, str]):
        self.title = title
        self.price = price

        # Use references to other objects, like author and chapters
        self.author = Author(*author)
        self.chapters = []

    def addchapter(self, chapter):
        self.chapters.append(chapter)

    def getbookpagecount(self):
        result = 0
        for ch in self.chapters:
            result += ch.pagecount
        return result


class Author:
    def __init__(self, fname, lname):
        self.fname = fname
        self.lname = lname

    def __str__(self):
        return f"{self.fname} {self.lname}"


class Chapter:
    def __init__(self, name, pagecount):
        self.name = name
        self.pagecount = pagecount


@dataclass
class Author_Data:
    fname: str
    lname: str

    def __post_init__(self):
        self.author = (self.fname, self.lname)


@dataclass
class Book_Data:
    title: str
    price: float
    author: Author_Data


wap_b = Book_Data(
    title="War and Peace",
    price=39.95,
)

wap_a = Author_Data(
    fname="Leo",
    lname="Tolstoy",
)


b1 = Book(wap_b.title, wap_b.price, wap_a.author)


name = "Chapter 1"
pagecount = 104
b1.addchapter(Chapter(name, pagecount))


b1.addchapter(Chapter("Chapter 2", 89))
b1.addchapter(Chapter("Chapter 3", 124))


print(b1.title)
print(b1.author)
print(b1.getbookpagecount())
