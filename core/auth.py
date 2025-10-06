import streamlit as st
import streamlit_authenticator as stauth
from .database import fetch_data, execute_command


def adicionar_usuario(nome, usuario, senha, id_empresa):
    """
    Adiciona um novo usuário ao banco de dados.
    Retorna True em caso de sucesso, False caso contrário.
    """
    try:
        # Verifica se o nome de usuário já existe
        if fetch_data(
            "SELECT id_usuario FROM usuarios WHERE usuario = :user", {"user": usuario}
        ):
            st.error("Nome de usuário já existente. Por favor, escolha outro.")
            return False

        # Gera o hash da senha
        hashed_password = stauth.Hasher.hash(senha)

        # Define a query de inserção
        query = """INSERT INTO usuarios (nome, usuario, senha, empresa_fk, acesso_dev_pessoal, is_staff)
                   VALUES (:nome, :usuario, :senha, :empresa, :acesso_dev, :is_staff)"""

        params = {
            "nome": nome,
            "usuario": usuario,
            "senha": hashed_password,
            "empresa": id_empresa,
            "acesso_dev": False,  # Default para novos usuários
            "is_staff": 0,  # Default para novos usuários
        }

        # Executa o comando
        rowcount = execute_command(query, params)
        return rowcount > 0

    except Exception as e:
        st.error(f"Ocorreu um erro inesperado ao cadastrar o usuário: {e}")
        return False


def inicializar_autenticador():
    """
    Busca os usuários do banco de dados e inicializa o autenticador do Streamlit.
    """
    try:
        usuarios_do_banco = fetch_data("SELECT nome, usuario, senha FROM usuarios")

        if not usuarios_do_banco:
            st.error("Nenhum usuário encontrado no banco de dados.")
            return None

        credenciais = {
            "usernames": {
                linha_usuario["usuario"]: {
                    "name": linha_usuario["nome"],
                    "password": linha_usuario["senha"],
                }
                for linha_usuario in usuarios_do_banco
            }
        }

        autenticador = stauth.Authenticate(
            credentials=credenciais,
            cookie_name="cookie_rpd_app",
            key="chave_secreta_rpd",
            cookie_expiry_days=30,
        )
        return autenticador

    except Exception as e:
        st.error(f"Erro ao inicializar o sistema de autenticação: {e}")
        return None
