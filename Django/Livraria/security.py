from werkzeug.security import safe_str_cmp
from config import DB_INFO
from psycopg2 import connect
from appful import Costumer

# Criação da conexão com o banco
conn = connect(host=DB_INFO['DB_ADDR'], database=DB_INFO['DB_NAME'],
               user=DB_INFO['DB_USER'], password=DB_INFO['DB_PASS'])
cur = conn.cursor()

conn.close()


def authentication(costumername, password):
    costumer = Costumer.costumername_mapping.get(costumername, None)
    if costumer and safe_str_cmp(Costumer.password, password):
        return costumer


def identity(payload):
    costumer_id = payload['identity']
    return Costumer.costumerid_mapping.get(costumer_id, None)

