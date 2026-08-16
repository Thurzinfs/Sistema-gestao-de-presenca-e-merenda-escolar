import axios from 'https://cdn.jsdelivr.net/npm/axios/+esm';

import API_BASE_URL from '../../config.js';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

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
  } catch (eror) {
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
