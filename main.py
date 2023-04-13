import mysql.connector

def select_data(connection):
    cursor=connection.cursor()
    testQuery= "SELECT * FROM pet_table"
    cursor.execute(testQuery)
    for item in cursor:
        print(item)
    cursor.close()

def insert_data(connection):
    cursor=connection.cursor()
    addData = "INSERT INTO table_name (column1, column2, column3…) VALUES (value1,value2,value3)"
    cursor.execute(addData)
    connection.commit()
    cursor.close()

connection = mysql.connector.connect(user = 'root', database = 'example_1', password = 'Bippyb00')

select_data(connection)

connection.close()