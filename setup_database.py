import sqlite3

def initialize_db():
    conn = sqlite3.connect('movies.db')  # This will create the database file
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS movies')
    cursor.execute('DROP TABLE IF EXISTS ratings')
    cursor.execute('DROP TABLE IF EXISTS movies_watchlist')

    cursor.execute('''
        CREATE TABLE movies (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            director TEXT NOT NULL,
            actors TEXT NOT NULL,
            year INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            rating_value INTEGER NOT NULL,
            FOREIGN KEY (movie_id) REFERENCES movies(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE movies_watchlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (movie_id) REFERENCES movies(id)
        )
    ''')

    cursor.execute('''INSERT INTO movies (title, director, actors, year) VALUES ('Inception', 'Christopher Nolan', 'Leonardo DiCaprio, Joseph Gordon-Levitt, Ellen Page', 2010);''')
    cursor.execute('''INSERT INTO movies (title, director, actors, year) VALUES ('The Matrix', 'Lana Wachowski', 'Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss', 1999);''')
    cursor.execute('''INSERT INTO movies (title, director, actors, year) VALUES ('Interstellar', 'Christopher Nolan', 'Matthew McConaughey, Anne Hathaway, Jessica Chastain', 2014);''')
    cursor.execute('''INSERT INTO movies (title, director, actors, year) VALUES ('The Lord of the Rings: The Fellowship of the Ring', 'Peter Jackson', 'Elijah Wood, Ian McKellen, Orlando Bloom', 2001);''')
    cursor.execute('''INSERT INTO movies (title, director, actors, year) VALUES ('Forrest Gump', 'Robert Zemeckis', 'Tom Hanks, Robin Wright, Gary Sinise', 1994);''')
    cursor.execute('''INSERT INTO movies (title, director, actors, year) VALUES ('Fight Club', 'David Fincher', 'Brad Pitt, Edward Norton, Helena Bonham Carter', 1999);''')
    cursor.execute('''INSERT INTO movies (title, director, actors, year) VALUES ('Pulp Fiction', 'Quentin Tarantino', 'John Travolta, Uma Thurman, Samuel L. Jackson', 1994);''')
    cursor.execute('''INSERT INTO movies (title, director, actors, year) VALUES ('Shutter Island', 'Martin Scorsese', 'Leonardo DiCaprio, Mark Ruffalo, Ben Kingsley', 2010);''')
    cursor.execute('''INSERT INTO movies (title, director, actors, year) VALUES ('The Dark Knight', 'Christopher Nolan', 'Christian Bale, Heath Ledger, Aaron Eckhart', 2008);''')
    cursor.execute('''INSERT INTO movies (title, director, actors, year) VALUES ('Gladiator', 'Ridley Scott', 'Russell Crowe, Joaquin Phoenix, Connie Nielsen', 2000);''')

    conn.commit()
    conn.close()

initialize_db()
