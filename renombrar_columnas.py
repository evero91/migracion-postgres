import psycopg2

conn = psycopg2.connect(database="sibima2", user="", password="", host="localhost", port="5432")

if conn == None:
    print('Error de conexion con la base de datos')
    exit()

cur = conn.cursor()
sql = "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema'"
cur.execute(sql)
tablas = []

for row in cur.fetchall():
    tablas.append(row[0])

for tabla in tablas:
    sql = f"SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{tabla}'"
    cur.execute(sql)

    for row in cur.fetchall():
        if row[0] == row[0].lower():
            continue

        sql = f'ALTER TABLE {tabla} RENAME COLUMN "{row[0]}" TO {row[0].lower()}'
        # print(sql)
        cur.execute(sql)
        conn.commit()

print('Exito')
cur.close()
conn.close()