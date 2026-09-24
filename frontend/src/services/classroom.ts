import { api } from './api';


export interface Classroom {
    id?: string,
    school: string,
    name: string,
    active: boolean,
    created_at: string
}

export const classroomService = {
    create: async (data: Classroom): Promise<void> => {
        await api.post('/academic/classroom/', data);
    },
    getById: async (id: string): Promise<Classroom> => {
        const response = await api.get(`/academic/classroom/${id}`);
        return response.data;
    },
    listActives: async (): Promise<Classroom[]> => {
        const response = await api.get('/academic/classroom/list/actives');
        return response.data;
    },
    listAll: async (): Promise<Classroom[]> => {
        const response = await api.get('/academic/classroom/list/all');
        return response.data;
    }
}
