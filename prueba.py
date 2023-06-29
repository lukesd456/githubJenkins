from testSeleniumV2 import Navigator
from models2 import Tests
from models import JsonRoutine
from selenium import webdriver

webdriver_url = 'http://localhost:4444/wd/hub'

firefoxOptions = webdriver.FirefoxOptions()
chromeOptions=webdriver.ChromeOptions()
edgeOptions = webdriver.EdgeOptions()

drivers = [
    firefoxOptions,
    chromeOptions,
    edgeOptions
]

credenciales = JsonRoutine('FrankRecordIniciarSesion.json')
test = Tests('FrankRecord.json')
test.createTests()
testerNavigators = []

for driver in drivers:
    nav = Navigator(command_executor=webdriver_url, options=driver)
    nav.initialArguments(erroresEsperados=test.erroresEsperados, targetURL=test.targetUrl, listaDeTests=test.testRoutines, rutinaIniciarSession=credenciales.routine)
    nav.implicitly_wait(10)
    nav.executeTests()