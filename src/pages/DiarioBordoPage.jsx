import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

const DiarioBordoPage = () => {
  const { authTokens, logout } = useAuth();
  const [diarioBordo, setDiarioBordo] = useState([]);
  const [atividades, setAtividades] = useState([]);
  const [selectedAtividade, setSelectedAtividade] = useState('');
  const [data, setData] = useState(new Date().toISOString().slice(0, 10));
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState(''); // 'success' or 'error'

  const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${authTokens?.access}`,
    },
  });

  useEffect(() => {
    fetchDiarioBordo();
    fetchAtividades();
  }, []);

  const fetchDiarioBordo = async () => {
    try {
      const response = await api.get('/diario_bordo/');
      setDiarioBordo(response.data);
    } catch (error) {
      console.error("Erro ao buscar diário de bordo:", error);
      if (error.response && error.response.status === 401) {
        logout();
      }
    }
  };

  const fetchAtividades = async () => {
    try {
      const response = await api.get('/atividades/');
      setAtividades(response.data);
      if (response.data.length > 0) {
        setSelectedAtividade(response.data[0].id);
      }
    } catch (error) {
      console.error("Erro ao buscar atividades:", error);
      if (error.response && error.response.status === 401) {
        logout();
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    setMessageType('');
    try {
      await api.post('/diario_bordo/', {
        atividade: selectedAtividade,
        data: `${data}T00:00:00Z`, // Send in ISO format with time
      });
      setSelectedAtividade(atividades.length > 0 ? atividades[0].id : '');
      setData(new Date().toISOString().slice(0, 10));
      fetchDiarioBordo();
      setMessage('Entrada no diário de bordo adicionada com sucesso!');
      setMessageType('success');
    } catch (error) {
      console.error("Erro ao adicionar entrada no diário de bordo:", error);
      if (error.response && error.response.status === 401) {
        logout();
      } else {
        setMessage('Erro ao adicionar entrada. Verifique o console.');
        setMessageType('error');
      }
    }
  };

  return (
    <>
      <h1 className="dashboard-title">Diário de Bordo</h1>
      
      <div className="form-container">
        <h2>Adicionar Nova Entrada</h2>
        {message && <p className={`message-${messageType}`}>{message}</p>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="atividade">Atividade:</label>
            <select
              id="atividade"
              value={selectedAtividade}
              onChange={(e) => setSelectedAtividade(e.target.value)}
              required
            >
              {atividades.map((atividade) => (
                <option key={atividade.id} value={atividade.id}>
                  {atividade.nome_atividade}
                </option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label htmlFor="data">Data:</label>
            <input
              type="date"
              id="data"
              value={data}
              onChange={(e) => setData(e.target.value)}
              required
            />
          </div>
          <div className="form-actions">
            <button type="submit" className="btn btn-primario">Salvar Entrada</button>
          </div>
        </form>
      </div>

      <h2 className="dashboard-title">Minhas Entradas</h2>
      {diarioBordo.length === 0 ? (
        <p>Nenhuma entrada no diário de bordo.</p>
      ) : (
        <div className="list-view-container">
          <table className="product-table">
            <thead>
              <tr>
                <th>Data</th>
                <th>Atividade</th>
              </tr>
            </thead>
            <tbody>
              {diarioBordo.map((entrada) => (
                <tr key={entrada.id}>
                  <td>{new Date(entrada.data).toLocaleDateString()}</td>
                  <td>{atividades.find(a => a.id === entrada.atividade)?.nome_atividade || 'Atividade não encontrada'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </>
  );
};

export default DiarioBordoPage;