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


# cursor.execute("SELECT * FROM vgsales limit 1")
# print(cursor.fetchall())

connection.close()



app = FastAPI()

@app.get("/") 
async def root():
    return {"message": "Hello, welcome!"}

# the top 10 most popular video games according to the global sales
query1 = """SELECT * FROM vgsales limit 10;"""

@app.get("/popular")
async def popular():
    return {"top 10 most popular video games": "10"} 


if __name__ == "__main__":
    uvicorn.run(app, port=8080, host="0.0.0.0")