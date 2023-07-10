from seleniumTest import Navigator
from selenium import webdriver
import json

webdriver_url = 'http://localhost:4444/wd/hub'


firefoxOptions = webdriver.FirefoxOptions()
chromeOptions=webdriver.ChromeOptions()
edgeOptions = webdriver.EdgeOptions()

drivers = [
    firefoxOptions,
    chromeOptions,
    edgeOptions
]

def executeScript(path:str, driver) -> list:
    with open(path, "r") as file:
        jsonData = json.load(file)

    result = Navigator(command_executor=driver)
    result.initialArguments(jsonData)
    result.executeRoutine()

    return result.sucesos



reportes = []

for driver in drivers:
    
    reportes.append(executeScript('./filteredTests.json', driver))

print(reportes)