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

    def initialArguments(self, rutinaIniciarSession:list, targetURL:str):

        self.targetURL:str = targetURL
        self.rutinaIniciarSession:list = rutinaIniciarSession
        self.sucesos:list = []

    def registrarSuceso(self, rutina:list, accion:dict, indice:int,tipoDeError:str):

        registro:dict = {
            "rutinaEjecutada": rutina,
            "accionFallida": accion,
            "indiceAccion" : indice,
            "tipoDeError": tipoDeError
        }

        registro = copy.deepcopy(registro)

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

    def clickAction(self, validador:bool, mensajeEsperado:str):
        self.element.click()
        if validador:
            mensajes:list = mensajeEsperado.split('|')

            for m in mensajes:
                try:
                    assert m in self.page_source

                    mensajes.remove(m)
                except AssertionError:
                    print('aviso no encontrado')

            
            if len(mensajes) != 0:
                print('No se ha cumplido con la restriccion')
                raise AssertionError

            


    def defaultExecuteRoutine(self, testRoutine:list):

        actions = testRoutine

        for action in actions:

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


    #Ejecutar esto para cada test que se encuentre en el array
    def executeRoutine(self, test:dict):
        
        mensajeEsperado = test["mensajeEsperado"]
        indice = test["indice"]
        rutina = test["actions"]
        tipoDeTest = test["tipoDeTest"]

        self.implicitly_wait(10)

        for action in rutina:

            print(action)

            path = action["target"]
            typePath = action["typePath"]

            if typePath == 'css':
                self.selectElementByCssSelector(path)
            else:
                self.selectElementByXPATH(path)

            #Hace una comparacion del tipo de accion
            match action["tipoDeAccion"]:

                #Si la accion es de tipear, ejecuta una accion de tipear
                case 'type':
                    content = action["value"]
                    self.typingAction(content=content)

                case 'click':
                    try:
                        validador:bool = action["validador"]
                        self.clickAction(validador, mensajeEsperado)

                    except AssertionError:
                        self.registrarSuceso(rutina, action, indice, tipoDeTest)
                        break

        #Volvemos al inicio
        self.get(self.targetURL)

    def initSession(self):
        self.get(self.targetURL)
        self.set_window_size(height=1000, width=1300)
        self.defaultExecuteRoutine(self.rutinaIniciarSession)

        # for a in self.rutinaIniciarSession:
        #     self.defaultExecuteRoutine(a)