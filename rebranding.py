import streamlit as st
import pandas as pd
from datetime import datetime
import gspread # Necessário para tratar exceções
from gspread_dataframe import get_as_dataframe
from sheets import salvar_consistencia_sheets, autenticar_gspread, SHEET_NAME 

# --- FUNÇÃO DE CARREGAMENTO DE DADOS DO SHEETS ---
def carregar_log_consistencia_sheets():
    """Carrega o log de consistência diretamente do Google Sheets."""
    try:
        client = autenticar_gspread()
        sheet = client.open(SHEET_NAME)
        worksheet = sheet.worksheet("D.Bordo")
        records = worksheet.get_all_records()
        df = pd.DataFrame(records)
        if not df.empty:
            df = df[['Data', 'Atividade', 'Usuario']]
        return df
    except gspread.WorksheetNotFound:
        # Se a aba não existe, retorna um DataFrame vazio
        return pd.DataFrame(columns=['Data', 'Atividade', 'Usuario'])
    except Exception as e:
        st.error(f"Falha ao carregar dados do 'D.Bordo'. Erro: {e}")
        return pd.DataFrame(columns=['Data', 'Atividade', 'Usuario'])


# --- FUNÇÃO PRINCIPAL DO MÓDULO ---

def exibir_painel_rebranding():
    
    st.header("Diário de Bordo da Consistência")
    st.markdown("A consistência é a prova da sua nova identidade. Cada marcação é uma vitória contra a inércia.")
    st.caption(f"Operador: Cid | Data da Operação: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

    # Carregar os dados existentes do Google Sheets
    log_consistencia = carregar_log_consistencia_sheets()

    atividades_comuns = [
        "Curso DBT", "Curso de Liderança", "Curso de RP", "Programação",
        "Leitura", "Assistir Série/Anime", "Atividade Física", "Tarefa Doméstica"
    ]
    
    st.divider()

    st.subheader("Registrar Nova AMV (Ação Mínima Viável) Concluída")
    atividade_selecionada = st.selectbox("Selecione a atividade concluída hoje:", atividades_comuns)
    
    # Assumindo que você tem o login do usuário em st.session_state
    usuario_login = st.session_state.get('usuario_logado', 'default_user') 

    if st.button("✅ Registrar Vitória na Nuvem!"):
        hoje_str = datetime.now().strftime('%Y-%m-%d')
        
        # Chama a nova função para salvar no Google Sheets
        salvar_consistencia_sheets(hoje_str, atividade_selecionada, usuario_login)
        
        st.success(f"Vitória registrada! AMV '{atividade_selecionada}' de hoje computada no Google Sheets.")
        st.balloons()
        # Força o recarregamento dos dados para atualizar a tela imediatamente
        log_consistencia = carregar_log_consistencia_sheets()
        st.rerun()

    st.divider()

    # --- VISUALIZAÇÃO DOS DADOS ---
    st.subheader("Painel de Controle da Consistência")
    if not log_consistencia.empty:
        st.markdown("#### Frequência de Ações por Atividade:")
        contagem_atividades = log_consistencia['Atividade'].value_counts()
        st.bar_chart(contagem_atividades)

        st.markdown("#### Histórico de Batalhas Vencidas:")
        st.dataframe(log_consistencia.reset_index().sort_values(by="Data", ascending=False), use_container_width=True)
    else:
        st.info("Nenhuma ação registrada na nuvem. A primeira vitória inicia a corrente.")