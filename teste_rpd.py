import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from gspread_dataframe import set_with_dataframe, get_as_dataframe
import json
from google.oauth2.service_account import Credentials


def autenticar_usuario(usuario, senha):
    client = autenticar_gspread()
    try:
        sheet = client.open(SHEET_NAME)
        worksheet = sheet.worksheet("Usuarios")
        df_usuarios = get_as_dataframe(worksheet, evaluate_formulas=True, header=0)
        df_usuarios = df_usuarios.dropna(how="all")
        # Converta para string para evitar problemas de tipo
        df_usuarios['usuario'] = df_usuarios['usuario'].astype(str).str.strip()
        df_usuarios['senha'] = df_usuarios['senha'].astype(str).str.strip()
        usuario = str(usuario).strip()
        senha = str(senha).strip()
        st.write(df_usuarios)  # Para depuração

        usuario_encontrado = df_usuarios[
            (df_usuarios['usuario'] == usuario) & (df_usuarios['senha'] == senha)
        ]
        if not usuario_encontrado.empty:
            st.session_state.usuario_logado = usuario_encontrado.iloc[0]['usuario']
            st.session_state.nome_usuario = usuario_encontrado.iloc[0]['nome']
            st.session_state.usuario_autenticado = True
            st.success(f"Bem-vindo, {st.session_state.nome_usuario}!")
            st.rerun()
            return st.session_state.nome_usuario
        else:
            st.error("Usuário ou senha incorretos.")
    except Exception as e:
        st.error(f"Erro ao acessar a aba de usuários: {e}")
        return None

