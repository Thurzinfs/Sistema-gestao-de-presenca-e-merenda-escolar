import styles from "./index.module.css";

interface CardProps {
    title: string,
    description: string,
    data: string
}

export function Card({ title, description, data }: CardProps) {
    return (
        <div className={styles.container}>
            <p className={styles.title}>{title}</p>
            <h1 className={styles.data}>{data}</h1>
            <p className={styles.description}>{description}</p>
        </div>
    )
}