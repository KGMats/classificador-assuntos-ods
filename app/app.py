#PROCESSADOR PDF

import PyPDF2
import tempfile
import google.generativeai as genai
import json

from classificador import ClassificadorAssuntoODS



# TO DO
# 1 - STREAMLIT



# TESTE
classificador = ClassificadorAssuntoODS(caminho_credenciais='/home/franciscofoz/Documents/credentials_google-api-key.json',
                                        caminho_pdf='/home/franciscofoz/Documents/GitHub/classificador-assuntos-ods/exemplos_documentos/10-1108_EOR-04-2023-0012.pdf') 
    

assuntos = classificador.catalogar_assunto()
ods = classificador.catalogar_ODS()
    
print(f'Assuntos:\n{assuntos}')
print(f'ODS:\n{ods}')



