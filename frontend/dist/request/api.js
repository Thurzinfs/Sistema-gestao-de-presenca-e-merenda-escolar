import axios from 'https://cdn.jsdelivr.net/npm/axios/+esm';

import API_BASE_URL from '../config.js';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');

  if (token) {
    config.headers.set('Authorization', `Bearer ${token}`)
  }
  return config
})


export const getStudentById = async (id) => {
  try {
    const response = await api.get(`/api/v1/academic/students/${id}`);
    return response.data;
  } catch (error) {
    console.error('Error: ', error);
    throw error;
  }
}

export const getStudentList = async () => {
  try {
    const response = await api.get('/api/v1/academic/students/list/all');
    return response.data;
  } catch (error) {
    console.error('Error: ', error);
    throw error;
  }
};

export const getClassroom = async (id) => {
  try {
    const response = await api.get(`/api/v1/academic/classroom/${id}`);
    return response.data;
  } catch (error) {
    console.error('Error: ', error);
    throw error;
  }
}

export const getSnackRegisters = async () => {
  try {
    const response = await api.get(`/api/v1/presence/registerSnack/`)
    return response.data;
  } catch (error) {
    console.error('Error: ', error);
    throw error;
  }
}

export const getAllSnacksByType = async (type) => {
  try {
     const response = await api.get(`/api/v1/presence/registerSnack/type/${type}`)
    return response.data;
  } catch (error) {
    console.error('Error: ', error);
    throw error;
  }
}

export const getPresenceFrequency = async () => {
  try {
    const response = await api.get(`/api/v1/presence/frequency/`)
    return response.data;
  } catch (error) {
    console.error('Error: ', error);
    throw error;
  }
}

export const registerUSer = async (data) => {
  try {
    const response = await api.post(`/api/v1/school/manager/`, data)
    return {dados: response.data, status: response.status};

  } catch (error) {
    console.error('Error: ', error.response.status);
    return {data: null, status: error.status}
  }
}

export const loginUser = async (data) => {
  try {
    const response = await api.post('/api/v1/auth/', data);

    if (response.status == 200 || response.status == 201) {
      if (response.data.access_token) {
        localStorage.setItem('access_token', response.data.access_token)
      }

      if (response.data.refresh_token) {
        localStorage.setItem('refresh_token', response.data.refresh_token)
      }

      return true;
    }

  } catch (error) {
    console.log(error);
    console.log(error.status)
  }
}

export const requestMe = async () => {
  try {
    const response = await api.get('/api/v1/auth/me');
    
    if (response.status == 201 || response.status == 200) {
      return response.data;
    }

  } catch (error) {
    console.log(error);
    console.log(error.status)
  }
}

export const getSchool = async (id) => {
  try {
    const response = await api.get(`/api/v1/school/${id}`);

    if (response.status == 201 || response.status == 200) {
      return response.data;
    };
    
  } catch (error) {
    console.log(error);
    console.log(error.status)
  }
}