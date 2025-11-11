import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api';

const api = axios.create({
  baseURL: API_URL,
});

export const loginUser = async (email, password) => {
  try {
    const response = await api.post('/token/', {
      email,
      password,
    });
    return response.data;
  } catch (error) {
    // Handle or throw error
    console.error("Login failed:", error);
    throw error;
  }
};

export default api;
