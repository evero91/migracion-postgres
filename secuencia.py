import csv
import psycopg2

conn = psycopg2.connect(database="sibima2", user="", password="", host="localhost", port="5432")

if conn == None:
    print('Error de conexion con la base de datos')
    exit()

def create_secuence(tabla, pk_tabla):
    cur = conn.cursor()
    sql = f'SELECT MAX("{pk_tabla}") + 1 FROM {tabla}'
    cur.execute(sql)
    inicio_secuencia = 0

    for row in cur.fetchall():
        inicio_secuencia = row[0]

    nombre_secuencia = (tabla + '_' + pk_tabla + '_seq').lower()
    sql = f'CREATE SEQUENCE {nombre_secuencia} START WITH {inicio_secuencia}'
    cur.execute(sql)

    sql = f'ALTER TABLE {tabla} ALTER COLUMN "{pk_tabla}" SET DEFAULT nextval(\'{nombre_secuencia}\');'
    cur.execute(sql)
    cur.close()
    conn.commit()

with open('secuencia_sibima.csv') as csv_file:
    csv_reader = csv.reader(csv_file)

    for row in csv_reader:
        create_secuence(row[0], row[1])


conn.close()
print('Exito')
