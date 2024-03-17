
from sys import exit
import pandas as pd
import os
import time
import requests

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import concurrent.futures

from openpyxl import Workbook
from openpyxl.drawing.image import Image



class Sunat_scraper:
    
    def __init__(self, ruc_list, direct):
        self.direct = direct
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")  # Opcional: para ejecución en segundo plano
        chrome_options.add_argument("--start-maximized")


        # Instanciar el controlador de Chrome y pasar las opciones como argumento
        selenium_service = Service(ChromeDriverManager().install())
        # self.driver = webdriver.maximize_window()
        self.driver = webdriver.Chrome(service=selenium_service, options=chrome_options)


        self.data = []  

        for ruc in ruc_list:
            self.scrape_info(ruc)

        # Convertir el diccionario en un DataFrame de pandas
        df = pd.DataFrame(self.data, columns=['Ruc','Proveedor', 'Teléfono', 'Domicilio', 
                                              'Tipo de Contribuyente', 'Desempeño','Sanciones del TCE', 
                                              'Penalidades', 'Inhabilitación por mandato judicial', 'Inhabilitación administrativa',
                                              'Sunat', 'SBS'])
        
        # Guardar el DataFrame en un archivo de Excel
        excel_file = os.path.join(self.direct, 'gob_info_img_p.xlsx')
        # Crear un nuevo libro de trabajo de openpyxl
        wb = Workbook()
        ws = wb.active
        
        # Escribir los encabezados en la primera fila del archivo Excel
        ws.append(['Ruc', 'Proveedor', 'Teléfono', 'Domicilio', 
                'Tipo de Contribuyente', 'Desempeño', 'Sanciones del TCE', 
                'Penalidades', 'Inhabilitación por mandato judicial', 'Inhabilitación administrativa',
                'Sunat', 'SBS'])
        # Iterar sobre los datos y escribirlos en el archivo Excel
        for row_data in self.data:
            ws.append(row_data)
        
        # Iterar sobre las filas para insertar las imágenes
        
        for idx, row in enumerate(df.iterrows(), start=1):  # Empieza desde la primera fila
            ruc, _, _, _, _, image_filenames, *_ = row[1]
            if image_filenames:
                for image_filename in image_filenames.split(','):  # Las imágenes están separadas por comas
                    img = Image(image_filename.strip())  # Elimina espacios en blanco alrededor de la ruta del archivo
                    img.width = 90  # Ancho de la imagen
                    img.height = 40
                    ws.add_image(img, f'F{idx}')  # Inserta la imagen en la columna F y la fila correspondiente

        # Guardar el archivo de Excel
        wb.save(excel_file)
        print("Información exportada a", excel_file)


    def descargar_archivo(self, origen, destino):
        # Esperar a que el archivo se descargue completamente
        tiempo_espera = 10  # Tiempo de espera máximo en segundos
        tiempo_inicio = time.time()
        while not os.path.exists(origen):
            if time.time() - tiempo_inicio > tiempo_espera:
                print("Tiempo de espera excedido para la descarga del archivo.")
                return False
            time.sleep(1)  # Esperar 1 segundo antes de verificar nuevamente

        # Mover el archivo descargado a la ubicación deseada
        try:
            os.rename(origen, destino)  # Mover el archivo a la carpeta destino
        except FileExistsError:
            print("El archivo ya existe en la carpeta destino.")
            return False
        except Exception as e:
            print(f"Error al mover el archivo: {e}")
            return False

        print(f"Archivo descargado correctamente en: {destino}")
        return True
        
            



    def scrape_info(self, ruc):
        print('Entrando al RUC', ruc)
        self.driver.get("https://appsprep.osce.gob.pe:8143/perfilprov-ui/")
        self.driver.find_element(By.XPATH, '//*[@id="textBuscar"]').send_keys(ruc)
        self.driver.find_element(By.XPATH, '//*[@id="btnBuscar"]/i').click()

        # Tu código restante permanece sin cambios
        try:
            # Hacer scroll hasta el final de la página
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Esperar a que el botón de descarga esté disponible
            boton_descarga = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnExcel"]')))
            
            # Hacer clic en el botón para iniciar la descarga
            boton_descarga.click()

            # Descargar el archivo con el nombre que incluye el RUC
            nombre_archivo = f"archivo_{ruc}.xlsx"
            origen = os.path.join(os.path.expanduser('~'), 'Downloads', nombre_archivo)  # Origen: carpeta de descargas
            destino = os.path.join(origen, nombre_archivo)  # Destino: carpeta especificada
            self.descargar_archivo(origen, destino)

        except TimeoutException:
            print("Botón de descarga no encontrado")
                        

        try:
            boton = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="idPanelA2"]/div[2]/div/app-tile/a/div/div[1]')))
            boton.click()
        except TimeoutException:
            print("Proveedores no encontrado")




        try:
            boton = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/div/div/app-prov-ficha/div/div/div[1]/div[2]/div[1]/div[3]/span[1]/i')))
            boton.click()
        except TimeoutException:
            print("Button no encontrado")



            
        try:
            time.sleep(5)
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/div/div/app-prov-ficha/div/div')))
            # Encontrar el elemento que contiene la información que deseas
            proveedor_element = self.driver.find_element(By.XPATH, '/html/body/app-root/div/div/app-prov-ficha/div/div/div[1]/div[2]/div[1]/div[1]/div[2]/div/div[1]')
            proveedor = proveedor_element.text.strip()


            try:
                telefono_elemnt = self.driver.find_element(By.XPATH, '/html/body/app-root/div/div/app-prov-ficha/div/div/div[1]/div[2]/div[1]/div[2]/div/span[3]')
                telefono = telefono_elemnt.text.strip()
            except NoSuchElementException:
                print("No se encontró el telefono para el RUC", ruc)
                telefono = ''

            try:
                domicilio_elemnt = self.driver.find_element(By.XPATH, '/html/body/app-root/div/div/app-prov-ficha/div/div/div[1]/div[2]/div[1]/div[2]/ul[2]/li[1]/div/span[3]')
                domicilio = domicilio_elemnt.text.strip()
            except NoSuchElementException:
                print("No se encontró el telefono para el RUC", ruc)
                domicilio = ''

            try:
                desem_element = self.driver.find_element(By.XPATH, '/html/body/app-root/div/div/app-prov-ficha/div/div/div[1]/div[3]/div/div[1]/div[2]/div/div/div/span/img')
                desempeno_url = desem_element.get_attribute("src")
                image_data = requests.get(desempeno_url).content
                image_filename = "../imgs/desempeno_image_{}.png".format(ruc) 
                with open(image_filename, "wb") as f:
                    f.write(image_data)
                print("La imagen de desempeño se ha descargado correctamente.")
            except NoSuchElementException:
                print("No se encontró la imagen de desempeño para el RUC", ruc)
                image_filename = ''

            try:
                tipo_contri_elemnt = self.driver.find_element(By.XPATH, '/html/body/app-root/div/div/app-prov-ficha/div/div/div[1]/div[2]/div[1]/div[2]/ul[2]/li[4]/div/span[3]')
                tipo_contri = tipo_contri_elemnt.text.strip()
            except NoSuchElementException:
                print("No se encontró el sunat para el RUC", ruc)
                tipo_contri = ''

            # WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/div/div/app-prov-ficha/div/div/div[1]/div[3]/div')))
            try:
                sanciones_elemnt = self.driver.find_element(By.XPATH, '/html/body/app-root/div/div/app-prov-ficha/div/div/div[1]/div[3]/div/div[2]/div[1]/a/span[1]')
                sanciones = sanciones_elemnt.text.strip()
            except NoSuchElementException:
                print("No se encontró el sunat para el RUC", ruc)
                sanciones = ''

            try:
                penalidades_element = self.driver.find_element(By.XPATH, '/html/body/app-root/div/div/app-prov-ficha/div/div/div[1]/div[3]/div/div[2]/div[2]/a/span[1]')
                penalidades = penalidades_element.text.strip()
            except NoSuchElementException:
                print("No se encontró el sunat para el RUC", ruc)
                penalidades = ''

            try:
                inabil_mand_jud_element = self.driver.find_element(By.XPATH, '/html/body/app-root/div/div/app-prov-ficha/div/div/div[1]/div[3]/div/div[2]/div[3]/a/span[1]')
                inabilitado_fudicial = inabil_mand_jud_element.text.strip()
            except NoSuchElementException:
                print("No se encontró el sunat para el RUC", ruc)
                inabilitado_fudicial = ''

            try:
                inabil_admi_element = self.driver.find_element(By.XPATH, '/html/body/app-root/div/div/app-prov-ficha/div/div/div[1]/div[3]/div/div[2]/div[4]/a/span[1]')
                inabilitado_admin = inabil_admi_element.text.strip()
            except NoSuchElementException:
                print("No se encontró el sunat para el RUC", ruc)
                inabilitado_admin = ''

            try:
                sunat_element = self.driver.find_element(By.XPATH, '/html/body/app-root/div/div/app-prov-ficha/div/div/div[1]/div[3]/div/div[2]/div[5]/a/span[1]')
                sunat = sunat_element.text.strip()
            except NoSuchElementException:
                print("No se encontró el sunat para el RUC", ruc)
                sunat = ''
            
            
            try:
                sbs_element = self.driver.find_element(By.XPATH, '/html/body/app-root/div/div/app-prov-ficha/div/div/div[1]/div[3]/div/div[2]/div[6]/a/span[1]')
                sbs = sbs_element.text.strip()
            except NoSuchElementException:
                print("No se encontró el sunat para el RUC", ruc)
                sbs = ''



            print('Información obtenida para el RUC', ruc, ':', proveedor,  )
            # Agregar la información al diccionario
            self.data.append((ruc, proveedor, telefono, domicilio, tipo_contri,  image_filename, sanciones, penalidades, inabilitado_fudicial, inabilitado_admin,  sunat, sbs)) #   
        except TimeoutException:
            print('No se pudo cargar la información para el RUC', ruc)


        # Espera unos segundos antes de continuar con el siguiente RUC
        time.sleep(5)

# Función para leer los RUCs desde un archivo Excel
def leer_rucs_desde_excel(archivo_excel):
    try:
        # Lee el archivo Excel
        df = pd.read_excel(archivo_excel)
        # Retorna los números de RUC como una lista
        return df['RUC'].tolist()
    except Exception as e:
        print("Error al leer el archivo Excel:", e)
        return []
    
archivo_excel = r"C:\Users\llore\Jupyter\Scrapers\Sunat\ruc_adjudicados.xlsx"

# Lista de RUCs a procesar
ruc_list = ["20508626402", "20603469471", "20552976810"]  # PRUEBAS
# ruc_list = leer_rucs_desde_excel(archivo_excel)

if not ruc_list:
    print("No se encontraron RUCs en el archivo Excel.")
    exit()

# Directorio de salida para el archivo de Excel
direct = r"C:\Users\llore\Jupyter\Scrapers\Sunat\proveedores"

s = Sunat_scraper(ruc_list, direct)



