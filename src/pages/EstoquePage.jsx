import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const EstoquePage = () => {
  const { authTokens, logout } = useAuth();
  const [estoque, setEstoque] = useState([]);
  const [item, setItem] = useState('');
  const [variacao, setVariacao] = useState('');
  const [quantidade, setQuantidade] = useState('');
  const [preco, setPreco] = useState('');
  const navigate = useNavigate();

  const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${authTokens?.access}`,
    },
  });

  useEffect(() => {
    fetchEstoque();
  }, []);

  const fetchEstoque = async () => {
    try {
      const response = await api.get('/estoque/');
      setEstoque(response.data);
    } catch (error) {
      console.error("Erro ao buscar estoque:", error);
      if (error.response && error.response.status === 401) {
        logout(); // Token expirado ou inválido
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/estoque/', {
        item,
        variacao,
        quantidade: parseInt(quantidade),
        preco: parseFloat(preco),
      });
      setItem('');
      setVariacao('');
      setQuantidade('');
      setPreco('');
      fetchEstoque(); // Recarrega a lista de estoque
    } catch (error) {
      console.error("Erro ao adicionar item:", error);
      if (error.response && error.response.status === 401) {
        logout();
      }
    }
  };

  return (
    <>
      <h1 className="dashboard-title">Controle de Estoque</h1>

      <div className="form-container">
        <h2>Adicionar/Atualizar Item</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="item">Item:</label>
            <input type="text" id="item" value={item} onChange={(e) => setItem(e.target.value)} required />
          </div>
          <div className="form-group">
            <label htmlFor="variacao">Variação:</label>
            <input type="text" id="variacao" value={variacao} onChange={(e) => setVariacao(e.target.value)} />
          </div>
          <div className="form-group">
            <label htmlFor="quantidade">Quantidade:</label>
            <input type="number" id="quantidade" value={quantidade} onChange={(e) => setQuantidade(e.target.value)} required />
          </div>
          <div className="form-group">
            <label htmlFor="preco">Preço:</label>
            <input type="number" step="0.01" id="preco" value={preco} onChange={(e) => setPreco(e.target.value)} required />
          </div>
          <div className="form-actions">
            <button type="submit" className="btn btn-primario">Salvar Item</button>
          </div>
        </form>
      </div>

      <h2 className="dashboard-title">Estoque Atual</h2>
      {estoque.length === 0 ? (
        <p>Nenhum item em estoque.</p>
      ) : (
        <div className="list-view-container">
          <table className="product-table">
            <thead>
              <tr>
                <th>Item</th>
                <th>Variação</th>
                <th>Quantidade</th>
                <th>Preço</th>
                <th>Última Atualização</th>
              </tr>
            </thead>
            <tbody>
              {estoque.map((estoqueItem) => (
                <tr key={estoqueItem.id}>
                  <td>{estoqueItem.item}</td>
                  <td>{estoqueItem.variacao}</td>
                  <td>{estoqueItem.quantidade}</td>
                  <td>R$ {parseFloat(estoqueItem.preco).toFixed(2)}</td>
                  <td>{new Date(estoqueItem.ultima_atualizacao).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </>
  );
};

export default EstoquePage;