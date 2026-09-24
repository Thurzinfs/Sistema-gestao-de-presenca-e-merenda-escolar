import type { LucideIcon } from "lucide-react";
import styles from "./index.module.css";

interface HeaderProps {
    titleWhite: string,
    titleOrange: string,
    subTitle: string,
    Icon: LucideIcon
}

export function HeaderPage({ titleWhite, titleOrange, subTitle, Icon }: HeaderProps) {
    return (
        <div className={styles.container}>
            <Icon size={24} className={styles.icon}/>

            <div className={styles.wrapper}>
                <h1 className={styles.title}><span className={styles.white}>{titleWhite}</span> <span className={styles.orange}>{titleOrange}</span></h1>
                <p className={styles.subTitle}>{subTitle}</p>
            </div>
        </div>
    )
}
