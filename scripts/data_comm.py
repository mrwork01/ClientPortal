import sqlite3
import pandas as pd

def query_db_all(database, table):
	conn = sqlite3.connect(database)

	query = 'SELECT * FROM {};'.format(table)

	data = pd.read_sql_query(query,conn)

	return data

def query_value(database, table, column, value):
	conn = sqlite3.connect(database)

	query = 'SELECT * FROM {} WHERE {}="{}";'.format(table, column, value)

	data = pd.read_sql_query(query,conn)

	return data

def query_mult(database, table, keys, variables):
	conn = sqlite3.connect(database)

	query = 'SELECT * FROM {}'.format(table)

	used = 0

	for i in range(len(variables)):
		if (variables[i] != ''):
			if used == 0:
				query = query + " WHERE {} = '{}'".format(keys[i], variables[i])
				used = used + 1
			else:
				query = query + " AND {} = '{}'".format(keys[i], variables[i])

	query = query + ';'

	print(query)

	data = pd.read_sql_query(query,conn)

	return data