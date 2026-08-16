import { getStudentList, getClassroom } from '../api.js';

const users = await getStudentList();
const tbody = document.querySelector('#pc-dt-simple tbody');
const h2CountStudents = document.querySelector('#count-all-students');

if (h2CountStudents && Array.isArray(users)) {
  h2CountStudents.textContent = `${users.length}`;
}

async function getClassroomName(id) {
  const response = await getClassroom(id);
  return response?.name ?? 'Sem sala';
}

if (tbody && Array.isArray(users)) {
  tbody.innerHTML = '';

  const rows = [];

  for (const u of users) {
    const classroom = await getClassroomName(u.classroom);
    const activeLabel = u.active === true ? 'Ativo' : 'Inativo';
    const activeClass = u.active  === true? 'text-success' : 'text-secondary';

    rows.push(`
      <tr>
        <td>
          <div class="d-flex align-items-center">
            <div class="flex-shrink-0">
              <img src="../assets/images/user/avatar-1.jpg" alt="user image" class="img-radius wid-40">
            </div>
            <div class="flex-grow-1 ms-3">
              <h6 class="mb-0">${u.name}</h6>
            </div>
          </div>
        </td>
        <td>${u.ra}</td>
        <td>${classroom}</td>
        <td class="${activeClass}"><i class="fas fa-circle f-10 m-r-10"></i>${activeLabel}</td>
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
    `);
  }

  tbody.innerHTML = rows.join('');

  if (window.simpleDatatables) {
    new window.simpleDatatables.DataTable('#pc-dt-simple', {
      searchable: true,
      perPage: 10,
      perPageSelect: [5, 10, 15, 20],
      labels: {
        placeholder: 'Buscar...',
        perPage: 'registros por página',
        noRows: 'Nenhum registro encontrado',
        info: 'Mostrando {start} a {end} de {rows} registros'
      }
    });
  }
}
