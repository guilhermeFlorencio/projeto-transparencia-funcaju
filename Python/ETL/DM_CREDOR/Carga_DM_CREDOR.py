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
    query = 'INSERT INTO dm_credor (codigo_nacional_credor, desc_credor) VALUES (%s, %s)'
    cursor.execute(query, dados)

# Leitura das tabelas Empenho, Pagamento e Liquidação
def lendo_tabelas(anos, tipo_despesa, dataframes):
    for i in range(len(tipo_despesa)):
        for j in range(len(anos)):
            df = pd.read_excel(f'/dados/Despesas{desc_tipo_despesa[i]}/Despesas-{tipo_despesa[i]}-{anos[j]}.xlsx')  # usecols('Credor')' Coluna a buscar
            df = df.drop_duplicates(subset=['Credor'])
            dataframes.append(df)
    # Concatenando em um único Dataframe
    df = pd.concat(dataframes, ignore_index=True)
    return df

# Removendo credores duplicados e realizando split na coluna desejada
def gerando_colunas(df):
    df = df.drop_duplicates(subset=['Credor'])
    df[['codigo_nacional_credor', 'desc_credor']] = df['Credor'].str.split(' - ', n=1, expand=True)
    return df

# Excluindo colunas desnecessárias
def excluir_colunas(df):
    del df['Credor']
    return df

def iterar_df_final(df):
    conn, cursor = abrir_conexao()
    for coluna, linha in df.iterrows():
        codigo_nacional_credor = linha['codigo_nacional_credor']
        desc_credor = linha['desc_credor']
        dados = (codigo_nacional_credor, desc_credor)
        inserir_dados(conn, cursor, dados)
    conn.commit()
    conn.close()

df = lendo_tabelas(anos, tipo_despesa, dataframes)
df = gerando_colunas(df)
iterar_df_final(df)
