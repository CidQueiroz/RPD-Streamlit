# estoque.py

import streamlit as st
import pandas as pd
from sheets import autenticar_gspread
import gspread
from gspread_dataframe import set_with_dataframe, get_as_dataframe

# Nome da planilha e aba
SHEET_NAME = "RPD"
WORKSHEET_ESTOQUE = "Estoque"
WORKSHEET_VENDAS = "Vendas"

# >>> CORREÇÃO ESTRATÉGICA APLICADA AQUI <<<
def ler_estoque_sheets():
    """
    Função centralizada e robusta para ler o estoque.
    SEMPRE retorna as colunas 'Quantidade' e 'Preço' como tipos numéricos corretos.
    """
    client = autenticar_gspread()
    sheet = client.open(SHEET_NAME)

    try:
        worksheet = sheet.worksheet(WORKSHEET_ESTOQUE)
        df = get_as_dataframe(worksheet, evaluate_formulas=True, header=0)
        df = df.dropna(how="all")

        # Garante a conversão de tipos imediatamente após a leitura.
        if not df.empty:
            # errors='coerce' transforma qualquer valor que não seja número em NaN (Not a Number)
            df['Quantidade'] = pd.to_numeric(df['Quantidade'], errors='coerce').fillna(0).astype(int)
            # .fillna(0) substitui os NaN por 0.
            df['Preço'] = pd.to_numeric(df['Preço'], errors='coerce').fillna(0.0).astype(float)
            # .astype(int) ou .astype(float) define o tipo final.

        return df
    except gspread.exceptions.WorksheetNotFound:
        # Se a aba não existe, cria e retorna um DataFrame vazio com as colunas corretas.
        worksheet = sheet.add_worksheet(title=WORKSHEET_ESTOQUE, rows=1000, cols=10)
        worksheet.append_row(["Item", "Variação", "Quantidade", "Preço"])
        return pd.DataFrame(columns=["Item", "Variação", "Quantidade", "Preço"])
    except Exception as e:
        st.error(f"Erro ao acessar a aba de estoque: {e}")
        return pd.DataFrame(columns=["Item", "Variação", "Quantidade", "Preço"])

# As outras funções permanecem as mesmas, mas se beneficiarão da leitura robusta
def adicionar_item_estoque(item, variacao, quantidade, preco=None):
    client = autenticar_gspread()
    try:
        sheet = client.open(SHEET_NAME)
        worksheet = sheet.worksheet(WORKSHEET_ESTOQUE)
        # Usamos nossa função robusta para garantir os tipos corretos
        df = ler_estoque_sheets() 

        item_padronizado = item.strip().capitalize()
        variacao_padronizada = variacao.strip().capitalize()

        filtro = (df['Item'].astype(str).str.strip().str.capitalize() == item_padronizado) & \
                 (df['Variação'].astype(str).str.strip().str.capitalize() == variacao_padronizada)
        
        if not df[filtro].empty:
            idx = df[filtro].index[0]
            # A soma agora é segura, pois 'Quantidade' é sempre um número.
            df.loc[idx, 'Quantidade'] += quantidade 
            st.success(f"Quantidade de {item_padronizado} - {variacao_padronizada} atualizada para {df.loc[idx, 'Quantidade']}!")
        else:
            if preco is None:
                st.error("Preço é obrigatório para novos itens.")
                return
            novo_item = pd.DataFrame([{
                "Item": item_padronizado,
                "Variação": variacao_padronizada,
                "Quantidade": int(quantidade),
                "Preço": float(preco)
            }])
            df = pd.concat([df, novo_item], ignore_index=True)
            st.success("Novo item adicionado ao estoque com sucesso!")
        
        worksheet.clear()
        set_with_dataframe(worksheet, df)
        
    except Exception as e:
        st.error(f"Erro ao adicionar/atualizar item ao estoque: {e}")

def registrar_venda_sheets(datahora, item, variacao, quantidade, preco_unitario, preco_total, vendedor):
    client = autenticar_gspread()
    try:
        sheet = client.open(SHEET_NAME)
        try:
            worksheet = sheet.worksheet(WORKSHEET_VENDAS)
        except gspread.exceptions.WorksheetNotFound:
            worksheet = sheet.add_worksheet(title=WORKSHEET_VENDAS, rows=1000, cols=10)
            worksheet.append_row(["Data/Hora", "Item", "Variação", "Quantidade", "Preço Unitário", "Preço Total", "Vendedor"])
        
        df = get_as_dataframe(worksheet, evaluate_formulas=True, header=0)
        nova_venda = pd.DataFrame([{
            "Data/Hora": datahora,
            "Item": item,
            "Variação": variacao,
            "Quantidade": int(quantidade),
            "Preço Unitário": float(preco_unitario),
            "Preço Total": float(preco_total),
            "Vendedor": vendedor
        }])
        df = pd.concat([df, nova_venda], ignore_index=True)
        worksheet.clear()
        set_with_dataframe(worksheet, df)
    except Exception as e:
        st.error(f"Erro ao registrar venda: {e}")

def atualizar_estoque_sheets(df_estoque):
    client = autenticar_gspread()
    try:
        sheet = client.open(SHEET_NAME)
        worksheet = sheet.worksheet(WORKSHEET_ESTOQUE)
        worksheet.clear()
        set_with_dataframe(worksheet, df_estoque)
    except Exception as e:
        st.error(f"Erro ao atualizar o estoque: {e}")