# Autenticação com Google Sheets
def autenticar_gspread():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds_dict = json.loads(st.secrets["gcp_service_account"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    return client

# Nome da planilha e aba
SHEET_NAME = "RPD"
WORKSHEET_NAME = "Respostas"
WORKSHEET_ESTOQUE = "Estoque"
WORKSHEET_VENDAS = "Vendas"

# Função para salvar respostas no Google Sheets
def salvar_resposta_sheets(datahora, situacao, pensamentos, emocao, conclusao, resultado, usuario_login):
    client = autenticar_gspread()
    aba_destino = "Respostas" if usuario_login == "admin" else usuario_login
    try:
        sheet = client.open(SHEET_NAME)
    except Exception:
        st.error("Não foi possível abrir a planilha. Verifique se compartilhou com o e-mail do serviço.")
        return
    try:
        worksheet = sheet.worksheet(aba_destino)
    except Exception:
        worksheet = sheet.add_worksheet(title=aba_destino, rows="1000", cols="10")
        worksheet.append_row(["Data/Hora", "Situação", "Pensamentos automáticos", "Emoção", "Conclusão", "Resultado"])
    df = get_as_dataframe(worksheet, evaluate_formulas=True, header=0)
    nova_resposta = pd.DataFrame([{
        "Data/Hora": datahora,
        "Situação": situacao,
        "Pensamentos automáticos": pensamentos,
        "Emoção": emocao,
        "Conclusão": conclusao,
        "Resultado": resultado
    }])
    df = pd.concat([df, nova_resposta], ignore_index=True)
    worksheet.clear()
    set_with_dataframe(worksheet, df)


def adicionar_usuario(nome, usuario, senha):
    try:
        client = autenticar_gspread()
        sheet = client.open(SHEET_NAME)
        worksheet_usuarios = sheet.worksheet("Usuarios")
        df_usuarios = get_as_dataframe(worksheet_usuarios, evaluate_formulas=True, header=0)
        df_usuarios = df_usuarios.dropna(how="all")
        usuario = str(usuario).strip()  # <-- Garante que não tem espaço
        # Verifica se usuário já existe
        if usuario in df_usuarios['usuario'].astype(str).values:
            return False
        nova_linha = pd.DataFrame([{
            "usuario": usuario,
            "senha": str(senha).strip(),
            "nome": str(nome).strip()
        }])
        df_usuarios = pd.concat([df_usuarios, nova_linha], ignore_index=True)
        worksheet_usuarios.clear()
        set_with_dataframe(worksheet_usuarios, df_usuarios)
        # Cria nova aba para o usuário
        try:
            sheet.add_worksheet(title=usuario, rows="1000", cols="10")
            ws_novo = sheet.worksheet(usuario)
            ws_novo.append_row(["Data/Hora", "Situação", "Pensamentos automáticos", "Emoção", "Conclusão", "Resultado"])
        except Exception as e:
            st.warning(f"Aviso ao criar aba do usuário: {e}")
        return True
    except Exception as e:
        st.error(f"Erro ao adicionar usuário: {e}")
        return False
        
# Função para ler respostas do Google Sheets
def ler_respostas_sheets(aba_destino):
    client = autenticar_gspread()
    try:
        sheet = client.open(SHEET_NAME)
        worksheet = sheet.worksheet(aba_destino)
        df = get_as_dataframe(worksheet, evaluate_formulas=True, header=0)
        df = df.dropna(how="all")
        return df
    except Exception as e:
        st.error(f"Erro ao acessar a aba '{aba_destino}': {e}")
        return pd.DataFrame(columns=[
            "Data/Hora",
            "Situação",
            "Pensamentos automáticos",
            "Emoção",
            "Conclusão",
            "Resultado"
        ])

# Funções para o estoque
def ler_estoque_sheets():
    client = autenticar_gspread()
    try:
        sheet = client.open(SHEET_NAME)
        worksheet = sheet.worksheet(WORKSHEET_ESTOQUE)
        df = get_as_dataframe(worksheet, evaluate_formulas=True, header=0)
        df = df.dropna(how="all")
        return df
    except gspread.exceptions.WorksheetNotFound:
        # Cria a aba se não existir
        worksheet = sheet.add_worksheet(title=WORKSHEET_ESTOQUE, rows="1000", cols="10")
        worksheet.append_row(["Item", "Variação", "Quantidade", "Preço"])
        return pd.DataFrame(columns=["Item", "Variação", "Quantidade", "Preço"])
    except Exception as e:
        st.error(f"Erro ao acessar a aba de estoque: {e}")
        return pd.DataFrame(columns=["Item", "Variação", "Quantidade", "Preço"])

def adicionar_item_estoque(item, variacao, quantidade, preco):
    client = autenticar_gspread()
    try:
        sheet = client.open(SHEET_NAME)
        worksheet = sheet.worksheet(WORKSHEET_ESTOQUE)
        df = get_as_dataframe(worksheet, evaluate_formulas=True, header=0)
        
        # Verifica se o item com a mesma variação já existe
        if not df[(df['Item'] == item) & (df['Variação'] == variacao)].empty:
            st.error("Este item com esta variação já existe no estoque.")
            return

        novo_item = pd.DataFrame([{
            "Item": item,
            "Variação": variacao,
            "Quantidade": quantidade,
            "Preço": preco
        }])
        df = pd.concat([df, novo_item], ignore_index=True)
        worksheet.clear()
        set_with_dataframe(worksheet, df)
        st.success("Item adicionado ao estoque com sucesso!")
    except Exception as e:
        st.error(f"Erro ao adicionar item ao estoque: {e}")

def atualizar_estoque_sheets(df_estoque):
    client = autenticar_gspread()
    try:
        sheet = client.open(SHEET_NAME)
        worksheet = sheet.worksheet(WORKSHEET_ESTOQUE)
        worksheet.clear()
        set_with_dataframe(worksheet, df_estoque)
    except Exception as e:
        st.error(f"Erro ao atualizar o estoque: {e}")

def registrar_venda_sheets(datahora, item, variacao, quantidade, preco_unitario, preco_total, vendedor):
    client = autenticar_gspread()
    try:
        sheet = client.open(SHEET_NAME)
        try:
            worksheet = sheet.worksheet(WORKSHEET_VENDAS)
        except gspread.exceptions.WorksheetNotFound:
            worksheet = sheet.add_worksheet(title=WORKSHEET_VENDAS, rows="1000", cols="10")
            worksheet.append_row(["Data/Hora", "Item", "Variação", "Quantidade", "Preço Unitário", "Preço Total", "Vendedor"])
        
        df = get_as_dataframe(worksheet, evaluate_formulas=True, header=0)
        nova_venda = pd.DataFrame([{
            "Data/Hora": datahora,
            "Item": item,
            "Variação": variacao,
            "Quantidade": quantidade,
            "Preço Unitário": preco_unitario,
            "Preço Total": preco_total,
            "Vendedor": vendedor
        }])
        df = pd.concat([df, nova_venda], ignore_index=True)
        worksheet.clear()
        set_with_dataframe(worksheet, df)
    except Exception as e:
        st.error(f"Erro ao registrar venda: {e}")

# Configuração inicial do Streamlit
if "usuario_autenticado" not in st.session_state:
    st.session_state.usuario_autenticado = False
    st.session_state.nome_usuario = ""
if "mostrar_cadastro" not in st.session_state:
    st.session_state.mostrar_cadastro = False

if not st.session_state.usuario_autenticado:
    st.title("Login")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        nome = autenticar_usuario(usuario, senha)
        if nome:
            st.session_state.usuario_autenticado = True
            st.session_state.nome_usuario = nome
            st.success(f"Bem-vindo, {nome}!")
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")

    st.markdown("---")
    st.subheader("Novo por aqui? Cadastre-se!")

    # O botão deve aparecer sempre
    if st.button("Adicionar usuário"):
        st.session_state.mostrar_cadastro = True

    # O formulário só aparece se mostrar_cadastro for True
    if st.session_state.get("mostrar_cadastro", False):
        with st.form("form_cadastro"):
            novo_nome = st.text_input("Nome completo")
            novo_usuario = st.text_input("Novo usuário")
            nova_senha = st.text_input("Nova senha", type="password")
            cadastrar = st.form_submit_button("Cadastrar")
            if cadastrar:
                sucesso = adicionar_usuario(novo_nome, novo_usuario, nova_senha)
                if sucesso:
                    st.success("Usuário cadastrado com sucesso! Faça login.")
                    st.session_state.mostrar_cadastro = False
                else:
                    st.error("Erro ao cadastrar usuário. Tente outro nome de usuário.")
    st.stop()
else:
    st.sidebar.write(f"Usuário: {st.session_state.nome_usuario}")
    if st.sidebar.button("Sair"):
        st.session_state.usuario_autenticado = False
        st.session_state.nome_usuario = ""
        st.rerun()

# Menu lateral
st.sidebar.title("Menu")
opcoes_menu = ["Estoque"]
if st.session_state.usuario_logado in ["cid", "cleo"]:
    opcoes_menu.append("Relatório de Vendas")
opcoes_menu.extend(["Responder perguntas", "Visualizar respostas"])
opcao = st.sidebar.radio("Escolha uma opção:", opcoes_menu)

if opcao == "Responder perguntas":
    st.title("Registro RPD")
    st.write("Preencha as informações abaixo:")

    with st.form(key="formulario"):
        # Pergunta 1
        situacao = st.text_area(
            "Situação (Que situação real, fluxo de pensamentos, devaneios ou recordações levaram à emoção desagradável?)"
        )

        # Pergunta 2
        pensamentos = st.text_area(
            "Pensamentos automáticos (Quais foram os pensamentos automáticos que passaram pela sua cabeça? Quanto você acredita em cada um deles? (0 a 100%))"
        )

        # Pergunta 3
        emocao = st.text_area(
            "Emoção (Qual foi a emoção que você sentiu? Qual foi a intensidade dessa emoção? (0 a 100%))"
        )

        # Pergunta 4
        conclusao = st.text_area(
            "Conclusão (1. Quais são suas respostas racionais aos pensamentos automáticos? Use as perguntas abaixo para compor uma resposta aos pensamentos automáticos. Quanto você acredita em cada resposta? (0 a 100%))"
        )

        # Pergunta 5
        resultado = st.text_area(
            "Resultado (Quanto você acredita agora em cada pensamento automático? (0 a 100%) Que emoções você sente agora? Qual a intensidade? (0 a 100%) O que você fará ou fez?)"
        )

        submitted = st.form_submit_button("Enviar Respostas")

    if submitted:
        datahora = datetime.now().strftime("%d/%m/%Y  %H:%M:%S")
        salvar_resposta_sheets(
            datahora, situacao, pensamentos, emocao, conclusao, resultado, st.session_state.usuario_logado
        )
        st.success("Respostas salvas com sucesso no Excel!")
        st.subheader("Resumo das respostas:")
        st.write(f"**Data/Hora:** {datahora}")
        st.write(f"**Situação:** {situacao}")
        st.write(f"**Pensamentos automáticos:** {pensamentos}")
        st.write(f"**Emoção:** {emocao}")
        st.write(f"**Conclusão:** {conclusao}")
        st.write(f"**Resultado:** {resultado}")

elif opcao == "Visualizar respostas":
    st.title("Respostas já registradas")
    # Se for admin, mostra painel para escolher aba/usuário
    if st.session_state.usuario_logado in ["cid", "cleo"]:
        client = autenticar_gspread()
        sheet = client.open(SHEET_NAME)
        abas = [ws.title for ws in sheet.worksheets() if ws.title not in ["Usuarios", "Estoque", "Vendas"]]
        aba_escolhida = st.selectbox("Selecione o usuário/aba para visualizar:", abas)
        df_respostas = ler_respostas_sheets(aba_escolhida)
        st.write(f"Visualizando respostas da aba: **{aba_escolhida}**")
    else:
        df_respostas = ler_respostas_sheets(st.session_state.usuario_logado)

    if df_respostas.empty:
        st.info("Nenhuma resposta registrada ainda.")
    else:
        st.dataframe(df_respostas, use_container_width=True, hide_index=True)
        csv = df_respostas.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Baixar todas as respostas em CSV",
            data=csv,
            file_name="RPD.csv",
            mime="text/csv"
        )

elif opcao == "Estoque":
    st.title("Controle de Estoque")
    df_estoque = ler_estoque_sheets()

    if st.session_state.usuario_logado in ["cid", "cleo"]:
        st.subheader("Adicionar Novo Item ao Estoque")
        with st.form("form_add_item"):
            novo_item = st.text_input("Nome do Item (camisa, pulseira, etc.)")
            nova_variacao = st.text_input("Variação (cor, tamanho, etc.)")
            nova_quantidade = st.number_input("Quantidade", min_value=1, step=1)
            novo_preco = st.number_input("Preço (R$)", min_value=0.0, format="%.2f")
            submitted_add = st.form_submit_button("Adicionar Item")
            if submitted_add:
                adicionar_item_estoque(novo_item, nova_variacao, nova_quantidade, novo_preco)
                st.rerun()

    st.subheader("Registrar Venda")
    if not df_estoque.empty:
        with st.form("form_venda"):
            # Combina Item e Variação para a seleção
            itens_disponiveis = [f"{row['Item']} - {row['Variação']}" for index, row in df_estoque.iterrows()]
            item_vendido_str = st.selectbox("Selecione o item vendido", itens_disponiveis)
            quantidade_vendida = st.number_input("Quantidade Vendida", min_value=1, step=1)
            submitted_venda = st.form_submit_button("Registrar Venda")

            if submitted_venda:
                # Encontra o item e a variação selecionados
                item_selecionado, variacao_selecionada = item_vendido_str.split(" - ")
                
                # Encontra o índice do item no DataFrame
                idx = df_estoque[(df_estoque['Item'] == item_selecionado) & (df_estoque['Variação'] == variacao_selecionada)].index[0]
                
                # Atualiza a quantidade
                if df_estoque.loc[idx, 'Quantidade'] >= quantidade_vendida:
                    preco_unitario = df_estoque.loc[idx, 'Preço']
                    preco_total = quantidade_vendida * preco_unitario
                    df_estoque.loc[idx, 'Quantidade'] -= quantidade_vendida
                    atualizar_estoque_sheets(df_estoque)
                    datahora = datetime.now().strftime("%d/%m/%Y  %H:%M:%S")
                    registrar_venda_sheets(datahora, item_selecionado, variacao_selecionada, quantidade_vendida, preco_unitario, preco_total, st.session_state.nome_usuario)
                    st.success(f"Venda registrada! Total: R$ {preco_total:.2f}")
                    st.rerun()
                else:
                    st.error("Quantidade em estoque insuficiente para esta venda.")

    st.subheader("Estoque Atual")
    if df_estoque.empty:
        st.info("Nenhum item em estoque.")
    else:
        st.dataframe(df_estoque, use_container_width=True)

elif opcao == "Relatório de Vendas":
    st.title("Relatório de Vendas")
    if st.session_state.usuario_logado in ["cid", "cleo"]:
        client = autenticar_gspread()
        try:
            sheet = client.open(SHEET_NAME)
            worksheet = sheet.worksheet(WORKSHEET_VENDAS)
            df_vendas = get_as_dataframe(worksheet, evaluate_formulas=True, header=0)
            df_vendas = df_vendas.dropna(how="all")
            if df_vendas.empty:
                st.info("Nenhuma venda registrada ainda.")
            else:
                # Adiciona o filtro de data
                data_filtro = st.date_input("Filtrar vendas por dia")
                if data_filtro:
                    df_vendas['Data/Hora'] = pd.to_datetime(df_vendas['Data/Hora'], format='%d/%m/%Y  %H:%M:%S')
                    df_filtrado = df_vendas[df_vendas['Data/Hora'].dt.date == data_filtro]
                else:
                    df_filtrado = df_vendas

                st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
                total_arrecadado = pd.to_numeric(df_filtrado['Preço Total']).sum()
                st.metric(label="Total Arrecadado (filtrado)", value=f"R$ {total_arrecadado:.2f}")

        except gspread.exceptions.WorksheetNotFound:
            st.info("Nenhuma venda registrada ainda.")
        except Exception as e:
            st.error(f"Erro ao ler o relatório de vendas: {e}")
    else:
        st.warning("Acesso restrito a administradores.")


