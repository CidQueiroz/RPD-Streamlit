[![Streamlit](https://img.shields.io/badge/streamlit-blue)](https://streamlit.app/)


# Módulo de Controle Operacional

Este projeto é um Módulo de Controle Operacional interativo, desenvolvido em Streamlit, que serve como uma "Caixa de Ferramentas" e "Diário de Bordo" para registrar esforços e fornecer dados para autoanálise. Ele é projetado para ajudar os usuários a monitorar suas "AMVs" (Ações Mínimas Viáveis) e a mapear e desarmar o "Crítico Interno" através do Registro de Pensamentos Disfuncionais (RPD).

## Funcionalidades

*   **Autenticação de Usuário:** Sistema de login seguro para acesso restrito ao aplicativo.
*   **Diário de Bordo da Consistência:** Uma seção dedicada ao registro diário de "vitórias contra a inércia" (AMVs), permitindo o acompanhamento do progresso e da consistência.
*   **Registro de Pensamentos Disfuncionais (RPD):** Uma ferramenta para mapear e desarmar padrões de pensamento negativos, conforme discutido em terapia.
*   **Gestão de Estoque (Potencial):** Embora não totalmente implementado ou detalhado, a presença de `estoque.py` sugere uma funcionalidade futura ou em desenvolvimento para gestão de inventário.
*   **Integração com Google Sheets:** Armazenamento e recuperação de dados de forma persistente através de planilhas Google Sheets, facilitando o acesso e a análise dos registros.
*   **Interface Intuitiva:** Desenvolvido com Streamlit para uma experiência de usuário amigável e interativa.

## Tecnologias Utilizadas

*   **Python:** Linguagem de programação principal.
*   **Streamlit:** Framework para construção de aplicações web interativas.
*   **Streamlit-Authenticator:** Biblioteca para adicionar autenticação a aplicativos Streamlit.
*   **gspread:** Biblioteca Python para interagir com a API do Google Sheets.
*   **pandas:** Biblioteca para manipulação e análise de dados.
*   **openpyxl:** Biblioteca para leitura e escrita de arquivos Excel (utilizada em `rebranding.py`).
*   **oauth2client:** Biblioteca para autenticação OAuth 2.0 com APIs do Google.

## Configuração e Instalação

Para configurar e executar este projeto localmente, siga os passos abaixo:

### Pré-requisitos

*   Python 3.7+
*   Conta Google com acesso à API do Google Sheets.

### 1. Clonar o Repositório

Comece clonando o repositório para sua máquina local. Utilize HTTPS ou SSH, conforme sua preferência:

```bash
# Via HTTPS
git clone https://github.com/seu-usuario/seu-repositorio.git # Substitua pelo link do seu repositório
cd RPD

# Ou via SSH (se você já configurou sua chave SSH com o GitHub)
git clone git@github.com:seu-usuario/seu-repositorio.git # Substitua pelo link do seu repositório
cd RPD
```

Após clonar, você pode verificar o status do seu repositório e os remotes configurados:

```bash
git status
git remote -v
```

Para manter seu repositório local atualizado com as últimas mudanças do `main` (ou `master`), utilize:

```bash
git pull origin main # ou master, dependendo do nome da branch principal
```

### 2. Configurar Credenciais da API do Google Sheets

1.  Vá para o [Google Cloud Console](https://console.cloud.google.com/).
2.  Crie um novo projeto (ou selecione um existente).
3.  Habilite a **Google Sheets API** e a **Google Drive API** para o seu projeto.
4.  Crie credenciais de **Conta de Serviço** (Service Account).
5.  Baixe o arquivo JSON da chave privada. Renomeie-o para `service_account.json` e coloque-o na raiz do seu projeto (`C:\Users\cydyq\Documents\Python\RPD\`).
6.  Compartilhe suas planilhas Google Sheets com o endereço de e-mail da conta de serviço (encontrado no arquivo `service_account.json`).

### 3. Instalar Dependências

Instale todas as dependências do projeto usando `pip`:

```bash
pip install -r requirements.txt
```

### 4. Executar a Aplicação

Inicie a aplicação Streamlit:

```bash
streamlit run app.py
```

O aplicativo será aberto no seu navegador padrão (geralmente em `http://localhost:8501`).

## Uso

Após iniciar a aplicação e fazer login, você encontrará duas abas principais:

*   **Diário de Bordo da Consistência:** Utilize esta aba para registrar suas AMVs diárias. Preencha os campos relevantes e salve seus registros.
*   **Registro de Pensamentos (RPD):** Nesta aba, você poderá registrar e analisar seus pensamentos disfuncionais, seguindo as orientações para desarmá-los.

## Estrutura do Projeto

*   `app.py`: O arquivo principal da aplicação Streamlit, orquestrando as diferentes seções e funcionalidades.
*   `auth.py`: Contém a lógica para autenticação de usuários.
*   `estoque.py`: Módulo para funcionalidades relacionadas à gestão de estoque.
*   `protocolo_diario.py`: Módulo para o registro de protocolos diários e AMVs.
*   `sheets.py`: Funções utilitárias para interação com a API do Google Sheets.
*   `rebranding.py`: Um script auxiliar, possivelmente para processamento de dados ou tarefas de manutenção (requer análise mais aprofundada para uso específico).
*   `requirements.txt`: Lista de todas as dependências do projeto.
*   `RPD.xlsx`: Um arquivo Excel que pode ser usado como modelo ou para armazenamento de dados offline/backup.
*   `respostas_formulario.pdf`: Um exemplo de arquivo PDF, possivelmente relacionado a formulários ou relatórios.

## Fluxo de Trabalho de Desenvolvimento (Git)

Adotamos um fluxo de trabalho baseado em *feature branches* para garantir um desenvolvimento organizado e colaborativo.

### Branches

*   `main` (ou `master`): A branch principal que contém o código de produção estável. Todas as novas funcionalidades e correções de bugs são desenvolvidas em branches separadas e, após revisão, são mescladas aqui.
*   `feature/nome-da-sua-feature`: Para o desenvolvimento de novas funcionalidades.
*   `bugfix/nome-da-correcao`: Para correções de bugs.
*   `hotfix/nome-da-correcao`: Para correções urgentes em produção.

### Commit Messages

Utilizamos o padrão [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) para mensagens de commit, o que facilita a geração de changelogs e a compreensão do histórico do projeto.

Exemplos:

*   `feat: Adiciona nova funcionalidade de autenticação`
*   `fix: Corrige erro de carregamento de dados no RPD`
*   `docs: Atualiza seção de instalação no README`
*   `refactor: Otimiza função de leitura de planilhas`
*   `chore: Atualiza dependências no requirements.txt`

### Processo de Contribuição

1.  **Fork** o repositório para sua conta GitHub.
2.  **Clone** seu fork para sua máquina local.
3.  Crie uma nova **branch** a partir de `main` (ou `master`) para sua funcionalidade ou correção:
    ```bash
    git checkout main
    git pull origin main # Garanta que sua branch main esteja atualizada
    git checkout -b feature/minha-nova-funcionalidade
    ```
4.  Faça suas **alterações** e **commits** seguindo o padrão Conventional Commits.
5.  Antes de abrir o Pull Request, **sincronize** sua branch com a `main` (ou `master`) mais recente. Considere usar `git rebase` para manter um histórico limpo:
    ```bash
    git fetch origin
    git rebase origin/main # ou origin/master
    ```
    *Alternativamente, você pode usar `git merge origin/main` se preferir um histórico de merge.*
6.  **Envie** suas mudanças para o seu fork:
    ```bash
    git push origin feature/minha-nova-funcionalidade
    ```
7.  Abra um **Pull Request (PR)** do seu fork para a branch `main` (ou `master`) do repositório original. Descreva suas mudanças detalhadamente e referencie quaisquer issues relevantes.

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Contato

- [![LinkedIn](https://img.shields.io/badge/LinkedIn-ciddy--queiroz-blue?logo=linkedin)](https://www.linkedin.com/in/ciddy-queiroz/)

- [![Email](https://img.shields.io/badge/Email-cydy.queiroz@gmail.com-red?style=flat-square&logo=gmail&logoColor=white)](mailto:cydy.queiroz@gmail.com)

---

<p align="center">
  <img src="https://img.shields.io/badge/feito%20com-❤%20por%20Ciddy%20Queiroz-blue" alt="Feito com amor por