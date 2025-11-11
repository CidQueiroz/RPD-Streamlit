import React from 'react';

const ContatoModal = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="modal show">
      <div className="modal-content contact-modal-content">
        <span className="close-button" onClick={onClose}>&times;</span>
        <img src="/assets/foto.jpg" title="Cid Queiroz" className="profile-pic" alt="Cid Queiroz" />
        <h2 id="contact-title">Cidirclay Queiroz</h2>
        <p id="contact-description">Olá! 👋 Sou Cidirclay Queiroz, Arquiteto de Soluções Cloud em formação e Cientista de Dados OCI Certified. Minha especialidade não é apenas programar em Python/Django/React, mas sim transformar desafios de negócio em soluções de infraestrutura e automação. Sou um profissional unicórnio que une a competência técnica (CI/CD, Cloud) à visão estratégica para entregar projetos de alto desempenho e estabilidade. Se você precisa de lógica e resultados, vamos conversar.</p>
        <div className="social-links">
          <a href="https://www.linkedin.com/in/ciddy-queiroz/" target="_blank" rel="noopener noreferrer" className="social-link-item">
            <i className="fab fa-linkedin"></i>
            <span>LinkedIn</span>
          </a>
          <a href="https://github.com/CidQueiroz" target="_blank" rel="noopener noreferrer" className="social-link-item">
            <i className="fab fa-github"></i>
            <span>GitHub</span>
          </a>
          <a href="https://api.whatsapp.com/send?phone=5521971583118" target="_blank" rel="noopener noreferrer" className="social-link-item">
            <i className="fab fa-whatsapp"></i>
            <span>WhatsApp</span>
          </a>
          <a href="https://www.instagram.com/ciddyqueiroz/" target="_blank" rel="noopener noreferrer" className="social-link-item">
            <i className="fab fa-instagram"></i>
            <span>Instagram</span>
          </a>
          <a href="https://www.facebook.com/cyrd.queiroz/" target="_blank" rel="noopener noreferrer" className="social-link-item">
            <i className="fab fa-facebook"></i>
            <span>Facebook</span>
          </a>
          <a href="/components/curriculo.pdf" download className="social-link-item">
            <i className="fas fa-download"></i>
            <span>Currículo</span>
          </a>
        </div>
        <button className="close-modal" onClick={onClose}>Fechar</button>
      </div>
    </div>
  );
};

export default ContatoModal;
