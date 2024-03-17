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





class Sunat_scraper:
    
    def __init__(self, ruc_list, direct):
        self.direct = direct
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")  # Opcional: para ejecución en segundo plano
        chrome_options.add_argument("--start-maximized")


        # Instanciar el controlador de Chrome y pasar las opciones como argumento
        selenium_service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=selenium_service, options=chrome_options)


        self.data = []
        self.excepciones = []    

        for ruc in ruc_list:
            self.scrape_info(ruc)

        # Convertir el diccionario en un DataFrame de pandas
        df = pd.DataFrame(self.data, columns=['Ruc','Proveedor', 'Teléfono', 'Domicilio', 
                                              'Tipo de Contribuyente','Sanciones del TCE', 
                                              'Penalidades', 'Inhabilitación por mandato judicial', 'Inhabilitación administrativa',
                                              'Sunat', 'SBS'])
        
        # Guardar el DataFrame en un archivo de Excel
        excel_file = os.path.join(self.direct, 'gob_info_p.xlsx')
        df.to_excel(excel_file, index=False, index_label=False)
        print("Información exportada a", excel_file)

        if self.excepciones:
            excepciones_df = pd.DataFrame(self.excepciones, columns=['RUC'])
            excepciones_excel_file = os.path.join(self.direct, 'proveedores_excepciones.xlsx')
            excepciones_df.to_excel(excepciones_excel_file, index=False)
            print("Lista de RUCs con excepciones guardada en", excepciones_excel_file) 

    def scrape_info(self, ruc):
        print('Entrando al RUC', ruc)
        self.driver.get("https://appsprep.osce.gob.pe:8143/perfilprov-ui/")
        self.driver.find_element(By.XPATH, '//*[@id="textBuscar"]').send_keys(ruc)
        self.driver.find_element(By.XPATH, '//*[@id="btnBuscar"]/i').click()

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
                tipo_contri_elemnt = self.driver.find_element(By.XPATH, '/html/body/app-root/div/div/app-prov-ficha/div/div/div[1]/div[2]/div[1]/div[2]/ul[2]/li[4]/div/span[3]')
                tipo_contri = tipo_contri_elemnt.text.strip()
            except NoSuchElementException:
                print("No se encontró el sunat para el RUC", ruc)
                tipo_contri = ''

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
            self.data.append((ruc, proveedor, telefono, domicilio, tipo_contri,  sanciones, penalidades, inabilitado_fudicial, inabilitado_admin,  sunat, sbs)) #   
        except TimeoutException:
            print('No se pudo cargar la información para el RUC', ruc)
            self.excepciones.append(ruc)
        except NoSuchElementException:
            print('No se encontraron elementos para el RUC', ruc)
            self.excepciones.append(ruc)
        except Exception as e:
            print('Se produjo un error inesperado para el RUC', ruc, ':', str(e))
            self.excepciones.append(ruc)

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
ruc_list = ["20508626402", "20603469471"]  # PRUEBAS
# ruc_list = leer_rucs_desde_excel(archivo_excel) # EJECUCION

if not ruc_list:
    print("No se encontraron RUCs en el archivo Excel.")
    exit()

# Directorio de salida para el archivo de Excel
direct = r"C:\Users\llore\Jupyter\Scrapers\Sunat\proveedores"

s = Sunat_scraper(ruc_list, direct)

