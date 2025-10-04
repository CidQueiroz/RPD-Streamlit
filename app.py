import streamlit as st
import pandas as pd
from datetime import datetime, date
import pytz
import streamlit_authenticator as stauth
from desenvolvimento_pessoal import rebranding, cursos, protocolo_diario, rpd
from core.database import fetch_data_as_dataframe, fetch_data, get_empresa_por_nome, execute_command
from core.auth import inicializar_autenticador, adicionar_usuario
from gestao.estoque import ler_estoque, adicionar_ou_atualizar_item, registrar_venda
from gestao.pdf_generator import criar_recibo_venda

GOOGLE_ANALYTICS = """<script async src="https://www.googletagmanager.com/gtag/js?id=G-PJG10ZYPBS"></script>  
                    <script>
                        window.dataLayer = window.dataLayer || [];
                        function gtag(){dataLayer.push(arguments);}
                        gtag('js', new Date());

                        gtag('config', 'G-PJG10ZYPBS');
                    </script>"""
st.html(GOOGLE_ANALYTICS)

def get_user_details(username):
    """Busca detalhes de um usuário no banco de dados."""
    query = """
        SELECT id_usuario, acesso_dev_pessoal, empresa_fk, is_staff, e.nome_empresa
        FROM usuarios u
        JOIN empresas e ON u.empresa_fk = e.id_empresa
        WHERE u.usuario = :username
    """
    user_info = fetch_data(query, {'username': username})
    if user_info:
        return user_info[0]
    return None

def construir_query_relatorio_vendas(filtro_opcao, data_selecionada, id_empresa, is_staff, user_id):
    """Constrói a query e os parâmetros para o relatório de vendas."""
    data_inicio, data_fim = None, None
    hoje = datetime.now(pytz.timezone('America/Sao_Paulo')).date()

    if filtro_opcao == "Hoje":
        data_inicio, data_fim = hoje, hoje + pd.Timedelta(days=1)
    elif filtro_opcao == "Ontem":
        data_inicio, data_fim = hoje - pd.Timedelta(days=1), hoje
    elif filtro_opcao == "Selecionar data" and data_selecionada:
        data_inicio, data_fim = data_selecionada, data_selecionada + pd.Timedelta(days=1)
    
    base_query = """
        SELECT v.data_hora AS "Data/Hora", p.item, p.variacao, v.quantidade, 
               v.preco_unitario AS "Preço Unitário", v.preco_total AS "Preço Total", u.nome AS "Vendedor"
        FROM vendas v
        JOIN estoque p ON v.estoque_fk = p.id_item
        JOIN usuarios u ON v.vendedor_fk = u.id_usuario
        WHERE v.empresa_fk = :id_empresa
    """
    params = {"id_empresa": id_empresa}

    if not is_staff:
        base_query += " AND v.vendedor_fk = :id_usuario"
        params["id_usuario"] = user_id

    date_filter_clause = ""
    if data_inicio and data_fim:
        date_filter_clause = " AND v.data_hora >= :start AND v.data_hora < :end"
        params["start"] = data_inicio
        params["end"] = data_fim

    query = base_query + date_filter_clause + " ORDER BY v.data_hora DESC"
    return query, params

