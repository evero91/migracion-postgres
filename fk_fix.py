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

fks_incorrectas = []

for tabla in tablas:
    sql = f"SELECT con.conname FROM pg_catalog.pg_constraint con INNER JOIN pg_catalog.pg_class rel ON rel.oid = con.conrelid INNER JOIN pg_catalog.pg_namespace nsp ON nsp.oid = connamespace WHERE nsp.nspname = 'public' AND rel.relname = '{tabla}'"
    cur.execute(sql)

    for row in cur.fetchall():
        if '0' in row[0] or '1' in row[0] or '2' in row[0] or '3' in row[0] or '4' in row[0] or '5' in row[0] or '6' in row[0] or '7' in row[0] or '8' in row[0] or '9' in row[0]:
            fks_incorrectas.append((tabla, row[0]))

for tabla, fk in fks_incorrectas:
    sql = f"ALTER TABLE {tabla} DROP CONSTRAINT {fk}"
    cur.execute(sql)
    conn.commit()

cur.close()
conn.close()

print('Exito')