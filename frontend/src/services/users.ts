import { api } from "./api";

export interface User {
    id?: string;
    school_id: string;
    role: 'PENDING' | 'DIRECTION' | 'COORDINATOR' | 'MONITOR' | 'CANTEEN';
    name: string;
    email: string;
    password: string;
}

export interface newUser extends User {
    id?: string;
}

export interface updateUser {
    name?: string;
    email?: string;
    password?: string;
    phone?: string;
    typeUser?: 'PENDING' | 'DIRECTION' | 'COORDINATOR' | 'MONITOR' | 'CANTEEN';
}

export interface loginUser {
    email: string;
    password: string;
}

export interface tokenService {
    access_token: string;
    refresh_token: string;
}

export const usersServices = {
    create: async (newUser: newUser): Promise<User> => {
        const { data } = await api.post('/school/manager/', newUser);
        return data;
    },
    getUserByID: async (id: string): Promise<User> => {
        const { data } = await api.get(`/school/manager/${id}`);
        return data;
    },
    login: async (loginData: loginUser): Promise<tokenService> => {
        const { data } = await api.post('/auth/', loginData);
        return data;
    }
}
