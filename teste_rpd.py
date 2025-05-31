import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from gspread_dataframe import set_with_dataframe, get_as_dataframe
import json
import io
from google.oauth2.service_account import Credentials  # <-- Novo import


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
def salvar_resposta_sheets(datahora, situacao, pensamentos, emocao, conclusao, resultado):
    client = autenticar_gspread()
    try:
        sheet = client.open(SHEET_NAME)
    except Exception:
        st.error("Não foi possível abrir a planilha. Verifique se compartilhou com o e-mail do serviço.")
        return
    try:
        worksheet = sheet.worksheet(WORKSHEET_NAME)
    except Exception:
        worksheet = sheet.add_worksheet(title=WORKSHEET_NAME, rows="1000", cols="10")
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
def ler_respostas_sheets():
    client = autenticar_gspread()
    try:
        sheet = client.open(SHEET_NAME)
        worksheet = sheet.worksheet(WORKSHEET_NAME)
        df = get_as_dataframe(worksheet, evaluate_formulas=True, header=0)
        df = df.dropna(how="all")  # Remove linhas completamente vazias
        return df
    except Exception:
        st.error(f"Erro ao acessar o Google Sheets: {e}")
        return pd.DataFrame(columns=[
            "Data/Hora",
            "Situação",
            "Pensamentos automáticos",
            "Emoção",
            "Conclusão",
            "Resultado"
        ])


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
        salvar_resposta_sheets(datahora, situacao, pensamentos, emocao, conclusao, resultado)
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
    df_respostas = ler_respostas_sheets()
    if df_respostas.empty:
        st.info("Nenhuma resposta registrada ainda.")
    else:
        st.dataframe(df_respostas)
        # Salva o Excel em memória para download
        buffer = io.BytesIO()
        df_respostas.to_excel(buffer, index=False, engine='openpyxl')
        buffer.seek(0)
        st.download_button(
            label="Baixar todas as respostas em Excel",
            data=buffer,
            file_name="RPD.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )