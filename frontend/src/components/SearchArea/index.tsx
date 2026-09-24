import styles from './index.module.css';

interface SearchProps {
    filters: string[],
    search: string,
    onChangeSearch: (value: string) => void,
    filter: string,
    onChangeFilter: (value: string) => void,
}

export function SearchArea({ filters, search, onChangeSearch, filter, onChangeFilter }: SearchProps) {
    return <div className={styles.container}>
        <input 
        className={styles.input} 
        placeholder='Buscar por nome, matricula ou turma...'
        value={search}
        onChange={(e) => onChangeSearch(e.target.value)}
        />

        <select 
        aria-label='Filtrar por turma' 
        value={filter}
        className={styles.filter}
        onChange={(e) => onChangeFilter(e.target.value)}
        >
            {
                filters.map((option) => (
                    <option key={option} value={option}>{option}</option>
                ))
            }
        </select>
    </div>
}