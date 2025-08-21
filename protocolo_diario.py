# MÓDULO DE CONTROLE DE MISSÕES DIÁRIAS
# ARQUIVO: protocolo_diario.py

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import pytz

# Funções impotdascdo arquivo de utilidades do Sheets.
from sheets import carregar_log_diario_sheets, salvar_log_diario_sheets

# --- DEFINIÇÃO DAS TAREFAS DO PROTOCOLO ---
TAREFAS_POD = {
    "Briefing da Manhã": [
        "Ativação: Beber 1 copo d'água cheio ao acordar.",
        "Calibração: Fazer 5 minutos de respiração guiada ",
        "Treinamento Principal: Executar 1 bloco de 25 minutos",
        "Projeto 'Caça-Preço': Executar 1 bloco de 25 minutos de programação (Manhã)"
    ],
    "Execução da Missão": [
        "Logística Escolar: Buscar as gêmeas na escola.",
        " Missão 'Explicador': Dedicar 1 hora de suporte nos estudos/deveres das gêmeas.",
        "Operações Domésticas: Executar 1 tarefa doméstica",
        "Logística Terapêutica: Levar as gêmeas para suas terapias/atividades."
    ],
    "Debriefing Noturno": [
        "Projeto 'Caça-Preço': Executar 1 bloco de 25 minutos de programação (Noite)",
        "Marcar o 'x' no seu 'D.Bordo' para a AMV de estudo que você fez pela manhã.",
        "preencher 1 RPD com a 'Resposta Adaptativa'. Se não houve, pule esta etapa.",
        "Planejamento: Definir qual será a tarefa de estudo de amanhã"
    ]
}

TODAS_TAREFAS = [tarefa for sublista in TAREFAS_POD.values() for tarefa in sublista]

# --- FUNÇÃO PRINCIPAL DO MÓDULO ---
def exibir_protocolo_diario():
    """Renderiza a página do Protocolo de Operações Diárias."""

    st.header("Protocolo de Operações Diárias (POD)")
    st.markdown("A vitória não é ter um dia perfeito. A vitória é completar o ciclo: **Planejar, Tentar, Registrar.**")
    
    log_df = carregar_log_diario_sheets()
    hoje_str = datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%d/%m/%Y  %H:%M:%S")

    # Filtra o log para obter apenas os dados de hoje
    log_hoje = log_df[log_df['Data'] == hoje_str]

    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader(f"Missões para hoje: {log_hoje}")

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
        st.markdown("<h3 style='text-align: center;'>Progresso do Dia</h3>", unsafe_allow_html=True)
        
        percentual_concluido = (tarefas_concluidas_hoje / len(TODAS_TAREFAS)) if TODAS_TAREFAS else 0.0
        
        # Para o gráfico, usamos o valor percentual (ex: 9 para 9%)
        valor_progresso = percentual_concluido * 100

        # 2. Criamos a figura e adicionamos as duas barras (traces)
        fig = go.Figure()

        # BARRA DE FUNDO (A "CAIXA" DE 100%)
        # Esta barra fica atrás, tem valor fixo de 100, preenchimento transparente e um contorno cinza.
        
        fig.add_trace(go.Bar(
            y=[100], name='Fundo',
            marker_color='rgba(0,0,0,0)', marker_line_color='gray',
            marker_line_width=1.5, hoverinfo='none'
        ))

        # BARRA DE PROGRESSO REAL
        # Esta é a barra que mostra o progresso atual. Ela não precisa de contorno.
        fig.add_trace(go.Bar(
            y=[valor_progresso],
            name='Progresso',
            texttemplate='%{y:.0f}%',
            textposition='inside',
            marker_color='#0068C9',        # Cor da barra de progresso
            hoverinfo='none'
        ))

        # 3. CONFIGURAR O LAYOUT FINAL
        # O 'barmode='overlay'' é a chave para colocar uma barra sobre a outra
        fig.update_layout(
            barmode='overlay',
            yaxis_range=[0, 100],
            xaxis_title="",
            xaxis_showticklabels=False,
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            height=500,
            showlegend=False  # Esconde a legenda
        )
        
        fig.update_yaxes( showgrid=False,showticklabels=False)

        # 4. Renderiza o gráfico customizado
        st.plotly_chart(fig, align="right", use_container_width=True, config={'displayModeBar': False})

        _, mid_col, _ = st.columns([1, 3, 1])
        with mid_col:
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
