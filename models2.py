from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidSelectorException
import json

import uuid
import random

def numberByLength(N:int) -> int:
    low = pow(10, N-1)
    up = pow(10, N) -1

    return random.randint(low,up)


class Tests:
    def __init__(self, jsonPath:str) -> None:
        
        self.routine = []

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
                    "typeTest": action["comment"]
                }

                actions.append(detail)
            
        self.routine.append({
            'valorEsperado':'primer',
            "actions":actions
        })

    def createTests(self):

        # Recorrido a todas acciones que se encuentran en la rutina inicial
        for i in range(0,len(self.routine[0]['actions'])):

            # Establezco la copia de la rutina
            # esto ofrece un diccionario {"valorEsperado", "actions"}
            copyRutine:list = self.routine[0]

            if self.routine[0]['actions'][i]['action'] == 'type':

                # Creo el arreglo de tipo de tests de la accion
                typeTests:list = copyRutine['actions'][i]['typeTest'].split('-')

                # Recorrido para establecer la longitud del dato 
                for test in typeTests:
                    t = test.split(':')

                    # Se busca el test que contenga la especificaicon de la longitud 
                    if t[0] == 'longitud':
                        self.routine[0]['actions'][i]['longitud'] = int(t[1])
                        copyRutine['actions'][i]['longitud'] = int(t[1])

                # Recorrida para capturar el valor esperado
                for test in typeTests:
                    t=test.split(':')
                    if t[0] == 'valorEsperado':
                        copyRutine['valorEsperado'] = t[1]

                # Recorro el arreglo de typeTests para detallar los tests 
                for test in typeTests:
                    
                    # Particiono el string del tipo de test 
                    # El primer indice tengra el tipo de test, y el segundo tendra que es lo que debe tener
                    # Ejemplo ['obligatorio','no']
                    t = test.split(':')

                    longitud = copyRutine['actions'][i]['longitud']

                    # Creamos una nueva rutina segun el tipo de test
                    match t[0]:
                        # ·Test para verificar la obligatoriedad
                        case 'obligatorio':
                            if t[1] == 'si':
                                copyRutine['actions'][i]['value']=''
                                self.routine.append(copyRutine)
                                print('se ejecuto para obligatorio')


                        case 'tipoDeDato':
                        
                        # test para probar que solo acepta numeros                            
                            if t[1] == 'number':
                                copyRutine['actions'][i]['value'] = str(uuid.uuid4())[:longitud]
                                self.routine.append(copyRutine)
                                print(f'se ejecuto test para number {i}')

                            
                        # test para probar que solo acepta strings
                            elif t[1] == 'string':
                                copyRutine['actions'][i]['value']= numberByLength(longitud)
                                self.routine.append(copyRutine)
                                print(f'se ejecuto test para string {i}')
  
                        
                        # Test para superar la longitud 
                        case 'longitud':
                            copyRutine['actions'][i]['value']=str(uuid.uuid4())[:longitud+1]
                            self.routine.append(copyRutine)
                            print('es ejecuto para longitud')

                        case _:
                            pass


prueba = Tests('prueba.json')
prueba.createTests()
print(len(prueba.routine))
print(prueba)