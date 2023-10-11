import pandas as pd
import psycopg2

anos = ['2018', '2019', '2020', '2021', '2022', '2023'] # Adicione aqui o ano referente a planilha que deseja carregar ao DW
tipo_despesa = [1, 2, 3] # 1 = Empenho; 2 = Pagamento; 3 - Liquidação
desc_tipo_despesa = ['EmpenhosAnuais', 'PagamentosAnuais', 'LiquidaçõesAnuais'] # Sufixo do nome das tabelas
dataframes = []
conexao = {'dbname': 'datawarehouse','user': 'postgres','password': 'postgres','host': 'postgres','port': '5432',}
i = j = 0

# conexão com o banco de dados
def abrir_conexao():
    conn = psycopg2.connect(**conexao)
    cursor = conn.cursor()
    return (conn, cursor)

# inserção no banco de dados
def inserir_dados(conn, cursor, dados):
    query = '''INSERT INTO ft_despesas (codigo_nacional_credor, 
                                        desc_credor,

                                        ) 
            VALUES (%s, %s)'''
    cursor.execute(query, dados)


# Consultar: 
# id_unidade
# id_tipo_despesa
# id_credor
# id_data

# Ler
# id_item_despesa (PK)
# etc...