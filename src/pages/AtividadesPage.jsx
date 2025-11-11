import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

const AtividadesPage = () => {
  const { authTokens, logout } = useAuth();
  const [atividades, setAtividades] = useState([]);
  const [nomeAtividade, setNomeAtividade] = useState('');
  const [periodo, setPeriodo] = useState('manha');
  const [ativa, setAtiva] = useState(true);
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
    fetchAtividades();
  }, []);

  const fetchAtividades = async () => {
    try {
      const response = await api.get('/atividades/');
      setAtividades(response.data);
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
      await api.post('/atividades/', {
        nome_atividade: nomeAtividade,
        periodo,
        ativa,
      });
      setNomeAtividade('');
      setPeriodo('manha');
      setAtiva(true);
      fetchAtividades();
      setMessage('Atividade adicionada com sucesso!');
      setMessageType('success');
    } catch (error) {
      console.error("Erro ao adicionar atividade:", error);
      if (error.response && error.response.status === 401) {
        logout();
      } else {
        setMessage('Erro ao adicionar atividade. Verifique o console.');
        setMessageType('error');
      }
    }
  };

  return (
    <>
      <h1 className="dashboard-title">Gerenciador de Atividades</h1>
      
      <div className="form-container">
        <h2>Adicionar Nova Atividade</h2>
        {message && <p className={`message-${messageType}`}>{message}</p>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="nomeAtividade">Nome da Atividade:</label>
            <input
              type="text"
              id="nomeAtividade"
              value={nomeAtividade}
              onChange={(e) => setNomeAtividade(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="periodo">Período:</label>
            <select id="periodo" value={periodo} onChange={(e) => setPeriodo(e.target.value)}>
              <option value="manha">Manhã</option>
              <option value="tarde">Tarde</option>
              <option value="noite">Noite</option>
            </select>
          </div>
          <div className="form-group">
            <label>
              <input
                type="checkbox"
                checked={ativa}
                onChange={(e) => setAtiva(e.target.checked)}
              />
              Ativa
            </label>
          </div>
          <div className="form-actions">
            <button type="submit" className="btn btn-primario">Salvar Atividade</button>
          </div>
        </form>
      </div>

      <h2 className="dashboard-title">Minhas Atividades</h2>
      {atividades.length === 0 ? (
        <p>Nenhuma atividade cadastrada.</p>
      ) : (
        <div className="list-view-container">
          <table className="product-table">
            <thead>
              <tr>
                <th>Nome</th>
                <th>Período</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {atividades.map((atividade) => (
                <tr key={atividade.id}>
                  <td>{atividade.nome_atividade}</td>
                  <td>{atividade.periodo}</td>
                  <td>{atividade.ativa ? 'Ativa' : 'Inativa'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </>
  );
};

export default AtividadesPage;