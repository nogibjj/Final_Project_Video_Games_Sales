from fastapi import FastAPI
import uvicorn
import pandas as pd
import sqlite3
import csv

# Creating the database
connection = sqlite3.connect('vgsales.db')
drop_table = 'DROP TABLE IF EXISTS vgsales'
create_table = 'CREATE TABLE vgsales (Rank INT, Name VAR, Platform VAR, Year INT, Genre VAR, Publisher VAR, NA_Sales REAL, EU_Sales REAL, JP_Sales REAL, Other_Sales REAL, Global_Sales REAL)'

#setting up connection
cursor = connection.cursor()
cursor.execute(drop_table)
cursor.execute(create_table)

#insert data into the table 
insert_data = 'INSERT INTO vgsales(Rank, Name, Platform, Year, Genre, Publisher, NA_Sales, EU_Sales, JP_Sales, Other_Sales, Global_Sales) VALUES (?,?,?,?,?,?,?,?,?,?,?)'
file = open('/workspaces/FINAL_PROJECT/vgsales.csv')
contents = csv.reader(file)
next(contents)

seq_of_parameters = []
for row in contents:
    seq_of_parameters.append(row)

for i in seq_of_parameters:
    cursor.execute(insert_data,i)

connection.commit()



app = FastAPI()

@app.get("/") 
async def root():
    return {"message": "Hello, welcome!"}

# the top 10 most popular video games according to the global sales
@app.get("/popular/")
async def popular():
    df = pd.read_csv('vgsales.csv', encoding= 'unicode_escape')
    table = df.head(10)
    print(table)
    return{"table": table}

if __name__ == "__main__":
    uvicorn.run(app, port=8080, host="0.0.0.0")