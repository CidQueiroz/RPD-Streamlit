import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import Cabecalho from './Cabecalho';
import Rodape from './Rodape';
import ContatoModal from './ContatoModal'; // Import ContatoModal

const Estrutura = ({ children }) => {
  const location = useLocation();
  const [showContactModal, setShowContactModal] = useState(false); // State for modal visibility

  let title = 'Gestão RPD'; // Default title

  if (location.pathname.startsWith('/gestao')) {
    title = 'Gestão';
  }
  else if (location.pathname.startsWith('/rpd')) {
    title = 'RPD';
  }

  const toggleContactModal = () => {
    setShowContactModal(!showContactModal);
  };

  return (
    <>
      <Cabecalho title={title} onContactClick={toggleContactModal} /> {/* Pass toggle function */}
      <main className="layout-logado-background">
        <div className="layout-logado-content">
          {children}
        </div>
      </main>
      <Rodape />
      <ContatoModal isOpen={showContactModal} onClose={toggleContactModal} /> {/* Render the modal */}
    </>
  );
};

export default Estrutura;
