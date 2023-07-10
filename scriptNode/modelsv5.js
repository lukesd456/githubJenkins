const {readFile, writeFile} = require('fs/promises')
const { v4:uuidV4 } = require('uuid')

class FilterSide {
    constructor (json) {
        this.url = json.url;
        this.commands = json.tests[0].commands
    }
}

const filterXPATH = (targets, type) => {
    let result = targets.filter(e => e.detail == type)

    result = result.length == 1 ? result[0] : false

    return result
}

const generarPalabraAleatoria = (longitud) => {
    const alfabeto = 'abcdefghijklmnopqrstuvwxyz';
    let palabra = '';
  
    for (let i = 0; i < longitud; i++) {
      const indice = Math.floor(Math.random() * alfabeto.length);
      const letra = alfabeto.charAt(indice);
      palabra += letra;
    }
  
    return palabra;
}

const generarNumeroAleatorio = (longitud) => {
    let numero = '';
    
    for (let i = 0; i < longitud; i++) {
      const digito = Math.floor(Math.random() * 10); // Generar un dígito aleatorio entre 0 y 9
      numero += digito;
    }
    
    return numero;
}

const filterTests = (rutina, indice, value, tipoDeTest,mensajeEsperado) => {

    rutina[indice].value = value

    return {
        rutina,
        indice,
        tipoDeTest,
        mensajeEsperado: mensajeEsperado
    }
}

const createTests = async (path) => {

    let file = await readFile(path, 'utf-8')

    file = await JSON.parse(file)

    file = new FilterSide(file)

    let filterCommands = []

    file.commands = file.commands.map(f => f.command === 'type' ? filterCommands.push(f) : f.command === 'click' && filterCommands.push(f))

    file.commands = filterCommands

    //Filter targets
    file.commands = file.commands.map((e) => {
        let objetivos = e.targets

        objetivos = objetivos.map((o) => {
            let location = o[0]
            let detail = o[1]

            let isTarget = false

            if (location.includes('xpath=')) {
                location = location.split('xpath=')[1]
                detail = detail.split(':')[1]
                isTarget = true
            } else if (location.includes('css=')) {
                location = location.split('css=')[1]
                detail = 'css'
                isTarget = true
            }

            return {
                location,
                detail,
                isTarget
            }

        })

        //Quitamos los tipos de target que no interesan
        objetivos = objetivos.filter(o => o.isTarget)

        e["targets"] = objetivos

        return e
    })

    //Establecemos el objetivo
    file.commands = file.commands.map((e) => {
        let objetivos = e.targets

        let target

        objetivos.map((o) => {

            let data = {
                location : o.location,
                detail : o.detail
            }

            target && o.detail === 'idRelative' ? target = data : o.detail === 'attributes'  ? target = data : o.detail === 'position' ? target = data : o.detail === 'innerText' ? target = data : target = data
        })

        e["target"] = target

        return e

    })

    let testsToDo = []
    let indice = 0

    file.commands = file.commands.map((e) => {
        
        let testToDo = e.comment !== '' ? true : false
        let validador = false
        let mensajesEsperados = []
        
        //Forma de documentar los detalles
        
        //tipoDeDato:string
        //obligatorio:si
        //longitud:10 o indefinida
        //mensajesEsperados:Campo requerido.|El RUC

        let testNumero = false
        let testLongitud = false
        let testObligatorio = false
        let longitud = 20

        if (testToDo) {

            let separateComments = e.comment.split('-')

            testNumero = e.comment.includes('numero')
            
            testObligatorio = e.comment.includes('obligatorio')

            testLongitud = !e.comment.includes('longitud:indefinida')
            
            validador = e.comment.includes('validador')

            let foundMessages = e.comment.includes('mensajesEsperados:')

            testLongitud && separateComments.map((c) => {
                
                if (c.includes('longitud:')) {
                    
                    //Si se encuentra longitud la establece
                    longitud = parseInt(c.split(':')[1])
                
                }
            })

            foundMessages && separateComments.map((c) => {
                if (c.includes('mensajesEsperados:')) {
                    
                    //Si se encuentran mensajes los establecemos
                    mensajesEsperados = c.split(':')[1].split('|')
                
                }
            })



        }

        e["indice"] = indice
        e["validador"] = validador
        e["mensajesEsperados"] = mensajesEsperados
        e["testLongitud"] = testLongitud
        e["testObligatorio"] = testObligatorio
        e["testNumero"] = testNumero
        e["longitud"] = e.command === 'type' && longitud
        
        testToDo && testsToDo.push(e)

        indice += 1

        return e
    })

    file.tests = []

    testsToDo.map((t) => {

        let indice = t.indice
        let copyArray = file.commands.slice()
        let mensajesEsperados = t.mensajesEsperados

        if (t.testLongitud) {
            copyArray.value = generarNumeroAleatorio(t.longitud)
            file.tests.push({
                indice,
                mensajesEsperados,
                tipoDeTest: 'longitud',
                rutina: copyArray,
            })    
        }

        if (t.testNumero) {
            copyArray.value = generarPalabraAleatoria(t.longitud)
            file.tests.push({
                indice,
                mensajesEsperados,
                tipoDeTest: 'tipoDeDato',
                rutina: copyArray
            })
        }

        if (t.testObligatorio) {
            copyArray.value = ''
            file.tests.push({
                indice,
                mensajesEsperados,
                tipoDeTest: 'obligatorio',
                rutina: copyArray
            })
        }

    })

    file.tests.map(t => t.rutina = t.rutina.filter(e => e.target))

    let finalObject = {
        targetURL : file.url,
        rutinaNormal : file.commands,
        tests: file.tests
    }

    finalObject = JSON.stringify(finalObject)

    writeFile('./filteredTests.json', finalObject, 'utf-8')
}

createTests('./testAcopio2.side')