# Web Scraping Sunat

<div align="center" style="width: 200px;">
  <img alt="GIF" src="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExODBkZ3plczJsa2Rzc2dmbDc4dHVoZ2pmZnhvOW10cmx4bWo3ZGJhNyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/9DDFjULdvJU57V9rkd/giphy.gif" width="50%"/>
</div>

----------------

## Overview

Este script de Python está diseñado para capturar y descargar información de la página web de la Superintendencia Nacional de Aduanas y de Administración Tributaria (SUNAT) 
utilizando la biblioteca Selenium. Su propósito es recopilar datos específicos de una lista de números de identificación de contribuyentes (RUC) y guardar la información en archivos de Excel para un análisis posterior.

### Tecnologías Utilizadas
![Python](https://www.vectorlogo.zone/logos/python/python-ar21.svg) 
<div align="let" style="width: 100px;">
  <img alt="GIF" src="https://miro.medium.com/v2/resize:fit:4800/format:webp/1*-yauD1PxgsdiOJQMqnmu1w.jpeg" width="15%"/>
</div>


## Requirements

1. Instala las bibliotecas requeridas:

   ```bash
   pip install -r requirements.txt


## Usage

1. Script `sunat.py`

   * Proporcione las rutas de entrada para la lista de identificadores y las rutas de salida para guardar la información.
   * Navegue a la sunatcarpeta usando el comando `cd sunat` ejecute el script con `python sunat.py`.

   Este script ejecutara la extraccion de informacion de cada numero de idenficación proporcionar en la lista.
   de la pagina de consultas de sunat, guardara un archivo excel con la informacion llamado `sunat_info.xlsx`
    


3. Script `gob_img.py`
 
   * Proporcione las rutas de entrada para la lista de identificadores y las rutas de salida para guardar la información.
   * Navegue a la carpeta proveedores usando el comando `cd proveedores` ejecute el script con `python gob_img.py`.
  
   Este script ejecutara la extraccion de informacion y un archivo excel que contiene informacion de `APTO PARA CONTRATAR` de cada numero de idenficación proporcionar en la lista.
   de la pagina Buscador de Proveedores del Estado, guardara un archivo excel con la informacion llamado `gob_info_img.xlsx`

4. Script `concat.py`
 
  * Proporcione las rutas de entrada para la lista de identificadores y las rutas de salida para guardar la información.
  * Navegue a la carpeta proveedores usando el comando `cd proveedores` ejecute el script con `python concat.py`.

  Este script crea un nuevo archivo llamado `proveedores.xlsx` concatenado la informacion de `gob_info_img.xlsx` y los archivos excel descargados que contienen la columna `APTO PARA CONTRATAR`

¡No dudes en comunicarte con nosotros si necesitas más ayuda o mejoras!


