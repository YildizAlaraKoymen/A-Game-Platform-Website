import sqlite3

def createDB(dbname):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    #creating the user table
    c.execute("CREATE TABLE IF NOT EXISTS User(username TEXT PRIMARY KEY, "
              "password TEXT NOT NULL,"
              "name TEXT NOT NULL,"
              "email TEXT NOT NULL,"
              "isAdmin BOOLEAN NOT NULL)")

    #creating the game table
    c.execute("""
    CREATE TABLE IF NOT EXISTS Game(
        gameID INTEGER PRIMARY KEY AUTOINCREMENT,
        price DOUBLE NOT NULL,
        title TEXT NOT NULL,
        isFullrelease BOOLEAN NOT NULL,
        description TEXT NOT NULL,
        username TEXT NOT NULL,
        FOREIGN KEY(username) REFERENCES User(username) ON DELETE CASCADE
    );
    """)

    #creating the genre table
    c.execute("CREATE TABLE IF NOT EXISTS Genre(genreID INTEGER PRIMARY KEY AUTOINCREMENT,"
              "name TEXT NOT NULL)")

    #creating the belong to relationship table
    c.execute("CREATE TABLE IF NOT EXISTS GenreOfGame(gameID INTEGER NOT NULL,"
              "genreID INTEGER NOT NULL,"
              "PRIMARY KEY (gameID, genreID),"
              " FOREIGN KEY (gameID) REFERENCES Game (gameID) ON DELETE CASCADE,"
              "FOREIGN KEY (genreID) REFERENCES Genre (genreID) ON DELETE CASCADE)")

    conn.commit() #saving changes
    conn.close()

def viewDB(dbname):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    # Fetching table names
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()

    print("Tables in the database:")
    for table in tables:
        print(f"- {table[0]}")

    # Displaying the content of each table
    for table in tables:
        print(f"\nContents of {table[0]}:")
        c.execute(f"SELECT * FROM {table[0]};")
        rows = c.fetchall()
        for row in rows:
            print(row)

    conn.close()

if __name__ == '__main__':
    createDB("game.db")
    viewDB("game.db")