import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import EstoquePage from './pages/EstoquePage';
import RegistrarVendaPage from './pages/RegistrarVendaPage';
import AtividadesPage from './pages/AtividadesPage';
import DiarioBordoPage from './pages/DiarioBordoPage';
import RPDPage from './pages/RPDPage';
import LogPODDiarioPage from './pages/LogPODDiarioPage';
import Estrutura from './components/Estrutura';

const PrivateRoute = ({ children }) => {
  const { user } = useAuth();
  return user ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <AuthProvider>
      <Estrutura>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          
          {/* Default route redirects to /gestao */}
          <Route 
            path="/" 
            element={
              <PrivateRoute>
                <Navigate to="/gestao" />
              </PrivateRoute>
            } 
          />

          {/* Gestão Routes */}
          <Route 
            path="/gestao" 
            element={
              <PrivateRoute>
                <DashboardPage />
              </PrivateRoute>
            } 
          />
          <Route 
            path="/gestao/estoque" 
            element={
              <PrivateRoute>
                <EstoquePage />
              </PrivateRoute>
            } 
          />
          <Route 
            path="/gestao/vendas/registrar" 
            element={
              <PrivateRoute>
                <RegistrarVendaPage />
              </PrivateRoute>
            } 
          />

          {/* RPD Routes */}
          <Route 
            path="/rpd" 
            element={
              <PrivateRoute>
                <DashboardPage />
              </PrivateRoute>
            } 
          />
          <Route 
            path="/rpd/atividades" 
            element={
              <PrivateRoute>
                <AtividadesPage />
              </PrivateRoute>
            } 
          />
          <Route 
            path="/rpd/diario_bordo" 
            element={
              <PrivateRoute>
                <DiarioBordoPage />
              </PrivateRoute>
            } 
          />
          <Route 
            path="/rpd/rpd" 
            element={
              <PrivateRoute>
                <RPDPage />
              </PrivateRoute>
            } 
          />
          <Route 
            path="/rpd/log_pod_diario" 
            element={
              <PrivateRoute>
                <LogPODDiarioPage />
              </PrivateRoute>
            } 
          />
        </Routes>
      </Estrutura>
    </AuthProvider>
  );
}

export default App;
