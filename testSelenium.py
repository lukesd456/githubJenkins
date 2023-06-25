from selenium import webdriver
from models import Navigator, JsonRoutine
import os

webdriver_url = 'http://localhost:4444/wd/hub'

firefoxOptions = webdriver.FirefoxOptions()
chromeOptions=webdriver.ChromeOptions()
edgeOptions = webdriver.EdgeOptions()

drivers = [
    firefoxOptions,
    chromeOptions,
    edgeOptions
]

data = JsonRoutine("CrearProductoresAGROS.json")

target_url = 'https://id-panel-stage.agros.tech/'

testerNavigators = []

for driver in drivers:
    nav = Navigator(webdriver_url, options=driver)
    nav.initSession(data.targetUrl)
    testerNavigators.append(nav)

for navigator in testerNavigators:
    navigator.executeRoutine(data.routine)
    navigator.deleteSession()