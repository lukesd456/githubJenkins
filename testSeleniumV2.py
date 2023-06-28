from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class Navigator(webdriver.Remote, By):

    def selectElementByXPATH(self, location:str):
        try:
            WebDriverWait(driver=self, timeout=30).until(EC.presence_of_element_located((self.XPATH, location)))
            self.element = self.find_element(by=self.XPATH, value=location)
        except TimeoutException:
            self.quit()

    def typingAction(self, content):
        self.element.send_keys(content)

    def clickAction(self, valoresEsperados:list, erroresEsperados:list):
        self.element.click()
        for v in valoresEsperados:
            

    def executeRoutine(self, routine:list):

        for action in routine:

            xpath = action["target"]
            self.selectElementByXPATH(xpath)
            match action["action"]:
                case 'type':
                    content = action["value"]
                    self.typingAction(content=content)
                case 'click':
                    self.clickAction()

    def initSession(self, testUrl:str, rutinaInicioSession:list):
        self.get(testUrl)
        self.set_window_size(height=1000,width=1300)
        self.executeRoutine(rutinaInicioSession)

    def executeTests(self, rutinaIniciarSession:list, listaDeTests:list):

        for test in listaDeTests:

            self.initSession(rutinaIniciarSession)
            self.executeRoutine(test)
            self.quit()