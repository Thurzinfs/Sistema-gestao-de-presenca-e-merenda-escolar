<<<<<<< HEAD
import { getStudentList, getClassroom, getSnackRegisters, getAllSnacksByType, getPresenceFrequency, getStudentById } from '../api.js';

const frequency = await getPresenceFrequency();

const tbody = document.querySelector('#pc-dt-simple tbody');
const countStudents = document.querySelector('#count-students');
const countSnack = document.querySelector('#count-snack');
const countSnackLittle = document.querySelector("#count-snack-little")

async function getClassroomName(id) {
  const response = await getClassroom(id);

  return response?.name ?? 'Sem sala de aula';
};

async function getCountSnacksByNormal() {
  const response = await getAllSnacksByType('NORMAL');
  return response?.length ?? 0
}

async function getCountSnacksByLittle() {
  const response = await getAllSnacksByType('LITTLE');
  return response?.length ?? 0
}

if (countStudents && countSnack && Array.isArray(frequency)) {
  const snackNormal = await getCountSnacksByNormal();
  const snackLitte = await getCountSnacksByLittle();

  countStudents.textContent = `${frequency.length}`;
  countSnack.textContent = `${snackNormal}`
  countSnackLittle.textContent = `${snackLitte}`
}

if (tbody && Array.isArray(frequency)) {
  tbody.innerHTML = '';

  for (const u of frequency) {
    const student = await getStudentById(u.student)
    const classroom = await getClassroomName(student.classroom);

    const tr = document.createElement('tr');
    tr.innerHTML = `
      <tr>
          <td>
            <div class="d-flex align-items-center">
              <div class="flex-grow-1 ms-3">
                <h6 class="mb-0">${student.name}</h6>
              </div>
            </div>
          </td>
          <td>${student.ra}</td>
          <td>${classroom}</td>
          <td class="text-success"><i class="fas fa-circle f-10 m-r-10"></i> Active</td>
          <td>
            <a href="#" class="avtar avtar-xs btn-link-secondary">
              <i class="ti ti-eye f-20"></i>
            </a>
            <a href="#" class="avtar avtar-xs btn-link-secondary">
              <i class=""></i>
            </a>
            <a href="#" class="avtar avtar-xs btn-link-secondary">
              <i class=""></i>
            </a>
          </td>
        </tr>
    `;
    tbody.appendChild(tr);
    
  }
};

new window.simpleDatatables.DataTable('#pc-dt-simple', {
  searchable: true,
  perPage: 10,
  perPageSelect: [5, 10, 15, 20]
});
=======
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
>>>>>>> main
