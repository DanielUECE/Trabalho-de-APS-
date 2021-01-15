from psycopg2 import connect
from config import DB_INFO
from appful import collection

# collection = [
#     {
#      'titulo': 'Guerra dos Tronos',
#      'preco': 59.9,
#      'autor': 'Geroge R. R. Martin'
#     },
#     {
#      'titulo': 'Fúria dos Reis',
#      'preco': 57.9,
#      'autor': 'Geroge R. R. Martin'
#     },
#     {
#      'titulo': 'Tormenta de Espadas',
#      'preco': 68.9,
#      'autor': 'Geroge R. R. Martin'
#     }
# ]

conn = connect(host=DB_INFO['DB_ADDR'], database=DB_INFO['DB_NAME'],
               user=DB_INFO['DB_USER'], password=DB_INFO['DB_PASS'])

cur = conn.cursor()
id_count = 1
for c in collection:
    cur.execute('INSERT INTO livros_flask_teste VALUES ({}, \'{}\', {}, \'{}\')'.format(id_count, *c.values()))
    id_count += 1

conn.commit()
conn.close()
