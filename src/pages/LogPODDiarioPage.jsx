import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

const LogPODDiarioPage = () => {
  const { authTokens, logout } = useAuth();
  const [logEntries, setLogEntries] = useState([]);
  const [atividades, setAtividades] = useState([]);
  const [selectedAtividade, setSelectedAtividade] = useState('');
  const [data, setData] = useState(new Date().toISOString().slice(0, 10));
  const [status, setStatus] = useState(false);
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
    fetchLogEntries();
    fetchAtividades();
  }, []);

  const fetchLogEntries = async () => {
    try {
      const response = await api.get('/log_pod_diario/');
      setLogEntries(response.data);
    } catch (error) {
      console.error("Erro ao buscar logs:", error);
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
      await api.post('/log_pod_diario/', {
        atividade: selectedAtividade,
        data: `${data}T00:00:00Z`,
        status,
      });
      setSelectedAtividade(atividades.length > 0 ? atividades[0].id : '');
      setData(new Date().toISOString().slice(0, 10));
      setStatus(false);
      fetchLogEntries();
      setMessage('Entrada de log adicionada com sucesso!');
      setMessageType('success');
    } catch (error) {
      console.error("Erro ao adicionar entrada de log:", error);
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
      <h1 className="dashboard-title">Log POD Diário</h1>
      
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
          <div className="form-group">
            <label>
              <input
                type="checkbox"
                checked={status}
                onChange={(e) => setStatus(e.target.checked)}
              />
              Status
            </label>
          </div>
          <div className="form-actions">
            <button type="submit" className="btn btn-primario">Salvar Entrada</button>
          </div>
        </form>
      </div>

      <h2 className="dashboard-title">Minhas Entradas</h2>
      {logEntries.length === 0 ? (
        <p>Nenhuma entrada de log.</p>
      ) : (
        <div className="list-view-container">
          <table className="product-table">
            <thead>
              <tr>
                <th>Data</th>
                <th>Atividade</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {logEntries.map((entry) => (
                <tr key={entry.id}>
                  <td>{new Date(entry.data).toLocaleDateString()}</td>
                  <td>{atividades.find(a => a.id === entry.atividade)?.nome_atividade || 'Atividade não encontrada'}</td>
                  <td>{entry.status ? 'Concluído' : 'Pendente'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </>
  );
};

export default LogPODDiarioPage;