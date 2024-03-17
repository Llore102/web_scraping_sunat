import pandas as pd
import os

# Ruta al archivo de destino
archivo_principal = r"C:\Users\llore\Jupyter\Scrapers\Sunat\proveedores\gob_info_img.xlsx"

# Ruta al directorio que contiene los archivos individuales
directorio = r"C:\Users\llore\Jupyter\Scrapers\Sunat\aptos"

# Leer el archivo principal
df_principal = pd.read_excel(archivo_principal)
apto_para_contratar_dict = {}

# Recorrer todos los archivos en el directorio
for archivo in os.listdir(directorio):
    if archivo.endswith(".xlsx"):
        ruta_archivo = os.path.join(directorio, archivo)
        # Leer cada archivo individual
        df_individual = pd.read_excel(ruta_archivo)
        df_individual.rename(columns={'RUC':'Ruc'}, inplace=True)
        # Verificar que las columnas existan en el DataFrame individual
        if 'Ruc' in df_individual.columns and 'APTO PARA CONTRATAR' in df_individual.columns:
            # Actualizar el diccionario con la información de 'APTO PARA CONTRATAR' por Ruc
            apto_para_contratar_dict.update(df_individual[['Ruc', 'APTO PARA CONTRATAR']].set_index('Ruc').to_dict()['APTO PARA CONTRATAR'])

# Agregar la información de 'APTO PARA CONTRATAR' al dataframe principal
df_principal['APTO PARA CONTRATAR'] = df_principal['Ruc'].map(apto_para_contratar_dict)

# Guardar el archivo con la nueva columna agregada
df_principal.to_excel("C:/Users/llore/Jupyter/Scrapers/Sunat/proveedores/proveedores.xlsx", index=False)