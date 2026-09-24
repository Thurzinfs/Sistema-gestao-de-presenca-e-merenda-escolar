import { useEffect, useState } from 'react';
import { Outlet } from 'react-router-dom';
import { Menu } from 'lucide-react';
import { Sidebar } from '../Sidebar';
import styles from './index.module.css';

export function AppLayout() {
    const [open, setOpen] = useState(false);

    useEffect(() => {
        const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') setOpen(false); };
        window.addEventListener('keydown', onKey);
        return () => window.removeEventListener('keydown', onKey);
    }, []);

    useEffect(() => {
        document.body.style.overflow = open ? 'hidden' : '';
        return () => { document.body.style.overflow = ''; };
    }, [open]);

    return (
        <div className={styles.container}>
            <Sidebar open={open} onClose={() => setOpen(false)} />

            {open && <div className={styles.scrim} onClick={() => setOpen(false)} />}

            <main className={styles.main}>
                <header className={styles.topbar}>
                    <button
                        type="button"
                        className={styles.menuBtn}
                        onClick={() => setOpen(true)}
                        aria-label="Abrir menu"
                        aria-expanded={open}
                    >
                        <Menu size={22} />
                    </button>
                </header>

                <Outlet />
            </main>
        </div>
    );
}