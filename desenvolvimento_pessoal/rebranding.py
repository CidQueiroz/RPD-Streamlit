
import streamlit as st
import pandas as pd
from datetime import datetime
from .rpd import (
    carregar_lista_atividades, 
    salvar_nova_atividade, 
    carregar_log_consistencia, 
    salvar_consistencia
)

def exibir_painel_rebranding(usuario_id, username):
    st.header("Diário de Bordo da Consistência")
    st.markdown("A consistência é a prova da sua nova identidade. Cada marcação é uma vitória.")
    st.caption(f"Operador: {username} | Data da Operação: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

    # Carrega dados do banco de dados, agora filtrados por usuário
    df_atividades = carregar_lista_atividades(usuario_id)
    log_consistencia = carregar_log_consistencia() # Esta função já parece ser global, vamos mantê-la assim por enquanto.
    
    atividades_base = ["Programação", "Leitura", "Atividade Física", "Tarefa Doméstica"]
    lista_atividades_db = df_atividades['nome_atividade'].tolist() if not df_atividades.empty else []
    todas_as_atividades = sorted(list(set(atividades_base + lista_atividades_db)))

    with st.expander("⚙️ Gerenciar Lista de Atividades"):
        nova_atividade_input = st.text_input("Nome da nova atividade:", key="nova_atividade_input")
        if st.button("➕ Adicionar Atividade"):
            if nova_atividade_input:
                if salvar_nova_atividade(nova_atividade_input, usuario_id):
                    st.rerun()
            else:
                st.warning("Por favor, digite o nome da atividade.")
    
    st.divider()

    st.subheader("Registrar Nova AMV (Ação Mínima Viável) Concluída")
    atividade_selecionada = st.selectbox("Selecione a atividade concluída hoje:", todas_as_atividades, index=None, placeholder="Escolha uma atividade...")

    if st.button("✅ Registrar Vitória!"):
        if atividade_selecionada and usuario_id:
            hoje_str = datetime.now().strftime('%Y-%m-%d')
            # Encontra o ID da atividade selecionada
            if atividade_selecionada in lista_atividades_db:
                atividade_id = df_atividades[df_atividades['nome_atividade'] == atividade_selecionada]['id_atividade'].iloc[0]
            else:
                # Se for uma atividade base, pode ser necessário adicioná-la primeiro
                st.warning(f'Atividade "{atividade_selecionada}" é uma atividade base. Para registrar, adicione-a à lista gerenciável primeiro.')
                atividade_id = None

            if atividade_id:
                if salvar_consistencia(hoje_str, atividade_id, usuario_id):
                    st.balloons()
                    st.rerun()
        else:
            st.error("Por favor, selecione uma atividade e certifique-se de que o usuário está logado.")

    st.divider()

    st.subheader("Painel de Controle da Consistência")
    if not log_consistencia.empty:
        st.markdown("#### Frequência de Ações por Atividade:")
        contagem_atividades = log_consistencia['nome_atividade'].value_counts()
        st.bar_chart(contagem_atividades)

        st.markdown("#### Histórico de Batalhas Vencidas:")
        st.dataframe(log_consistencia, hide_index=True)
    else:
        st.info("Nenhuma ação registrada. A primeira vitória inicia a corrente.")
