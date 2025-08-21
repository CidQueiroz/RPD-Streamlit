import gspread
from google.oauth2.service_account import Credentials
import json
import streamlit as st
import pandas as pd
from gspread_dataframe import set_with_dataframe, get_as_dataframe

SHEET_NAME = "RPD"
WORKSHEET_NAME = "Respostas"
GOOGLE_ANALYTICS = """<script async src="https://www.googletagmanager.com/gtag/js?id=G-PJG10ZYPBS"></script>
                    <script>
                        window.dataLayer = window.dataLayer || [];
                        function gtag(){dataLayer.push(arguments);}
                        gtag('js', new Date());

                        gtag('config', 'G-PJG10ZYPBS');
                    </script>"""
st.html(GOOGLE_ANALYTICS)

# Autenticação com Google Sheets
def autenticar_gspread():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    client = gspread.authorize(creds)
    return client

# Função para salvar respostas no Google Sheets
def salvar_resposta_sheets(datahora, situacao, pensamentos, emocao, conclusao, resultado, usuario_login):
    client = autenticar_gspread()
    aba_destino = "Respostas" if usuario_login == "cid" else usuario_login
    try:
        sheet = client.open(SHEET_NAME)
    except Exception:
        st.error("Não foi possível abrir a planilha. Verifique se compartilhou com o e-mail do serviço.")
        return
    try:
        worksheet = sheet.worksheet(aba_destino)
    except Exception:
        worksheet = sheet.add_worksheet(title=aba_destino, rows=1000, cols=10)
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


def salvar_consistencia_sheets(data_hoje, atividade, usuario_login):
    """
    Salva um novo registro de consistência em uma aba específica do Google Sheets.
    """
    client = autenticar_gspread() # Reutiliza sua função de autenticação
    aba_destino = "D.Bordo" # Nome fixo para a nova aba

    try:
        sheet = client.open(SHEET_NAME) # Reutiliza o nome da sua planilha principal
    except Exception as e:
        st.error(f"Não foi possível abrir a planilha. Erro: {e}")
        return

    try:
        worksheet = sheet.worksheet(aba_destino)
    except gspread.WorksheetNotFound:
        # Se a aba não existir, cria uma nova com os cabeçalhos corretos
        worksheet = sheet.add_worksheet(title=aba_destino, rows=1000, cols=3)
        worksheet.append_row(["Data", "Atividade", "Usuario"])
        st.toast(f"Aba '{aba_destino}' criada com sucesso.")

    # Adiciona a nova linha de forma eficiente
    nova_linha = [data_hoje, atividade, usuario_login]
    worksheet.append_row(nova_linha)


def carregar_log_diario_sheets():
    """Carrega o log de operações diárias (POD) do Google Sheets."""
    try:
        client = autenticar_gspread()
        sheet = client.open(SHEET_NAME)
        worksheet = sheet.worksheet("Log Diario POD") # Nome da nova aba
        df = get_as_dataframe(worksheet, evaluate_formulas=True, header=0)
        # Remove linhas que possam ter sido importadas como totalmente vazias
        df = df.dropna(how='all')
        if not df.empty:
            df['Status'] = df['Status'].astype(bool) # Garante que o status seja booleano
            df['Data'] = df['Data'].astype(str)
        return df
    except gspread.WorksheetNotFound:
        # Se a aba não existe, retorna um DataFrame vazio com a estrutura correta
        return pd.DataFrame(columns=['Data', 'Tarefa', 'Status'])
    except Exception as e:
        st.error(f"Falha ao carregar o 'Log Diario POD'. Verifique se a aba existe. Erro: {e}")
        return pd.DataFrame(columns=['Data', 'Tarefa', 'Status'])


def salvar_log_diario_sheets(df_completo):
    """Salva o DataFrame completo do log diário no Google Sheets, substituindo os dados antigos."""
    try:
        client = autenticar_gspread()
        sheet = client.open(SHEET_NAME)
        aba_destino = "Log Diario POD"
        try:
            worksheet = sheet.worksheet(aba_destino)
        except gspread.WorksheetNotFound:
            # Cria a aba se ela não existir
            worksheet = sheet.add_worksheet(title=aba_destino, rows=1000, cols=3)
            worksheet.append_row(["Data", "Tarefa", "Status"])
        
        # Limpa a planilha e escreve o DataFrame atualizado
        # (Seguindo a mesma lógica da sua função de RPD)
        worksheet.clear()
        set_with_dataframe(worksheet, df_completo)
        st.toast("Progresso diário salvo na nuvem.", icon="☁️")
    except Exception as e:
        st.error(f"Não foi possível salvar o log diário no Google Sheets. Erro: {e}")
