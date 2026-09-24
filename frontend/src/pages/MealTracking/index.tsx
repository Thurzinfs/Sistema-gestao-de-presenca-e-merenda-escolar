import { useEffect, useState } from 'react';
import { Card } from '../../components/Card';
import { HeaderPage } from '../../components/HeaderPages';
import { SearchArea } from '../../components/SearchArea';
import { StudentRow } from '../../components/StudentRow';
import styles from './index.module.css';
import { readingsSnackServices, type readingSnack } from '../../services/readings';
import { StudentServices, type Student } from '../../services/students';
import { classroomService } from '../../services/classroom';
import { GraduationCap } from 'lucide-react';

const ALL_CLASSROOMS = 'Todas as turmas';

const normalize = (text: string) => text.normalize('NFC').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();

export function HomePage() {
    type StudentReading = Student & { classroomName: string, type_snack: string };

    const [registers, setRegisters] = useState<readingSnack[]>([]);
    const [students, setStudents] = useState<StudentReading[]>([]);

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const [search, setSearch] = useState('');
    const [classroomFilter, setClassroomFilter] = useState(ALL_CLASSROOMS);


    const filteredStudents = students.filter((student) => {
        const matchesClassroom = classroomFilter === ALL_CLASSROOMS || student.classroomName === classroomFilter;
        const term = normalize(search);
        const matchesSearch =
            term === '' ||
            [student.name, String(student.ra), student.classroomName]
                .some((field) => normalize(field).includes(term));

        return matchesClassroom && matchesSearch;
    })

    const classroomOptions = [
        ALL_CLASSROOMS,
        ...new Set(students.map((student) => student.classroomName))
    ]

    const handleResponseSubmit = async () => {
        setLoading(true);

        try {
            const response = await readingsSnackServices.getAll();

            if (response) {
                setRegisters(response)
            }

            const studentsIds = [...response.map((students) => students.student)]

            const studentsData = await Promise.all(
                studentsIds.map(async (students) => await StudentServices.getById(students))
            )
            
            const classroomIds = [...studentsData.map((student) => student.classroom)]

            const classroomData = await Promise.all(
                classroomIds.map((classroom) => classroomService.getById(classroom))
            )

            const classroomById = new Map(
                classroomData.map((classroom) => [classroom.id, classroom])
            )

            const readingSnack = new Map(
                response.map((response) => [response.student, response])
            )

            const studentsWithClassroom = studentsData.map((student) => ({
                ...student,
                classroomName: classroomById.get(student.classroom)?.name ?? '-',
                type_snack: readingSnack.get(student.id)?.type_snack ?? '-'
            }))

            setStudents(studentsWithClassroom);
        } catch (error) {
            setError(`Error: ${error}`)
        } finally {
            setLoading(false);
        }
    }

    const lengthLunchStudents = (type: String) => {
        return filteredStudents.filter((student) => student.type_snack == type).length;
    }

    useEffect(() => {
        handleResponseSubmit();
    }, [])

    return (
        <div className={styles.container}>
            <div className={styles.wrapperContent}>
                <HeaderPage titleWhite='CONTROLE DE' titleOrange='REFEIÇÕES' subTitle='Registro diário de lanche e almoço por aluno.' Icon={GraduationCap}/>
                <div className={styles.cards}>
                    <Card title='ALUNOS' data={String(students.length)} description='cadastrados'/>
                    <Card title='FILTRADOS' data={String(filteredStudents.length)} description='exibidos'/>
                    <Card title='ALMOÇARAM' data={String(lengthLunchStudents('NORMAL'))} description='normal'/>
                    <Card title='ALMOÇARAM' data={String(lengthLunchStudents('LITTLE'))} description='pouco'/>
                </div>

                <SearchArea filters={classroomOptions} search={search} onChangeSearch={setSearch} filter={classroomFilter} onChangeFilter={setClassroomFilter}/>
                <div className={styles.labelsContainer}>
                    <div className={styles.labelUserInfo}>
                        <p>ALUNO</p>
                    </div>

                    <div className={styles.labelSnacks}>
                        <p>TURMA</p>
                        <p>ALMOÇO</p>
                    </div>
                </div>
                {
                    loading ? <p className={styles.feedback}>Carregando...</p> 
                    : error ? (
                        <div className={`${styles.feedback} ${styles.feedbackError}`} role="alert">
                            <p>{error}</p>
                            <button className={styles.retryButton} onClick={handleResponseSubmit}>
                                Tentar novamente
                            </button>
                        </div>
                    )
                    : filteredStudents.length == 0 ? (
                        <p className={`${styles.feedback} ${styles.feedbackEmpty}`} role="status">
                            Nenhuma leitura registrada até o momento.
                        </p>
                    ) :
                    filteredStudents.map((option) => (
                        <StudentRow key={option.id} name={option.name} classroom={option.classroomName} ra={option.ra} lunch={option.type_snack} />
                    ))
                }
            </div>
        </div>
    )
}
