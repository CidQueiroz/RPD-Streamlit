import React, { createContext, useState, useContext } from 'react';
import { jwtDecode } from 'jwt-decode';
import { loginUser } from '../api';
import { useNavigate } from 'react-router-dom';

const AuthContext = createContext();

export const useAuth = () => {
  return useContext(AuthContext);
};

export const AuthProvider = ({ children }) => {
  const [authTokens, setAuthTokens] = useState(() => localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null);
  const [user, setUser] = useState(() => localStorage.getItem('authTokens') ? jwtDecode(localStorage.getItem('authTokens')) : null);
  const navigate = useNavigate();

  const login = async (email, password) => {
    try {
      const data = await loginUser(email, password);
      if (data) {
        setAuthTokens(data);
        setUser(jwtDecode(data.access));
        localStorage.setItem('authTokens', JSON.stringify(data));
        navigate('/');
      }
    } catch (error) {
      alert('Login failed! Check console for details.');
    }
  };

  const logout = () => {
    setAuthTokens(null);
    setUser(null);
    localStorage.removeItem('authTokens');
    navigate('/login');
  };

  const contextData = {
    user,
    authTokens,
    login,
    logout,
  };

  return (
    <AuthContext.Provider value={contextData}>
      {children}
    </AuthContext.Provider>
  );
};
