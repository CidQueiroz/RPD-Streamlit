import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import pytz
from core.database import fetch_data_as_dataframe, execute_command

# Mapeamento de períodos
PERIODOS = {
    "manha": "Manhã: Briefing da Manhã",
    "tarde": "Tarde: Execução da Missão",
    "noite": "Noite: Debriefing Noturno",
}


def carregar_atividades_por_periodo(usuario_id: int, apenas_ativas=True):
    """Carrega atividades de um usuário, organizadas por período."""
    try:
        query = """
            SELECT id_atividade, nome_atividade, COALESCE(periodo, 'manha') as periodo
            FROM atividades 
            WHERE usuario_fk = :usuario_id
        """
        params = {"usuario_id": usuario_id}

        if apenas_ativas:
            query += " AND ativa = 1"

        query += " ORDER BY periodo, nome_atividade"

        df = fetch_data_as_dataframe(query, params)

        atividades_por_periodo = {periodo: [] for periodo in PERIODOS.keys()}
        for _, row in df.iterrows():
            periodo = row.get("periodo", "manha")
            atividades_por_periodo[periodo].append(
                {"id": row["id_atividade"], "nome": row["nome_atividade"]}
            )
        return atividades_por_periodo

    except Exception as e:
        st.error(f"Erro ao carregar atividades: {e}")
        return {periodo: [] for periodo in PERIODOS.keys()}


def adicionar_nova_atividade(nome_atividade: str, periodo: str, usuario_id: int):
    """Adiciona uma nova atividade para um usuário específico."""
    try:
        query = "INSERT INTO atividades (nome_atividade, periodo, usuario_fk) VALUES (:nome, :periodo, :usuario_id)"
        params = {"nome": nome_atividade, "periodo": periodo, "usuario_id": usuario_id}
        if execute_command(query, params):
            st.success(f"Atividade '{nome_atividade}' adicionada com sucesso!")
            return True
        return False
    except Exception as e:
        st.error(f"Erro ao adicionar atividade: {e}")
        return False


def desativar_atividade(atividade_id: int, usuario_id: int):
    """Marca uma atividade de um usuário como inativa."""
    try:
        query = "UPDATE atividades SET ativa = 0 WHERE id_atividade = :id AND usuario_fk = :uid"
        if execute_command(query, {"id": atividade_id, "uid": usuario_id}):
            st.success("Atividade desativada com sucesso!")
            return True
        return False
    except Exception as e:
        st.error(f"Erro ao desativar atividade: {e}")
        return False


def reativar_atividade(atividade_id: int, usuario_id: int):
    """Marca uma atividade de um usuário como ativa."""
    try:
        query = "UPDATE atividades SET ativa = 1 WHERE id_atividade = :id AND usuario_fk = :uid"
        if execute_command(query, {"id": atividade_id, "uid": usuario_id}):
            st.success("Atividade reativada com sucesso!")
            return True
        return False
    except Exception as e:
        st.error(f"Erro ao reativar atividade: {e}")
        return False


def salvar_log_pod(registros_df, usuario_id):
    """Salva o log do POD na tabela log_pod_diario"""
    try:
        hoje_str = datetime.now(pytz.timezone("America/Sao_Paulo")).strftime("%Y-%m-%d")
        execute_command(
            "DELETE FROM log_pod_diario WHERE DATE(data) = :data AND usuario_fk = :uid",
            {"data": hoje_str, "uid": usuario_id},
        )

        for _, row in registros_df.iterrows():
            data_completa = f"{row['data']} {datetime.now(pytz.timezone('America/Sao_Paulo')).strftime('%H:%M:%S')}"
            execute_command(
                "INSERT INTO log_pod_diario (data, status, usuario_fk, atividade_fk) VALUES (:data, :status, :uid, :aid)",
                {
                    "data": data_completa,
                    "status": 1 if row["status"] else 0,
                    "uid": usuario_id,
                    "aid": row["atividade_id"],
                },
            )
    except Exception as e:
        st.error(f"Erro ao salvar log: {e}")


def carregar_log_diario(usuario_id):
    """Carrega o log do POD da tabela log_pod_diario"""
    try:
        query = """
            SELECT DATE(l.data) as data, a.id_atividade as atividade_id, a.nome_atividade as atividade, l.status
            FROM log_pod_diario l JOIN atividades a ON l.atividade_fk = a.id_atividade
            WHERE l.usuario_fk = :usuario_id AND a.usuario_fk = :usuario_id
            ORDER BY l.data DESC
        """
        df = fetch_data_as_dataframe(query, {"usuario_id": usuario_id})
        if not df.empty:
            df["status"] = df["status"].astype(bool)
            df["data"] = df["data"].astype(str)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar log: {e}")
        return pd.DataFrame(columns=["data", "atividade_id", "atividade", "status"])


