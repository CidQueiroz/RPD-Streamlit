import streamlit as st
import pandas as pd
from sheets import autenticar_gspread
from gspread_dataframe import set_with_dataframe, get_as_dataframe

# Nome da planilha e aba
SHEET_NAME = "RPD"
GOOGLE_ANALYTICS = """<script async src="https://www.googletagmanager.com/gtag/js?id=G-PJG10ZYPBS"></script>
                    <script>
                        window.dataLayer = window.dataLayer || [];
                        function gtag(){dataLayer.push(arguments);}
                        gtag('js', new Date());

                        gtag('config', 'G-PJG10ZYPBS');
                    </script>"""
st.html(GOOGLE_ANALYTICS)

def autenticar_usuario(usuario, senha):
    try:
        client = autenticar_gspread()
        sheet = client.open(SHEET_NAME)
        worksheet = sheet.worksheet("Usuarios")
        df_usuarios = get_as_dataframe(worksheet, evaluate_formulas=True, header=0)
        df_usuarios = df_usuarios.dropna(how="all")
        df_usuarios['usuario'] = df_usuarios['usuario'].astype(str).str.strip()
        df_usuarios['senha'] = df_usuarios['senha'].astype(str).str.strip()
        usuario = str(usuario).strip()
        senha = str(senha).strip()

        usuario_encontrado = df_usuarios[
            (df_usuarios['usuario'] == usuario) & (df_usuarios['senha'] == senha)
        ]
        if not usuario_encontrado.empty:
            st.session_state.usuario_logado = usuario_encontrado.iloc[0]['usuario']
            st.session_state.nome_usuario = usuario_encontrado.iloc[0]['nome']
            st.session_state.usuario_autenticado = True
            return True
        else:
            return False
    except Exception as e:
        st.error(f"Erro ao acessar a aba de usuários: {e}")
        return False

def adicionar_usuario(nome, usuario, senha):
    try:
        client = autenticar_gspread()
        sheet = client.open(SHEET_NAME)
        worksheet_usuarios = sheet.worksheet("Usuarios")
        df_usuarios = get_as_dataframe(worksheet_usuarios, evaluate_formulas=True, header=0)
        df_usuarios = df_usuarios.dropna(how="all")
        usuario = str(usuario).strip()
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