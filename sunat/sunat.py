from sys import exit
import pandas as pd
import time
import os
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service




headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/80.0.3987.149 Safari/537.36"}

class Sunat_scraper:
    
    def __init__(self, ruc_list, direct):
        self.direct = direct
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f"user-agent={headers['User-Agent']}")
        # chrome_options.add_argument("--headless")  # Opcional: para ejecución en segundo plano

        # Instanciar el controlador de Chrome y pasar las opciones como argumento
        selenium_service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=selenium_service, options=chrome_options)
        


        self.data = []
        self.excepciones = []  

        for ruc in ruc_list:
            self.scrape_info(ruc)

        # Convertir el diccionario en un DataFrame de pandas
        df = pd.DataFrame(self.data, columns=['Nombres', 'Fecha de Inscripción', 'Fecha de Inicio de Actividades', 
                                              'Estado del Contribuyente', 'Condición del Contribuyente',  'Domicilio Fiscal',
                                               'Actividad Comercio Exterior', 'Actividad(es) Económica(s)', 'Emisor electrónico desde',
                                               'Afiliado al PLE desde', 'Padrones'])
        
        # Guardar el DataFrame en un archivo de Excel
        excel_file = os.path.join(self.direct, 'sunat_info_p.xlsx')
        df.to_excel(excel_file, index=False, index_label=False)
        print("Información exportada a", excel_file)

        if self.excepciones:
            excepciones_df = pd.DataFrame(self.excepciones, columns=['RUC'])
            excepciones_excel_file = os.path.join(self.direct, 'ruc_excepciones_p.xlsx')
            excepciones_df.to_excel(excepciones_excel_file, index=False)
            print("Lista de RUCs con excepciones guardada en", excepciones_excel_file) 

    def scrape_info(self, ruc):
        # time.sleep(3)
        print('Entrando al RUC', ruc)
        # self.driver.get("https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/FrameCriterioBusquedaWeb.jsp")
        try:
            self.driver.get("https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/FrameCriterioBusquedaWeb.jsp")
        except WebDriverException as e:
            print("Se produjo un error de conexión:", str(e))
            self.restart_driver()
            return
        
        self.driver.find_element(By.XPATH, '//*[@id="txtRuc"]').send_keys(ruc)
        self.driver.find_element(By.XPATH, '//*[@id="btnAceptar"]').click()

        
        try:
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/div[3]/div[2]')))
            # Encontrar el elemento que contiene la información que deseas
            nombre_element = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[3]/div[2]/div[1]/div/div[2]/h4')
            nombre = nombre_element.text.strip()

            fecha_inscripcion_elemnt = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[3]/div[2]/div[4]/div/div[2]/p')
            fecha_in = fecha_inscripcion_elemnt.text.strip()

            fecha_in_act_elemnt = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[3]/div[2]/div[4]/div/div[4]/p')
            fecha_in_act = fecha_in_act_elemnt.text.strip()

            estado_contri_elemnt = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[3]/div[2]/div[5]/div/div[2]/p')
            estado_contri = estado_contri_elemnt.text.strip()

            condicion_contri_elemnt = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[3]/div[2]/div[6]/div/div[2]/p')
            condicion_contri = condicion_contri_elemnt.text.strip()

            domicilio_fical_element = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[3]/div[2]/div[7]/div/div[2]/p')
            domicilio_fical = domicilio_fical_element.text.strip()

            actividad_comer_ext_element = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[3]/div[2]/div[8]/div/div[4]/p')
            actividad_c_ex_fical = actividad_comer_ext_element.text.strip()

            actividades_economicas_element = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[3]/div[2]/div[10]/div/div[2]/table/tbody/tr/td')
            actividades_econ = actividades_economicas_element.text.strip()

            emisor_element = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[3]/div[2]/div[13]/div/div[2]/p')
            emisor = emisor_element.text.strip()

            afiliado_element = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[3]/div[2]/div[15]/div/div[2]/p')
            afiliado = afiliado_element.text.strip()

            padrones_element = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[3]/div[2]/div[16]/div/div[2]/table/tbody/tr/td')
            padrones = padrones_element.text.strip()


            # print('Información obtenida para el RUC', ruc, ':', nombre, ':', fecha_in, ':', fecha_in_act, ':',  estado_contri, ':', condicion_contri, ':', domicilio_fical, )
            print('Información obtenida para el RUC',  nombre,  )
            # Agregar la información al diccionario
            self.data.append((nombre, fecha_in, fecha_in_act, estado_contri, condicion_contri, domicilio_fical, actividad_c_ex_fical, actividades_econ, emisor, afiliado, padrones))
        except TimeoutException:
            print('No se pudo cargar la información para el RUC', ruc)
            self.excepciones.append(ruc)
            self.restart_driver()
        except NoSuchElementException:
            print('No se encontraron elementos para el RUC', ruc)
            self.excepciones.append(ruc)
            self.restart_driver()
        except Exception as e:
            print('Se produjo un error inesperado para el RUC', ruc, ':', str(e))
            self.excepciones.append(ruc)
            self.restart_driver()

        # Espera unos segundos antes de continuar con el siguiente RUC
        time.sleep(15)

    def restart_driver(self):
        self.driver.quit()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f"user-agent={headers['User-Agent']}")
        # chrome_options.add_argument("--headless")  # Opcional: para ejecución en segundo plano

        # Instanciar el controlador de Chrome y pasar las opciones como argumento
        selenium_service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=selenium_service, options=chrome_options)
        print("Driver reiniciado.")

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


# ruc_list = leer_rucs_desde_excel(archivo_excel) # EJECUCION COMPLETA
ruc_list = ["20508626402", "20603469471"] # PRUEBAS

if not ruc_list:
    print("No se encontraron RUCs en el archivo Excel.")
    exit()
print("Cantidad de RUCs leídos desde el archivo:", len(ruc_list))

# Directorio de salida para el archivo de Excel
direct = r"C:\Users\llore\Jupyter\Scrapers\Sunat\sunat"


s = Sunat_scraper(ruc_list, direct)


