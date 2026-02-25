# ⚖️ Fork do GPS Jus - Painel de Controle para Vara de Fazenda Pública

Este é um módulo para gestão e visualização de dados voltado para **Gabinetes de Varas de Fazenda Pública**. Ele permite uma análise rápida e eficiente da fila de processos conclusos, facilitando a triagem, organização de grupos de trabalho e acompanhamento de metas.

Este projeto é um **fork do GPS Jus**, otimizado especificamente para as necessidades das Varas de Fazenda Pública, desenvolvido por **Nailton Gomes** ([https://github.com/nailtongomes](https://github.com/nailtongomes)).

---

## 🚀 Funcionalidades Principais

- **📥 Carregamento Simples**: Basta fazer o upload da planilha extraída do sistema GPSJus.
- **🧹 Triagem e Limpeza**: Filtros automáticos para remover processos minutados, embargos de declaração, URV e sindicatos.
- **📂 Grupos Temáticos**: Identificação automática de processos de Saúde, INSS, Mandados de Segurança e Ações Civis Públicas.
- **🔥 Filtro de Urgência**: Destaque para processos parados há mais de 80 dias.
- **👥 Grupos de Trabalho**: Agrupamento inteligente por classe ou assunto para aumentar a produtividade.
- **📈 Estatísticas em Tempo Real**: Visualize a distribuição de dias conclusos e o volume por classe processual.

---

## 🛠️ Tecnologias Utilizadas

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/) (Interface Web)
- [Pandas](https://pandas.pydata.org/) (Processamento de Dados)
- [Openpyxl](https://openpyxl.readthedocs.io/) (Leitura de Excel)

---

## 🏃 Como Executar o Projeto Localmente

### 1. Pré-requisitos
Certifique-se de ter o Python instalado em sua máquina.

### 2. Instalação de Dependências
Abra o terminal na pasta do projeto e execute:
```bash
pip install streamlit pandas openpyxl
```

### 3. Iniciar a Aplicação
Execute o seguinte comando:
```bash
streamlit run app.py
```
ou
```bash
python -m streamlit run app.py
```
A aplicação abrirá automaticamente no seu navegador padrão.

---

## 📖 Como Usar

1. Extraia a planilha de processos conclusos do sistema **GPSJus**.
2. No painel lateral do **GPS Jus - Painel de Gabinete**, faça o upload do arquivo `.xlsx`.
3. Utilize os filtros na barra lateral para refinar sua lista de trabalho.
4. Navegue pelas abas para ver a lista detalhada, sugestões de grupos ou estatísticas gerais.
5. Se necessário, exporte a lista filtrada de volta para Excel.

---

## ⚠️ Dica Importante (Solução de Erros)

Se encontrar um erro ao carregar a planilha, tente o seguinte:
1. Abra o arquivo original no seu computador usando o **Microsoft Excel**.
2. Vá em **Arquivo > Salvar** (ou `Ctrl + S`).
3. Tente carregar o arquivo novamente no sistema. 
*Isso geralmente corrige problemas de formatação gerados na exportação automática de sistemas web.*

---

## 👨‍💻 Créditos
- **Desenvolvedor**: Nailton Gomes
- **Baseado no projeto**: GPS Jus
