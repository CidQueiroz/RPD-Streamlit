import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

const RPDPage = () => {
  const { authTokens, logout } = useAuth();
  const [rpdEntries, setRpdEntries] = useState([]);
  const [formData, setFormData] = useState({
    data: new Date().toISOString().slice(0, 10),
    situacao: '',
    pensamento_automatico: '',
    emocao: '',
    resposta_adaptativa: '',
    resultado: '',
  });
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
    fetchRpdEntries();
  }, []);

  const fetchRpdEntries = async () => {
    try {
      const response = await api.get('/rpd/');
      setRpdEntries(response.data);
    } catch (error) {
      console.error("Erro ao buscar entradas de RPD:", error);
      if (error.response && error.response.status === 401) {
        logout();
      }
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    setMessageType('');
    try {
      await api.post('/rpd/', {
        ...formData,
        data: `${formData.data}T00:00:00Z`,
      });
      setFormData({
        data: new Date().toISOString().slice(0, 10),
        situacao: '',
        pensamento_automatico: '',
        emocao: '',
        resposta_adaptativa: '',
        resultado: '',
      });
      fetchRpdEntries();
      setMessage('Entrada de RPD adicionada com sucesso!');
      setMessageType('success');
    } catch (error) {
      console.error("Erro ao adicionar entrada de RPD:", error);
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
      <h1 className="dashboard-title">Registro de Pensamentos Disfuncionais (RPD)</h1>
      
      <div className="form-container">
        <h2>Adicionar Nova Entrada</h2>
        {message && <p className={`message-${messageType}`}>{message}</p>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="data">Data:</label>
            <input type="date" id="data" name="data" value={formData.data} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label htmlFor="situacao">Situação:</label>
            <textarea id="situacao" name="situacao" value={formData.situacao} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label htmlFor="pensamento_automatico">Pensamento Automático:</label>
            <textarea id="pensamento_automatico" name="pensamento_automatico" value={formData.pensamento_automatico} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label htmlFor="emocao">Emoção:</label>
            <input type="text" id="emocao" name="emocao" value={formData.emocao} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label htmlFor="resposta_adaptativa">Resposta Adaptativa:</label>
            <textarea id="resposta_adaptativa" name="resposta_adaptativa" value={formData.resposta_adaptativa} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label htmlFor="resultado">Resultado:</label>
            <textarea id="resultado" name="resultado" value={formData.resultado} onChange={handleChange} required />
          </div>
          <div className="form-actions">
            <button type="submit" className="btn btn-primario">Salvar Entrada</button>
          </div>
        </form>
      </div>

      <h2 className="dashboard-title">Minhas Entradas</h2>
      {rpdEntries.length === 0 ? (
        <p>Nenhuma entrada de RPD.</p>
      ) : (
        <div className="list-view-container">
          <table className="product-table">
            <thead>
              <tr>
                <th>Data</th>
                <th>Situação</th>
                <th>Pensamento Automático</th>
                <th>Emoção</th>
              </tr>
            </thead>
            <tbody>
              {rpdEntries.map((entry) => (
                <tr key={entry.id}>
                  <td>{new Date(entry.data).toLocaleDateString()}</td>
                  <td>{entry.situacao}</td>
                  <td>{entry.pensamento_automatico}</td>
                  <td>{entry.emocao}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </>
  );
};

export default RPDPage;