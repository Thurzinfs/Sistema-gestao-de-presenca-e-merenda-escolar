import styles from './index.module.css';


interface StudentRowProps {
    name: string,
    ra: string,
    classroom: string,
    lunch: string,
}

export function StudentRow({ name, ra, classroom, lunch }: StudentRowProps) {
    const splitName = (name: string) => {
        const nameWithoutSpace = name.split(' ')
        return `${nameWithoutSpace[0][0]}${nameWithoutSpace[1][0]}`.toUpperCase()
    }

    return <div className={styles.container}>
        <div className={styles.userInfo}>
            <div className={styles.icon}>{splitName(name)}</div>

            <div className={styles.infoWrapper}>
                <p className={styles.name}>{name}</p>
                <p className={styles.ra}>Matricula: {ra}</p>
            </div>
        </div>

        <div className={styles.snacks}>
            <p className={styles.bunddle}>{classroom}</p>
            <p className={styles.bunddle}>{lunch}</p>
        </div>
    </div>
}
