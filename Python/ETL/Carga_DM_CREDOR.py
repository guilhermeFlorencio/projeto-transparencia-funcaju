import pandas as pd

anos = ['2018']#, '2019', '2020', '2021', '2022', '2023'] # Adicione aqui o ano referente a planilha que deseja carregar ao DW
tipo_despesa = [3] # [1, 2, 3]
dataframes = []

i = j = 0

def lendo_tabelas(anos, tipo_despesa, dataframes):
    for i in range(len(tipo_despesa)):
        for j in range(len(anos)):
            df = pd.read_excel(f'C:\\Users\\eduar\\Desktop\\TCC\\Dados\\DespesasLiquidaçõesAnuais\\Despesas-{tipo_despesa[i]}-{anos[j]}.xlsx')  # usecols('Credor')' Coluna a buscar
            df = df.drop_duplicates(subset=['Credor'])
            dataframes.append(df)
    # Concatenando em um único Dataframe
    df = pd.concat(dataframes, ignore_index=True)
    return df

# Realizando split na coluna desejada
def gerando_colunas(df):
    df[['codigo_nacional_credor', 'desc_credor']] = df['Credor'].str.split(' - ', 1, expand=True)
    return df

# Excluindo colunas desnecessárias
def excluir_colunas(df):
    del df['Credor']
    return df

df = lendo_tabelas(anos, tipo_despesa, dataframes)
df = gerando_colunas(df)
#df = excluir_colunas(df)

print(df)

# Trabalhar na carga das colunas 'id_credor', 'codigo_nacional_credor' e 'desc_credor' em DM_CREDOR
# Lembrar que id_credor é autoincremental