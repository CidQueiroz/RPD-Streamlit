# Módulo de Controle Operacional e Pessoal 🚀

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas">
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly">
</p>

<p align="center">
  Um aplicativo web multifuncional que combina ferramentas de desenvolvimento pessoal com um sistema de gestão simplificado.
</p>

---

## 🎯 Funcionalidades Principais

O projeto se divide em duas grandes áreas:

### 🧠 Desenvolvimento Pessoal
*   **Registro de Pensamentos Disfuncionais (RPD):** Uma ferramenta baseada em terapia para ajudar o usuário a mapear e reestruturar pensamentos automáticos.
*   **Protocolo de Operações Diárias (POD):** Um sistema de checklist para acompanhar a execução de hábitos e rotinas diárias, com visualização de progresso.
*   **AMV Tracker (Ação Mínima Viável):** Um diário para registrar pequenas vitórias e construir consistência em novas habilidades ou atividades.

### 📈 Gestão e Vendas
*   **Controle de Estoque:** Adicione, atualize e visualize o inventário de produtos em tempo real.
*   **Registro de Vendas:** Registre transações de forma simples e rápida, atualizando o estoque automaticamente.
*   **Relatório de Vendas:** Visualize um dashboard com o total de vendas, comissões e um alerta para itens com baixo estoque.

---

## 🛠️ Tecnologias Utilizadas

Este projeto foi construído com as seguintes tecnologias:

| Tecnologia | Badge |
| :--- | :--- |
| **Linguagem** | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) |
| **Framework Web** | ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white) |
| **Banco de Dados** | ![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white) |
| **Manipulação de Dados** | ![Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white) |
| **Visualização de Dados** | ![Plotly](https.img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white) |
| **Autenticação** | ![streamlit-authenticator](https://img.shields.io/badge/streamlit--authenticator-FF4B4B?style=for-the-badge) |

---

## 🚀 Como Executar a Aplicação

Siga os passos abaixo para rodar o projeto em sua máquina local:

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio
    ```

2.  **Instale as dependências:** 📦
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure as variáveis de ambiente:** 🔑
    Crie um arquivo `.env` na raiz do projeto e preencha com as credenciais do seu banco de dados MySQL:
    ```env
    DB_HOST=seu_host
    DB_USER=seu_usuario
    DB_PASS=sua_senha
    DB_NAME=seu_banco_de_dados
    ```

4.  **Execute a aplicação:** ▶️
    ```bash
    streamlit run app.py
    ```
    Acesse `http://localhost:8501` no seu navegador.

---

## 📂 Estrutura do Projeto

<details>
  <summary>Clique para expandir e ver a estrutura de arquivos</summary>

  '''
  .
  ├── app.py                # Ponto de entrada principal da aplicação
  ├── auth.py               # Módulo de autenticação de usuários
  ├── database.py           # Camada de acesso ao banco de dados (MySQL)
  ├── estoque.py            # Lógica de negócio para estoque e vendas
  ├── protocolo_diario.py   # Lógica do módulo "Protocolo Diário (POD)"
  ├── rebranding.py         # Lógica do módulo "AMV Tracker"
  ├── rpd.py                # Lógica do módulo "Registro de Pensamentos"
  ├── requirements.txt      # Lista de dependências do projeto
  └── .env.example          # Exemplo de arquivo de variáveis de ambiente
  '''
</details>

---

## 👨‍💻 Autor

Feito com ❤️ por **Cido**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/seu-linkedin/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/seu-github/)
[![Portfolio](https://img.shields.io/badge/Portfolio-000000?style=for-the-badge&logo=About.me&logoColor=white)](https://www.cdkteck.com.br)
