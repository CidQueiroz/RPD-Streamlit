import streamlit as st
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
from fpdf import FPDF
import os

# Configuração da página
st.set_page_config(page_title="Formulário com Envio de PDF", layout="centered")
st.title("Formulário de Perguntas")
st.write("Por favor, responda as perguntas abaixo:")

# Criação do formulário
with st.form(key="formulario"):
    # Pergunta 1 - Picklist (Checkbox multiple choice)
    st.subheader("Pergunta 1:")
    st.write("Quais linguagens de programação você conhece?")
    opcoes_linguagens = ["Python", "JavaScript", "Java", "Outra"]
    respostas_linguagens = {}
    for opcao in opcoes_linguagens:
        respostas_linguagens[opcao] = st.checkbox(opcao)
    
    # Pergunta 2 - Lista suspensa (Dropdown)
    st.subheader("Pergunta 2:")
    st.write("Qual o seu nível de experiência com programação?")
    nivel_experiencia = st.selectbox(
        "Selecione uma opção",
        ["Iniciante", "Intermediário", "Avançado", "Especialista"]
    )
    
    # Pergunta 3 - Campo de texto
    st.subheader("Pergunta 3:")
    st.write("Descreva um projeto em que você gostaria de trabalhar:")
    descricao_projeto = st.text_area("Sua resposta", height=150)
    
    # Campo para email
    st.subheader("Envio do resultado:")
    email_destino = st.text_input("Digite seu email para receber as respostas:")
    
    # Configurações do email (para ser preenchido com suas credenciais)
    email_remetente = 'cydy.potter@gmail.com'
    senha_remetente = 'daom kmgv lbnx syxb'
    
    # Botão de envio
    submitted = st.form_submit_button("Enviar Respostas")

# Função para criar o PDF
def criar_pdf(respostas_linguagens, nivel_experiencia, descricao_projeto):
    pdf = FPDF()
    pdf.add_page()
    
    # Configuração de fonte
    pdf.set_font("Arial", "B", 16)
    pdf.cell(190, 10, "Respostas do Formulário", ln=True, align="C")
    pdf.ln(10)
    
    # Pergunta 1
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "Pergunta 1: Quais linguagens de programação você conhece?", ln=True)
    pdf.set_font("Arial", "", 12)
    
    linguagens_selecionadas = [lang for lang, selected in respostas_linguagens.items() if selected]
    if linguagens_selecionadas:
        pdf.cell(190, 10, "Resposta: " + ", ".join(linguagens_selecionadas), ln=True)
    else:
        pdf.cell(190, 10, "Resposta: Nenhuma linguagem selecionada", ln=True)
    pdf.ln(5)
    
    # Pergunta 2
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "Pergunta 2: Qual o seu nível de experiência com programação?", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(190, 10, f"Resposta: {nivel_experiencia}", ln=True)
    pdf.ln(5)
    
    # Pergunta 3
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "Pergunta 3: Descreva um projeto em que você gostaria de trabalhar:", ln=True)
    pdf.set_font("Arial", "", 12)
    
    # Quebrar texto longo em linhas
    pdf.multi_cell(190, 10, f"Resposta: {descricao_projeto}")
    
    # Salvar o PDF
    pdf_path = "respostas_formulario.pdf"
    pdf.output(pdf_path)
    return pdf_path

# Função para enviar email com anexo
def enviar_email(remetente, senha, destinatario, anexo_path):
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = "Respostas do Formulário"
    
    texto_email = "Olá!\n\nSegue em anexo o PDF com as respostas do formulário que você preencheu.\n\nAtenciosamente,\nAplicativo de Formulário"
    msg.attach(MIMEText(texto_email))
    
    with open(anexo_path, "rb") as arquivo:
        parte = MIMEBase('application', 'octet-stream')
        parte.set_payload(arquivo.read())
    
    encoders.encode_base64(parte)
    parte.add_header('Content-Disposition', f'attachment; filename={os.path.basename(anexo_path)}')
    msg.attach(parte)
    
    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(remetente, senha)
        texto = msg.as_string()
        servidor.sendmail(remetente, destinatario, texto)
        servidor.quit()
        return True
    except Exception as e:
        st.error(f"Erro ao enviar email: {str(e)}")
        return False

# Processamento após o envio do formulário
if submitted:
    if not email_destino:
        st.error("Por favor, informe um email para receber os resultados.")
    elif not email_remetente or not senha_remetente:
        st.error("Por favor, informe as credenciais de email para envio.")
    else:
        with st.spinner("Processando respostas..."):
            # Criar o PDF
            pdf_path = criar_pdf(respostas_linguagens, nivel_experiencia, descricao_projeto)
            
            # Enviar o email
            if enviar_email(email_remetente, senha_remetente, email_destino, pdf_path):
                st.success(f"Respostas enviadas com sucesso para {email_destino}!")
                
                # Exibir resumo das respostas
                st.subheader("Resumo das respostas:")
                
                st.write("**Linguagens de programação:**")
                linguagens_selecionadas = [lang for lang, selected in respostas_linguagens.items() if selected]
                if linguagens_selecionadas:
                    st.write(", ".join(linguagens_selecionadas))
                else:
                    st.write("Nenhuma linguagem selecionada")
                
                st.write(f"**Nível de experiência:** {nivel_experiencia}")
                
                st.write("**Descrição do projeto:**")
                st.write(descricao_projeto)
                
                # Opção para baixar o PDF diretamente
                with open(pdf_path, "rb") as file:
                    st.download_button(
                        label="Baixar PDF",
                        data=file,
                        file_name="respostas_formulario.pdf",
                        mime="application/pdf"
                    )
            else:
                st.error("Não foi possível enviar o email. Por favor, verifique as credenciais e tente novamente.")

# Rodapé com informações
st.markdown("---")
st.markdown("### Observações importantes:")
st.markdown("""
- TESTE
""")