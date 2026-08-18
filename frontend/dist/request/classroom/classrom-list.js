import { getClassroomActives } from "../api.js"

const tbody = document.getElementById('turmas-table')

const classrooms = await getClassroomActives();

console.log(classrooms);

tbody.innerHTML = '';

for (const u of classrooms){
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
          <td></td>
          <td></td>
          <td class="text-success"><i class="fas fa-circle f-10 m-r-10"></i> ${u.active ? 'Ativo' : 'Desativada'}</td>
          <td>
            <a href="#" class="btn-view avtar avtar-xs btn-link-secondary" id="btn-link">
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

    tbody.appendChild(tr);

    const btnView = tr.querySelector('.btn-view')

    btnView.addEventListener('click', (event) => {
        event.preventDefault()
        localStorage.setItem('id_sala', u.id)
        localStorage.setItem('name_classroom', u.name)
        window.location.href = '/dist/application/user-list-clasrrom.html'
    })

}
