import pandas as pd

df = {'id_tipo_despesa': ['1', '2', '3'], 'desc_tipo_despesa': ['Empenho', 'Pagamento', 'Liquidação']}
df = pd.DataFrame(df)

print(df)
# Trabalhar na carga das colunas 'id_tipo_despesa', 'desc_tipo_despesa' em DM_TIPO_DESPESA
# 1 = Empenho; 2 = Pagamento; 3 =  Liquidação