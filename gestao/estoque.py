import streamlit as st
import pandas as pd
from core.database import (
    fetch_data,
    fetch_data_as_dataframe,
    execute_command,
    _display_error,
)


def ler_estoque(id_empresa: int):
    """Lê os itens de estoque de uma empresa específica."""
    try:
        query = "SELECT id_item, item, variacao, quantidade, preco FROM estoque WHERE empresa_fk = :id_empresa ORDER BY item, variacao"
        return fetch_data_as_dataframe(query, {"id_empresa": id_empresa})
    except Exception as e:
        _display_error(f"Erro ao ler estoque: {e}")
        return pd.DataFrame()


def adicionar_ou_atualizar_item(
    item: str, variacao: str, quantidade: int, preco: float, id_empresa: int
):
    """Adiciona ou atualiza um item no estoque de uma empresa específica."""
    try:
        sql_check = "SELECT id_item, quantidade FROM estoque WHERE item = :item AND variacao = :variacao AND empresa_fk = :id_empresa"
        params_check = {"item": item, "variacao": variacao, "id_empresa": id_empresa}
        result = fetch_data(sql_check, params_check)

        if result:  # Item existe, ATUALIZA
            item_existente = result[0]
            nova_quantidade = item_existente["quantidade"] + quantidade
            sql_update = "UPDATE estoque SET quantidade = :quantidade WHERE id_item = :id_item AND empresa_fk = :id_empresa"
            params_update = {
                "quantidade": nova_quantidade,
                "id_item": item_existente["id_item"],
                "id_empresa": id_empresa,
            }
            execute_command(sql_update, params_update)
            st.success(
                f'Estoque de "{item} - {variacao}" atualizado para {nova_quantidade}!'
            )
        else:  # Item não existe, INSERE
            if preco is None:
                _display_error("O preço é obrigatório para adicionar um novo item.")
                return False
            sql_insert = "INSERT INTO estoque (item, variacao, quantidade, preco, empresa_fk) VALUES (:item, :variacao, :quantidade, :preco, :id_empresa)"
            params_insert = {
                "item": item,
                "variacao": variacao,
                "quantidade": quantidade,
                "preco": preco,
                "id_empresa": id_empresa,
            }
            execute_command(sql_insert, params_insert)
            st.success(f'Item "{item} - {variacao}" adicionado ao estoque!')
        return True
    except Exception as e:
        _display_error(f"Erro ao adicionar ou atualizar item: {e}")
        return False


def registrar_venda(
    data_venda: str, estoque_id: int, quantidade: int, usuario_id: int, id_empresa: int
):
    """Registra uma nova venda para uma empresa específica."""
    try:
        # 1. Buscar o preço unitário do item para garantir consistência
        produto_info = fetch_data(
            "SELECT preco FROM estoque WHERE id_item = :id AND empresa_fk = :id_empresa",
            params={"id": estoque_id, "id_empresa": id_empresa},
        )
        if not produto_info:
            _display_error(
                f"Não foi possível encontrar o item de estoque com ID {estoque_id} nesta empresa."
            )
            return False
        preco_unitario = produto_info[0]["preco"]

        # 2. Inserir o registro da venda
        sql_venda = """
            INSERT INTO vendas (data_hora, estoque_fk, quantidade, preco_unitario, vendedor_fk, empresa_fk)
            VALUES (:data_hora, :estoque_fk, :quantidade, :preco_unitario, :vendedor_fk, :id_empresa)
        """
        params_venda = {
            "data_hora": data_venda,
            "estoque_fk": estoque_id,
            "quantidade": quantidade,
            "preco_unitario": preco_unitario,
            "vendedor_fk": usuario_id,
            "id_empresa": id_empresa,
        }

        rows_affected_venda = execute_command(sql_venda, params_venda)
        if not rows_affected_venda:
            _display_error("A inserção da venda falhou.")
            return False

        # 3. Atualizar a quantidade no estoque
        sql_estoque = "UPDATE estoque SET quantidade = quantidade - :quantidade WHERE id_item = :id_item AND empresa_fk = :id_empresa"
        params_estoque = {
            "quantidade": quantidade,
            "id_item": estoque_id,
            "id_empresa": id_empresa,
        }
        execute_command(sql_estoque, params_estoque)

        # A mensagem de sucesso agora é tratada pela interface principal
        # st.success(f"Venda registrada com sucesso! Total: R$ {valor_total:.2f}")
        return True
    except Exception as e:
        _display_error(f"Erro ao registrar venda: {e}")
        return False
