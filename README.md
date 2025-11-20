<div align="center">

# 📊 Gestão RPD
### Sua Plataforma Integrada de Produtividade e Gestão Pessoal

![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

[**Portfólio CDKTeck**](https://www.cdkteck.com.br) | [**LinkedIn do Autor**](https://www.linkedin.com/in/ciddy-queiroz/)

<br />
</div>

---

## 🚀 Visão Geral

O **Gestão RPD** é uma aplicação web robusta desenvolvida para otimizar a produtividade pessoal e empresarial. A plataforma integra ferramentas essenciais como o Registro de Pensamentos Disfuncionais (RPD) para bem-estar mental, um eficiente sistema de controle de hábitos, e um módulo simplificado para gestão de vendas e estoque, ideal para pequenas e médias empresas.

---

## 🧠 Arquitetura & Tecnologias

Este projeto é construído com uma arquitetura moderna e escalável, focada em performance e manutenibilidade.

| Camada | Tecnologias | Descrição |
| :--- | :--- | :--- |
| **Frontend** | React.js, Vite, Chart.js, Axios | Interface de usuário dinâmica e responsiva para uma experiência fluida. |
| **Backend** | Python, Django REST Framework, djangorestframework-simplejwt, django-cors-headers, gunicorn | API robusta e segura para manipulação de dados e lógica de negócio. |
| **Database** | Oracle, oracledb | Banco de dados relacional para armazenamento seguro e eficiente das informações. |
| **Deployment** | Docker, Firebase | Containerização para ambientes consistentes e hospedagem ágil e escalável. |

---

## ✨ Funcionalidades Chave

- 📝 **Registro de Pensamentos Disfuncionais (RPD):** Ferramenta interativa para auxiliar na identificação e reestruturação cognitiva de pensamentos negativos.
- ✅ **Controle de Hábitos:** Módulo intuitivo para acompanhamento e construção de hábitos diários, com visualização de progresso.
- 📦 **Gestão Simplificada de Vendas e Estoque:** Funcionalidades essenciais para controle de produtos, transações e inventário, ideal para otimização de pequenos negócios.
- 📈 **Dashboard Interativo:** Visualização clara e concisa de dados de produtividade e vendas através de gráficos e relatórios.
- 🧠 **RAG Inteligente:** Sistema de busca semântica com embeddings.
- 🚀 **Groq AI:** Respostas ultra-rápidas com Llama 3.
- 🌐 **Google AI:** Fallback automático com Gemini 1.5.
- 🔐 **Segurança:** Autenticação Firebase + dados protegidos.
- 🐳 **Containerizado:** Ambiente de desenvolvimento e produção 100% em Docker.
- 🤖 **Versionamento Automático:** Releases e changelogs automáticos com semantic-release.

---

## 🛠️ Como Executar Localmente

### Pré-requisitos
* Python 3.10+
* Node.js 18+
* Docker

### 1. Clone o repositório

```bash
git clone https://github.com/CidQueiroz/GestaoRPD.git
cd GestaoRPD
```

### 2. Configuração do Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# .\venv\Scripts\activate # Windows

pip install -r requirements.txt

# Configure as variáveis de ambiente (.env)
# DATABASE_URL=... (Se estiver usando um banco de dados externo)

python manage.py migrate
python manage.py runserver
```

### 3. Configuração do Frontend

```bash
cd ../ # Voltar para a raiz do projeto
npm install
npm run dev
```

A aplicação estará disponível em `http://localhost:3000`.

---

## 🛣️ Roadmap

- [ ] **Integração com Google Sheets:** Sincronização de dados de vendas/estoque com planilhas Google.
- [ ] **Módulo Financeiro:** Adição de controle de despesas e receitas pessoais/empresariais.
- [ ] **Gamificação:** Implementação de elementos de gamificação para o controle de hábitos e RPD.
- [ ] **Deploy Automatizado (CI/CD):** Configuração de GitHub Actions para deploy contínuo na OCI.

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👨‍💻 Autor

<img src="https://github.com/CidQueiroz.png" width="100px;" alt="Foto de Cidirclay"/>
**Cidirclay Queiroz** <br>
Solutions Architect AI | MLOps Engineer | OCI Specialist

[LinkedIn](https://www.linkedin.com/in/ciddy-queiroz/) | [Website](https://cdkteck.com.br/) | [Email](mailto:cydy.queiroz@cdkteck.com.br) | [Instagram](https://www.instagram.com/ciddyqueiroz/)

Especialista em transformar problemas de negócio complexos em soluções escaláveis na nuvem. Focado em Arquitetura Multi-Cloud e Engenharia de IA Generativa.

---

<div align="center"> <sub>Built with ❤️ and paixão</sub> </div>