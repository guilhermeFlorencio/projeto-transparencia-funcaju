import pandas as pd

anos = ['2018', '2019', '2020', '2021', '2022', '2023'] # Adicione aqui o ano referente a planilha que deseja atualizar

# Renomeando colunas
def renomear_colunas(df):
    print('Padronizando colunas')
    cabecalhos = {'DsEmpenho' : 'id_despesa', 'DsItemDespesa' : 'desc_despesa', 'Unnamed: 15' : 'DsItemDespesa'}
    df.rename(columns=cabecalhos, inplace=True)
    print(df)
    #df.to_excel(f"C:\\Users\\eduar\\Desktop\\{ano}.xlsx", index=False)
    return df

# Realizando split nas colunas desejadas e concatenando id_data
def gerando_colunas(df):
    print('Dividindo colunas')
    df[['id_orgao', 'desc_orgao']] = df['Órgão'].str.split(' - ', 1, expand=True)
    df[['id_unidade', 'desc_unidade']] = df['Unidade'].str.split(' - ', 1, expand=True)
    df[['dia', 'mes', 'ano']] = df['Data'].str.split('/', 2, expand=True)
    df['id_data'] = df['dia'].astype(str) + df['mes'].astype(str) + df['ano'].astype(str)
    df[['codigo_nacional_credor', 'desc_credor']] = df['Credor'].str.split(' - ', 1, expand=True)
    df[['id_item_despesa', 'desc_item_despesa']] = df['DsItemDespesa'].str.split(' - ', 1, expand=True)
    df['id_tipo_despesa'] = 3
    df['desc_tipo_despesa'] = 'Liquidação'

df = pd.read_excel(f"C:\\Users\\eduar\\Desktop\\TCC\\Dados\\DespesasLiquidaçõesAnuais - Original\\DespesasLiquidações2018.xlsx")
df = renomear_colunas(df)
gerando_colunas(df)
df.to_excel(f"C:\\Users\\eduar\\Desktop\\99.xlsx", index=False)

# Unindo todos os anos em um único Dataframe
#tabelas = []
#for ano in anos:
#    df = pd.read_excel(f"C:\\Users\\eduar\\Desktop\\TCC\\Dados\\DespesasLiquidaçõesAnuais\\DespesasLiquidações{ano}.xlsx") # Certifique-se de que o caminho para o arquivo está correto.
#    tabelas.append(df)
#df = pd.concat(tabelas, ignore_index=True)

#######################################################

#for ano in anos: 
#    print(f'Ano: {ano}')
#    df = pd.read_excel(f"C:\\Users\\eduar\\Desktop\\TCC\\Dados\\DespesasLiquidaçõesAnuais\\DespesasLiquidações{ano}.xlsx") # Certifique-se de que o caminho para o arquivo está correto.       
#    df = padronizar_colunas(df, ano)


# Formatar nome das colunas iniciais
#for i in range(len(anos)): 
#    try:
#        df = pd.read_excel(f"C:\\Users\\eduar\\Desktop\\TCC\\Dados\\DespesasLiquidaçõesAnuais\\DespesasLiquidações{anos[i]}.xlsx") # Certifique-se de que o caminho para o arquivo está correto.
#        df.rename(columns=cabecalhos, inplace=True)
#        df.to_excel(f"C:\\Users\\eduar\\Desktop\\TCC\\Dados\\DespesasLiquidaçõesAnuais\\DespesasLiquidações{anos[i]}.xlsx", index=False)
#        del df
#    except FileNotFoundError:
#        print(f"Planilha não encontrada\nC:\\Users\\eduar\\Desktop\\TCC\\Dados\\DespesasLiquidaçõesAnuais\\DespesasLiquidações{anos[i]}.xlsx")
#
# Formatar coluna Órgão em id_orgao e desc_orgao
