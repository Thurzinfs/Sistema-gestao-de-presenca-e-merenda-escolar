import axios from 'axios';
import { tokenService } from './tokenStorage';


export const api = axios.create({
    baseURL: 'http://localhost:8000/api/v1',
    headers: {
        'Content-Type': 'application/json'
    }
});


api.interceptors.request.use((config) => {
    const token = tokenService.getAccessToken();
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }

    return config;
})
