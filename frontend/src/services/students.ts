import { api } from './api';


export interface Student {
    id: string,
    classroom: string,
    name: string,
    ra: string,
    active: boolean,
    qr_code: string,
    created_at: string
}


export const StudentServices = {
    create: async (student: Student): Promise<void> => {
        await api.post('/academic/students/', student);
    },
    getById: async (id: string): Promise<Student> => {
        const response = await api.get(`/academic/students/${id}`);
        return response.data
    },
    listActivesStudents: async (): Promise<Student[]> => {
        const response = await api.get('/academic/students/list/active');
        return response.data;
    },
    listAllStudents: async (): Promise<Student[]> => {
        const response = await api.get('/academic/students/list/all');
        return response.data;
    },
    listByClassroom: async (classroom: string): Promise<Student[]> => {
        const response = await api.get(`/academic/students/list-by-classroom`, {
            params: { classroom }
        });
        return response.data;
    },
    getStudentByQRcode: async (qr: string): Promise<Student> => {
        const response = await api.get(`/academic/students/qr_code/${qr}`);
        return response.data;
    }
}