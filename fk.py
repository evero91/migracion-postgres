import csv
import psycopg2

conn = psycopg2.connect(database="sibima2", user="", password="", host="localhost", port="5432")

if conn == None:
    print('Error de conexion con la base de datos')
    exit()

cur = conn.cursor()

with open('fk_sibima.csv') as csv_file:
    csv_reader = csv.reader(csv_file)

    for row in csv_reader:
        sql = f'ALTER TABLE {row[0].lower()} ADD FOREIGN KEY({row[1].lower()}) REFERENCES {row[2].lower()}({row[3].lower()});'
        print(sql)
        # cur.execute(sql)
        # conn.commit()

cur.close()
conn.close()
print('Exito')