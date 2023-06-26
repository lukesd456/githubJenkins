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
            "actions":actions,
            "valorEsperado": 'primer'
        })

    def createTests(self):

        # Recorrido a todas acciones que se encuentran en la rutina inicial
        for i in range(0,len(self.routine[0]['actions'])):
            
            #Rutina Individual
            rutina:list = self.routine[0]['actions']

            #Accion individual segun el orden de accion
            accion:dict = rutina[i]

            val = accion['action']
            
            if val == 'type':

                tests:list = accion['typeTest'].split('-')

                arrayTests = []

                for t in tests:
                    arrayTests.append(t.split('-'))

                for test in arrayTests:

                    match

            # if val == 'type':

            #     #Tipo de test a realizar
            #     tests:list = accion['typeTest'].split('-')

            #     arrayTests:list = []

            #     for t in tests:
            #         arrayTests.append(t.split(':'))
                
            #     for t in arrayTests:
            #         if t[0] == 'longitud':
            #             longitud = int(t[1])

            #         if t[0] == 'valorEsperado':
            #             valorEsperado=t[1]
                
            #     #Crear test por strings
            #     for t in arrayTests:

            #         dataTypeRoutine = rutina
            #         dataTypeAction = accion

            #         if t[0] == 'tipoDeDato':
                        
            #             testByData = ''
                        
            #             match t[1]:
            #                 case 'string':
                                
            #                     testByData = numberByLength(longitud)
                            
            #                 case 'number':

            #                     testByData = str(uuid.uuid4())[:longitud]

            #             dataTypeAction['value'] = testByData
            #             dataTypeRoutine[i] = dataTypeAction



            #             self.routine.append({
            #                 'valorEsperado' : valorEsperado,
            #                 "actions" : dataTypeRoutine
            #             })

            #     for t in arrayTests:
                    
            #         requiredAction = accion
            #         requiredRoutine = rutina

            #         if (t[0] == 'obligatorio') & (t[1] == 'si'):

            #             requiredAction['value'] = ''
            #             requiredRoutine[i] = requiredAction

            #             self.routine.append({
            #                 'valorEsperado' : valorEsperado,
            #                 "actions" : requiredRoutine
            #             })


            #     for t in arrayTests:

            #         if t[0] == 'longitud':

            #             lengthAction = accion
            #             lenghtRoutine = rutina

            #             lengthAction['value'] = str(uuid.uuid4())[:longitud+1]
            #             lenghtRoutine[i] = lengthAction

            #             self.routine.append({
            #                 'valorEsperado' : valorEsperado,
            #                 "actions" : lenghtRoutine
            #             })           

prueba = Tests('prueba.json')

prueba.createTests()


print(prueba.routine)
# for r in range(0,len(prueba.routine)):
#     print('')
#     print(prueba.routine[r]['actions'])
#     print('')