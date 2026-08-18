import { registerUSer } from "../api.js";

const formRegisterUser = document.querySelector('#form-register');

const formName = document.querySelector('#form-name');
const formEmail = document.querySelector('#form-email');
const formPassword = document.querySelector('#form-password');
const formRole = document.querySelector('#role');

async function dataUser(school, role, name, email, password) {
    if (!school || !role || !name || !email || !password) return null;

    const data = {
        school_id: school,
        role: role,
        name: name,
        email: email,
        password: password
    };

    const response = await registerUSer(data);
    console.log("response 1: ", response);
    return response;
}

formRegisterUser.addEventListener('submit', async (e) => {
    e.preventDefault();

    const roleValue = formRole.value;
    const nameValue = formName.value;
    const emailValue = formEmail.value;
    const passwordValue = formPassword.value;

    if (roleValue && nameValue && emailValue && passwordValue) {    
        const response = await dataUser(
            '4ddbb1f0-3d91-4e0b-86ad-60153db0bb24', 
            roleValue, 
            nameValue, 
            emailValue, 
            passwordValue
        );

        if (response && response.status === 201) {
            window.location.href = '../../../dist/application/user-card-v1.html';
        }
    }
});