def main():
    """Função principal que executa a aplicação Streamlit."""
    # --- 1. AUTENTICAÇÃO ---
    st.set_page_config(
        page_title="Gestão CDKTeck",
        page_icon="logo.png",
        layout="wide",
    )

    authenticator = inicializar_autenticador()
    if not authenticator:
        st.stop()
    authenticator.login()

    name = st.session_state.get("name")
    authentication_status = st.session_state.get("authentication_status")
    username = st.session_state.get("username")

    if not authentication_status:
        if authentication_status is False:
            st.error('Usuário ou senha incorretos.')

        if 'auth_view' not in st.session_state:
            st.session_state.auth_view = 'none'

        if st.session_state.auth_view == 'none':
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Esqueci minha senha", use_container_width=True):
                    st.session_state.auth_view = 'forgot_password'
                    st.rerun()
            with col2:
                if st.button("Novo usuário", use_container_width=True):
                    st.session_state.auth_view = 'register'
                    st.rerun()
        
        elif st.session_state.auth_view == 'forgot_password':
            st.subheader("Recuperação de Senha")
            with st.form("forgot_password_form"):
                username_input = st.text_input("Usuário")
                new_password = st.text_input("Nova Senha", type="password")
                confirm_password = st.text_input("Confirmar Nova Senha", type="password")
                submit = st.form_submit_button("Mudar Senha")

                if submit:
                    if new_password == confirm_password:
                        hashed_password = stauth.Hasher.hash(new_password)
                        query = "UPDATE usuarios SET senha = :senha WHERE usuario = :usuario"
                        params = {"senha": hashed_password, "usuario": username_input}
                        if execute_command(query, params):
                            st.success("Senha alterada com sucesso!")
                            st.session_state.auth_view = 'none'
                            st.rerun()
                        else:
                            st.error("Não foi possível alterar a senha.")
                    else:
                        st.error("As senhas não coincidem.")
            if st.button("Voltar para o Login"):
                st.session_state.auth_view = 'none'
                st.rerun()

        elif st.session_state.auth_view == 'register':
            st.subheader("Novo por aqui? Cadastre-se!")
            with st.form("form_cadastro"):
                novo_nome = st.text_input("Nome completo")
                novo_usuario = st.text_input("Novo usuário")
                nova_senha = st.text_input("Nova senha", type="password")
                confirmar_senha = st.text_input("Confirmar senha", type="password")
                nome_empresa = st.text_input("Nome da sua empresa")
                
                cadastrar = st.form_submit_button("Cadastrar")
                
                if cadastrar:
                    if not all([novo_nome, novo_usuario, nova_senha, confirmar_senha, nome_empresa]):
                        st.warning("Todos os campos são obrigatórios.")
                    elif nova_senha != confirmar_senha:
                        st.error("As senhas não coincidem.")
                    else:
                        empresa_data = get_empresa_por_nome(nome_empresa.strip())
                        if not empresa_data:
                            st.error(f'A empresa "{nome_empresa}" não foi encontrada. Verifique o nome ou peça ao seu gerente para cadastrá-la.')
                        else:
                            id_empresa = empresa_data[0]['id_empresa']
                            if adicionar_usuario(novo_nome, novo_usuario, nova_senha, id_empresa):
                                st.success("Usuário cadastrado com sucesso! Por favor, faça o login.")
                                st.session_state.auth_view = 'none'
                                st.rerun()
            if st.button("Voltar para o Login"):
                st.session_state.auth_view = 'none'
                st.rerun()

        st.stop()

    # --- 2. LÓGICA PÓS-LOGIN ---
    nome_usuario = st.session_state.get("name", "N/A")
    username = st.session_state.get("username", "").lower()
    
    user_details = get_user_details(username)

    if not user_details:
        st.error("Não foi possível carregar os detalhes do usuário. Tente fazer login novamente.")
        st.stop()

    st.session_state['user_id'] = user_details['id_usuario']
    st.session_state['empresa_id'] = user_details['empresa_fk']
    st.session_state['empresa_nome'] = user_details['nome_empresa']
    st.session_state['is_staff'] = bool(user_details['is_staff'])
    st.session_state['acesso_dev_pessoal'] = bool(user_details['acesso_dev_pessoal'])

    # --- 3. RENDERIZAÇÃO DO MENU (SIDEBAR) ---
    with st.sidebar:
        st.write(f"Usuário: {nome_usuario}")
        st.caption(f"Empresa: {st.session_state['empresa_nome']}")
        authenticator.logout("Sair", "sidebar")
        st.divider()

        modulos_disponiveis = ["Gestão"]
        if st.session_state['acesso_dev_pessoal']:
            modulos_disponiveis.append("Desenvolvimento Pessoal")

        modulo_selecionado = st.selectbox("Módulo:", modulos_disponiveis)

        opcao = None
        if modulo_selecionado == "Gestão":
            opcoes_gestao = ["Estoque", "Registrar Venda", "Relatório de Vendas"]
            opcao = st.radio("Opções de Gestão:", opcoes_gestao, key="gestao_radio")
        
        elif modulo_selecionado == "Desenvolvimento Pessoal":
            opcoes_dev = ["Responder RPD", "Visualizar Respostas", "AMV Tracker", "Protocolo Diário (POD)", "Painel de Cursos"]
            opcao = st.radio("Opções de Desenvolvimento Pessoal:", opcoes_dev)

    # --- 4. RENDERIZAÇÃO DA PÁGINA SELECIONADA ---
    if opcao == "Estoque":
        st.title(f"Controle de Estoque - {st.session_state['empresa_nome']}")
        df_estoque = ler_estoque(st.session_state['empresa_id'])

        if st.session_state['is_staff']:
            st.subheader("Adicionar/Incrementar Estoque")
            with st.form("form_add_item", clear_on_submit=True):
                item = st.text_input("Nome do item")
                variacao = st.text_input("Variação (cor, tamanho, etc.)")
                quantidade = st.number_input("Quantidade", min_value=1, step=1)
                preco = st.number_input("Preço (R$)", min_value=0.01, format="%.2f", help="O preço só é necessário para itens novos.")
                submitted_add = st.form_submit_button("Salvar Item")

                if submitted_add:
                    if item and variacao and quantidade:
                        adicionar_ou_atualizar_item(
                            item=item.strip(), 
                            variacao=variacao.strip(), 
                            quantidade=quantidade, 
                            preco=preco, 
                            id_empresa=st.session_state['empresa_id']
                        )
                        st.rerun()
                    else:
                        st.warning("Por favor, preencha todos os campos.")

        st.subheader("Estoque Atual")
        if df_estoque.empty:
            st.info("Nenhum item em estoque.")
        else:
            df_estoque_display = df_estoque.copy()
            df_estoque_display['preco'] = pd.to_numeric(df_estoque_display['preco']).map('R$ {:,.2f}'.format)
            df_estoque_display = df_estoque_display[["id_item", "item", "variacao", "quantidade", "preco"]]
            st.dataframe(df_estoque_display, hide_index=True)

    elif opcao == "Registrar Venda":
        st.title(f"Registrar Venda - {st.session_state['empresa_nome']}")

        if 'last_sale_details' in st.session_state and st.session_state.last_sale_details:
            sale_details = st.session_state.last_sale_details
            st.success("Venda registrada com sucesso!")
            
            st.subheader("Detalhes da Venda")
            st.json(sale_details)

            pdf_bytes = criar_recibo_venda(sale_details)
            st.download_button(
                label="Gerar PDF do Recibo",
                data=pdf_bytes,
                file_name=f"recibo_venda_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )

            if st.button("Registrar Nova Venda"):
                del st.session_state.last_sale_details
                st.rerun()
        
        else:
            df_estoque = ler_estoque(st.session_state['empresa_id'])
            if not df_estoque.empty:
                with st.form("form_venda"):
                    itens_disponiveis = [f"{row['item']} - {row['variacao']} (ID: {row['id_item']})" for index, row in df_estoque.iterrows()]
                    item_vendido_str = st.selectbox("Selecione o item vendido", itens_disponiveis)
                    quantidade_vendida = st.number_input("Quantidade Vendida", min_value=1, step=1)
                    st.divider()
                    st.markdown("_(Opcional)_ Informações do Cliente")
                    cliente_nome = st.text_input("Nome do Cliente")
                    cliente_cpf = st.text_input("CPF do Cliente")
                    submitted_venda = st.form_submit_button("Registrar Venda")

                    if submitted_venda:
                        estoque_id = int(item_vendido_str.split('(ID: ')[-1][:-1])
                        item_selecionado = df_estoque.loc[df_estoque['id_item'] == estoque_id].iloc[0]
                        
                        if item_selecionado['quantidade'] >= quantidade_vendida:
                            data_venda_dt = datetime.now(pytz.timezone('America/Sao_Paulo'))
                            
                            st.session_state['last_sale_details'] = {
                                "empresa_nome": st.session_state['empresa_nome'],
                                "data_venda": data_venda_dt.strftime("%d/%m/%Y %H:%M:%S"),
                                "vendedor_nome": st.session_state['name'],
                                "cliente_nome": cliente_nome.strip() if cliente_nome else None,
                                "cliente_cpf": cliente_cpf.strip() if cliente_cpf else None,
                                "item": item_selecionado['item'],
                                "variacao": item_selecionado['variacao'],
                                "quantidade": quantidade_vendida,
                                "preco_unitario": item_selecionado['preco'],
                                "preco_total": quantidade_vendida * item_selecionado['preco']
                            }

                            registrar_venda(
                                data_venda=data_venda_dt.strftime("%Y-%m-%d %H:%M:%S"), 
                                estoque_id=estoque_id, 
                                quantidade=quantidade_vendida, 
                                usuario_id=st.session_state['user_id'], 
                                id_empresa=st.session_state['empresa_id']
                            )
                            st.rerun()
                        else:
                            st.error("Quantidade em estoque insuficiente para esta venda.")
            else:
                st.warning("Nenhum item em estoque para vender. Adicione itens na página de Estoque.")

    elif opcao == "Relatório de Vendas":
        st.title(f"Relatório de Vendas - {st.session_state['empresa_nome']}")
        try:
            st.subheader("Filtros")
            filtro_opcao = st.selectbox("Filtrar período:", ["Hoje", "Ontem", "Todo o período", "Selecionar data"])
            data_selecionada = None
            if filtro_opcao == "Selecionar data":
                data_selecionada = st.date_input("Selecione a data")

            query, params = construir_query_relatorio_vendas(
                filtro_opcao, 
                data_selecionada, 
                st.session_state['empresa_id'], 
                st.session_state['is_staff'], 
                st.session_state['user_id']
            )
            df_filtrado = fetch_data_as_dataframe(query, params)

            st.divider()
            total_arrecadado = pd.to_numeric(df_filtrado["Preço Total"]).sum()
            st.metric(label="Total Arrecadado (filtrado)", value=f"R$ {total_arrecadado:,.2f}")

            st.subheader("Vendas no Período")
            if df_filtrado.empty:
                st.info("Nenhuma venda registrada para o período selecionado.")
            else:
                df_display = df_filtrado.copy()
                df_display['Preço Unitário'] = pd.to_numeric(df_display['Preço Unitário']).map('R$ {:,.2f}'.format)
                df_display['Preço Total'] = pd.to_numeric(df_display['Preço Total']).map('R$ {:,.2f}'.format)
                st.table(df_display)

            if st.session_state['is_staff']:
                st.divider()
                st.subheader("Comissão do Dia (baseado no total filtrado)")
                comissoes = {"Cid": 0.30, "Cleo": 0.20, "Quiópa": 0.15, "Zanah": 0.15, "Caixa": 0.20}
                data_comissao = [{"Nome": nome, "Percentual": f"{p:.0%}", "Valor": f"R$ {total_arrecadado * p:,.2f}"} for nome, p in comissoes.items()]
                st.table(pd.DataFrame(data_comissao))

                st.divider()
                st.subheader("Itens em Falta ou com Baixo Estoque")
                LOW_STOCK_THRESHOLD = 3
                df_estoque_baixo = fetch_data_as_dataframe("SELECT item, variacao, quantidade, preco FROM estoque WHERE quantidade <= :threshold AND empresa_fk = :id_empresa", {"threshold": LOW_STOCK_THRESHOLD, "id_empresa": st.session_state['empresa_id']})
                
                if df_estoque_baixo.empty:
                    st.info(f"Nenhum item com estoque igual ou inferior a {LOW_STOCK_THRESHOLD} unidades.")
                else:
                    df_estoque_baixo['preco'] = pd.to_numeric(df_estoque_baixo['preco']).map('R$ {:,.2f}'.format)
                    st.table(df_estoque_baixo)

        except Exception as e:
            st.error(f"Ocorreu um erro ao gerar o relatório: {e}")

    elif opcao == "Responder RPD":
        st.subheader("Mapeamento e Desarmamento do 'Crítico Interno'")
        with st.form(key="formulario_rpd"):
            situacao = st.text_area("1. Situação")
            pensamentos = st.text_area("2. Pensamento Automático")
            emocao = st.text_area("3. Emoção / Sentimento")
            conclusao = st.text_area("4. Resposta Adaptativa")
            submitted = st.form_submit_button("Enviar Respostas")

        if submitted:
            datahora = datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%Y-%m-%d %H:%M:%S")
            if rpd.salvar_resposta(datahora, situacao, pensamentos, emocao, conclusao, 'Retirado', st.session_state['user_id']):
                st.rerun()

    elif opcao == "Visualizar Respostas":
        st.title("Respostas já registradas")
        if username in ["cid", "cleo"]: # Mantendo a lógica original de admin para RPD
            df_respostas = rpd.ler_todas_as_respostas()
            st.write("Visualizando respostas de todos os usuários (visão de admin).")
        else:
            df_respostas = rpd.ler_respostas_por_usuario(st.session_state['user_id'])

        if df_respostas.empty:
            st.info("Nenhuma resposta registrada ainda.")
        else:
            st.dataframe(df_respostas, hide_index=True)
            csv = df_respostas.to_csv(index=False).encode("utf-8")
            st.download_button("Baixar CSV", csv, "rpd_export.csv", "text/csv")

    elif opcao == "AMV Tracker":
        rebranding.exibir_painel_rebranding(st.session_state['user_id'], username)

    elif opcao == "Painel de Cursos":
        # MODIFICAÇÃO 2: Chamar a nova função que usa o banco de dados
        cursos.exibir_painel_cursos_sql(st.session_state['user_id'])

    elif opcao == "Protocolo Diário (POD)":
        protocolo_diario.exibir_protocolo_diario(st.session_state['user_id'], st.session_state['is_staff'])

if __name__ == "__main__":
    main()