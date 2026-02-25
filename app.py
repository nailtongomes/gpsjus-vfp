import streamlit as st
import pandas as pd
import io

# Set page configuration
st.set_page_config(
    page_title="GPS Jus - Painel de Gabinete",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for premium look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    /* Premium Cards */
    div[data-testid="stMetric"] {
        background-color: white;
        padding: 24px !important;
        border-radius: 16px !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05) !important;
        border: 1px solid rgba(0, 0, 0, 0.05) !important;
    }
    
    /* Titles */
    h1 {
        color: #0f172a !important;
        font-weight: 700 !important;
        letter-spacing: -0.025em !important;
    }
    
    h3 {
        color: #334155 !important;
        font-weight: 600 !important;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.3) !important;
        filter: brightness(1.1);
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        height: 45px;
        white-space: pre-wrap;
        background-color: white;
        border-radius: 8px 8px 0px 0px;
        gap: 1px;
        padding: 10px 20px;
        border: 1px solid #e2e8f0;
    }

    .stTabs [aria-selected="true"] {
        background-color: #1e3a8a !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is None:
        return None
    try:
        # User specified: Skip first row, column names in second row (header=1)
        # Also remove last row (footer)
        df = pd.read_excel(uploaded_file, header=1)
        
        # Remove empty columns if any
        df = df.dropna(axis=1, how='all')
        
        # Remove last row if it's noise
        if len(df) > 0:
            df = df[:-1]
            
        # Refinement: Remove columns 'SISTEMA' and 'FÍSICO / ELETRÔNICO?'
        cols_to_drop = ['SISTEMA', 'FÍSICO / ELETRÔNICO?']
        df = df.drop(columns=[c for c in cols_to_drop if c in df.columns])
        
        # Refinement: Extract 'ANO' from 'INÍCIO'
        if 'INÍCIO' in df.columns:
            df['INÍCIO'] = pd.to_datetime(df['INÍCIO'], errors='coerce')
            df['ANO'] = df['INÍCIO'].dt.year.astype(str).replace('nan', 'N/A')
            
        return df
    except Exception as e:
        st.error(f"⚠️ Erro ao ler a planilha: {e}")
        st.warning("Dica: Frequentemente, problemas de leitura em arquivos baixados de sistemas podem ser resolvidos abrindo o arquivo no Excel e salvando-o novamente (Arquivo > Salvar) antes de fazer o upload aqui.")
        return None

def main():
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/scales.png", width=64)
        st.title("GPS Jus")
        st.caption("Visualização de Vara de Fazenda Pública")
        st.markdown("---")
        
        uploaded_file = st.file_uploader("📥 Carregar Planilha Conclusos", type=["xlsx"])
        
        if uploaded_file:
            st.success("Planilha carregada!")
            if st.button("🔄 Substituir Planilha"):
                st.cache_data.clear()
                st.rerun()
        
        st.markdown("---")
        st.markdown("""
            <div style='font-size: 0.8rem; color: #666; margin-top: 50px;'>
                <b>Fork do GPS Jus</b><br>
                Otimizado para Varas de Fazenda Pública<br>
                Elaborado por <b>Nailton Gomes</b>
            </div>
        """, unsafe_allow_html=True)

    # Main Area
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        
        if df is not None:
            # Filters in the sidebar
            with st.sidebar:
                st.header("🔍 Filtros")
                
                # CLEANING AND SCREENING (Legacy Logic)
                with st.expander("🧹 Limpeza e Triagem", expanded=False):
                    remover_minutados = st.checkbox("Remover Minutados", value=True, help="Ocultar processos que já possuem minuta (Tarefa 'Assinar')")
                    remover_ed = st.checkbox("Remover Emb. Declaração", value=False)
                    remover_urv = st.checkbox("Remover URV", value=False)
                    remover_sindicatos = st.checkbox("Remover Sindicatos", value=False)

                # THEMATIC GROUPS (Legacy Logic)
                with st.expander("📂 Grupos Temáticos", expanded=False):
                    filter_saude = st.checkbox("⚕️ Apenas Saúde")
                    filter_inss = st.checkbox("👴 Apenas INSS")
                    filter_ms = st.checkbox("📜 Mandado de Segurança")
                    filter_acp = st.checkbox("⚖️ ACP / Ação Popular")
                    filter_metas = st.checkbox("🎯 Pendente de Meta")

                st.markdown("---")
                # Urgency Filter (> 80 days)
                urgency_only = st.checkbox("🔥 Urgência (> 80 dias)", help="Mostrar apenas processos com mais de 80 dias conclusos")
                
                # Etiqueta Filters
                st.markdown("---")
                st.subheader("🏷️ Etiquetas PJe")
                etiqueta_contains = st.text_input("Contém etiqueta:", placeholder="Ex: Prioridade")
                etiqueta_not_contains = st.text_input("Não contém etiqueta:", placeholder="Ex: Aguardando")
                
                # Year Filter
                st.markdown("---")
                if 'ANO' in df.columns:
                    years = sorted(df['ANO'].unique().tolist(), reverse=True)
                    selected_years = st.multiselect("Filtrar por Ano (Início)", options=years, default=years)
                else:
                    selected_years = []

                # Specific filters based on discovered columns
                st.markdown("---")
                col_options = {
                    "CLASSE": "Classe",
                    "ASSUNTO": "Assunto",
                    "TIPO CONCLUSÃO": "Tipo de Conclusão",
                    "PENDENTE DE META?": "Pendente de Meta",
                    "PRIORIDADE(S)": "Prioridade"
                }
                
                filters = {}
                for col_key, label in col_options.items():
                    if col_key in df.columns:
                        options = ["Todos"] + sorted(df[col_key].dropna().unique().tolist())
                        filters[col_key] = st.selectbox(f"Filtrar por {label}", options)
                
                # Numeric filter for "DIAS CONCLUSO"
                if "DIAS CONCLUSO" in df.columns:
                    min_days = int(df["DIAS CONCLUSO"].min())
                    max_days = int(df["DIAS CONCLUSO"].max())
                    days_range = st.slider("Dias Concluso (Intervalo)", min_days, max_days, (min_days, max_days))
                    filters["DIAS CONCLUSO"] = days_range

            # Apply filters
            filtered_df = df.copy()

            # --- APPLY CLEANING LOGIC ---
            if remover_minutados and "TAREFAS PJE" in filtered_df.columns:
                filtered_df = filtered_df[~filtered_df["TAREFAS PJE"].fillna("").str.contains("Assinar ", case=False)]
            
            if remover_ed and "TAREFAS PJE" in filtered_df.columns:
                filtered_df = filtered_df[~filtered_df["TAREFAS PJE"].fillna("").str.contains("Emb. Declaração ", case=False)]
            
            if remover_urv:
                if "ASSUNTO" in filtered_df.columns:
                    filtered_df = filtered_df[~filtered_df["ASSUNTO"].fillna("").str.contains("URV Lei 8.880/1994", case=False)]
                if "ETIQUETAS PJE" in filtered_df.columns:
                    filtered_df = filtered_df[~filtered_df["ETIQUETAS PJE"].fillna("").str.contains("URV", case=False)]

            if remover_sindicatos and "ETIQUETAS PJE" in filtered_df.columns:
                sindicatos_patterns = ["3 - SINTE", "3 - SINAI", "3 - SINSENAT", "SINSENAT"]
                for pat in sindicatos_patterns:
                    filtered_df = filtered_df[~filtered_df["ETIQUETAS PJE"].fillna("").str.contains(pat, case=False)]

            # --- APPLY THEMATIC GROUPS LOGIC ---
            if filter_saude and "ASSUNTO" in filtered_df.columns:
                saude_assuntos = [
                    "11884 - Fornecimento de Medicamentos", "12506 - Unidade de terapia intensiva (UTI) / unidade de cuidados intensivos (UCI)",
                    "11885 - Unidade de terapia intensiva (UTI) ou unidade de cuidados intensivos (UCI)", "12484 - Fornecimento de medicamentos",
                    "10356 - Assistência Médico-Hospitalar", "10064 - Saúde", "11854 - Saúde Mental", "12501 - Cirurgia",
                    "12502 - Eletiva", "12508 - Internação compulsória", "12483 - Internação/Transferência Hospitalar",
                    "11856 - Hospitais e Outras Units de Saúde", "11883 - Tratamento Médico-Hospitalar",
                    "12491 - Tratamento médico-hospitalar", "11847 - ASSISTÊNCIA SOCIAL"
                ]
                filtered_df = filtered_df[filtered_df["ASSUNTO"].isin(saude_assuntos)]

            if filter_inss and "ASSUNTO" in filtered_df.columns:
                inss_assuntos = [
                    "10567 - Aposentadoria por Invalidez Acidentária", "6095 - Aposentadoria por Invalidez",
                    "6101 - Auxílio-Doença Previdenciário", "6107 - Auxílio-Acident (Art. 86)",
                    "7757 - Auxílio-Doença Acidentário", "6111 - Movimentos Repetitivos/Tenossinovite/LER/DORT",
                    "6108 - Incapacidade Laborativa Parcial", "6110 - Incapacidade Laborativa Temporária",
                    "6109 - Incapacidade Laborativa Permanente"
                ]
                filtered_df = filtered_df[filtered_df["ASSUNTO"].isin(inss_assuntos)]

            if filter_ms and "CLASSE" in filtered_df.columns:
                ms_classes = ["120 - MANDADO DE SEGURANÇA CÍVEL", "1710 - MANDADO DE SEGURANÇA CRIMINAL"]
                filtered_df = filtered_df[filtered_df["CLASSE"].isin(ms_classes)]

            if filter_acp and "CLASSE" in filtered_df.columns:
                acp_classes = [
                    "64 - AÇÃO CIVIL DE IMPROBIDADE ADMINISTRATIVA", "1690 - (ECA) AÇÃO CIVIL PÚBLICA INFÂNCIA E JUVENTUDE",
                    "65 - AÇÃO CIVIL PÚBLICA", "66 - AÇÃO POPULAR"
                ]
                filtered_df = filtered_df[filtered_df["CLASSE"].isin(acp_classes)]

            if filter_metas and "PENDENTE DE META?" in filtered_df.columns:
                filtered_df = filtered_df[filtered_df["PENDENTE DE META?"].notnull()]

            # --- APPLY OTHER FILTERS ---
            
            # Year filter
            if selected_years and 'ANO' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['ANO'].isin(selected_years)]
            
            # Urgency filter
            if urgency_only and "DIAS CONCLUSO" in filtered_df.columns:
                filtered_df = filtered_df[filtered_df["DIAS CONCLUSO"] > 80]
                
            # Etiqueta filters
            if "ETIQUETAS PJE" in filtered_df.columns:
                if etiqueta_contains:
                    filtered_df = filtered_df[filtered_df["ETIQUETAS PJE"].fillna("").str.contains(etiqueta_contains, case=False)]
                if etiqueta_not_contains:
                    filtered_df = filtered_df[~filtered_df["ETIQUETAS PJE"].fillna("").str.contains(etiqueta_not_contains, case=False)]

            # Sidebar specific selectbox/slider filters
            for col, val in filters.items():
                if isinstance(val, str) and val != "Todos":
                    filtered_df = filtered_df[filtered_df[col] == val]
                elif isinstance(val, tuple):
                    filtered_df = filtered_df[(filtered_df[col] >= val[0]) & (filtered_df[col] <= val[1])]
            
            # Header Metrics
            st.title("📊 Painel de Controle de Gabinete")
            
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total", len(df))
            m2.metric("Filtrados", len(filtered_df))
            
            avg_days = int(filtered_df["DIAS CONCLUSO"].mean()) if "DIAS CONCLUSO" in filtered_df.columns else 0
            max_days_val = int(filtered_df["DIAS CONCLUSO"].max()) if "DIAS CONCLUSO" in filtered_df.columns else 0
            
            m3.metric("Média Dias", f"{avg_days} d")
            m4.metric("Máximo Dias", f"{max_days_val} d")

            st.markdown("---")

            # Main Tabs
            tab1, tab2, tab3 = st.tabs(["📋 Processos", "👥 Grupos de Trabalho", "📈 Estatísticas"])

            with tab1:
                st.subheader("Lista de Processos")
                search = st.text_input("🔍 Pesquisa rápida (Número, Classe, Assunto...)", "")
                if search:
                    mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)
                    view_df = filtered_df[mask]
                else:
                    view_df = filtered_df
                
                st.dataframe(view_df, width='stretch', hide_index=True)
                
                # Download
                towrite = io.BytesIO()
                view_df.to_excel(towrite, index=False)
                towrite.seek(0)
                st.download_button(label="📥 Exportar Excel", data=towrite, file_name="gps_jus_filtrado.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

            with tab2:
                st.subheader("Sugestão de Grupos de Trabalho")
                st.info("Processos agrupados por critérios similares para otimizar a produtividade.")
                
                group_by = st.segmented_control("Agrupar por:", options=["CLASSE", "ASSUNTO", "TIPO CONCLUSÃO"], default="CLASSE")
                
                if group_by in filtered_df.columns:
                    groups = filtered_df.groupby(group_by).size().reset_index(name='Qtd').sort_values('Qtd', ascending=False)
                    
                    c1, c2 = st.columns([1, 2])
                    with c1:
                        st.write("Resumo do Agrupamento")
                        st.table(groups)
                    with c2:
                        st.bar_chart(groups.set_index(group_by))
                        
                    selected_group = st.selectbox(f"Ver detalhes de um grupo:", groups[group_by].tolist())
                    if selected_group:
                        st.dataframe(filtered_df[filtered_df[group_by] == selected_group], width='stretch')

            with tab3:
                st.subheader("Visão Geral do Gabinete")
                if "DIAS CONCLUSO" in filtered_df.columns:
                    st.markdown("##### Distribuição de Dias Concluso")
                    st.area_chart(filtered_df["DIAS CONCLUSO"].value_counts().sort_index())
                
                if "CLASSE" in filtered_df.columns:
                    st.markdown("##### Processos por Classe")
                    st.bar_chart(filtered_df["CLASSE"].value_counts())

        else:
            st.error("Erro ao processar os dados. Verifique o formato da planilha.")
    else:
        # Welcome Screen
        st.markdown(f"""
        <div style="text-align: center; padding: 80px 40px; border: 1px solid #e2e8f0; border-radius: 24px; background: white; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1);">
            <div style="font-size: 4rem; margin-bottom: 20px;">⚖️</div>
            <h1 style="color: #1e3a8a; font-size: 3rem; margin-bottom: 10px;">GPS Jus</h1>
            <p style="font-size: 1.25rem; color: #64748b; margin-bottom: 40px;">Sistema Inteligente de Gestão de Gabinete</p>
            <div style="background: #f1f5f9; padding: 20px; border-radius: 12px; display: inline-block; margin-bottom: 40px;">
                <p style="margin: 0; color: #475569;">Por favor, carregue a planilha baixada do GPSJus na barra lateral para iniciar.</p>
            </div>
            <div style="border-top: 1px solid #f1f5f9; pt-20; margin-top: 20px;">
                <p style="font-size: 0.9rem; color: #94a3b8; line-height: 1.6;">
                    Este é um <b>fork do gpsjus</b> para visualização dos dados de vara de fazenda pública<br>
                    elaborado por <b>Nailton Gomes</b>.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
