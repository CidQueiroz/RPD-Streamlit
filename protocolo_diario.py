# MÓDULO DE CONTROLE DE MISSÕES DIÁRIAS
# ARQUIVO: protocolo_diario.py

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px

# --- ATENÇÃO: AJUSTE ESTES IMPORTS ---
# Funções impotdascdo arquivo de utilidades do Sheets.
from sheets import carregar_log_diario_sheets, salvar_log_diario_sheets
# -----------------------------------------

# --- DEFINIÇÃO DAS TAREFAS DO PROTOCOLO ---
TAREFAS_POD = {
    "Briefing da Manhã": [
        "Ativação Física (Água)",
        "Calibração Emocional (DBT - 5 min)",
        "Definição da Missão (1 AMV)",
        "Logística (Medicação)"
    ],
    "Execução da Missão": [
        "Execução da AMV Prioritária",
        "Treinamento de Campo (Prática do PIP)",
        "Ação Mínima Oportunista"
    ],
    "Debriefing Noturno": [
        "Registro no Diário de Bordo (Marcar 'X')",
        "Análise Tática (RPD, se necessário)",
        "Planejamento da Próxima Missão (AMV de amanhã)",
        "Descompressão e Recuperação"
    ]
}

TODAS_TAREFAS = [tarefa for sublista in TAREFAS_POD.values() for tarefa in sublista]

# --- FUNÇÃO PRINCIPAL DO MÓDULO ---
def exibir_protocolo_diario():
    """Renderiza a página do Protocolo de Operações Diárias."""

    st.header("Protocolo de Operações Diárias (POD)")
    st.markdown("A vitória não é ter um dia perfeito. A vitória é completar o ciclo: **Planejar, Tentar, Registrar.**")
    
    log_df = carregar_log_diario_sheets()
    hoje_str = datetime.now().strftime('%Y-%m-%d')

    # Filtra o log para obter apenas os dados de hoje
    log_hoje = log_df[log_df['Data'] == hoje_str]

    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader(f"Missões para hoje: {datetime.now().strftime('%d/%m/%Y')}")

        tarefas_concluidas_hoje = 0
        status_atual_tarefas = {}

        # Itera sobre as tarefas para criar os checkboxes e registrar o estado atual
        for categoria, tarefas in TAREFAS_POD.items():
            st.markdown(f"**{categoria}**")
            for tarefa in tarefas:
                status_inicial = tarefa in log_hoje[log_hoje['Status'] == True]['Tarefa'].values
                novo_status = st.checkbox(tarefa, value=status_inicial, key=f"cb_{tarefa}")
                status_atual_tarefas[tarefa] = novo_status
                if novo_status:
                    tarefas_concluidas_hoje += 1
        
        # --- Lógica de Salvamento ---
        # Cria um DataFrame com o estado atual de todas as tarefas de hoje
        registros_hoje_para_salvar = [{'Data': hoje_str, 'Tarefa': tarefa, 'Status': status} for tarefa, status in status_atual_tarefas.items()]
        df_hoje_atualizado = pd.DataFrame(registros_hoje_para_salvar)

        # Remove qualquer registro antigo de hoje do log principal
        log_df_sem_hoje = log_df[log_df['Data'] != hoje_str]
        
        # Adiciona os registros atualizados de hoje ao log principal
        log_final_para_salvar = pd.concat([log_df_sem_hoje, df_hoje_atualizado], ignore_index=True)
        
        # Salva o estado completo no Google Sheets
        salvar_log_diario_sheets(log_final_para_salvar)

    with col2:
        st.subheader("Progresso do Dia")
        
        percentual_concluido = (tarefas_concluidas_hoje / len(TODAS_TAREFAS)) if TODAS_TAREFAS else 0.0

        progresso_df = pd.DataFrame({'Progresso': [percentual_concluido * 100]})
        fig = px.bar(progresso_df, y='Progresso', orientation='v',
                     height=300) # Define uma altura fixa para a barra
        
        # 2. Customização para criar a "box" e adicionar o rótulo
        fig.update_layout(
            yaxis_range=[0, 100],  # Define o eixo Y de 0 a 100, criando a "box"
            xaxis_title="",        # Remove o título do eixo X
            xaxis_showticklabels=False, # Remove os labels do eixo X
            plot_bgcolor='rgba(0,0,0,0)', # Fundo transparente
            margin=dict(l=10, r=10, t=10, b=10) # Margens pequenas
        )
        
        # 3. Adiciona o rótulo de dados e remove as linhas de grade
        fig.update_traces(
            texttemplate='%{y:.0f}%',      # Formato do texto (número inteiro + %)
            textposition='inside',         # Posição do texto
            marker_color='#0068C9',        # Cor de preenchimento da barra
            marker_line_color='white',     # Cor do contorno da barra
            marker_line_width=2            # Espessura do contorno em pixels
        )

        fig.update_yaxes(
            showgrid=False,      # Remove as linhas de grade do eixo Y
            showticklabels=False # Remove os labels do eixo Y
        )

        # 4. Renderiza o gráfico customizado
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.metric(label="Missão Diária", value=f"{percentual_concluido:.0%}")


    st.divider()

    st.subheader("Análise de Consistência (Últimos 30 Dias Móveis)")

    data_limite = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    log_30_dias = log_df[log_df['Data'] >= data_limite]
    log_concluido_30_dias = log_30_dias[log_30_dias['Status'] == True]

    if not log_concluido_30_dias.empty:
        progresso_diario = log_concluido_30_dias.groupby('Data').size()
        percentual_diario = (progresso_diario / len(TODAS_TAREFAS)) * 100
        
        idx = pd.date_range(end=datetime.now(), periods=30, freq='D').strftime('%Y-%m-%d')
        percentual_diario.index = pd.to_datetime(percentual_diario.index).strftime('%Y-%m-%d')
        percentual_diario = percentual_diario.reindex(idx, fill_value=0)
        
        st.line_chart(percentual_diario)
    else:
        st.info("Ainda não há dados suficientes para exibir o histórico de 30 dias.")
