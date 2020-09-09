import psycopg2

conn = psycopg2.connect(database="bdalmacen", user="", password="", host="localhost", port="5432")

if conn == None:
    print('Error de conexion con la base de datos')
    exit()

cur = conn.cursor()
sql = "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema'"
cur.execute(sql)
tablas = []

for row in cur.fetchall():
    tablas.append(row[0])

tablas_idusuario = []

for tabla in tablas:
    sql = f"SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name   = '{tabla}'"
    cur.execute(sql)

    for row in cur.fetchall():
        if row[0] == 'idusuario':
            tablas_idusuario.append(tabla)
            break

tabla_idusuario_incorrecto = []

for tabla in tablas_idusuario:
    sql = f'SELECT DISTINCT(idusuario) FROM {tabla} WHERE idusuario NOT IN (SELECT idusuario FROM usuario)'
    cur.execute(sql)

    for row in cur.fetchall():
        tabla_idusuario_incorrecto.append((tabla, row[0]))

for tabla, valor in tabla_idusuario_incorrecto:
    print(f'{tabla}\t{valor}')

cur.close()
conn.close()