import sqlite3
from datetime import datetime

conn = sqlite3.connect('var/tweets.db')
cursor = conn.cursor()

cursor.execute("INSERT INTO Tweets (count, country, date) VALUES (?,?,?)", [10, "united states of america", datetime.strptime("19/04/2023", '%d/%m/%Y').date()])
cursor.execute("INSERT INTO Tweets (count, country, date) VALUES (?,?,?)", [5, "united states of america", datetime.strptime("20/04/2023", '%d/%m/%Y').date()])
cursor.execute("INSERT INTO Tweets (count, country, date) VALUES (?,?,?)", [3, "united states of america", datetime.strptime("21/04/2023", '%d/%m/%Y').date()])

results = cursor.execute("SELECT * FROM tweets WHERE country=?", ["united states of america"]).fetchall()

for elt in results:
    print(elt)

conn.commit()
conn.close()