import { requestMe, getSchool, getStudentById, getClassroom } from "../api.js";

const nameUser = document.getElementById('nameUser');
const roleUser = document.getElementById('roleUser');
const schoolUser = document.getElementById("schoolUser");

async function getSchoolByID(id) {
    const response = await getSchool(id);
    if (response) {
        return response;
    }
}

async function getStudent() {
    const access_token = localStorage.getItem("access_token");

    const id_student = localStorage.getItem("id_student");

    const response = await getStudentById(id_student);

    const school = await getClassroom(response.classroom);

    console.log(response)

    nameUser.textContent = response.name;
    roleUser.textContent = response.role;
    schoolUser.textContent = school.name;
}

getStudent();
