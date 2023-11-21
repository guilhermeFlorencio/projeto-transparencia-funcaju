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
    query = '''
    INSERT INTO ft_despesas (id_unidade, id_tipo_despesa, id_data, id_item_despesa, id_credor, id_despesa, desc_despesa, valor_empenhado, valor_reforcado, valor_liquidado, valor_pago, valor_retido, valor_anulado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    cursor.execute(query, dados)

def definir_tipo_despesa(tipo_despesa, i, df):
    if tipo_despesa[i] == 1:
        df['id_tipo_despesa'] = 1
        df = df.rename(columns={'SqEmpenho': 'id_despesa'})
        df = df.rename(columns={'DsEmpenho': 'desc_despesa'})
        return df
    
    if tipo_despesa[i] == 2:
        df['id_tipo_despesa'] = 2
        df = df.rename(columns={'Nota de Pagamento': 'id_despesa'})
        df = df.rename(columns={'DsEmpenho': 'desc_despesa'})
        return df
    
    if tipo_despesa[i] == 3:
        df['id_tipo_despesa'] = 3
        return df

# Leitura das tabelas Empenho, Pagamento e Liquidação
def lendo_tabelas(anos, tipo_despesa, dataframes):
    for i in range(len(tipo_despesa)):
        if tipo_despesa[i] == 1:
            for j in range(len(anos)):
                df = pd.read_excel(f'/dados/Despesas{desc_tipo_despesa[i]}/Despesas-{tipo_despesa[i]}-{anos[j]}.xlsx')  # usecols('Coluna')' Coluna a buscar
                df[['id_item_despesa', 'desc_item_despesa']] = df['DsItemDespesa'].str.split(' - ', n=1, expand=True)
                df = df.rename(columns={'Anulado': 'Anulação'})
                df = definir_tipo_despesa(tipo_despesa, i, df)
                dataframes.append(df)

        if tipo_despesa[i] == 2:
            for j in range(len(anos)):
                df = pd.read_excel(f'/dados/Despesas{desc_tipo_despesa[i]}/Despesas-{tipo_despesa[i]}-{anos[j]}.xlsx')  # usecols('Coluna')' Coluna a buscar
                df[['id_item_despesa', 'desc_item_despesa']] = df['DsItemDespesa'].str.split(' - ', n=1, expand=True)
                df = definir_tipo_despesa(tipo_despesa, i, df)
                dataframes.append(df)

        if tipo_despesa[i] == 3:
            for j in range(len(anos)):
                df = pd.read_excel(f'/dados/Despesas{desc_tipo_despesa[i]}/Despesas-{tipo_despesa[i]}-{anos[j]}.xlsx')  # usecols('Coluna')' Coluna a buscar
                df = df.rename(columns={'DsEmpenho': 'id_despesa'})
                df = df.rename(columns={'DsItemDespesa': 'desc_despesa'})
                df = df.rename(columns={df.columns[15]: 'DsItemDespesa'})
                df[['id_item_despesa', 'desc_item_despesa']] = df['DsItemDespesa'].str.split(' - ', n=1, expand=True)
                df = definir_tipo_despesa(tipo_despesa, i, df)
                dataframes.append(df)
            
    # Concatenando em um único Dataframe
    df = pd.concat(dataframes, ignore_index=True)
    return df

# Removendo duplicados e realizando split nas colunas desejadas (Colunas padronizadas)
def gerando_colunas_padrao(df):
    #df = df.drop_duplicates(subset=['Credor', 'Órgão', 'Unidade', 'Data'])
    df[['codigo_nacional_credor', 'desc_credor']] = df['Credor'].str.split(' - ', n=1, expand=True)
    df[['id_orgao', 'desc_orgao']] = df['Órgão'].str.split(' - ', n=1, expand=True)
    df[['id_unidade', 'desc_unidade']] = df['Unidade'].str.split(' - ', n=1, expand=True)
    df[['dia', 'mes', 'ano']] = df['Data'].str.split('/', n=2, expand=True)
    df['id_data'] = df['dia'].astype(str) + df['mes'].astype(str) + df['ano'].astype(str)
    return df

# Atribuindo id_tipo_despesa e desc_tipo_despesa

# Capturar o id_credor incremental atribuido ao credor na tabela DM_CREDOR
def resgatar_id_credor(cursor, query_credor, df):
    query = '''
    SELECT id_credor
    FROM dm_credor
    WHERE codigo_nacional_credor = %s AND
          desc_credor = %s
    '''
    cursor.execute(query, query_credor)
    query_id_credor = cursor.fetchone()
    return query_id_credor[0]
    

# Iterar Dataframe, buscar id_credor e realizar carga em FT_DESPESAS
def iterar_df(df):
    conn, cursor = abrir_conexao()
    for coluna, linha in df.iterrows():
        id_unidade = linha['id_unidade']
        id_tipo_despesa = linha['id_tipo_despesa']
        id_data = linha['id_data']
        id_item_despesa = linha['id_item_despesa']
        id_despesa = linha['id_despesa']
        valor_empenhado = linha['Empenhado']
        valor_reforcado = linha['Reforçado']
        valor_liquidado = linha['Liquidado']
        valor_pago = linha['Pago']
        valor_retido = linha['Retido']
        valor_anulado = linha['Anulação']
        desc_despesa = linha['desc_despesa']
        codigo_nacional_credor = linha['codigo_nacional_credor']
        desc_credor = linha['desc_credor']

        query_credor = (codigo_nacional_credor, desc_credor)
        id_credor = resgatar_id_credor(cursor, query_credor, df)

        dados = (int(id_unidade), int(id_tipo_despesa), int(id_data), int(id_item_despesa), int(id_credor), int(id_despesa),
                 str(desc_despesa), str(valor_empenhado), str(valor_reforcado), str(valor_liquidado), 
                 str(valor_pago), str(valor_retido), str(valor_anulado))
        inserir_dados(conn, cursor, dados)
    conn.commit()
    conn.close()

df = lendo_tabelas(anos, tipo_despesa, dataframes)   
df = gerando_colunas_padrao(df)   
iterar_df(df)

