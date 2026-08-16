import { getStudentList, getClassroom } from '../api.js';

const users = await getStudentList();

const tbody = document.querySelector('#pc-dt-simple tbody');
const countStudents = document.querySelector('#count-students');

async function getClassroomName(id) {
  const response = await getClassroom(id);

  return response?.name ?? 'Sem sala de aula';
};

if (countStudents && Array.isArray(users)) {
  countStudents.textContent = `${users.length}`
}

if (tbody && Array.isArray(users)) {
  tbody.innerHTML = '';

  for (const u of users) {
    const classroom = await getClassroomName(u.classroom);

    const tr = document.createElement('tr');
    tr.innerHTML = `
      <tr>
          <td>
            <div class="d-flex align-items-center">
              <div class="flex-grow-1 ms-3">
                <h6 class="mb-0">${u.name}</h6>
              </div>
            </div>
          </td>
          <td>${classroom}</td>
          <td>${u.active}</td>
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
    `;
    tbody.appendChild(tr);
    
  }
};

new window.simpleDatatables.DataTable('#pc-dt-simple', {
  searchable: true,
  perPage: 10,
  perPageSelect: [5, 10, 15, 20]
});
