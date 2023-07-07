import json
import copy

class TestTemplates:
    def __init__(self, routine:list, mensajeEsperado:str = '') -> None:

        self.mensajeEsperado:str = mensajeEsperado
        self.routine:list = routine


class GeneralTemplate:
    def __init__(self, value:str, target:str, typePath:str, indice:int, mensajeEsperado:str, validador:bool ) -> None:

        self.target=target,
        self.value=value,
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
            "mensajeEsperado" : self.mensajeEsperado,

            #tipoDeDato:string
            "tipoDeDato" : tipoDeDato,
            #longitud:10
            "longitud" : longitud,
            #obligatorio:si
            "obligatorio" : obligatorio,
            #unico:si
            "unico" : unico,

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

                #Establecer el mensaje esperado
                for indicacion in indicaciones.split('-'):
                    if indicacion.split(':')[0] == 'mensajeEsperado':
                        mensajeEsperado=indicacion.split(':')[1]
                    elif (indicacion.split(':')[0] == 'validador') & (indicacion.split(':')[1]):
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
                                    longitud = valorIndicacion
                            case 'obligatorio':
                                if valorIndicacion == 'si':
                                    obligatorio = True
                            case 'unico':
                                if valorIndicacion == 'si':
                                    unico = True

                    #Agregar accion
                    detailedActions.append(TypingTemplate(value=valor,target=path, typePath=typePath, indice=indice, mensajeEsperado=mensajeEsperado,validador=validador ).createDetail(tipoDeDato,longitud,obligatorio,unico))

                # #Si existen indicaciones para esta etiqueta, y es de tipo click, pasará por este statement
                # elif (tipoDeAccion == 'click') & (indicaciones != ''):

                #     #Por defecto establecemos que el validador es falso
                #     validador = False

                #     #Realizamos un recorrido por las indicaciones, son posibles las de validador y mensaje esperado
                #     for clickIndicacion in indicaciones.split('-'):
                #         splitIndicacion:list = clickIndicacion.split(':')
                #         tipoIndicacion = splitIndicacion[0]
                #         valorIndicacion = splitIndicacion[1]

                #         #Hallamos la indicacion de validador
                #         if (tipoIndicacion == 'validador') & (valorIndicacion == 'si'):
                #             validador = True
                        
                #     detailedActions.append(ClickTemplate(valor,target=path,typePath=typePath, indice=indice, mensajeEsperado=mensajeEsperado).createDetail(validador))

                #Agregamos la rutina por default
                actions.append(GeneralTemplate(value=valor,target=path,typePath=typePath, indice=indice, validador=validador).defaultDetail(tipoDeAccion=tipoDeAccion))

                indice += 1

        self.detailActions:list = detailedActions
        self.routine:list = actions
        self.tests:list = []
        self.uniqueTests:list = []

    def createTests(self):

        #Definir rutina default
        routineTest:list = copy.copy(self.routine)

        #Definir el click validador
        for test in self.detailActions:
            if test["tipoDeAccion"] == 'click':
                validador:bool = test["validador"]
                i = test["indice"]
                if validador:
                    routineTest[i]["validador"] = validador

        #Definimos los tests
        for test in self.detailActions:
            
            #Copiamos la rutina default anteriormente modificada
            routineTest:list = copy.copy(routineTest)

            #Establecemos las variables por default
            valor:str = test["value"]
            target:str = test["target"]
            typePath:str = test["typePath"]
            tipoDeAccion:str = test["tipoDeAccion"]
            indice:int = test["indice"]

            

            
                    

                    



test = Tests('Test.json')
# test.creaTests()

        # self.routine.append(actions)
        # self.testRoutines = []
        # self.erroresEsperados = []

# test = Tests('FrankRecord.json')