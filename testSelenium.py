from selenium import webdriver
#For tags
from selenium.webdriver.common.by import By
#For wait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

webdriver_url = 'http://localhost:4444/wd/hub'

firefoxOptions = webdriver.FirefoxOptions()
chromeOptions=webdriver.ChromeOptions()
edgeOptions = webdriver.EdgeOptions()

drivers = [
    firefoxOptions,
    chromeOptions,
    edgeOptions
]

class Routine:
    def __init__(self, jsonRoutine) -> None:

        self.routine = []

        for action in jsonRoutine:
            detail = {
                "target" : action["target"].split('xpath=')[1],
                "value" : action["value"],
                "action" : action["command"]
            }
            self.routine.append(detail)

class Navigator(webdriver.Remote, By):

    def selectElementByXPATH(self, location:str):
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

            # print(action["action"])
            # print(action["target"])
            # print(action["value"])

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
        

import json
with open("CrearProductoresAGROS.json", "r") as file:
      newData = json.load(file)

raw = newData["tests"][0]["commands"]

cleanup = Routine(raw).routine

target_url = 'https://id-panel-stage.agros.tech/'

# nav = Navigator(webdriver_url, options=drivers[1])
# nav.implicitly_wait(15)
# nav.initSession(target_url)
# nav.executeRoutine(cleanup)
# nav.quit()

for driver in drivers:
    nav = Navigator(webdriver_url, options=driver)
    nav.implicitly_wait(15)
    nav.initSession(target_url)
    nav.executeRoutine(cleanup)
    nav.deleteSession()
    print('Rutina terminada ')