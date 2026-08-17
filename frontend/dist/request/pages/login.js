import { loginUser } from "../api.js";

const btnLogin = document.querySelector("#btn-login");


async function loginManager(email, password) {
    const data = {
        email: email,
        password: password
    }

    const response = await loginUser(data);
    return response
}

btnLogin.addEventListener('click', async (e) => {
    e.preventDefault();

    const inputEmail = document.getElementById('floatingInput')?.value;
    const inputPassword = document.getElementById('floatingInput1').value;

    const response = await loginManager(inputEmail, inputPassword)

    if (response == true) {
        window.location.href = '../../../dist/application/user-card-v1.html'
    }
})
