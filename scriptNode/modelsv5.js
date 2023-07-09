const {readFile} = require('fs/promises')

const test = async () => {
    const test = await readFile('./testAcopio.side', 'utf-8')

    const testJson = JSON.parse(test)

    console.log(testJson.tests[0].commands)
}

test()