import { requestMe } from "../api.js";

const me = await requestMe()

const card = document.getElementById('label-nome')
const name2 = document.getElementById('name2')

const role = document.getElementById('label-role')

card.textContent = me.name
name2.textContent = me.name

role.textContent = `Cargo: ${me.role}`

console.log(me);