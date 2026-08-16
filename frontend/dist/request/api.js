import axios from 'https://cdn.jsdelivr.net/npm/axios/+esm';

import { API_BASE_URL } from '../config.js';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getStudentList = async () => {
  try {
    const response = await api.get('/academic/students/list/active');
    return response.data;
  } catch (error) {
    console.error('Error fetching student list:', error);
    throw error;
  }
};
