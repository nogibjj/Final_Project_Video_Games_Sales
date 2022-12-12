from fastapi import FastAPI
import uvicorn
import sqlite3
import csv

# Creating the database
connection = sqlite3.connect('vgsales.db')

#setting up connection
cursor = connection.cursor()

drop_table = 'DROP TABLE IF EXISTS vgsales'
create_table = 'CREATE TABLE vgsales (Rank INT, Name VAR, Platform VAR, Year INT, Genre VAR, Publisher VAR, NA_Sales REAL, EU_Sales REAL, JP_Sales REAL, Other_Sales REAL, Global_Sales REAL)'

cursor.execute(drop_table)
cursor.execute(create_table)

#insert data into the table 
insert_data = 'INSERT INTO vgsales(Rank, Name, Platform, Year, Genre, Publisher, NA_Sales, EU_Sales, JP_Sales, Other_Sales, Global_Sales) VALUES (?,?,?,?,?,?,?,?,?,?,?)'
file = open("vgsales.csv", encoding='utf-8')
contents = csv.reader(file)
header = next(contents)
if header != None:
    for row in contents:
        cursor.execute(insert_data,(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10]))

connection.commit()


cursor.execute("SELECT Publisher, COUNT(Publisher) AS 'num_of_pub' FROM vgsales WHERE Year BETWEEN 2011 AND 2015 GROUP BY Publisher ORDER BY num_of_pub DESC LIMIT 10;")
print(cursor.fetchall())

connection.close()


app = FastAPI()

@app.get("/") 
async def root():
    return {"message": "Hello, welcome!"}

# the top 10 most popular video games according to the global sales
query1 = """SELECT Rank, Name, Platform, Year, Genre, Publisher, Global_Sales FROM vgsales limit 10;"""

@app.get("/popular")
async def popular():
    return {"top 10 most popular video games": "10"} 







# The types of games that users preferred from 2011 to 2015, 2015-2020

query2 = """
    SELECT Genre, COUNT(Genre) AS 'num_of_genre' 
    FROM vgsales 
    WHERE Year BETWEEN 2011 AND 2015 
    GROUP BY Genre 
    ORDER BY num_of_genre DESC;
"""
query3 = """
    SELECT Genre, COUNT(Genre) AS 'num_of_genre' 
    FROM vgsales 
    WHERE Year BETWEEN 2015 AND 2020 
    GROUP BY Genre 
    ORDER BY num_of_genre DESC;
"""


@app.get("/type")
async def type1():
    return {"2011-2015": "10"} 



# Top 10 global publishers from 2011-2015, 2015-2020

query4 = """
    SELECT Publisher, COUNT(Publisher) AS 'num_of_pub' 
    FROM vgsales 
    WHERE Year BETWEEN 2011 AND 2015 
    GROUP BY Publisher 
    ORDER BY num_of_pub DESC
    LIMIT 10;
"""
query5 = """
    SELECT Publisher, COUNT(Publisher) AS 'num_of_pub' 
    FROM vgsales 
    WHERE Year BETWEEN 2015 AND 2020 
    GROUP BY Publisher 
    ORDER BY num_of_pub DESC
    LIMIT 10;
"""












if __name__ == "__main__":
    uvicorn.run(app, port=8080, host="0.0.0.0")