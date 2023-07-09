from modelsv3 import Tests
from testSeleniumV3 import Navigator
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
test = Tests('test3.json')
test.createTests()

testObligatorios:list = test.obligatorioTests
testLongitud:list = test.longitudTests
testTipoDeDato:list = test.tipoDeDatoTests
targetURL = test.targetUrl

def ejecutarTestsWithNavigator(navegadores:list,tests:list):

    for navegador in navegadores:

        #Creamos el objeto con webDriver
        nav = Navigator(command_executor=webdriver_url, options=navegador)

        #Establecemos los argumentos iniciales
        nav.initialArguments(credenciales.routine,targetURL)

        nav.initSession()

        for t in tests:

            #Ejecutamos las acciones del test
            nav.executeRoutine(t)

        print(nav.sucesos)
        nav.close()


#Tests De obligatoriedad

if len(testObligatorios) > 0:
    ejecutarTestsWithNavigator(drivers, testObligatorios)

if len(testLongitud) > 0:
    ejecutarTestsWithNavigator(drivers, testLongitud)

if len(testTipoDeDato) > 0:
    ejecutarTestsWithNavigator(drivers, testTipoDeDato)      


            



