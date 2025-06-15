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

# Função para salvar respostas no Google Sheets
def salvar_resposta_sheets(datahora, situacao, pensamentos, emocao, conclusao, resultado, usuario):
    client = autenticar_gspread()
    aba_destino = "Respostas" if usuario == "admin" else usuario
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
        # Adiciona usuário na aba "Usuarios"
        worksheet_usuarios = sheet.worksheet("Usuarios")
        df_usuarios = get_as_dataframe(worksheet_usuarios, evaluate_formulas=True, header=0)
        df_usuarios = df_usuarios.dropna(how="all")
        # Verifica se usuário já existe
        if usuario in df_usuarios['usuario'].astype(str).values:
            return False
        nova_linha = pd.DataFrame([{
            "usuario": str(usuario).strip(),
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
        except Exception:
            pass  # Se já existir, ignora
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
    
# Configuração inicial do Streamlit
if "usuario_autenticado" not in st.session_state:
    st.session_state.usuario_autenticado = False
    st.session_state.nome_usuario = ""

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
    st.stop()
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
    if st.button("Adicionar usuário"):
        st.session_state.mostrar_cadastro = True

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
opcao = st.sidebar.radio("Escolha uma opção:", ["Responder perguntas", "Visualizar respostas"])

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
        salvar_resposta_sheets(datahora, situacao, pensamentos, emocao, conclusao, resultado, st.session_state.nome_usuario)
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
    if st.session_state.usuario_logado == "admin":
        client = autenticar_gspread()
        sheet = client.open(SHEET_NAME)
        abas = [ws.title for ws in sheet.worksheets() if ws.title not in ["Usuarios"]]
        aba_escolhida = st.selectbox("Selecione o usuário/aba para visualizar:", abas)
        df_respostas = ler_respostas_sheets(aba_escolhida)
        st.write(f"Visualizando respostas da aba: **{aba_escolhida}**")
    else:
        df_respostas = ler_respostas_sheets(st.session_state.nome_usuario)

    if df_respostas.empty:
        st.info("Nenhuma resposta registrada ainda.")
    else:
        st.dataframe(df_respostas)
        csv = df_respostas.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Baixar todas as respostas em CSV",
            data=csv,
            file_name="RPD.csv",
            mime="text/csv"
        )