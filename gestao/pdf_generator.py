
from fpdf import FPDF
from datetime import datetime

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Recibo de Venda', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def criar_recibo_venda(sale_details: dict) -> bytes:
    """Gera um recibo de venda em PDF com base nos detalhes fornecidos."""
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)

    # --- Informações da Empresa e Venda ---
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, sale_details.get('empresa_nome', 'N/A'), 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f"Data da Venda: {sale_details.get('data_venda', 'N/A')}", 0, 1, 'L')
    pdf.cell(0, 10, f"Vendedor: {sale_details.get('vendedor_nome', 'N/A')}", 0, 1, 'L')
    
    # Adiciona informações do cliente se existirem
    if sale_details.get('cliente_nome'):
        pdf.cell(0, 10, f"Cliente: {sale_details['cliente_nome']}", 0, 1, 'L')
    if sale_details.get('cliente_cpf'):
        pdf.cell(0, 10, f"CPF: {sale_details['cliente_cpf']}", 0, 1, 'L')
        
    pdf.ln(10)

    # --- Tabela de Itens ---
    pdf.set_font('Arial', 'B', 12)
    # Cabeçalhos
    pdf.cell(80, 10, 'Item', 1, 0, 'C')
    pdf.cell(30, 10, 'Qtd', 1, 0, 'C')
    pdf.cell(40, 10, 'Preço Unit.', 1, 0, 'C')
    pdf.cell(40, 10, 'Preço Total', 1, 1, 'C')

    pdf.set_font('Arial', '', 12)
    # Linha do item
    item_nome = f"{sale_details.get('item', '')} - {sale_details.get('variacao', '')}"
    pdf.cell(80, 10, item_nome, 1, 0, 'L')
    pdf.cell(30, 10, str(sale_details.get('quantidade', 0)), 1, 0, 'C')
    pdf.cell(40, 10, f"R$ {sale_details.get('preco_unitario', 0):.2f}", 1, 0, 'R')
    pdf.cell(40, 10, f"R$ {sale_details.get('preco_total', 0):.2f}", 1, 1, 'R')
    pdf.ln(10)

    # --- Total Geral ---
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, f"Valor Total da Venda: R$ {sale_details.get('preco_total', 0):.2f}", 0, 1, 'R')

    return bytes(pdf.output(dest='S'))
