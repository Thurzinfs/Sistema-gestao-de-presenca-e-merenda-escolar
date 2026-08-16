import { getStudentList } from '../api.js';

const users = await getStudentList();
const tbody = document.querySelector('#pc-dt-simple tbody');

if (tbody && Array.isArray(users)) {
  tbody.innerHTML = '';

  users.forEach((u) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>
        <div class="d-inline-block align-middle">
          <div class="d-inline-block">
            <h6 class="m-b-0">${u.name || u.full_name || ''}</h6>
            <p class="m-b-0 text-primary">${u.title || ''}</p>
          </div>
        </div>
      </td>
      <td>${String(u.ra || '')}</td>
      <td>${String(u.qr_code || '')}</td>
      <td>${String(u.classroom || '')}</td>
      <td>
        <span class="badge ${u.active === 'Active' ? 'bg-light-success' : 'bg-light-danger'}">${u.active || ''}</span>
        <div class="overlay-edit">
          <ul class="list-inline mb-0">
            <li class="list-inline-item m-0"><a href="#" class="avtar avtar-s btn btn-primary"><i class="ti ti-pencil f-18"></i></a></li>
            <li class="list-inline-item m-0"><a href="#" class="avtar avtar-s btn bg-white btn-link-danger"><i class="ti ti-trash f-18"></i></a></li>
          </ul>
        </div>
      </td>
    `;
    tbody.appendChild(tr);
  });
};
