import { getStudentsByClassRoom } from "../api.js"

const tbody = document.getElementById('turmas-table')

const students = await getStudentsByClassRoom(localStorage.getItem('id_sala'))

console.log(students);

tbody.innerHTML = '';

const label = document.getElementById('label');

label.textContent = ''

label.textContent = localStorage.getItem('name_classroom')

for (const u of students){
    const tr = document.createElement('tr')
    tr.innerHTML = `
      <tr>
          <td>
            <div class="d-flex align-items-center">
              <div class="flex-grow-1 ms-3">
                <h6 class="mb-0">${u.name}</h6>
              </div>
            </div>
          </td>
          <td>${u.ra}</td>
          <td></td>
          <td class="text-success"><i class="fas fa-circle f-10 m-r-10"></i> Active</td>
          <td>
            <a href="#" class="avtar avtar-xs btn-link-secondary">
              <i class="ti ti-eye f-20"></i>
            </a>
            <a href="#" class="avtar avtar-xs btn-link-secondary">
              <i class="ti ti-edit f-20"></i>
            </a>
            <a href="#" class="avtar avtar-xs btn-link-secondary">
              <i class="ti ti-trash f-20"></i>
            </a>
          </td>
        </tr>
    `

    tbody.append(tr)
}