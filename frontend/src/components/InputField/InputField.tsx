import { useState } from 'react';
import styles from './InputField.module.css';
import { Eye, EyeOff } from 'lucide-react';

interface InputProps {
    label: string;
    placeholder: string;
    name: string;
    type?: string;
    value: string;
    isPassword?: boolean;
    onChange: (value: string) => void;
}

export function InputField({ label, name, placeholder, type, value, isPassword, onChange }: InputProps) {
    const [showPassword, setShowPassword] = useState(false);

    const inputType = isPassword ? (showPassword ? 'text' : 'password') : type;

    return (
        <div className={styles.inputGroup}>
            <label htmlFor={name} className={styles.label}>{label}</label>

            <div className={styles.inputWrapper}>
                <input
                    className={styles.input}
                    id={name}
                    name={name}
                    type={inputType}
                    value={value}
                    placeholder={placeholder}
                    onChange={(e) => onChange(e.target.value)}
                    required
                />
                {isPassword && (
                    <button
                        type='button'
                        onClick={() => setShowPassword(!showPassword)}
                        className={styles.toggleButton}
                    >
                        {showPassword ? <EyeOff size={18} color='#696969'/> : <Eye size={18} color='#696969'/>}
                    </button>
                )}
            </div>
        </div>
    )
}