import { requestMe, getSchool } from "../api.js";

const nameUser = document.getElementById('nameUser');
const roleUser = document.getElementById('roleUser');
const schoolUser = document.getElementById("schoolUser");

async function getSchoolByID(id) {
    const response = await getSchool(id);
    if (response) {
        return response;
    }
}

async function getMe() {
    const access_token = localStorage.getItem("access_token");

    const response = await requestMe();

    const school = await getSchoolByID(response.school_id);

    console.log(response)

    nameUser.textContent = response.name;
    roleUser.textContent = response.role;
    schoolUser.textContent = school.name;
}

getMe();
