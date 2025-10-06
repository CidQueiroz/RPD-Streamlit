# rpd.py
import streamlit as st
from core.database import execute_command, fetch_data_as_dataframe

# --- Funções para o RPD (Registro de Pensamento Disfuncionais) ---


def salvar_resposta(
    data_hora, situacao, pensamentos, emocao, conclusao, resultado, usuario_id
):
    resultado = "Retirado"
    """Salva um novo registro de pensamento no banco de dados."""
    sql = """INSERT INTO respostas 
             (data_hora, situacao, pensamento, emocao, conclusao, resultado, usuario_fk) 
             VALUES (:data_hora, :situacao, :pensamento, :emocao, :conclusao, :resultado, :usuario_fk)"""
    params = {
        "data_hora": data_hora,
        "situacao": situacao,
        "pensamento": pensamentos,
        "emocao": emocao,
        "conclusao": conclusao,
        "resultado": resultado,
        "usuario_fk": usuario_id,
    }
    if execute_command(sql, params) is not None:
        st.success("Respostas salvas com sucesso no banco de dados!")
        return True
    return False


def ler_respostas_por_usuario(usuario_id):
    """Lê todos os registros de RPD para um usuário específico."""
    sql = "SELECT data_hora, situacao, pensamento, emocao, conclusao FROM respostas WHERE usuario_fk = :usuario_fk ORDER BY data_hora DESC"
    params = {"usuario_fk": usuario_id}
    return fetch_data_as_dataframe(sql, params)


def ler_todas_as_respostas():
    """Lê todos os registros de RPD de todos os usuários, juntando o nome de usuário."""
    sql = """SELECT r.data_hora, r.situacao, r.pensamento, r.emocao, r.conclusao, u.id_usuario AS username 
             FROM respostas r 
             JOIN usuarios u ON r.usuario_fk = u.id_usuario
             ORDER BY u.id_usuario, r.data_hora DESC"""
    return fetch_data_as_dataframe(sql)
