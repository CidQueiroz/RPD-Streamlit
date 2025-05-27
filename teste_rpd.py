import streamlit as st
import pandas as pd
import os
from datetime import datetime
import io

# Caminho do arquivo Excel
EXCEL_PATH = "RPD.xlsx"

# Função para salvar respostas no Excel
def salvar_resposta_excel(datahora, situacao, pensamentos, emocao, conclusao, resultado):
    nova_resposta = {
        "Data/Hora": datahora,
        "Situação": situacao,
        "Pensamentos automáticos": pensamentos,
        "Emoção": emocao,
        "Conclusão": conclusao,
        "Resultado": resultado
    }
    if os.path.exists(EXCEL_PATH):
        df = pd.read_excel(EXCEL_PATH)
        df = pd.concat([df, pd.DataFrame([nova_resposta])], ignore_index=True)
    else:
        df = pd.DataFrame([nova_resposta])
    df.to_excel(EXCEL_PATH, index=False)


# Função para ler respostas do Excel
def ler_respostas_excel():
    if os.path.exists(EXCEL_PATH):
        return pd.read_excel(EXCEL_PATH)
    else:
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
        salvar_resposta_excel(datahora, situacao, pensamentos, emocao, conclusao, resultado)
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
    df_respostas = ler_respostas_excel()
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



