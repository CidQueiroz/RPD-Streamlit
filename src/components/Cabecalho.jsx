import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import ThemeToggle from './ThemeToggle';

const Cabecalho = ({ title, onContactClick }) => { // Add onContactClick prop
  const [dropdownOpen, setDropdownOpen] = useState(false);

  const toggleDropdown = () => {
    setDropdownOpen(!dropdownOpen);
  };

  return (
    <header className="cabecalho">
      <Link to="/" className="cabecalho-logo">
        <img id="header-logo" src="/assets/favicon2.png" alt="Logo CDK TECK" />
        <span>{title}</span>
      </Link>

      <nav className="main-nav">
        <div className="dropdown">
          <button className="dropdown-toggle" onClick={toggleDropdown}>
            Universo CDK ▼
          </button>
          {dropdownOpen && (
            <div className="dropdown-menu">
              <Link to="/">Página Inicial</Link>
              <a href="/PBI/portfolio_pbi.html">Portfólio de Dashboards</a>
              <a href="https://sensei.cdkteck.com.br" target="_blank" rel="noopener noreferrer">SenseiDB</a>
              <a href="https://gestao.cdkteck.com.br" target="_blank" rel="noopener noreferrer">Gestão RPD</a>
              <a href="/Portfolio_html/labs.html">Laboratório de Projetos</a>
              <a href="/caca_preco/caca_preco.html">Caça-Preço</a>
              <a href="/Portfolio_html/AdivinhaNumero/adivinha_numero.html">AdivinhaNumero</a>
              <a href="/Portfolio_html/geocoding/geocoding.html">Geocodificação</a>
              <a href="/Portfolio_html/unicornio/unicorn.html">Unicórnio</a>
            </div>
          )}
        </div>
        
        <ThemeToggle />
        
        <a href="#" onClick={onContactClick}>Contato</a> {/* Re-add Contact link with onClick */}
      </nav>
    </header>
  );
};

export default Cabecalho;