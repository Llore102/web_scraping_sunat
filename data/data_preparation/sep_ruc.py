import pandas as pd

# Leer el archivo Excel
df = pd.read_excel(r'C:\Users\llore\Jupyter\Scrapers\Sunat\ruc_adjudicados_completos.xlsx')

# Obtener el número total de filas
total_filas = len(df)
print("Total filas ", total_filas)

# Calcular el número de filas por archivo
filas_por_archivo = total_filas // 5
print("Total filas por archivo",filas_por_archivo)

# Dividir el DataFrame en 5 partes
parte_1 = df.iloc[:filas_por_archivo]
parte_2 = df.iloc[filas_por_archivo:2*filas_por_archivo]
parte_3 = df.iloc[2*filas_por_archivo:3*filas_por_archivo]
parte_4 = df.iloc[3*filas_por_archivo:4*filas_por_archivo]
parte_5 = df.iloc[4*filas_por_archivo:]

# Guardar cada parte en un archivo Excel separado
parte_1.to_excel('../data_preparation/ruc_parte_1.xlsx', index=False)
parte_2.to_excel('../data_preparation/ruc_parte_2.xlsx', index=False)
parte_3.to_excel('../data_preparation/ruc_parte_3.xlsx', index=False)
parte_4.to_excel('../data_preparation/ruc_parte_4.xlsx', index=False)
parte_5.to_excel('../data_preparation/ruc_parte_5.xlsx', index=False)
