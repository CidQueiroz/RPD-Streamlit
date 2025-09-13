
import pytest
import datetime
from core.database import execute_command, fetch_data

@pytest.fixture(scope="session")
def empresa_de_teste():
    """Garante que a empresa de teste exista e retorna seu ID."""
    # Usa um nome fixo para evitar múltiplas inserções em execuções de teste
    nome_empresa = "EMPRESA_TESTE_PYTEST"
    execute_command("INSERT IGNORE INTO empresas (nome_empresa) VALUES (:nome)", {"nome": nome_empresa})
    empresa_data = fetch_data("SELECT id_empresa FROM empresas WHERE nome_empresa = :nome", {"nome": nome_empresa})
    empresa_id = empresa_data[0]['id_empresa']
    return empresa_id

@pytest.fixture
def usuario_de_teste_gerenciado(empresa_de_teste):
    """Cria um usuário de teste e o remove no final."""
    user_info = {
        "nome": "Test User Pytest", 
        "usuario": f"pytest_user_{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}", 
        "senha": "xyz",
        "empresa_fk": empresa_de_teste,
        "is_staff": False
    }
    execute_command("INSERT INTO usuarios (nome, usuario, senha, empresa_fk, is_staff) VALUES (:nome, :usuario, :senha, :empresa_fk, :is_staff)", user_info)
    
    user_data = fetch_data("SELECT id_usuario FROM usuarios WHERE usuario = :usuario", {"usuario": user_info["usuario"]})
    user_id = user_data[0]['id_usuario'] if user_data else None

    yield user_id

    # --- TEARDOWN ---
    if user_id:
        execute_command("DELETE FROM usuarios WHERE id_usuario = :id", {"id": user_id})

@pytest.fixture
def item_de_teste_gerenciado(empresa_de_teste):
    """Cria um item de teste no DB, associado à empresa de teste, e o remove depois."""
    from gestao.estoque import adicionar_ou_atualizar_item
    nome_item = f"item_teste_auto_{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    variacao = "independente"
    preco = 12.50
    quantidade_inicial = 10
    
    adicionar_ou_atualizar_item(nome_item, variacao, quantidade_inicial, preco, id_empresa=empresa_de_teste)
    
    item_inserido = fetch_data("SELECT id_item FROM estoque WHERE item = :nome AND variacao = :var", {"nome": nome_item, "var": variacao})
    item_id = item_inserido[0]['id_item'] if item_inserido else None

    yield nome_item, variacao, item_id

    # --- TEARDOWN ---
    if item_id:
        execute_command("DELETE FROM vendas WHERE estoque_fk = :id", {"id": item_id})
        execute_command("DELETE FROM estoque WHERE id_item = :id", {"id": item_id})
