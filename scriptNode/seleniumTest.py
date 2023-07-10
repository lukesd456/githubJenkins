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

    def initialArguments(self, JSON:dict):

        self.targetURL:str = JSON["targetURL"]
        self.rutinaNormal:list = JSON["rutinaNormal"]
        self.tests:list = JSON["tests"]
        self.sucesos:list = []

    def registrarSuceso(self, tipoDeTest:str, indice:int, mensajeEsperado:list, action:dict):

        reporte = {
            "tipoDeTest" : tipoDeTest,
            "indice" : indice,
            "mensajeEsperado" : mensajeEsperado,
            "action" : action
        }

        self.sucesos.append(reporte)

    def selectElementByXPATH(self, location:str):
        WebDriverWait(driver=self, timeout=30).until(EC.presence_of_element_located((self.XPATH, location)))
        self.element = self.find_element(by=self.XPATH, 
        value=location)

    def selectElementByCssSelector(self, location:str):
        WebDriverWait(driver=self, timeout=30).until(EC.presence_of_element_located((self.CSS_SELECTOR, location))) 
        self.element = self.find_element(by=self.CSS_SELECTOR, 
        value=location)

    def clickAction(self, validador:bool, mensajeEsperado:str):
        self.element.click()

        if validador:

            for m in mensajeEsperado:
                try:
                    assert m in self.page_source

                    mensajeEsperado.remove(m)
                except AssertionError:

                    print('aviso no encontrado')

            
            if len(mensajeEsperado) != 0:
                print('No se ha cumplido con la restriccion')
                raise AssertionError

    def initSession(self):
        self.get(self.targetURL)
        self.set_window_size(height=1000, width=1300)

    #Ejecutar esto para cada test que se encuentre en el array
    def executeRoutine(self):

        tests:list = self.tests

        for t in tests:

            self.initSession()

            indice:int = int(t["indice"])
            tipoDeTest:str = t["tipoDeTest"]
            mensajeEsperado:list = copy.deepcopy(t["mensajeEsperado"])
            rutina:list = t["rutina"]

            for action in rutina:

                action:dict

                typeTarget:str = action["typeTarget"]
                location:str = action["location"]
                
                value:str = action["value"]
                validador:bool = action["validador"]
                command:str = action["command"]

                #Seleccionar elemento:
                match typeTarget:
                    case 'xpath':
                        self.selectElementByXPATH(location)
                    case 'css':
                        self.selectElementByCssSelector(location)

                #Realizar accion:
                match command:
                    case 'type':
                        self.sendKeys(value)
                    case 'click':
                        try:
                            self.clickAction(validador,mensajeEsperado)
                        except AssertionError:
                            self.registrarSuceso(tipoDeTest, indice,)

            self.close()