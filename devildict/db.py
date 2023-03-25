import sqlite3


class DictDB():
    def __init__(self, filename="devild.db"):
        self.createDB(filename)

    def createDB(self, filename="devild.db"):
        self.conn = sqlite3.connect(filename)
        self.cur = self.conn.cursor()
        self.cur.executescript('''
        CREATE TABLE IF NOT EXISTS Dict (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            name TEXT,
            pos TEXT,
            mean TEXT,
            ex TEXT
        );
        ''')

    def insertWord(self, name, pos, meaning, example):
        self.cur.execute('''INSERT OR IGNORE INTO Dict (name, pos, mean, ex)
         VALUES (?, ?, ?, ?)''', (name, pos, meaning, example))
        self.conn.commit()

    def searchWord(self, searchTerm="", tags=["name"]):
        self.cur.execute("SELECT * from Dict ORDER BY name")
        if searchTerm != "":
            self.cur.execute(f"""SELECT * from Dict
            WHERE LOWER(name) LIKE '%{searchTerm.lower()}%' ORDER BY name""")
        return self.cur.fetchall()

    def getOneWord(self, prop="id", value=0):
        self.cur.execute(f"SELECT * from Dict WHERE {prop} = ?", (value,))
        return self.cur.fetchone()

    def deleteWord(self, prop="id", value=0):
        self.cur.execute(f"DELETE from Dict WHERE {prop} = ?", (value,))
        self.conn.commit()

    def updateWord(self, with_prop, with_value, where_prop="id", where_value=0):
        if type(with_prop) == str and type(with_value) == str:
            self.cur.execute(
                f"UPDATE Dict SET {with_prop} = ? WHERE {where_prop} = ?", (with_value, where_value))
            self.conn.commit()
        else:
            if len(with_prop) != len(with_value):
                print("Length of with_prop and with_value are not same")
                return
            for i in range(len(with_prop)):
                self.updateWord(
                    with_prop[i], with_value[i], where_prop, where_value)

    def closeDB(self):
        self.conn.close()
