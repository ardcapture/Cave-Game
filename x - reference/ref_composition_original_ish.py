# Python Object Oriented Programming by Joe Marini course example
# Using composition to build complex objects


class Author:
    def __init__(self, fname: str, lname: str):
        self.fname = fname
        self.lname = lname

    def __str__(self):
        return f"{self.fname} {self.lname}"


class Chapter:
    def __init__(self, name: str, pagecount: int):
        self.name = name
        self.pagecount = pagecount


class Book:
    def __init__(self, title: str, price: float, author: Author):
        self.title = title
        self.price = price

        # Use references to other objects, like author and chapters
        self.author = author
        self.chapters: list[Chapter] = []

    def add_chapter(self, chapter: Chapter):
        self.chapters.append(chapter)

    def get_book_pagecount(self):
        result = 0
        for ch in self.chapters:
            result += ch.pagecount
        return result


auth = Author("Leo", "Tolstoy")
b1 = Book("War and Peace", 39.95, auth)

b1.add_chapter(Chapter("Chapter 1", 104))
b1.add_chapter(Chapter("Chapter 2", 89))
b1.add_chapter(Chapter("Chapter 3", 124))

print(b1.title)
print(b1.author)
print(b1.get_book_pagecount())
