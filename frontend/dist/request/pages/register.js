import { registerUSer } from "../api.js";

const formRegisterUser = document.querySelector('#form-register');
const btnRegister = document.querySelector('#btn-register');

const formName = document.querySelector('#form-name');
const formEmail = document.querySelector('#form-email');
const formPassword = document.querySelector('#form-password');
const formRole = "DIRECTOR"

async function dataUser(school, role, name, email, password) {
    if(!school || !role || !name || !email || !password) return;

    const data = {
        school_id: school,
        role: role,
        name: name,
        email: email,
        password: password
    }

    const response = await registerUSer(data);
    console.log("response 1: ", response)
    return response
}

btnRegister.addEventListener('click', async (e) => {
    e.preventDefault();

    if (formRole && formName.value && formEmail.value && formPassword.value) {    
        const response = await dataUser('4ddbb1f0-3d91-4e0b-86ad-60153db0bb24', formRole, formName.value, formEmail.value, formPassword.value);
        console.log(response.status, response.dados)
        if (response.status == 201) {
            window.location.href = '../../../dist/application/user-card-v1.html'
        }
    }
})
