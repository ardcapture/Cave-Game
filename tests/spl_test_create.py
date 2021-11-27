import sqlite3

db = sqlite3.connect('books.db')

cur = db.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS books(
    id interger PRIMARY KEY,
    title text NOT NULL,
    author text NOT NULL,
    price real);''')

book_list = [('2', 'Lucky Jim', 'Kingsley Amis', '6.20'),
             ('3', 'Animal Farm', 'George Orwell', '7.49'),
             ('4', 'Why I am so Clever', 'Friedrich Nietzsch', '10.40'),
             ('1', 'Untold Stories', 'Alan Bennett', '17.49')
            ]

cur.executemany('''INSERT INTO books(id, title, author, price)
        VALUES(?,?,?,?)''', book_list)


cur.execute('SELECT * FROM books')
print(cur.fetchall())



db.commit()
db.close()