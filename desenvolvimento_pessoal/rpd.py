
# rpd.py
import streamlit as st
import pandas as pd
from core.database import execute_command, fetch_data_as_dataframe, fetch_data

# --- Funções para o RPD (Registro de Pensamento Disfuncionais) ---

def salvar_resposta(data_hora, situacao, pensamentos, emocao, conclusao, resultado, usuario_id):
    resultado = 'Retirado'
    """Salva um novo registro de pensamento no banco de dados."""
    sql = """INSERT INTO respostas 
             (data_hora, situacao, pensamento, emocao, conclusao, resultado, usuario_fk) 
             VALUES (:data_hora, :situacao, :pensamento, :emocao, :conclusao, :resultado, :usuario_fk)"""
    params = {"data_hora": data_hora, "situacao": situacao, "pensamento": pensamentos, "emocao": emocao, "conclusao": conclusao, "resultado": resultado, "usuario_fk": usuario_id}
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

# --- Funções para o Protocolo Diário (POD) ---

def carregar_log_diario(usuario_id):
    """Carrega o log de atividades diárias de um usuário."""
    sql = "SELECT data, atividade_fk as atividade, status FROM log_pod_diario WHERE usuario_fk = :usuario_fk"
    params = {"usuario_fk": usuario_id}
    return fetch_data_as_dataframe(sql, params)

def salvar_log_diario(log_df, usuario_id):
    """Salva o DataFrame de log diário para um usuário, limpando os registros do dia antes de inserir."""
    if log_df.empty:
        return True
    hoje_str = log_df['data'].iloc[0]
    sql_delete = "DELETE FROM log_pod_diario WHERE usuario_fk = :usuario_fk AND data = :data"
    params_delete = {"usuario_fk": usuario_id, "data": hoje_str}
    
    if execute_command(sql_delete, params_delete) is None:
        return False # Falhou ao deletar

    for _, row in log_df.iterrows():
        sql_insert = "INSERT INTO log_pod_diario (data, status, usuario_fk, atividade_fk) VALUES (:data, :status, :usuario_fk, :atividade_fk)"
        params_insert = {"data": row['data'], "status": bool(row['status']), "usuario_fk": usuario_id, "atividade_fk": row['atividade']}
        
        if execute_command(sql_insert, params_insert) is None:
            return False # Falhou ao inserir

    return True

# --- Funções para o AMV Tracker (rebranding) ---

def carregar_lista_atividades(usuario_id: int):
    """Carrega a lista de atividades customizadas de um usuário específico."""
    query = "SELECT id_atividade, nome_atividade FROM atividades WHERE usuario_fk = :usuario_id ORDER BY nome_atividade"
    return fetch_data_as_dataframe(query, {"usuario_id": usuario_id})

def salvar_nova_atividade(nome_atividade: str, usuario_id: int):
    """Salva uma nova atividade para um usuário, evitando duplicatas para o mesmo usuário."""
    check_sql = "SELECT id_atividade FROM atividades WHERE nome_atividade = :nome_atividade AND usuario_fk = :usuario_id"
    check_params = {"nome_atividade": nome_atividade, "usuario_id": usuario_id}
    if fetch_data(check_sql, check_params): 
        st.warning(f"A atividade '{nome_atividade}' já existe!")
        return False
    sql = "INSERT INTO atividades (nome_atividade, usuario_fk) VALUES (:nome_atividade, :usuario_id)"
    params = {"nome_atividade": nome_atividade, "usuario_id": usuario_id}
    if execute_command(sql, params) is not None:
        st.success(f"Nova atividade '{nome_atividade}' adicionada com sucesso!")
        return True
    return False

def carregar_log_consistencia():
    """Carrega o log de consistência (D.Bordo) do banco de dados."""
    sql = """SELECT l.data, a.nome_atividade, u.id_usuario
             FROM log_pod_diario l
             JOIN atividades a ON l.atividade_fk = a.id_atividade
             JOIN usuarios u ON l.usuario_fk = u.id_usuario 
             ORDER BY l.data DESC"""
    return fetch_data_as_dataframe(sql)

def salvar_consistencia(data, atividade_id, usuario_id):
    """Salva um novo registro de consistência no log."""
    sql = "INSERT INTO log_pod_diario (data, status, atividade_fk, usuario_fk) VALUES (:data, '1', :atividade_fk, :usuario_fk)"
    params = {"data": data, "atividade_fk": atividade_id, "usuario_fk": usuario_id}
    if execute_command(sql, params) is not None:
        st.success(f"Vitória registrada! AMV de hoje computada no banco de dados.")
        return True
    return False
