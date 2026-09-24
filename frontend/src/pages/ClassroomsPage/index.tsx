import { Utensils } from 'lucide-react';
import { Card } from '../../components/Card';
import { HeaderPage } from '../../components/HeaderPages';
import styles from './index.module.css';
import { SearchArea } from '../../components/SearchArea';
import { useEffect, useState } from 'react';
import { classroomService, type Classroom } from '../../services/classroom';

export function ClassroomsPage() {
    const [search, setSearch] = useState('');
    const [classroomFilter, setFilter] = useState('Todas as salas');

    const [loading, setLoading] = useState(false);

    const [classrooms, setClassrooms] = useState<Classroom[]>([]);

    const requestClassrooms = async () => {
        const response = await classroomService.listActives();

        if (response) {
            setClassrooms(response)
        }
    }

    useEffect(() => {
        setLoading(true);

        try {
            requestClassrooms();

        } catch (error) {
            console.log('Error: ', error)
        } finally {
            setLoading(false)
        }
    }, [])

    return (
        <div className={styles.container}>
            <div className={styles.wrapperContent}>
                <HeaderPage titleWhite='Turmas' titleOrange='2026' subTitle='Painel geral' Icon={Utensils}/>

                <div className={styles.cards}>
                    <Card title='TURMAS' description='' data='0' />
                    <Card title='ALUNOS' description='' data='0' />
                    <Card title='FALTOSOS HOJE' description='' data='0' />
                </div>

                <SearchArea search={search} onChangeSearch={setSearch} filter={classroomFilter} onChangeFilter={setFilter} filters={['3° DS', '3° PJ']}/>

                <div className={styles.labelsContainer}>
                    <div className={styles.labelStudentInfo}>
                        <p>SERIE</p>

                        <p>CURSO</p>
                    </div>

                    <div className={styles.labelFrequency}>
                        <p>FALTOSOS</p>
                        <p>FREQUÊNCIA</p>
                    </div>
                </div>
            </div>
        </div>
    )
}