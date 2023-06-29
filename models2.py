import json
import copy
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
                    path = target[0]

                    #Para evitar los ID de un solo elemento
                    if len(location) > 1 :

                        if location[0] != 'css':
                            path = path.split('xpath=')[1]
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
                        else:
                            path = path.split('css=')[1]
                            typePath = 'css'
                            break

                detail = {
                    "target" : path,
                    "typeTarget": typePath,
                    "value" : action["value"],
                    "action" : action["command"],
                    "typeTest": action["comment"]
                }

                actions.append(detail)
            
        self.routine.append({
            "actions":actions
        })
        self.testRoutines = []
        self.erroresEsperados = []

    def waitedClicks(self, typeTest:str, routine:list):

        #POR MODIFICAR

        routine:list = copy.copy(routine)

        if typeTest != '':
            self.testRoutines.append(routine)

    def filterTests(self, test:list, defaultValue, routine:list, accion:dict, longitud:int, iteracion:int, tipoDeDato:str):
        
        accion:dict = copy.copy(accion)
        routine:list = copy.copy(routine)
        newValue = copy.copy(defaultValue)
        changed = False

        uniqueValue = uuid.uuid4()

        match test[0]:
            case 'tipoDeDato':

                if test[1] == 'string':

                    newValue = numberByLength(longitud)
                    changed = True
                
                elif test[1] == 'number':

                    newValue = str(uniqueValue)[:longitud]
                    changed = True

            case 'longitud':

                if tipoDeDato == 'string':
                    newValue = str(uniqueValue)[:longitud+1]
                    
                elif tipoDeDato == 'number':
                    newValue = numberByLength(longitud+1)

                changed = True

            case 'obligatorio':

                if test[1] == 'si':
                    newValue = ''
                    changed = True

        if changed:
            accion['value'] = newValue
            routine[iteracion] = accion
            self.testRoutines.append(routine)

    
    def createTests(self):

        # Recorrido a todas acciones que se encuentran en la rutina inicial
        for i in range(0,len(self.routine[0]['actions'])):
            
            #Rutina Individual
            rutina:list = copy.copy(self.routine[0]['actions'])

            #Accion individual segun el orden de accion
            accion:dict = copy.copy(rutina[i])

            #Valor por defecto de la accion
            defaultValue = accion['value']

            #Descripcion de la especificacion a validar
            tipoTest:str = accion['typeTest']

            #Descripcion del tipo de accion que realiza
            val = accion['action']

            #Valida si existe alguna especificacion, en caso de ser nula, no crea test adicionales
            if tipoTest != '':

                match val:
                    #En caso de que val sea un click
                    case 'click':

                        #Crea un escenario donde valida el tipo de test

                        if tipoTest != 'validador':
                            self.waitedClicks(tipoTest, rutina)

                    #En caso de ser    
                    case 'type':

                        tests:list = tipoTest.split('-')

                        arrayTests:list = []

                        for t in tests:
                            arrayTests.append(t.split(':'))

                        for t in arrayTests:

                            if t[0] == 'errorEsperado':
                                valorEsperado = copy.copy(t[1])
                                self.erroresEsperados.append(valorEsperado)
                            elif t[0] == 'longitud':
                                longitud = int(t[1])

                            elif t[0] == 'tipoDeDato':
                                tipoDeDato = t[1]

                        for t in arrayTests:
                            
                            self.filterTests(t,defaultValue,rutina,accion,longitud,i, tipoDeDato)


# prueba = Tests('prueba.json')

# prueba.createTests()

# print(prueba.erroresEsperados)

# for r in prueba.testRoutines:
#     print('')
#     print(r)
#     print('')