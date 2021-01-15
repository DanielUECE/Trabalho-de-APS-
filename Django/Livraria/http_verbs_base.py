from flask import Flask, request, render_template
from psycopg2 import connect
from config import DB_INFO


def post_base(item, items, item_endpoint, table_name, item_name):
    new_item = request.get_json()
    if new_item[item_endpoint] != item:
        raise Exception("Dados incompatíveis com endpoint")
    for i in items:
        if i[item] == item:
            return {'mensagem': f'{item_name} já cadastrado!'}, 400
    items.append(new_item)
    conn = connect(host=DB_INFO['DB_ADDR'], database=DB_INFO['DB_NAME'],
                   user=DB_INFO['DB_USER'], password=DB_INFO['DB_PASS'])
    cur = conn.cursor()
    keys = '('
    values = '('
    for k, v in new_item.items():
        keys += k.replace('\'', '\\''')
        keys += ', '
        if isinstance(v, str):
            values += ''' + v + '''
        else:
            values += str(v)

        values += ', '
    keys = keys[:-2] + ')'
    values = values[:-2] + ')'
    cur.execute('INSERT INTO {} {} VALUES {}'.format(table_name, keys, values))
    conn.commit()
    conn.close()
    return new_item, 201
