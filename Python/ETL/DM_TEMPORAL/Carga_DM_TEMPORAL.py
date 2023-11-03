import pandas as pd
import psycopg2

anos = ['2018', '2019', '2020', '2021', '2022', '2023'] # Adicione aqui o ano referente a planilha que deseja carregar ao DW
tipo_despesa = [1, 2, 3] # 1 = Empenho; 2 = Pagamento; 3 - Liquidação
desc_tipo_despesa = ['EmpenhosAnuais', 'PagamentosAnuais', 'LiquidaçõesAnuais'] # Sufixo do nome das tabelas
dataframes = []
conexao = {'dbname': 'datawarehouse','user': 'postgres','password': 'postgres','host': 'postgres','port': '5432',}
i = j = 0

meses = {'01':'Janeiro', '02':'Fevereiro', '03':'Março',
        '04':'Abril', '05':'Maio', '06':'Junho',
        '07':'Julho', '08':'Agosto', '09':'Setembro',
        '10':'Outubro', '11':'Novembro', '12':'Dezembro',
        }

# conexão com o banco de dados
def abrir_conexao():
    conn = psycopg2.connect(**conexao)
    cursor = conn.cursor()
    return (conn, cursor)

# inserção no banco de dados
def inserir_dados(conn, cursor, dados):
    query = 'INSERT INTO dm_temporal (id_data, ano, mes, desc_mes, dia) VALUES (%s, %s, %s, %s, %s)'
    cursor.execute(query, dados)

# Leitura das tabelas Empenho, Pagamento e Liquidação
def lendo_tabelas(anos, tipo_despesa, dataframes):
    for i in range(len(tipo_despesa)):
        for j in range(len(anos)):
            df = pd.read_excel(f'/dados/Despesas{desc_tipo_despesa[i]}/Despesas-{tipo_despesa[i]}-{anos[j]}.xlsx')  # usecols('Credor')' Coluna a buscar
            df = df.drop_duplicates(subset=['Data'])
            dataframes.append(df)
    # Concatenando em um único Dataframe
    df = pd.concat(dataframes, ignore_index=True)
    return df

# Realizando split na coluna desejada
def gerando_colunas(df):
    df = df.drop_duplicates(subset=['Data'])
    df[['dia', 'mes', 'ano']] = df['Data'].str.split('/', n=2, expand=True)
    df['id_data'] = df['dia'].astype(str) + df['mes'].astype(str) + df['ano'].astype(str)
    return df

# Excluindo colunas desnecessárias
def excluir_colunas(df):
    del df['Data']
    return df

def iterar_df_final(df):
    conn, cursor = abrir_conexao()
    for coluna, linha in df.iterrows():
        id_data = linha['id_data']
        ano = linha['ano']
        mes = linha['mes']
        desc_mes = meses[mes]
        dia = linha['dia']
        dados = (id_data, ano, mes, desc_mes, dia)
        inserir_dados(conn, cursor, dados)
    conn.commit()
    conn.close()

df = lendo_tabelas(anos, tipo_despesa, dataframes)
df = gerando_colunas(df)
iterar_df_final(df)
