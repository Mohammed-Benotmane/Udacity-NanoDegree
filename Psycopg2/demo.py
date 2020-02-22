import psycopg2

connection = psycopg2.connect(user = "postgres",
                              password = "1475963mimo",
                              database = "udacity")

cursor = connection.cursor()

cursor.execute('DROP table if exists table2;')

cursor.execute('''
CREATE TABLE table2 (
    id INTEGER primary key,
    completed BOOLEAN not null default False
);  
''')
data ={
    'id': 2,
    'completed': False
}

data2 ={
    'id': 1,
    'completed': True
}

SQL ='INSERT INTO table2 (id, completed) values (%(id)s, %(completed)s);'
cursor.execute(SQL,data)
cursor.execute(SQL,data2)

cursor.execute('SELECT * from table2;')

result = cursor.fetchall()
print(result[1])
connection.commit()

connection.close()
cursor.close()