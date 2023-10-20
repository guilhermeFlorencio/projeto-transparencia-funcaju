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
    query = 'INSERT INTO dm_item_despesa (id_item_despesa, desc_item_despesa) VALUES (%s, %s)'
    cursor.execute(query, dados)

# Leitura das tabelas Empenho, Pagamento e Liquidação
def lendo_tabelas(anos, tipo_despesa, dataframes):
    for i in range(len(tipo_despesa)):
        if tipo_despesa[i] == 1 or tipo_despesa[i] == 2:
            for j in range(len(anos)):
                df = pd.read_excel(f'/dados/Despesas{desc_tipo_despesa[i]}/Despesas-{tipo_despesa[i]}-{anos[j]}.xlsx')  # usecols('Coluna')' Coluna a buscar
                df = df.drop_duplicates(subset=['DsItemDespesa'])
                df = df[['id_item_despesa', 'desc_item_despesa']] = df['DsItemDespesa'].str.split(' - ', n=1, expand=True)
                dataframes.append(df)
        if tipo_despesa[i] == 3:
            for j in range(len(anos)):
                df = pd.read_excel(f'/dados/Despesas{desc_tipo_despesa[i]}/Despesas-{tipo_despesa[i]}-{anos[j]}.xlsx')  # usecols('Coluna')' Coluna a buscar
                df = df.drop(['DsItemDespesa'], axis=1)
                df = df.rename(columns={df.columns[14]: 'DsItemDespesa'})
                df = df.drop_duplicates(subset=['DsItemDespesa'])
                df = df[['id_item_despesa', 'desc_item_despesa']] = df['DsItemDespesa'].str.split(' - ', n=1, expand=True)
                dataframes.append(df)

    # Concatenando em um único Dataframe
    df = pd.concat(dataframes, ignore_index=True)
    df = df.drop_duplicates(subset=['id_item_despesa', 'desc_item_despesa'])
    return df

def iterar_df_final(df):
    conn, cursor = abrir_conexao()
    for coluna, linha in df.iterrows():
        id_item_despesa = linha['id_item_despesa']
        desc_item_despesa = linha['desc_item_despesa']
        dados = (id_item_despesa, desc_item_despesa)
        inserir_dados(conn, cursor, dados)
    conn.commit()
    conn.close()

df = lendo_tabelas(anos, tipo_despesa, dataframes)
iterar_df_final(df)
