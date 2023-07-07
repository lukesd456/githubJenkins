import json
import copy
import uuid
import random

def numberByLength(N:int) -> int:
    low = pow(10, N-1)
    up = pow(10, N) -1

    return random.randint(low,up)

class TestTemplates:
    def __init__(self, routine:list, mensajeEsperado:str, indice:int) -> None:

        self.mensajeEsperado:str = mensajeEsperado
        self.listActions:list = [ e for e in routine]
        self.indice = indice


class GeneralTemplate:
    def __init__(self, value:str, target:str, typePath:str, indice:int, mensajeEsperado:str, validador:bool ) -> None:

        self.target=target
        self.value=value
        self.typePath = typePath
        self.indice = indice
        self.mensajeEsperado = mensajeEsperado
        self.validador = validador

    def defaultDetail(self, tipoDeAccion:str):
        
        detail = {
            #Estos valores son obligatorio
            "value" : self.value,
            "target": self.target,
            "typePath" : self.typePath,
            "tipoDeAccion" : tipoDeAccion,
            #Por defecto es falso
            "validador" : self.validador,
            #MensajeEsperado puede ser vacio ''
            "mensajeEsperado" : self.mensajeEsperado
        }

        return detail

class TypingTemplate(GeneralTemplate):
    def __init__(self, value: str, target: str, typePath: str, indice: int, mensajeEsperado: str, validador: bool) -> None:
        super().__init__(value, target, typePath, indice, mensajeEsperado, validador)

    def createDetail(self, tipoDeDato:str, longitud:int, obligatorio:bool, unico:bool):
        detail = {

            #Detalles generales
            "value" : self.value,
            "target" : self.target,
            "typePath" : self.typePath,
            "tipoDeAccion": "type",

            #Por default es '' (Vacio)
            "mensajeEsperado" : self.mensajeEsperado,

            #Estos valores siempre son obligatorios

            #tipoDeDato:string
            "tipoDeDato" : tipoDeDato,
            #longitud:10
            "longitud" : longitud,
            #obligatorio:si
            "obligatorio" : obligatorio,
            #unico:si
            "unico" : unico,

            #Generado por el bucle
            "indice" : self.indice
        }

        return detail

# class ClickTemplate(GeneralTemplate):
#     def __init__(self, value: str, target: str, typePath: str, indice: int, mensajeEsperado: str) -> None:
#         super().__init__(value, target, typePath, indice, mensajeEsperado)
    
#     def createDetail(self, validador:bool):
#         detail = {
#             "value" : self.value,
#             "target" : self.target,
#             "typePath" : self.typePath,
#             "tipoDeAccion" : "click",
#             "mensajeEsperado" : self.mensajeEsperado,

#             #validador:no
#             "validador" : validador,

#             "indice" : self.indice
#          }

