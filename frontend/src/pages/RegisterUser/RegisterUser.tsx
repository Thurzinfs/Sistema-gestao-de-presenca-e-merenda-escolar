import { useState } from "react";
import { Link, useNavigate } from 'react-router-dom'

import styles from './RegisterUser.module.css';

import { HeaderRegisterUser } from "../../components/Header/header";
import { InputField } from "../../components/InputField/InputField";
import { ButtonSend } from "../../components/buttonSend/buttonSend";
import { USER_ROLES } from "../../constrants/roles";
import { usersServices, type User } from "../../services/users";

export function RegisterUser () {
    const navigate = useNavigate();

    const [nomeCompleto, setNameCompleto] = useState<User['name']>('');
    const [passwordUser, setPasswordUser] = useState<User['password']>('');
    const [emailUser, setEmailUser] = useState<User['email']>("");
    const [role, setRole] = useState<User['role']>('PENDING');

    const [isLoading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        try {
            setLoading(true);

            const response = await usersServices.create({
                school_id: '9feee81a-55ad-4ce8-b825-e193afe5717a',
                role: role,
                name: nomeCompleto,
                email: emailUser,
                password: passwordUser
            })

            console.log(response)

            navigate('/home');
        } catch (error) {
            console.log("Erro: ", error)
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className={styles.container}>
            <div className={styles.contentWrapper}>
                <HeaderRegisterUser boxText="REG" textHeaderPart1="CRIAR" textHeaderPart2="CONTA" descriptionBox="sistema de cadastro"/>

                <form onSubmit={handleSubmit}>
                    <InputField label="NOME COMPLETO" placeholder="Maria Silva" name="nameUser" value={nomeCompleto} onChange={setNameCompleto}></InputField>

                    <InputField label="E-MAIL" placeholder="maria.email@gmail.com" name="emailUser" value={emailUser} onChange={setEmailUser}></InputField>

                    <InputField label="PASSWORD" placeholder="********" type="password" isPassword name="passwordUser" value={passwordUser} onChange={setPasswordUser}></InputField>

                    <div className={styles.inputGroup}>
                        <label htmlFor="role" className={styles.label}>TIPO DE USUARIO</label>
                        <select id="role" value={role} onChange={(e) => setRole(e.target.value as User['role'])} className={styles.selectRole}>
                            {
                                USER_ROLES.map((option) => (
                                    <option key={option.value} value={option.value}>{option.label}</option>
                                ))
                            }
                        </select>
                    </div>

                    <ButtonSend text={isLoading ? "ENTRANDO..." : "CADASTRAR AGORA"} type="submit"/>
                </form>

                <div className={styles.otherAccount}>
                    <span className={styles.textOtherAccount}>
                        Já possui uma conta?
                    </span>

                    <Link to='/' className={styles.buttonOtherAccount}>
                        Fazer login
                    </Link>
                </div>
            </div>
        </div>
    )
}