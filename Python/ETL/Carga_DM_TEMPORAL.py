import pandas as pd

anos = ['2018']#, '2019', '2020', '2021', '2022', '2023'] # Adicione aqui o ano referente a planilha que deseja carregar ao DW
tipo_despesa = [3] # [1, 2, 3]
dataframes = []

i = j = 0

def lendo_tabelas(anos, tipo_despesa, dataframes):
    for i in range(len(tipo_despesa)):
        for j in range(len(anos)):
            df = pd.read_excel(f'C:\\Users\\eduar\\Desktop\\TCC\\Dados\\DespesasLiquidaçõesAnuais\\Despesas-{tipo_despesa[i]}-{anos[j]}.xlsx')  # usecols('Data')' Coluna a buscar
            df = df.drop_duplicates(subset=['Data'])
            dataframes.append(df)
    # Concatenando em um único Dataframe
    df = pd.concat(dataframes, ignore_index=True)
    return df

# Realizando split na coluna desejada
def gerando_colunas(df):
    df[['dia', 'mes', 'ano']] = df['Data'].str.split('/', 2, expand=True)
    df['id_data'] = df['dia'].astype(str) + df['mes'].astype(str) + df['ano'].astype(str)
    return df

# Excluindo colunas desnecessárias
def excluir_colunas(df):
    del df['Data']
    return df

df = lendo_tabelas(anos, tipo_despesa, dataframes)
df = gerando_colunas(df)
#df = excluir_colunas(df)

print(df)

# Trabalhar na carga das colunas 'id_data', 'ano', 'mes' e 'dia' em DM_TEMPORAL
