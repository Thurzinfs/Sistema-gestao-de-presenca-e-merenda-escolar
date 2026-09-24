import { NavLink } from 'react-router-dom';
import { CalendarDays, GraduationCap, UtensilsCrossed, X } from 'lucide-react';
import styles from './index.module.css';

const linkClass = ({ isActive }: { isActive: boolean }) =>
    `${styles.link} ${isActive ? styles.active : ''}`;

type SidebarProps = {
    open: boolean;
    onClose: () => void;
};

export function Sidebar({ open, onClose }: SidebarProps) {
    return (
        <aside className={`${styles.container} ${open ? styles.open : ''}`}>
            <div className={styles.header}>
                <div className={styles.icon}>
                    <GraduationCap size={22} />
                </div>

                <div className={styles.wrapper}>
                    <h1 className={styles.title}>
                        <span className={styles.white}>GESTÃO</span>{' '}
                        <span className={styles.orange}>ESCOLAR</span>
                    </h1>
                    <p className={styles.gray}>Coordenação</p>
                </div>

                <button type="button" className={styles.close} onClick={onClose} aria-label="Fechar menu">
                    <X size={20} />
                </button>
            </div>

            <p className={styles.label}>FREQUÊNCIA</p>
            <NavLink to="/classrooms" className={linkClass} onClick={onClose}>
                <GraduationCap size={20} /> Turmas
            </NavLink>

            <p className={styles.label}>ALIMENTAÇÃO</p>
            <NavLink to="/home" className={linkClass} onClick={onClose}>
                <UtensilsCrossed size={20} /> Controle de refeições
            </NavLink>
            <NavLink to="/weeklyMenu" className={linkClass} onClick={onClose}>
                <CalendarDays size={20} /> Cardápio semanal
            </NavLink>
        </aside>
    );
}