#PROCESSADOR PDF - Subject and SDG Classifier powered by Generative AI

import PyPDF2
import tempfile
import google.generativeai as genai
import json
import streamlit as st

from gerador import GeradorAssuntoODS


#CONFICURAÇÕES INICIAIS
st.set_page_config(
    layout='wide',
    page_title='ia-geratemas',
    page_icon='::robot_face::'
)

#TÍTULO DO APP
st.title('IA GeraTemas',anchor='string')
st.header('Gerador de Assuntos e ODS',anchor=False)

#PREÂMBULO
st.write('''
        Bem-vindo ao IA GeraTemas, uma aplicação que utiliza inteligência artificial generativa para identificar e gerar os principais assuntos e Objetivos de Desenvolvimento Sustentável (ODS) de documentos. A ferramenta é projetada para facilitar a análise de textos, proporcionando uma compreensão rápida e precisa dos temas abordados.
        ''')
st.markdown("&nbsp;")
st.write('''
        **Como usar:**
        1. **Insira a API Key:** No campo designado, insira sua chave de API para ativar a funcionalidade de geração de assuntos e ODS.
        2. **Faça o upload do arquivo:** Carregue o documento desejado usando o botão de upload. O documento deve ser um PDF OCR.
        3. **Visualização dos Resultados:** Após o processamento, os assuntos e ODS identificados serão exibidos na tela, proporcionando uma visão clara dos tópicos principais e como eles se relacionam com os Objetivos de Desenvolvimento Sustentável.
        ''')
st.markdown("&nbsp;")
st.write(
        '''
        A aplicação é projetada para ser intuitiva e balizadora, permitindo que você obtenha informações norteadoras para a análise descritiva de seus documentos com apenas alguns cliques.
        ''')
st.markdown('&nbsp;')

st.divider()
st.markdown("&nbsp;")

#INPUT DE DADOS
api_key = st.text_input('Insira sua API Key', 'AIopS0AraGsD3Pd3g_dfrvUsdP89L7u8LM_md-cg')
uploaded_file = st.file_uploader('Faça o upload do arquivo:', type=['pdf'],accept_multiple_files=False)


#INTERFACE
if st.button('Processar'):
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_pdf_path = temp_file.name
            
            gerador = GeradorAssuntoODS(api_key=api_key,caminho_pdf=temp_pdf_path)
            assuntos = gerador.catalogar_assunto()
            ods = gerador.catalogar_ODS()
            
            st.write(f'ASSUNTOS:\n\n{assuntos}')
            st.write(f'ODS:\n\n{ods}')
    else:
        st.warning('Por favor, faça o upload de um documento para continuar.')

st.markdown('&nbsp;&nbsp;')
st.divider()
st.markdown('''
    Elaborado por Francisco Tadeu Gonçalves de Oliveira Foz.\n
    GitHub: [FranciscoFoz](https://github.com/FranciscoFoz)
    ''')

