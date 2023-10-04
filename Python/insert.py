import psycopg2

host = 'localhost',
database = 'datawarehouse'
user = 'postgres'
password = 'postgres'

def conexao_dw(host, database, user, password):
    con = psycopg2.connect(host = host, \
        database = database, \
        user = user, \
        password = password)
    return con

con_dw = conexao_dw(host, database, user, password)

