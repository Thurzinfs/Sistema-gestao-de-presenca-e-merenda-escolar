import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { HeaderRegisterUser } from "../../components/Header/header";
import { InputField } from "../../components/InputField/InputField";
import { ButtonSend } from "../../components/buttonSend/buttonSend";

import { usersServices } from "../../services/users";

import styles from './index.module.css'
import { tokenService } from "../../services/tokenStorage";

export function LoginPage() {
    const [emailUser, setEmailUser] = useState('');
    const [passwordUser, setPasswordUser] = useState('');
    
    const [loading, setLoading] = useState(false);

    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setLoading(true);

        try {
            const response = await usersServices.login({ email: emailUser, password: passwordUser });

            tokenService.saveTokens(response.access_token, response.refresh_token);

            navigate('/home')

        } catch (error) {
            console.log('erro no login: ', error);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className={styles.container}>
            <div className={styles.contentWrapper} >
                <HeaderRegisterUser boxText="LOG" descriptionBox="sistema de login" textHeaderPart1="LOGIN" textHeaderPart2=""/>

                <form onSubmit={handleSubmit} className={styles.formLogin}>
                    <InputField label="E-MAIL" placeholder="maria.email@gmail.com" name="emailUser" value={emailUser} onChange={setEmailUser}></InputField>
                    
                    <InputField label="PASSWORD" isPassword placeholder="********" name="passwordUser" value={passwordUser} onChange={setPasswordUser}></InputField>

                    <ButtonSend text={loading ? "ENTRANDO..." : "ENTRAR"} type="submit" isLoading={loading}/>
                </form>

                <div className={styles.otherAccount}>
                    <span className={styles.textOtherAccount}>
                        Não possui uma conta?
                    </span>

                    <Link to='/register' className={styles.buttonOtherAccount}>
                        Cadastre-se
                    </Link>
                </div>
            </div>
        </div>
    )
}
