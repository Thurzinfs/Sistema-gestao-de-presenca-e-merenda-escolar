import { getMenuCanteen } from "../api.js"

const tbody = document.getElementById('cardapio')

function getConvertDate() {
    /*
    const timeElapsed = Date.now();
    const today = new Date(timeElapsed);
    console.log(today)

    console.log(today.toDateString())

    */

    const date = new Date()

    const _today = date.getDate()

    console.log(_today)

    const dataString = date.toDateString()
    const dataLista = dataString.split(' ')
    
    console.log(dataLista)
    console.log(dataLista[0])

    const dataTraduzida = traducaoData(dataLista[0])

    console.log(dataTraduzida);

    const verificacao = verificacaoData(dataTraduzida, _today)


    console.log(verificacao)
    console.log(verificacao['from_date'])
    console.log(verificacao['to_date'])

    const d = {
        'from_date': verificacao['from_date'],
        'to_date': verificacao['to_date'],
        'day': dataTraduzida
    }

    return d

}


function verificacaoData(data, dateDay){

    let from_date = 0;
    let to_date = 0;

    switch(data){
        case 'Segunda':
            from_date = dateDay;
            to_date = dateDay + 4
            return {from_date, to_date}
        break;

        case 'Terça':
            from_date = dateDay - 1
            to_date = dateDay + 3
            return {from_date, to_date}
        break;

        case 'Quarta':
            from_date = dateDay - 2
            to_date = dateDay + 2
            return {from_date, to_date}
        break;

        case 'Quinta':
            from_date = dateDay - 3
            to_date = dateDay + 1
            return {from_date, to_date}
        break;

        case 'Sexta':
            from_date = dateDay - 4
            to_date = dateDay
            return {from_date, to_date}
        break;
    }
}


function traducaoData(dateEnglashe){
    const d = {
        'Mon':'Segunda',
        'Tue':'Terça',
        'Wed':'Quarta',
        'Wed':'Quinta',
        'Fri': 'Sexta'
    }

    return d[dateEnglashe]
}

const dataConvertida = getConvertDate()
console.log(dataConvertida)

const response = await getMenuCanteen(`2026-08-${dataConvertida['from_date']}`, `2026-08-${dataConvertida['to_date']}`)

console.log(response)

for (const u of response){
    
    console.log(u.date)

    const tr = document.createElement('tr')

        tr.innerHTML = `
            <th>${u.date}</th>
            <th>${u.main_course}</th>
        `

    tbody.appendChild(tr)
}