import streamlit as st
import pandas as pd
from core.database import fetch_data_as_dataframe, execute_command

@st.cache_data(ttl=60)
def ler_cursos_sql(user_id):
    """
    Lê os dados da tabela 'cursos' do banco de dados para um usuário específico
    e os retorna como um DataFrame.
    Aplica cache para evitar leituras repetidas.
    """
    try:
        query = "SELECT * FROM cursos WHERE usuario_fk = :user_id"
        params = {"user_id": user_id}
        df = fetch_data_as_dataframe(query, params)

        if df is None:
             st.warning("Ocorreu um erro ao buscar os cursos, o DataFrame retornou nulo.")
             return pd.DataFrame()

        # Garante que colunas importantes não tenham valores nulos e tenham o tipo correto
        if not df.empty:
            df['Percentual'] = pd.to_numeric(df['Percentual'], errors='coerce').fillna(0).astype(int)
            df['Fase do curso'] = pd.to_numeric(df['Fase do curso'], errors='coerce').fillna(1).astype(int)
            # Preenche valores nulos em colunas de texto para evitar erros
            for col in ['Nome do curso', 'Motivação', 'Prazo conclusão']:
                if col in df.columns:
                    df[col] = df[col].fillna('Não informado')

        return df
    except Exception as e:
        st.error(f"Erro ao ler os cursos do banco de dados: {e}")
        return pd.DataFrame()


def atualizar_progresso_sql(nome_curso, novo_percentual, user_id):
    """
    Atualiza o percentual de um curso específico na tabela 'cursos' para um usuário.
    """
    try:
        query = """
            UPDATE cursos
            SET Percentual = :percentual
            WHERE "Nome do curso" = :nome_curso AND usuario_fk = :user_id
        """
        params = {
            "percentual": novo_percentual,
            "nome_curso": nome_curso,
            "user_id": user_id
        }
        rows_affected = execute_command(query, params)

        if rows_affected is not None and rows_affected > 0:
            st.toast(f"Progresso de '{nome_curso}' salvo!", icon="✅")
        elif rows_affected == 0:
             st.warning(f"Nenhum curso com o nome '{nome_curso}' foi encontrado para o seu usuário.")
        # Se rows_affected for None, a função execute_command já exibiu um erro.

    except Exception as e:
        st.error(f"Erro ao atualizar o progresso no banco de dados: {e}")


def salvar_curso_sql(curso_data, user_id):
    """
    Salva (insere ou atualiza) um curso no banco de dados.
    """
    try:
        # Se id_curso for None ou 0, é um novo curso (INSERT)
        if not curso_data.get('id_curso'):
            query = """
                INSERT INTO cursos (`Fase do curso`, `Nome do curso`, `Motivação`, `Prazo conclusão`, `Link do curso`, `Observação`, `usuario_fk`)
                VALUES (:fase, :nome, :motivacao, :prazo, :link, :obs, :user_id)
            """
            params = {
                "fase": curso_data['fase'],
                "nome": curso_data['nome'],
                "motivacao": curso_data['motivacao'],
                "prazo": curso_data['prazo'],
                "link": curso_data['link'],
                "obs": curso_data['obs'],
                "user_id": user_id
            }
            st.success("Curso adicionado com sucesso!")
        # Caso contrário, é um curso existente (UPDATE)
        else:
            query = """
                UPDATE cursos SET
                    `Fase do curso` = :fase,
                    `Nome do curso` = :nome,
                    `Motivação` = :motivacao,
                    `Prazo conclusão` = :prazo,
                    `Link do curso` = :link,
                    `Observação` = :obs
                WHERE id_curso = :id_curso AND usuario_fk = :user_id
            """
            params = {
                "fase": curso_data['fase'],
                "nome": curso_data['nome'],
                "motivacao": curso_data['motivacao'],
                "prazo": curso_data['prazo'],
                "link": curso_data['link'],
                "obs": curso_data['obs'],
                "id_curso": curso_data['id_curso'],
                "user_id": user_id
            }
            st.success("Curso atualizado com sucesso!")

        execute_command(query, params)
        st.cache_data.clear() # Limpa o cache para recarregar a lista
        st.rerun()

    except Exception as e:
        st.error(f"Erro ao salvar o curso: {e}")


def deletar_curso_sql(id_curso, user_id):
    """ Deleta um curso do banco de dados. """
    try:
        query = "DELETE FROM cursos WHERE id_curso = :id_curso AND usuario_fk = :user_id"
        params = {"id_curso": id_curso, "user_id": user_id}
        execute_command(query, params)
        st.warning("Curso deletado.")
        st.cache_data.clear()
        st.rerun()
    except Exception as e:
        st.error(f"Erro ao deletar o curso: {e}")


