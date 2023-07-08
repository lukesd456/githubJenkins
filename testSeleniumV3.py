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

    def initialArguments(self, rutinaIniciarSession:list, listaDeTests:list, targetURL:str):

        self.targetURL:str = targetURL
        self.rutinaIniciarSession:list = rutinaIniciarSession
        self.listaDeTests:list = listaDeTests
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