#         return detail

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

        #Acciones detalladas
        detailedActions = []

        #Defino los comandos
        comandos = jsonRawData['tests'][0]['commands']

        #Defino el indice
        indice = 0

        #Realizo un recorrido
        for action in comandos:

            #Extraigo los valores base de la accion
            valor:str = action["value"]
            comentarios:str = action["comment"]
            tipoDeAccion:str = action['command']
            mensajeEsperado = ''
            validador = False

            #Si el comando es Type o click, entonces ejecuta un ciclo
            if tipoDeAccion in ['type', 'click']:

                #Formato para comentarios:
                #longitud:numero-tipoDeDato:string-obligatorio:si-unico:si
                indicaciones = comentarios

                if indicaciones != '':
                    #Establecer el mensaje esperado
                    for indicacion in indicaciones.split('-'):
                        if indicacion.split(':')[0] == 'mensajeEsperado':
                            mensajeEsperado=indicacion.split(':')[1]
                        elif (indicacion.split(':')[0] == 'validador') & (indicacion.split(':')[1]=='si'):
                            validador = True

                targets = action['targets']

                #Establezco la ubicacion del elemento
                #Dado que Selenium otorga arrayz mayores a 1, tambien puede otorgarr arreglos de solo 1; por lo tanto filtramos
                if len(targets) > 1:
                
                    #Por cada localizacion en localizaciones    
                    for target in targets:

                        target:list
                        
                        #Filtramos que no tome los que son id o name
                        if target[1] == 'id':
                            continue
                        elif target[1] == 'name':
                            continue

                        #Separa el formato y conviertelo en array porque es entregado así css:localizacion
                        location = target[1].split(':')
                        #Guarda el path en esta variable
                        path = target[0]

                        if location[0] != 'css':
                            path = path.split('xpath=')[1]
                            typePath = location[1]
                            match location[1]:
                                case 'idRelative':
                                    break
                                case 'attributes':
                                    break
                                case 'position':
                                    break
                        # else:
                        #     path = path.split('css=')[1]
                        #     typePath='css'
                
                else:
                    individualTarget:str = targets[0]
                    
                    path:str = individualTarget[0]
                    location:list = individualTarget[1].split(':')
                    
                    if location[0] != 'css':
                        path = path.split('xpath=')[1]
                        typePath='xpath'
                    else:
                        path = path.split('css=')[1]
                        typePath='css'

            
                #Si existen indicaciones para hacer testing, pasará por este statement (Para tipearr)
                if (tipoDeAccion == 'type') & (indicaciones != ''):

                    #Longitud Default
                    longitudDefault = 50

                    #Siempre deben existir estos valores en comentarios
                    tipoDeDato:str
                    longitud:int=longitudDefault
                    obligatorio:bool=False
                    unico:bool=False

                    #Recorrido en el bucle para establecer las variables de la accion
                    for indicacion in indicaciones.split('-'):

                        splitIndicacion:list = indicacion.split(':')
                        tipoIndicacion = splitIndicacion[0]
                        valorIndicacion = splitIndicacion[1]

                        match tipoIndicacion:
                            case 'tipoDeDato':
                                tipoDeDato = valorIndicacion
                            case 'longitud':
                                if valorIndicacion != 'indefinido':
                                    longitud = int(valorIndicacion)
                            case 'obligatorio':
                                if valorIndicacion == 'si':
                                    obligatorio = True
                            case 'unico':
                                if valorIndicacion == 'si':
                                    unico = True

                    #Agregar accion
                    detailedActions.append(TypingTemplate(valor,path,typePath, indice,mensajeEsperado,validador ).createDetail(tipoDeDato,longitud,obligatorio,unico))

                #Agregamos la rutina por default
                actions.append(GeneralTemplate(valor,path,typePath, indice,mensajeEsperado,validador).defaultDetail(tipoDeAccion=tipoDeAccion))

                indice += 1

        self.detailActions:list = detailedActions
        self.routine:list = actions
        self.detailedTests:list = []

    def createTests(self):

        templateRoutine = [e for e in self.routine]

        #Definir el click validador
        for test in self.detailActions:
            if test["tipoDeAccion"] == 'click':
                validador:bool = test["validador"]
                i = test["indice"]
                if validador:
                    templateRoutine[i]["validador"] = validador

        for test2 in self.detailActions:
            
            routineTest = []
            routineTest = copy.deepcopy(self.routine)

            indice = test2["indice"]

            tipoDeDato = test2["tipoDeDato"]
            longitud = test2["longitud"]
            obligatorio = test2["obligatorio"]
            mensajeEsperado = test2["mensajeEsperado"]
            unico = test2["unico"]

            tipoDeDatoRoutine = copy.deepcopy(routineTest)
            longitudRoutine = copy.deepcopy(routineTest)
            obligatorioRoutine = copy.deepcopy(routineTest)

            cadenaRandom = str(uuid.uuid4())


            rutinas = []

            if tipoDeDato == 'number':
                cadenaRandom = str(uuid.uuid4())
                tipoDeDatoRoutine[indice]["value"] = (cadenaRandom*4)[:longitud]
                rutinas.append(tipoDeDatoRoutine)

            if obligatorio:
                obligatorioRoutine[indice]["value"] = ''
                rutinas.append(obligatorioRoutine)

            if tipoDeDato == 'string':
                longitudRoutine[indice]["value"] =  (cadenaRandom*4)[:longitud+1]
            elif tipoDeDato == 'number':
                longitudRoutine[indice]["value"] = numberByLength(longitud+1)

            rutinas.append(longitudRoutine)

            for e in rutinas:
                element = {
                    "indice" : indice,
                    "mensajeEsperado":mensajeEsperado,
                    "acciones" : e
                }

                self.detailedTests.append(element)
                


test = Tests('testAcopio.json')
test.createTests()
print(test.detailedTests)
# test.creaTests()

        # self.routine.append(actions)
        # self.testRoutines = []
        # self.erroresEsperados = []

# test = Tests('FrankRecord.json')