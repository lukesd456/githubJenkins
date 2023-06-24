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

cleaunp = JsonRoutine("CrearProductoresAGROS.json").routine

target_url = 'https://id-panel-stage.agros.tech/'

for driver in drivers:
    nav = Navigator(webdriver_url, options=driver)
    nav.implicitly_wait(5)
    nav.initSession(target_url)
    nav.executeRoutine(cleaunp)
    nav.deleteSession()
    print('Rutina terminada ')