def exibir_painel_cursos_sql(user_id):
    """
    Renderiza a página do Painel de Controle de Cursos com dados do banco de dados MySQL.
    """
    st.title("Painel de Controle de Treinamento")
    st.markdown("O mapa estratégico da sua evolução. Monitore seu progresso e mantenha o foco na missão atual.")

    df_cursos = ler_cursos_sql(user_id)

    # --- FORMULÁRIO DE GERENCIAMENTO DE CURSOS ---
    with st.expander("Gerenciar Cursos"):
        cursos_list = ["Adicionar Novo Curso"] + df_cursos["Nome do curso"].tolist()
        curso_selecionado_nome = st.selectbox("Selecione um curso para editar ou adicione um novo:", cursos_list)

        curso_atual = None
        if curso_selecionado_nome != "Adicionar Novo Curso":
            curso_atual = df_cursos[df_cursos["Nome do curso"] == curso_selecionado_nome].iloc[0]

        with st.form("form_curso", clear_on_submit=True):
            nome = st.text_input("Nome do curso", value=curso_atual["Nome do curso"] if curso_atual is not None else "")
            fase = st.number_input("Fase", min_value=1, step=1, value=int(curso_atual["Fase do curso"]) if curso_atual is not None else 1)
            motivacao = st.text_area("Motivação", value=curso_atual["Motivação"] if curso_atual is not None else "")
            prazo = st.text_input("Prazo para conclusão", value=curso_atual["Prazo conclusão"] if curso_atual is not None else "")
            link = st.text_input("Link do curso", value=curso_atual["Link do curso"] if curso_atual is not None else "")
            obs = st.text_area("Observação", value=curso_atual["Observação"] if curso_atual is not None else "")

            col1, col2, col3 = st.columns([2, 1, 2])
            with col1:
                submitted_save = st.form_submit_button("Salvar Curso", use_container_width=True, type="primary")
            if curso_atual is not None:
                with col3:
                    submitted_delete = st.form_submit_button("Deletar", use_container_width=True, type="secondary")

            if submitted_save:
                if not nome:
                    st.warning("O nome do curso é obrigatório.")
                else:
                    curso_data = {
                        "id_curso": int(curso_atual["id_curso"]) if curso_atual is not None else None,
                        "nome": nome, "fase": fase, "motivacao": motivacao,
                        "prazo": prazo, "link": link, "obs": obs
                    }
                    salvar_curso_sql(curso_data, user_id)

            if curso_atual is not None and submitted_delete:
                deletar_curso_sql(int(curso_atual["id_curso"]), user_id)

    if df_cursos.empty:
        st.info("Nenhum curso encontrado para você no banco de dados.")
        return

    fases = sorted(df_cursos['Fase do curso'].unique())
    
    cursos_concluidos = 0
    total_cursos = len(df_cursos)

    for fase in fases:
        with st.expander(f"**Fase {int(fase)}**"):
            cursos_na_fase = df_cursos[df_cursos['Fase do curso'] == fase]
            
            for _, curso_row in cursos_na_fase.iterrows():
                nome_curso = curso_row['Nome do curso']
                motivacao = curso_row['Motivação']
                prazo = curso_row['Prazo conclusão']
                percentual_atual = int(curso_row['Percentual'])

                st.subheader(nome_curso)
                st.caption(f"Motivação: {motivacao} | Prazo: {prazo}")

                # Layout em colunas para o slider e o status
                col1, col2 = st.columns([3, 1])

                with col1:
                    novo_percentual = st.slider(
                        label="Progresso",
                        min_value=0,
                        max_value=100,
                        value=percentual_atual,
                        step=5,
                        key=f"slider_{nome_curso}"
                    )
                    # Se o valor do slider mudou, salva o novo progresso
                    if novo_percentual != percentual_atual:
                        atualizar_progresso_sql(nome_curso, novo_percentual, user_id)
                        # Força o rerender para limpar o cache e mostrar o valor atualizado
                        st.cache_data.clear()
                        st.rerun()

                with col2:
                    if percentual_atual == 100:
                        st.success("✅ Concluído")
                    else:
                        st.info(f"{percentual_atual}%")
                
                # Contabiliza para a barra de progresso geral
                if percentual_atual == 100:
                    cursos_concluidos += 1
            
            st.write("---")

    st.divider()

    # --- BARRA DE PROGRESSO GERAL ---
    st.header("Progresso Geral da Campanha de Rebranding")
    if total_cursos > 0:
        percentual_geral = (cursos_concluidos / total_cursos) * 100
        st.progress(int(percentual_geral), text=f"{percentual_geral:.1f}% Concluído")
    else:
        st.info("Nenhum curso catalogado para calcular o progresso geral.")
