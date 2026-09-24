import { api } from './api';


export interface readingSnack {
    id?: string;
    student: string;
    date: string;
    type_snack: string;
    reading: string
}

export const readingsSnackServices = {
    create: async (readingSnack: readingSnack): Promise<void> => {
        await api.post('/presence/registerSnack/', readingSnack)
    },
    getAll: async (): Promise<readingSnack[]> => {
        const response = await api.get(`/presence/registerSnack/`)
        return response.data
    },
    getSnackByDate: async (date: string): Promise<readingSnack> => {
        const response = await api.get(`/presence/registerSnack/${date}`)
        return response.data
    },
    getSnackByMoment: async (moment: string): Promise<readingSnack[]> => {
        const response = await api.get(`/presence/registerSnack/moment/${moment}`)
        return response.data
    }
}
