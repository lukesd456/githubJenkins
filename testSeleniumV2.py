from typing import List, Union
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.options import BaseOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import copy

class Navigator(webdriver.Remote, By):

    def __init__(self, command_executor="http://127.0.0.1:4444", keep_alive=True, file_detector=None, options: BaseOptions | List[BaseOptions] = None) -> None:
        super().__init__(command_executor, keep_alive, file_detector, options)

    def initialArguments(self, rutinaIniciarSession:list, listaDeTests:list, targetURL:str, erroresEsperados:list):
        self.targetURL:str = targetURL
        self.rutinaIniciarSession:list = rutinaIniciarSession
        self.listaDeTests:list = listaDeTests
        self.erroresEsperados:list = erroresEsperados
        self.sucesos:list = []

    def registrarSuceso(self, rutina:list, accion:dict, indice:int,tipoDeError:str):

        registro:dict = {
            "rutinaEjecutada": rutina,
            "accionFallida": accion,
            "indiceAccion" : indice,
            "tipoDeError": tipoDeError
        }

        registro = copy.copy(registro)

        self.sucesos.append(registro)

    def selectElementByXPATH(self, location:str):
        # print(location)
        WebDriverWait(driver=self, timeout=30).until(EC.presence_of_element_located((self.XPATH, location)))
        self.element = self.find_element(by=self.XPATH, 
        value=location)
        

    def selectElementByCssSelector(self, location:str):
        # print(location)
        WebDriverWait(driver=self, timeout=30).until(EC.presence_of_element_located((self.CSS_SELECTOR, location))) 
        self.element = self.find_element(by=self.CSS_SELECTOR, 
        value=location)
           

    def typingAction(self, content):
        self.element.send_keys(content)

    def clickAction(self, validador:str):
        
        #Ejecuta click en el elemento seleccionado
        self.element.click()

        #Copia de errores
        listaErrores:list = copy.copy(self.erroresEsperados)

        #Si el click es validador, entonces ejecuta la comprobacion de los errores esperados
        if validador == 'validador':

            #Realiza un recorrido por cada error que se encuentre almacenado
            for e in self.erroresEsperados:
                try:
                    
                    #Revisa en el codigo fuente de la pagina y busca el mensaje de comprobacion
                    assert e in self.page_source

                    #Remueve el mensaje de error
                    listaErrores.remove(e)
                except AssertionError:
                    
                    #Para evitar que lance error si no encuentra el error esperado
                    print('Hay Error')            

            if len(listaErrores) != 0:
                print('No se ha cumplido con la restriccion')
                raise AssertionError

    #Ejecucion de rutina sin validacion de datos
    def defaultExecuteRoutine(self, routine:list):

        for action in routine:

            path = action["target"]
            typePath = action['typeTarget']
            
            if typePath == 'css':
                self.selectElementByCssSelector(path)
            else:
                self.selectElementByXPATH(path)

            match action["action"]:
                case 'type':
                    content = action["value"]
                    self.element.send_keys(content)
                case 'click':
                    self.element.click()

    def executeRoutine(self, routine:list):

        indiceAccion = 0
        #Realiza un recorrido de cada accion que encuentre
        for action in routine:

            indiceAccion += 1

            #Establece el lugar donde se encuentra en el HTML el elemento a interactuar
            path = action["target"]
            print(path)
            typePath = action['typeTarget']
            
            if typePath == 'css':
                self.selectElementByCssSelector(path)
            else:
                self.selectElementByXPATH(path)

            #Hace una comparacion del tipo de accion
            match action["action"]:

                #Si la accion es de tipear, ejecuta una accion de tipear
                case 'type':
                    content = action["value"]
                    self.typingAction(content=content)

                #Si la accion es de clickear, ejecuta la funcion de clickear y analiza valores esperados    
                case 'click':
                    try:
                        validador = action['typeTest']
                        self.clickAction(validador=validador)
                    except AssertionError:
                        #Se activa cada vez que no se encuentra el mensaje de verificacion ante datos erroneos
                        self.registrarSuceso(routine, action, indice=indiceAccion, tipoDeError='No se encontró mensaje de error')                        
                        break
                
        #Termina la rutina y vuelve a la pagina de inicio
        self.get(self.targetURL)

    def initSession(self):
        self.get(self.targetURL)
        self.set_window_size(height=1000,width=1300)
        self.defaultExecuteRoutine(self.rutinaIniciarSession)

    def executeTests(self):

        #Inicia sesion en el navegador e introduce las credenciales necesarias para realizar las operaciones
        self.initSession()

        #Realiza cada test que se encuentra almacenado en esa lista
        for test in self.listaDeTests:

            #En la primera ejecucion se encontrará en la pagina de inicio, por lo que no es necesario llamar a la pagina
            self.executeRoutine(test)

        self.quit()
