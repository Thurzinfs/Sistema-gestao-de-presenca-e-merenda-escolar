import styles from './buttonSend.module.css';

interface ButtonProps {
    text: string;
    isLoading?: boolean;
    type: 'reset' | 'submit' | 'button';
}

export function ButtonSend({ text, isLoading, type }: ButtonProps) {
    return <button 
        className={styles.button}
        type={type}
        disabled={isLoading}
        >
            {text}
        </button>
}
