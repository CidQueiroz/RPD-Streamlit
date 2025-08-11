import streamlit as st
import pandas as pd
from sheets import autenticar_gspread
import gspread
from gspread_dataframe import set_with_dataframe, get_as_dataframe

# Nome da planilha e aba
SHEET_NAME = "RPD"
WORKSHEET_ESTOQUE = "Estoque"
WORKSHEET_VENDAS = "Vendas"

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
        worksheet = sheet.add_worksheet(title=WORKSHEET_ESTOQUE, rows="1000", cols="10")
        worksheet.append_row(["Item", "Variação", "Quantidade", "Preço"])
        return pd.DataFrame(columns=["Item", "Variação", "Quantidade", "Preço"])
    except Exception as e:
        st.error(f"Erro ao acessar a aba de estoque: {e}")
        return pd.DataFrame(columns=["Item", "Variação", "Quantidade", "Preço"])

def adicionar_item_estoque(item, variacao, quantidade, preco=None):
    client = autenticar_gspread()
    try:
        sheet = client.open(SHEET_NAME)
        worksheet = sheet.worksheet(WORKSHEET_ESTOQUE)
        df = get_as_dataframe(worksheet, evaluate_formulas=True, header=0)
        df = df.dropna(how="all")

        item_padronizado = item.strip().capitalize()
        variacao_padronizada = variacao.strip().capitalize()

        filtro = (df['Item'].astype(str).str.strip().str.capitalize() == item_padronizado) & \
                 (df['Variação'].astype(str).str.strip().str.capitalize() == variacao_padronizada)
        
        if not df[filtro].empty:
            idx = df[filtro].index[0]
            df.loc[idx, 'Quantidade'] = pd.to_numeric(df.loc[idx, 'Quantidade']) + quantidade
            st.success(f"Quantidade de {item_padronizado} - {variacao_padronizada} atualizada para {int(df.loc[idx, 'Quantidade'])}!")
        else:
            if preco is None:
                st.error("Preço é obrigatório para novos itens.")
                return
            novo_item = pd.DataFrame([{
                "Item": item_padronizado,
                "Variação": variacao_padronizada,
                "Quantidade": quantidade,
                "Preço": preco
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

def atualizar_estoque_sheets(df_estoque):
    client = autenticar_gspread()
    try:
        sheet = client.open(SHEET_NAME)
        worksheet = sheet.worksheet(WORKSHEET_ESTOQUE)
        worksheet.clear()
        set_with_dataframe(worksheet, df_estoque)
    except Exception as e:
        st.error(f"Erro ao atualizar o estoque: {e}")