def exibir_gerenciamento_atividades(usuario_id: int):
    """Interface para gerenciar atividades de um usuário."""
    st.subheader("Gerenciar Atividades")
    tab1, tab2, tab3 = st.tabs(["Adicionar", "Desativar", "Reativar"])

    with tab1:
        with st.form("adicionar_atividade"):
            nome_atividade = st.text_input("Nome da Atividade")
            periodo = st.selectbox(
                "Período",
                options=list(PERIODOS.keys()),
                format_func=lambda x: PERIODOS[x],
            )
            if st.form_submit_button("Adicionar Atividade") and nome_atividade.strip():
                if adicionar_nova_atividade(
                    nome_atividade.strip(), periodo, usuario_id
                ):
                    st.rerun()

    with tab2:
        atividades_ativas = carregar_atividades_por_periodo(
            usuario_id, apenas_ativas=True
        )
        todas_ativas = [
            ativ
            for periodo_atividades in atividades_ativas.values()
            for ativ in periodo_atividades
        ]
        if todas_ativas:
            opcoes = [f"{ativ['nome']} (ID: {ativ['id']})" for ativ in todas_ativas]
            atividade_selecionada = st.selectbox(
                "Selecione a atividade para desativar", opcoes, key="desativar_select"
            )
            if st.button("Desativar Atividade"):
                atividade_id = int(atividade_selecionada.split("(ID: ")[-1][:-1])
                if desativar_atividade(atividade_id, usuario_id):
                    st.rerun()
        else:
            st.info("Nenhuma atividade ativa para desativar.")

    with tab3:
        query_inativas = "SELECT id_atividade, nome_atividade FROM atividades WHERE ativa = 0 AND usuario_fk = :uid ORDER BY nome_atividade"
        atividades_inativas = fetch_data_as_dataframe(
            query_inativas, {"uid": usuario_id}
        )
        if not atividades_inativas.empty:
            opcoes_inativas = [
                f"{row['nome_atividade']} (ID: {row['id_atividade']})"
                for _, row in atividades_inativas.iterrows()
            ]
            atividade_para_reativar = st.selectbox(
                "Selecione a atividade para reativar",
                opcoes_inativas,
                key="reativar_select",
            )
            if st.button("Reativar Atividade"):
                atividade_id = int(atividade_para_reativar.split("(ID: ")[-1][:-1])
                if reativar_atividade(atividade_id, usuario_id):
                    st.rerun()
        else:
            st.info("Nenhuma atividade inativa.")


def exibir_protocolo_diario(usuario_id: int, is_staff: bool):
    """Renderiza a página do Protocolo de Operações Diárias."""
    st.header("Protocolo de Operações Diárias (POD)")
    st.markdown(
        "A vitória não é ter um dia perfeito. A vitória é completar o ciclo: **Planejar, Tentar, Registrar.**"
    )

    if is_staff:
        with st.expander("⚙️ Gerenciar Atividades"):
            exibir_gerenciamento_atividades(usuario_id)

    atividades_por_periodo = carregar_atividades_por_periodo(usuario_id)
    log_df = carregar_log_diario(usuario_id)
    hoje_str = datetime.now(pytz.timezone("America/Sao_Paulo")).strftime("%Y-%m-%d")
    log_hoje = log_df[log_df["data"] == hoje_str]

    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader(f"Missões para hoje: {hoje_str}")
        registros_para_salvar = []
        total_atividades = sum(len(ativs) for ativs in atividades_por_periodo.values())
        atividades_concluidas_hoje = 0

        for periodo_key, nome_periodo in PERIODOS.items():
            atividades_periodo = atividades_por_periodo[periodo_key]
            if atividades_periodo:
                st.markdown(f"**{nome_periodo}**")
                for atividade in atividades_periodo:
                    ativ_log = log_hoje[log_hoje["atividade_id"] == atividade["id"]]
                    status_inicial = not ativ_log.empty and ativ_log.iloc[0]["status"]
                    novo_status = st.checkbox(
                        atividade["nome"],
                        value=status_inicial,
                        key=f"cb_{atividade['id']}",
                    )
                    if novo_status:
                        registros_para_salvar.append(
                            {
                                "data": hoje_str,
                                "atividade_id": atividade["id"],
                                "status": True,
                            }
                        )
                        atividades_concluidas_hoje += 1

        if registros_para_salvar:
            salvar_log_pod(pd.DataFrame(registros_para_salvar), usuario_id)

    with col2:
        st.markdown(
            "<h3 style='text-align: center;'>Progresso do Dia</h3>",
            unsafe_allow_html=True,
        )
        percentual_concluido = (
            (atividades_concluidas_hoje / total_atividades)
            if total_atividades > 0
            else 0.0
        )
        fig = go.Figure(
            go.Bar(
                y=[100],
                marker_color="rgba(0,0,0,0)",
                marker_line_color="gray",
                marker_line_width=1.5,
                hoverinfo="none",
            )
        )
        fig.add_trace(
            go.Bar(
                y=[percentual_concluido * 100],
                texttemplate="%{y:.0f}%",
                textposition="inside",
                marker_color="#0068C9",
                hoverinfo="none",
            )
        )
        fig.update_layout(
            barmode="overlay",
            yaxis_range=[0, 100],
            xaxis_showticklabels=False,
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=0, b=0),
            height=500,
            showlegend=False,
        )
        fig.update_yaxes(showgrid=False, showticklabels=False)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.metric(label="Missão Diária", value=f"{percentual_concluido:.0%}")

    st.divider()
    st.subheader("Análise de Consistência (Últimos 30 Dias)")
    data_limite = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    log_30_dias = log_df[log_df["data"] >= data_limite]
    log_concluido_30_dias = log_30_dias[log_30_dias["status"] is True]
    if not log_concluido_30_dias.empty:
        progresso_diario = log_concluido_30_dias.groupby("data").size()
        percentual_diario = (
            (progresso_diario / total_atividades) * 100 if total_atividades > 0 else 0
        )
        idx = pd.date_range(end=datetime.now(), periods=30, freq="D").strftime(
            "%Y-%m-%d"
        )
        percentual_diario = percentual_diario.reindex(idx, fill_value=0)
        st.line_chart(percentual_diario)
    else:
        st.info("Ainda não há dados suficientes para exibir o histórico de 30 dias.")
