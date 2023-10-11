import pandas as pd
import psycopg2

def criar_dataframe():
    df = {'id_tipo_despesa': ['1', '2', '3'], 'desc_tipo_despesa': ['Empenho', 'Pagamento', 'Liquidação']}
    df = pd.DataFrame(df)
    return df

conexao = {'dbname': 'datawarehouse','user': 'postgres','password': 'postgres','host': 'postgres','port': '5432',}

# conexão com o banco de dados
def abrir_conexao():
    conn = psycopg2.connect(**conexao)
    cursor = conn.cursor()
    return (conn, cursor)

# inserção no banco de dados
def inserir_dados(conn, cursor, dados):
    query = 'INSERT INTO dm_tipo_despesa (id_tipo_despesa, desc_tipo_despesa) VALUES (%s, %s)'
    cursor.execute(query, dados)

def iterar_df_final(df):
    conn, cursor = abrir_conexao()
    for coluna, linha in df.iterrows():
        id_tipo_despesa = linha['id_tipo_despesa']
        desc_tipo_despesa = linha['desc_tipo_despesa']
        dados = (id_tipo_despesa, desc_tipo_despesa)
        inserir_dados(conn, cursor, dados)
    conn.commit()
    conn.close()

df = criar_dataframe()
iterar_df_final(df)