import styles from './header.module.css';

interface HeaderProps {
    boxText: string;
    textHeaderPart1: string;
    textHeaderPart2: string;
    descriptionBox: string;
}

export function HeaderRegisterUser({ boxText, textHeaderPart1, textHeaderPart2, descriptionBox, }: HeaderProps) {
    return (
        <header className={styles.header}>
            <div className={styles.divReg}>
                <h1 className={styles.textBox}>{boxText}</h1>
                <span className={styles.title}>{descriptionBox}</span>
            </div>

            <h1 className={styles.mainTitle}>
                <span className={styles.white}>{textHeaderPart1}</span> <span className={styles.orange}>{textHeaderPart2}</span>
            </h1>

            <p className={styles.description}>Preencha os campos abaixo para se cadastrar na plataforma.</p>
        </header>
    );
}