import streamlit as st
import pandas as pd
from datetime import datetime
import gspread # Necessário para tratar exceções
from gspread_dataframe import get_as_dataframe
from sheets import salvar_consistencia_sheets, autenticar_gspread, SHEET_NAME 

usuario_login = st.session_state.get('usuario_logado', 'default_user') 

# --- FUNÇÃO DE CARREGAMENTO DE DADOS DO LOG ---
def carregar_log_consistencia_sheets():
    """Carrega o log de consistência (D.Bordo) diretamente do Google Sheets."""
    try:
        client = autenticar_gspread()
        sheet = client.open(SHEET_NAME)
        worksheet = sheet.worksheet("D.Bordo")
        records = worksheet.get_all_records()
        df = pd.DataFrame(records)
        if not df.empty and all(col in df.columns for col in ['Data', 'Atividade', 'Usuario']):
            df = df[['Data', 'Atividade', 'Usuario']]
        else: # Garante que as colunas existam mesmo se a planilha estiver vazia
             return pd.DataFrame(columns=['Data', 'Atividade', 'Usuario'])
        return df
    except gspread.WorksheetNotFound:
        return pd.DataFrame(columns=['Data', 'Atividade', 'Usuario'])
    except Exception as e:
        st.error(f"Falha ao carregar dados do 'D.Bordo'. Erro: {e}")
        return pd.DataFrame(columns=['Data', 'Atividade', 'Usuario'])

# --- NOVAS FUNÇÕES PARA GERENCIAR A LISTA DE ATIVIDADES ---

def carregar_lista_atividades():
    """Carrega a lista de atividades customizadas da aba 'Atividades'."""
    try:
        client = autenticar_gspread()
        sheet = client.open(SHEET_NAME)
        worksheet = sheet.worksheet("Atividades")
        
        # Pega todos os valores da primeira coluna, ignorando o cabeçalho
        lista_atividades = worksheet.col_values(1)[1:]
        return lista_atividades
    
    except gspread.WorksheetNotFound:
        # Se a aba 'Atividades' não existir, retorna uma lista vazia
        return []
    
    except Exception as e:
        st.warning(f"Não foi possível carregar a lista de atividades customizadas. Erro: {e}")
        return []

def salvar_nova_atividade(nova_atividade, lista_existente):
    """Salva uma nova atividade na aba 'Atividades', evitando duplicatas."""
    if nova_atividade in lista_existente:
        st.warning(f"A atividade '{nova_atividade}' já existe!")
        return False
    try:
        client = autenticar_gspread()
        sheet = client.open(SHEET_NAME)
        worksheet = sheet.worksheet("Atividades")
        worksheet.append_row([nova_atividade])
        st.success(f"Nova atividade '{nova_atividade}' adicionada com sucesso!")
        return True
    except Exception as e:
        st.error(f"Falha ao salvar a nova atividade. Erro: {e}")
        return False


# --- FUNÇÃO PRINCIPAL DO MÓDULO ---

def exibir_painel_rebranding():
    
    st.header("Diário de Bordo da Consistência")
    st.markdown("A consistência é a prova da sua nova identidade. Cada marcação é uma vitória contra a inércia.")
    st.caption(f"Operador: {usuario_login} | Data da Operação: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

    # --- CARREGAMENTO INICIAL DOS DADOS ---
    log_consistencia = carregar_log_consistencia_sheets()
    
    # Lista de atividades base (padrão)
    atividades_base = [
        "Curso DBT", "Curso de Liderança", "Curso de RP", "Programação",
        "Leitura", "Assistir Série/Anime", "Atividade Física", "Tarefa Doméstica"
    ]
    # Carrega as atividades salvas na planilha
    atividades_salvas = carregar_lista_atividades()
    # Junta as duas listas e remove duplicatas, garantindo uma lista completa e única
    todas_as_atividades = sorted([str(item) for item in set(atividades_base + atividades_salvas) if item])

    # --- NOVA SESSÃO: GERENCIAR ATIVIDADES ---
    with st.expander("⚙️ Gerenciar Lista de Atividades"):
        st.info("Adicione aqui novas atividades que passarão a aparecer na lista de seleção abaixo.")
        nova_atividade_input = st.text_input("Nome da nova atividade:", key="nova_atividade_input")
        
        if st.button("➕ Adicionar Atividade"):
            if nova_atividade_input:
                if salvar_nova_atividade(nova_atividade_input, todas_as_atividades):
                    # Força o recarregamento do script para que a nova atividade
                    # apareça imediatamente no selectbox
                    st.rerun()
            else:
                st.warning("Por favor, digite o nome da atividade.")
    
    st.divider()

    # --- REGISTRO DA ATIVIDADE CONCLUÍDA ---
    st.subheader("Registrar Nova AMV (Ação Mínima Viável) Concluída")
    
    # O selectbox agora usa a lista dinâmica 'todas_as_atividades'
    atividade_selecionada = st.selectbox(
        "Selecione a atividade concluída hoje:",
        todas_as_atividades,
        index=None, # Deixa o campo sem nenhuma opção pré-selecionada
        placeholder="Escolha uma atividade..."
    )

    if st.button("✅ Registrar Vitória na Nuvem!"):
        if atividade_selecionada:
            hoje_str = datetime.now().strftime('%Y-%m-%d')
            salvar_consistencia_sheets(hoje_str, atividade_selecionada, usuario_login)
            st.success(f"Vitória registrada! AMV '{atividade_selecionada}' de hoje computada no Google Sheets.")
            st.balloons()
            st.rerun()
        else:
            st.error("Por favor, selecione uma atividade antes de registrar.")


    st.divider()

    # --- VISUALIZAÇÃO DOS DADOS ---
    st.subheader("Painel de Controle da Consistência")
    if not log_consistencia.empty:
        st.markdown("#### Frequência de Ações por Atividade:")
        contagem_atividades = log_consistencia['Atividade'].value_counts()
        st.bar_chart(contagem_atividades)

        st.markdown("#### Histórico de Batalhas Vencidas:")
        # Garante que a coluna 'Data' seja tratada como texto para ordenação correta
        log_consistencia['Data'] = log_consistencia['Data'].astype(str)
        st.dataframe(log_consistencia.sort_values(by="Data", ascending=False), use_container_width=True)
    else:
        st.info("Nenhuma ação registrada na nuvem. A primeira vitória inicia a corrente.")