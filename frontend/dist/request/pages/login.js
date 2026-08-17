import { loginUser } from "../api";

const inputEmail = document.querySelector('#input-email-login');
const inputPassword = document.querySelector('#input-password-login');

const btnLogin = document.querySelector("#btn-login");


async function loginManager(email, password) {
    const data = {
        email: email,
        password: password
    }

    const response = await loginUser(data);
    return response
}
console.log('ola')

btnLogin.addEventListener('click', async (e) => {
    e.preventDefault();
    
    if (inputEmail.value && inputPassword.value) {
        const login = loginManager(inputEmail.value, inputPassword.value)
        if (login) {
            console.log(localStorage.getItem('access_token'))

            window.location.href = '../../application/user-card-v1.html'
        }
    }
})
