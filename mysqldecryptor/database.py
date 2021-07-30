import re

import mysql.connector


def connect_to_database(user, password, host, port, database):
    return mysql.connector.connect(user=user, password=password, host=host, port=port, database=database)


def close_connection(connection):
    connection.close()


def read_from_table(connection, table_name, columns_name_list):
    cursor = connection.cursor(dictionary=True)

    # Formatting query string in the Python way is dangerous but needed if we want to use variable columns list
    # Following code will ensure, that columns and table names contain only safe characters
    is_name_safe(table_name)
    for name in columns_name_list:
        is_name_safe(name)
    query = 'SELECT `{}` FROM `{}`'.format(
        '`, `'.join(columns_name_list),
        table_name
    )

    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()

    return rows


def write_to_table(connection, rows, table_name, columns_name_list):
    cursor = connection.cursor()

    # Formatting query string in the Python way is dangerous but needed if we want to use variable columns list
    # Following code will ensure, that columns and table names contain only safe characters
    is_name_safe(table_name)
    for name in columns_name_list:
        is_name_safe(name)
    query = 'INSERT INTO `{}` (`{}`) VALUES (%({})s)'.format(
        table_name,
        '`, `'.join(columns_name_list),
        ')s, %('.join(columns_name_list)
    )

    cursor.executemany(query, rows)
    connection.commit()

    cursor.close()


def is_name_safe(name):
    if not re.match('^[a-zA-Z0-9 _-]+$', name):
        raise ValueError('Provided name "{}" is invalid! It can only contains small and capital ASCII letters, '
                         'numbers, space ( ), underscore (_) and dash (-).'.format(name))
