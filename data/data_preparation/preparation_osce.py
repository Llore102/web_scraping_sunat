# import pandas as pd
# import os

# directorio = '../osce'

# ruc_unicos = []

# for archivo in os.listdir(directorio):
#     if archivo.endswith('.xlsx') or archivo.endswith('.xls'):
#         df = pd.read_excel(os.path.join(directorio, archivo))
#         ruc_unicos.extend(df['RUC'].unique())

# df_ruc_unicos = pd.DataFrame({'RUC': list(set(ruc_unicos))})

# df_ruc_unicos.to_excel('../data_preparation/ruc_unicos.xlsx', index=False)
