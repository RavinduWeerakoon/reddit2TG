import sqlite3
import datetime 

class PrevPosts:
    def __init__(self):
        self.db = sqlite3.connect("reddit_bot.db")
        self.cursor = self.db.cursor()
        self.cursor.execute("""
                            CREATE TABLE if not exists posted
                            (
    
                                date  text    not null,
                                url   text    not null
                            )""")
        self.db.commit()
    

    def execute(self, query):
        res = self.cursor.execute(query)
        return res if res else None

    def insert_urls(self, url_list):
        self.cursor.executemany("INSERT INTO posted VALUES(?, ?)", [(datetime.date.today().strftime("%d/%m/%Y"), url) for url in url_list])
        self.db.commit()

    def get_last_urls(self, count=20):

        res = self.execute(f"SELECT url FROM posted ORDER BY rowid")
        last_urls = res.fetchmany(count)
        return [item[0] for item in last_urls]
