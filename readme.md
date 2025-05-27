# Registro RPD

Este projeto é um aplicativo Streamlit para registro e acompanhamento de respostas do modelo RPD (Registro de Pensamentos Disfuncionais). As respostas são armazenadas em um arquivo Excel (`RPD.xlsx`) na mesma pasta do projeto.

## Funcionalidades

- **Registro de respostas:**  
  Permite ao usuário preencher um formulário com perguntas abertas sobre situações, pensamentos, emoções, conclusões e resultados.
- **Visualização de respostas:**  
  Exibe todas as respostas já registradas em uma tabela e permite o download do arquivo Excel com todos os registros.

## Como usar

1. **Instale as dependências:**
   ```bash
   pip install streamlit pandas openpyxl
   ```

2. **Execute o aplicativo:**
   ```bash
   streamlit run teste_rpd.py
   ```

3. **Utilize o menu lateral** para alternar entre:
   - **Responder perguntas:** Preencha o formulário e envie suas respostas.
   - **Visualizar respostas:** Veja todas as respostas já registradas e faça o download do Excel.

## Estrutura do Excel

O arquivo `RPD.xlsx` contém as seguintes colunas:

- **Data/Hora:** Data e hora do registro (ex: 16/05/2025  19:45:13)
- **Situação:** Situação real, fluxo de pensamentos, devaneios ou recordações que levaram à emoção desagradável.
- **Pensamentos automáticos:** Pensamentos automáticos e o quanto acredita em cada um (0 a 100%).
- **Emoção:** Emoção sentida e intensidade (0 a 100%).
- **Conclusão:** Respostas racionais aos pensamentos automáticos e o quanto acredita em cada resposta (0 a 100%).
- **Resultado:** Quanto acredita agora nos pensamentos automáticos, emoções sentidas, intensidade e ações tomadas.

## Observações

- O arquivo Excel é criado automaticamente na primeira resposta.
- O download do Excel pode ser feito na tela de visualização das respostas.

---

Desenvolvido com [Streamlit](https://streamlit.io/).