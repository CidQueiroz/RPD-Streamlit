import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Tenta importar o Streamlit. Se falhar, sabemos que estamos em um script.
IS_STREAMLIT_APP = False
try:
    # Check if streamlit is available and running
    import streamlit.runtime.scriptrunner

    IS_STREAMLIT_APP = True
except ImportError:
    from dotenv import load_dotenv

    load_dotenv()  # Carrega variáveis do arquivo .env


def get_db_engine():
    """Cria uma engine de conexão SQLAlchemy."""
    creds = _get_db_credentials()
    if not all(creds.values()):
        _handle_error("Credenciais do banco de dados não configuradas corretamente.")
        return None
    try:
        db_url = f"mysql+mysqlconnector://{creds['user']}:{creds['password']}@{creds['host']}/{creds['database']}"
        engine = create_engine(db_url)
        return engine
    except Exception as err:
        _handle_error(f"Erro ao criar a engine de conexão com o banco de dados: {err}")
        return None


def _get_db_credentials():
    """Função interna para obter credenciais do Streamlit ou do .env"""

    if IS_STREAMLIT_APP and "connections" in st.secrets:
        creds = st.secrets["connections"]
        return creds

    else:
        from dotenv import load_dotenv

        load_dotenv()
        creds = {
            "host": os.getenv("DB_HOST"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASS"),
            "database": os.getenv("DB_NAME"),
        }
        print(f"Usando .env: {creds}")
        return creds


# New helper function for displaying errors
def _display_error(message):
    """Mostra o erro no Streamlit ou imprime no console."""
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx

        if get_script_run_ctx():
            st.error(message)
        else:
            print(f"ERRO: {message}")
    except (ImportError, AttributeError):
        print(
            f"ERRO: {message}"
        )  # Fallback if Streamlit is not available or context is missing


def _handle_error(message):
    """Mostra o erro no Streamlit ou imprime no console."""
    _display_error(message)  # Now just calls the helper


def fetch_data(query, params=None):
    """Lê dados e retorna uma lista de dicionários."""
    engine = get_db_engine()
    if engine:
        try:
            with engine.connect() as conn:
                result = conn.execute(text(query), params or {})
                return [dict(row) for row in result.mappings()]
        except SQLAlchemyError as err:
            _handle_error(f"Erro ao executar a consulta: {err}")
    return None


def execute_command(query, params=None):
    """Executa comandos (INSERT, UPDATE, DELETE)."""
    engine = get_db_engine()
    if engine:
        conn = None
        conn = engine.connect()
        trans = conn.begin()
        try:
            result = conn.execute(text(query), params or {})
            trans.commit()
            return result.rowcount  # Retorna o número de linhas afetadas
        except SQLAlchemyError as err:
            if conn and trans:
                trans.rollback()
            _handle_error(f"Erro ao executar o comando: {err}")
            return None
        finally:
            if conn:
                conn.close()
    return None


def fetch_data_as_dataframe(query, params=None):
    """Busca dados e retorna um DataFrame do Pandas."""
    engine = get_db_engine()
    if engine:
        try:
            return pd.read_sql(text(query), engine, params=params)
        except SQLAlchemyError as err:
            _handle_error(f"Erro ao buscar dados como DataFrame: {err}")
    return pd.DataFrame()


def get_empresas():
    """Busca todas as empresas para exibição."""
    return fetch_data(
        "SELECT id_empresa, nome_empresa FROM empresas ORDER BY nome_empresa"
    )


def get_empresa_por_nome(nome_empresa):
    """Busca uma empresa pelo nome e retorna seus dados."""
    return fetch_data(
        "SELECT id_empresa FROM empresas WHERE nome_empresa = :nome",
        {"nome": nome_empresa},
    )


# Funções de debug permanecem as mesmas...
