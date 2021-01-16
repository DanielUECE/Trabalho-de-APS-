from flask import Flask, request, render_template
from psycopg2 import connect, extras
from config import DB_INFO


def format_string_type(attribute):
    if isinstance(attribute, str):
        formated_attribute = '\'' + attribute + '\''
    elif isinstance(attribute, list):
        formated_attribute = 'ARRAY' + str(attribute)
    elif attribute is None:
        formated_attribute = 'Null'
    else:
        formated_attribute = str(attribute)
    return formated_attribute


def get_columns(table_name):
    conn = connect(host=DB_INFO['DB_ADDR'], database=DB_INFO['DB_NAME'],
                   user=DB_INFO['DB_USER'], password=DB_INFO['DB_PASS'])
    cur = conn.cursor(cursor_factory=extras.DictCursor)
    cur.execute(f'SELECT * FROM {table_name}')
    columns_names = [desc[0] for desc in cur.description]
    cur.execute("""select *
                           from information_schema.columns
                           where table_schema NOT IN ('information_schema', 'pg_catalog')
                           order by table_schema, table_name""")
    columns_types = []
    for ccn in columns_names:
        for row in cur:
            if row['table_name'] == table_name and row['column_name'] == ccn:
                columns_types.append(row['data_type'])
    conn.close()
    return columns_names, columns_types


def mapping_base(table_name, columns_names):
    conn = connect(host=DB_INFO['DB_ADDR'], database=DB_INFO['DB_NAME'],
                   user=DB_INFO['DB_USER'], password=DB_INFO['DB_PASS'])
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM {table_name}')
    fetch_items = cur.fetchall()
    conn.close()
    t = len(columns_names)
    items = []
    for i in fetch_items:
        id = dict()
        for j in range(t):
            id.update({columns_names[j]: i[j]})
        items.append(id)
    return items, {i['id']: i for i in items}, {i['nome']: i for i in items}


def get_base(item_endpoint, item_key, table_name, item_name):
    conn = connect(host=DB_INFO['DB_ADDR'], database=DB_INFO['DB_NAME'],
                   user=DB_INFO['DB_USER'], password=DB_INFO['DB_PASS'])
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM {table_name} WHERE {item_key} = {format_string_type(item_endpoint)}')
    fetch_item = list(cur.fetchone())
    conn.close()
    columns, _ = get_columns(table_name)
    fetch_item_dict = dict()
    if fetch_item is not None:
        for c in columns:
            fetch_item_dict.update({c: format_string_type(fetch_item[columns.index(c)])})
    else:
        return {'mensagem': f'{item_name}'}, 404
    return fetch_item_dict, 200


def post_base(item_endpoint, items, item_key, table_name, item_name):
    new_item = request.get_json()
    if new_item[item_key] != item_endpoint:
        raise Exception(f"{item_key} incompatível com endpoint".capitalize())
    for i in items:
        if i[item_key] == item_endpoint:
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
        values += format_string_type(v) + ', '

    keys = keys[:-2] + ')'
    values = values[:-2] + ')'

    cur.execute(f'INSERT INTO {table_name} {keys} VALUES {values}')
    conn.commit()
    conn.close()

    return new_item, 201


def put_base(item_endpoint, item_key, table_name):
    new_item = request.get_json()
    conn = connect(host=DB_INFO['DB_ADDR'], database=DB_INFO['DB_NAME'],
                   user=DB_INFO['DB_USER'], password=DB_INFO['DB_PASS'])
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM {table_name} WHERE {item_key} = {format_string_type(item_endpoint)}')
    fetch_item = cur.fetchone()
    keys = '('
    values = '('
    for k, v in new_item.items():
        keys += k.replace('\'', '\\''')
        keys += ', '
        values += format_string_type(v) + ', '
    keys = keys[:-2] + ')'
    values = values[:-2] + ')'

    if fetch_item is None:
        cur.execute(f'INSERT INTO {table_name} {keys} VALUES {values}')
    else:
        keys = keys.replace('(', '').replace(')', '')
        values = values.replace('(', '').replace(')', '')
        keys = keys.split(',')
        values = values.split(',')
        t = len(values)
        assignments = ''
        for i in range(t):
            assignments += keys[i] + ' = ' + values[i] + ','

        cur.execute(f'UPDATE {table_name} SET {assignments[:-1]} WHERE id = {fetch_item[0]}')

    conn.commit()
    conn.close()

    return new_item


def delete_base(item_endpoint, item_key, table_name):
    conn = connect(host=DB_INFO['DB_ADDR'], database=DB_INFO['DB_NAME'],
                   user=DB_INFO['DB_USER'], password=DB_INFO['DB_PASS'])
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM {table_name} WHERE {item_key} = {format_string_type(item_endpoint)}')
    fetch_item = cur.fetchone()
    columns, _ = get_columns(table_name)
    fetch_item_dict = dict()
    if fetch_item is not None:
        for c in columns:
            fetch_item_dict.update({c: format_string_type(fetch_item[columns.index(c)])})
    else:
        for c in columns:
            fetch_item_dict.update({c: None})
    fetch_item_dict.update({item_key: item_endpoint})
    cur.execute(f'DELETE FROM {table_name} WHERE {item_key} = {format_string_type(item_endpoint)}')
    conn.commit()
    conn.close()

    return fetch_item_dict
