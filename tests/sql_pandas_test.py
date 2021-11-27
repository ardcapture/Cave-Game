import sqlite3
import pandas as pd


db = sqlite3.connect('books.db')


data = pd.read_sql_query('SELECT * from books;', db)


# # show top 5 rows
# print(data.head())


# print(data)

