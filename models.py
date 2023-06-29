from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidSelectorException
import json



class JsonRoutine:
    def __init__(self, jsonPath:str) -> None:
        
        #abrir archivo JSON
        with open(jsonPath, "r") as file:
            jsonRawData = json.load(file)
        
        #Establecer ruta objetivo
        self.targetUrl = jsonRawData['url']

        #Limpiar iteraciones
        actions = []

        comandos = jsonRawData['tests'][0]['commands']

        for action in comandos:

            if action['command'] in ['type', 'click']:
                for target in action['targets']:
                    location = target[1].split(':')
                    xpath = target[0]

                    if len(location) > 1 :

                        if location[0] != 'css':
                            xpath = xpath.split('xpath=')[1]
                            match location[1]:
                                case 'idRelative':
                                    typePath = 'idRelative'
                                    break
                                case 'attributes':
                                    typePath = 'attributes'
                                    break
                                case 'position':
                                    typePath = 'position'
                                    break

                detail = {
                    "target" : xpath,
                    "typeTarget": typePath,
                    "value" : action["value"],
                    "action" : action["command"],
                    "typeTest":''
                }

                actions.append(detail)
            

        self.routine = actions

class Navigator2(webdriver.Remote, By):

    def selectElementByXPATH(self, location:str):
        WebDriverWait(driver=self, timeout=30).until(EC.presence_of_element_located((self.XPATH, location)))
        self.element = self.find_element(by=self.XPATH, value=location)


    def typingAction(self, content):
        self.element.send_keys(content)

    def clickAction(self):
        self.element.click()

    def initSession(self, testUrl:str):
        self.get(testUrl)
        self.set_window_size(height=1000,width=1300)

    def executeRoutine(self, routine):

        for action in routine:

            xpath = action["target"]
            self.selectElementByXPATH(xpath)
            match action["action"]:
                case 'type':
                    content = action["value"]
                    self.typingAction(content=content)
                case 'click':
                    self.clickAction()

    def deleteSession(self):
        self.quit()