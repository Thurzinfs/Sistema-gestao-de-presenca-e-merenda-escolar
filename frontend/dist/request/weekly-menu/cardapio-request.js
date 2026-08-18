import { getMenuCanteen } from "../api.js"
import { getMenuCanteenDate } from "../api.js";

const tbody = document.getElementById('cardapio')
const labelData = document.getElementById('label-data');
const almocLabel = document.getElementById('almoc-label')

let storageDates = {}

function getConvertDate() {
    const date = new Date()

    const _today = date.getDate()

    console.log('1: ', _today)

    const dataString = date.toDateString()
    console.log('ds', dataString)
    const dataLista = dataString.split(' ')
    
    console.log('2: ', dataLista)
    console.log('3', dataLista[0])

    const dataTraduzida = traducaoData(dataLista[0])

    console.log('4', dataTraduzida);

    const verificacao = verificacaoData(dataTraduzida, _today)

    console.log('5', verificacao)
    console.log(verificacao['from_date'])
    console.log(verificacao['to_date'])

    const d = {
        'from_date': verificacao['from_date'],
        'to_date': verificacao['to_date'],
        'day': dataTraduzida
    }

    return d

}

function forDateInStorage(from) {
    // let count = from



    // while (from < to) {
    //     storageDates[count] = 

    //     count += 1
    // }

    const date = new Date();

    const today = date.toDateString();

    const lista = today.split(" ");

    lista[2] = from.split('-')[2]

    const newDate = new Date(lista.toString())
    console.log("teste: ", newDate.toDateString());

    console.log('traducao: ', traducaoData(newDate.toDateString().split(" ")[0]))


    console.log('lista: ', lista);

    return traducaoData(newDate.toDateString().split(" ")[0])
}

forDateInStorage("2026-08-19");


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

function traducaoDataLabel(data){
    const dataSplit = data.split(' ')

    const d = {
        'Mon':'Segunda',
        'Tue':'Terça',
        'Wed':'Quarta',
        'Wed':'Quinta',
        'Fri': 'Sexta'
    }

    const mesT = {
        'Jan':'Janeiro',
        'Feb':'Fevereiro',
        'Apr':'Março',
        'Mar':'Abril',
        'May': 'Maio',
        'Jun':'Junho',
        'Jul':'Julho',
        'Aug':'Agosto',
        'Set':'Setembro',
        'Out':'Outubro',
        'Nov':'Dezembro',
        'Dez':'Setembro',
    }

    return {
        'dia': d[dataSplit[0]],
        'mes': mesT[dataSplit[1]],
        'mesN': dataSplit[2],
        'ano': dataSplit[3],
    }
}

const dataConvertida = getConvertDate()
console.log(dataConvertida)

const response = await getMenuCanteen(`2026-08-${dataConvertida['from_date']}`, `2026-08-${dataConvertida['to_date']}`)

console.log(response)

for (const u of response){
    
    console.log(forDateInStorage(u.date))

    const tr = document.createElement('tr')

        tr.innerHTML = `
            <th>${forDateInStorage(u.date)}</th>
            <th>${u.main_course}</th>
        `

    tbody.appendChild(tr)
}

const date = new Date()

const dateTra = traducaoDataLabel(date.toDateString())

console.log(dateTra)

labelData.textContent = `${dateTra['dia']}, ${dateTra['mesN']} de ${dateTra['mes']} de ${dateTra['ano']}`

const toDay = `${date.getFullYear()}-0${date.getMonth() + 1}-${date.getDate()}`

console.log(toDay)

const menuHoje = await getMenuCanteenDate(toDay)

console.log(menuHoje)

almocLabel.textContent = `Prato principal hoje: ${menuHoje.main_course}`


