##### example work ####

import mysql.connector

def select_data(connection):
    cursor=connection.cursor()
    testQuery= "SELECT * FROM pet_table"
    cursor.execute(testQuery)
    for item in cursor:
        print(item)
    cursor.close()

def select_databyid(connection,id):
    cursor=connection.cursor()
    testQuery= "SELECT * FROM pet_table WHERE `id_pet`=%s"
    cursor.execute(testQuery, id)
    for item in cursor:
        print(item)
    cursor.close()

def insert_data(connection, data):
    cursor=connection.cursor()
    addData = "INSERT INTO pet_table (pet_name, pet_age, pet_owner) VALUES (%s,%s,%s);"
    cursor.execute(addData, data)
    id=cursor.lastrowid
    cursor.close()
    return id

connection = mysql.connector.connect(user = 'root', database = 'example_1', password = 'Bippyb00')

id= insert_data(connection, ('pumpkin', 5000, 'mindy'))
print(id)

select_databyid(connection, (id,))

connection.close()