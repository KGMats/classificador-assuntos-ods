# CLASSIFICADOR

import google.generativeai as genai
import json
import PyPDF2
import pandas as pd
#import time

#FUNÇÕES

def transformar_pdf_texto(file_path):
    arquivo_pdf = open(file_path, 'rb')
    leitor_pdf = PyPDF2.PdfReader(arquivo_pdf)
    texto = ''
    
    for pagina_num in range(len(leitor_pdf.pages)):
        page = leitor_pdf.pages[pagina_num]
        texto += page.extract_text()
        texto += '\n\n'

    arquivo_pdf.close()
       
    return texto

'''
def carregar_arquivo_genai(path_arquivo):

  arquivo = genai.upload_file(path=path_arquivo,display_name='pdf_texto')
  
  return arquivo
'''


def catalogar_653a(caminho):
  
  prompt = '''
  Catalogue esse documento conforme o campo 653$a do MARC 21.

  
  - Analise o documento e insira apenas 5 assuntos, em PT-BR, mais relevantes de acordo com o conteúdo.
  - Responda apenas os assuntos.
  
  '''
  
  arquivo = transformar_pdf_texto(caminho)
  
  response = model.generate_content([prompt, arquivo])

  return response.text



def catalogar_655a(arquivo):
  
  prompt = '''
  Catalogue esse documento conforme o campo 655$a do MARC 21.
  
  - Analise o documento e insira UM ou MAIS ODS (Objetivos do Desenvolvimento Sustentável) que ele representa.
  
  Seguem ODS's:
  """
  ODS: 1. Erradicação da pobreza
  ODS: 2. Erradicação da fome
  ODS: 3. Saúde e bem-estar
  ODS: 4. Educação de qualidade
  ODS: 5. Igualdade de gênero
  ODS: 6. Água potável e saneamento
  ODS: 7. Energia acessível e limpa
  ODS: 8. Trabalho decente e crescimento econômico
  ODS: 9. Inovação e infraestrutura
  ODS: 10. Redução das desigualdades
  ODS: 11. Cidades e comunidades sustentáveis
  ODS: 12. Consumo e produção responsáveis
  ODS: 13. Ação contra a mudança global do clima
  ODS: 14. Vida na água
  ODS: 15. Vida terrestre
  ODS: 16. Paz, justiça e instituições eficazes
  ODS: 17. Parcerias e meios de implementação

  """
  Caso haja mais que uma, responda como esse exemplo de formatação separado por ';':
  
  ODS: 1. Erradicação da pobreza;ODS: 6. Água potável e saneamento
  
  - Responda apenas a(s) ODS(s).
  
  '''
  response = model.generate_content([prompt, arquivo])

  return response.text

    
def processar_arquivo(caminho_arquivo):

    assuntos = catalogar_653a(caminho_arquivo)
    ods = catalogar_655a(caminho_arquivo)

    print(f'Assuntos:\n{assuntos}')
    print(f'ODS:\n{ods}')
    
    
    

#------------------------------------------------------------------------------------
#CONFIGURAÇÕES INICIAIS

def configurar_modelo_generativo(credentials_path):

    with open(credentials_path) as file:
        api_key = json.load(file)[0]['API-KEY']


    genai.configure(api_key=api_key)


    generation_config = {
        'temperature': 1,
        'top_p': 1,
        'top_k': 0,
        'max_output_tokens': 2000,
    }

    safety_settings = [
      {
        'category': 'HARM_CATEGORY_HARASSMENT',
        'threshold': 'BLOCK_NONE'
      },
      {
        'category': 'HARM_CATEGORY_HATE_SPEECH',
        'threshold': 'BLOCK_NONE'
      },
      {
        'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT',
        'threshold': 'BLOCK_NONE'
      },
      {
        'category': 'HARM_CATEGORY_DANGEROUS_CONTENT',
        'threshold': 'BLOCK_NONE'
      },
    ]


    model = genai.GenerativeModel(
        model_name='models/gemini-1.5-pro',
        generation_config=generation_config,
        safety_settings=safety_settings
    )
    
    return model


#-------------------------------------------------------------
model = configurar_modelo_generativo(credentials_path='/home/franciscofoz/Documents/credentials_google-api-key.json')

caminho_pasta = '/home/franciscofoz/Documents/GitHub/classificador-assuntos-ods/exemplos_documentos/Flávio Tonioli Mariotto_212-226.pdf'


processar_arquivo(caminho_pasta)


# Teste inicial: string sem carregamento no genai
'''
Assuntos:
- Ônibus elétrico
- Mobilidade elétrica
- Transporte público
- Laboratório Vivo
- Unicamp
ODS:
ODS: 2. Erradicação da fome;ODS: 12. Consumo e produção responsáveis 
'''