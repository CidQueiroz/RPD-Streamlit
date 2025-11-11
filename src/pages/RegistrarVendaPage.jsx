import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const RegistrarVendaPage = () => {
  const { authTokens, logout } = useAuth();
  const [estoqueItems, setEstoqueItems] = useState([]);
  const [selectedItem, setSelectedItem] = useState('');
  const [quantidadeVendida, setQuantidadeVendida] = useState('');
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState(''); // 'success' or 'error'
  const navigate = useNavigate();

  const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${authTokens?.access}`,
    },
  });

  useEffect(() => {
    fetchEstoqueItems();
  }, []);

  const fetchEstoqueItems = async () => {
    try {
      const response = await api.get('/estoque/');
      setEstoqueItems(response.data);
    } catch (error) {
      console.error("Erro ao buscar itens de estoque:", error);
      if (error.response && error.response.status === 401) {
        logout();
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    setMessageType('');

    if (!selectedItem || !quantidadeVendida) {
      setMessage('Por favor, selecione um item e insira a quantidade.');
      setMessageType('error');
      return;
    }

    const itemData = estoqueItems.find(item => item.id === parseInt(selectedItem));
    if (!itemData) {
      setMessage('Item selecionado inválido.');
      setMessageType('error');
      return;
    }

    if (quantidadeVendida > itemData.quantidade) {
      setMessage(`Quantidade insuficiente em estoque. Disponível: ${itemData.quantidade}`);
      setMessageType('error');
      return;
    }

    try {
      await api.post('/vendas/', {
        estoque_item: itemData.id,
        quantidade: parseInt(quantidadeVendida),
      });
      setMessage('Venda registrada com sucesso!');
      setMessageType('success');
      setSelectedItem('');
      setQuantidadeVendida('');
      fetchEstoqueItems(); // Atualiza a lista de estoque após a venda
    } catch (error) {
      console.error("Erro ao registrar venda:", error);
      if (error.response && error.response.status === 401) {
        logout();
      } else if (error.response && error.response.data && error.response.data.detail) {
        setMessage(`Erro: ${error.response.data.detail}`);
        setMessageType('error');
      } else if (error.response && error.response.data && error.response.data.non_field_errors) {
        setMessage(`Erro: ${error.response.data.non_field_errors.join(', ')}`);
        setMessageType('error');
      } else {
        setMessage('Erro ao registrar venda. Verifique o console.');
        setMessageType('error');
      }
    }
  };

  return (
    <>
      <h1 className="dashboard-title">Registrar Venda</h1>

      <div className="form-container">
        <h2>Nova Venda</h2>
        {message && <p className={`message-${messageType}`}>{message}</p>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="itemEstoque">Item de Estoque:</label>
            <select
              id="itemEstoque"
              value={selectedItem}
              onChange={(e) => setSelectedItem(e.target.value)}
              required
            >
              <option value="">Selecione um item</option>
              {estoqueItems.map((item) => (
                <option key={item.id} value={item.id}>
                  {item.item} ({item.variacao}) - Estoque: {item.quantidade} - R$ {parseFloat(item.preco).toFixed(2)}
                </option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label htmlFor="quantidadeVendida">Quantidade Vendida:</label>
            <input
              type="number"
              id="quantidadeVendida"
              value={quantidadeVendida}
              onChange={(e) => setQuantidadeVendida(e.target.value)}
              min="1"
              required
            />
          </div>
          <div className="form-actions">
            <button type="submit" className="btn btn-primario">Registrar Venda</button>
          </div>
        </form>
      </div>
    </>
  );
};

export default RegistrarVendaPage;