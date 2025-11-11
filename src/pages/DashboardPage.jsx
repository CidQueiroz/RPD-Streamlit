import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const DashboardPage = () => {
  const { logout } = useAuth();
  const location = useLocation();
  const isGestao = location.pathname.startsWith('/gestao');

  const gestaoLinks = (
    <>
      <div className="card">
        <h2 className="card-title">Controle de Estoque</h2>
        <p className="card-text">Gerencie seus produtos e inventário.</p>
        <Link to="/gestao/estoque" className="btn btn-primario">Acessar Estoque</Link>
      </div>

      <div className="card">
        <h2 className="card-title">Registrar Venda</h2>
        <p className="card-text">Registre suas vendas de forma rápida e fácil.</p>
        <Link to="/gestao/vendas/registrar" className="btn btn-primario">Nova Venda</Link>
      </div>
    </>
  );

  const rpdLinks = (
    <>
      <div className="card">
        <h2 className="card-title">Gerenciar Atividades</h2>
        <p className="card-text">Organize suas tarefas e projetos.</p>
        <Link to="/rpd/atividades" className="btn btn-primario">Minhas Atividades</Link>
      </div>

      <div className="card">
        <h2 className="card-title">Diário de Bordo</h2>
        <p className="card-text">Registre seus pensamentos e experiências diárias.</p>
        <Link to="/rpd/diario_bordo" className="btn btn-primario">Abrir Diário</Link>
      </div>

      <div className="card">
        <h2 className="card-title">Registro de Pensamentos Disfuncionais (RPD)</h2>
        <p className="card-text">Identifique e reestruture pensamentos negativos.</p>
        <Link to="/rpd/rpd" className="btn btn-primario">Iniciar RPD</Link>
      </div>

      <div className="card">
        <h2 className="card-title">Log POD Diário</h2>
        <p className="card-text">Acompanhe seu progresso diário.</p>
        <Link to="/rpd/log_pod_diario" className="btn btn-primario">Ver Log</Link>
      </div>
    </>
  );

  return (
    <>
      <h1 className="dashboard-title">Dashboard</h1>
      <div className="saas-cta-buttons">
        <Link to="/gestao" className={`btn ${isGestao ? 'btn-primario' : 'btn-secundario'}`}>Gestão</Link>
        <Link to="/rpd" className={`btn ${!isGestao ? 'btn-primario' : 'btn-secundario'}`}>RPD</Link>
      </div>
      <div className="card-grid">
        {isGestao ? gestaoLinks : rpdLinks}
      </div>
      <button onClick={logout} className="btn btn-perigo">Sair</button>
    </>
  );
};

export default DashboardPage;
