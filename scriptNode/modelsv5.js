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

const generarNumeroAleatorio = (longitud) => {
    let numero = '';
    
    for (let i = 0; i < longitud; i++) {
      const digito = Math.floor(Math.random() * 10); // Generar un dígito aleatorio entre 0 y 9
      numero += digito;
    }
    
    return numero;
}

const filterTests = (rutina, indice, value, tipoDeTest,mensajeEsperado) => {

    let copyRoutine = rutina
    copyRoutine[indice].value = value
    console.log(mensajeEsperado)

    return {
        rutina:copyRoutine,
        indice,
        tipoDeTest,
        mensajeEsperado: mensajeEsperado
    }
}

const createTests = async (path) => {

    let file = await readFile(path, 'utf-8')

    file = await JSON.parse(file)

    file = new FilterSide(file)

    file.commands = file.commands.map((e) => {
        let objetivos = e.targets

        let command = e.command
        let comment = e.comment
        let value = e.value

        //Filtrar los objetivos

        objetivos = objetivos.map((o) => {

            let location = o[0]
            let detail = o[1]
            let typeTarget

            if (location.includes('xpath=')) {

                location = location.split('xpath=')[1]
                detail = detail.split(':')[1]
                typeTarget = 'xpath'

            } else if (location.includes('css=')) {

                location = location.split('css=')[1]
                detail = detail.split(':')[1]
                typeTarget = 'css'

            } else {

                location = location
                detail = detail
                typeTarget = 'none'

            }
            
            return {
                location,
                detail,
                typeTarget,
                value
            }

        })

        //Definir la ruta

        let cssTarget = objetivos.filter(e=>e.typeTarget == 'css')[0]

        let xpathTargets = objetivos.filter(e=>e.typeTarget === 'xpath' && e)
        
        let location

        if (xpathTargets.length>0) {
            let attributes = filterXPATH(xpathTargets,'attributes')
            let idRelative = filterXPATH(xpathTargets, 'idRelative')
            let position = filterXPATH(xpathTargets, 'position')
            let innerText = filterXPATH(xpathTargets, 'innerText')

            location = idRelative ? idRelative : attributes ? attributes : position ? position : innerText

        } else {
            location = cssTarget
        }

        return {
            ...location,
            command,
            comment
        }

    })

    file.commands = file.commands.map((e) => {
        let comment = e.comment
        let indice = file.commands.indexOf(e)
        
        //filtrar los tests

        comment = comment.split('-').filter(c=>c!='')

        let testToDo = comment.length > 0 ? true : false

        e['validador'] = false

        testToDo && comment.map((c) => {
            let element = c.split(':')

            switch (element[0]) {
                case 'tipoDeDato':
                    e['tipoDeDato'] = element[1]
                    break
                case 'obligatorio':
                    e['obligatorio'] = element[1] == 'si' ? true:false
                    break
                case 'longitud':
                    e['longitud'] = element[1]
                    break
                case 'mensajeEsperado':
                    e['mensajeEsperado'] = element[1].split('|')
                    break
                case 'validador':
                    e['validador'] = element[1] == 'si' && true
                    testToDo = false
            }

        })

        return {
            ...e,
            indice,
            testToDo
        }


    })

    let testsToDo = file.commands.filter(e => e.testToDo == true)

    let tests = []

    testsToDo.map((t) => {

        let copy = file.commands
        let indice = t.indice
        let mensajeEsperado = t.mensajeEsperado

        t.tipoDeDato != 'string' && tests.push(filterTests(copy, indice,uuidV4() + uuidV4(), 'tipoDeDato', mensajeEsperado))

        t.longitud != 'indefinida' && tests.push(filterTests(copy, indice, generarNumeroAleatorio(parseInt(t.longitud)+1), 'longitud', mensajeEsperado))

        t.obligatorio && tests.push(filterTests(copy, indice, '', 'obligatoriedad', mensajeEsperado))

    })

    let finalObject = {
        targetURL : file.url,
        rutinaNormal : file.commands,
        tests
    }

    finalObject = JSON.stringify(finalObject)

    writeFile('./filteredTests.json', finalObject, 'utf-8')

}

createTests('./testAcopio2.side')