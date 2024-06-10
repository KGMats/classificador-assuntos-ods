# CLASSIFICADOR

import PyPDF2
import tempfile
import google.generativeai as genai
import json

class ClassificadorAssuntoODS:
    def __init__(self, caminho_credenciais, caminho_pdf):
        self.model = self.configurar_modelo_generativo(caminho_credenciais)
        self.caminho_pdf = caminho_pdf


    def configurar_modelo_generativo(self, caminho_credenciais):
        with open(caminho_credenciais) as file:
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

    def transformar_pdf_texto(self):
        arquivo_pdf = open(self.caminho_pdf, 'rb')
        leitor_pdf = PyPDF2.PdfReader(arquivo_pdf)
        texto = ''

        for pagina_num in range(len(leitor_pdf.pages)):
            page = leitor_pdf.pages[pagina_num]
            texto += page.extract_text()
            texto += '\n\n'

        arquivo_pdf.close()

        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w', encoding='utf-8') as arquivo_saida:
            arquivo_saida.write(texto)
            caminho_arquivo_txt = arquivo_saida.name

        return caminho_arquivo_txt

    def carregar_arquivo_genai(self, caminho_arquivo):
        arquivo = genai.upload_file(path=caminho_arquivo, display_name='pdf_texto')
        return arquivo

    def processar_arquivo(self):
        caminho_txt = self.transformar_pdf_texto()
        arquivo = self.carregar_arquivo_genai(caminho_txt)

        return arquivo

    def catalogar_assunto(self):
        arquivo = self.processar_arquivo()
        
        prompt = '''
        Catalogue os assuntos desse documento conforme o campo 653$a do MARC 21.

        - Analise o documento e insira apenas 5 assuntos, em PT-BR, mais relevantes de acordo com o conteúdo.
        - Responda apenas os assuntos.
        '''
        
        response = self.model.generate_content([prompt, arquivo])
        
        return response.text

    def catalogar_ODS(self):
      
        arquivo = self.processar_arquivo()
        
        prompt = '''
        Catalogue a ODS (Objetivos do Desenvolvimento Sustentável) que esse documento representa.

        - Analise o documento e insira UM ou MAIS ODS (Objetivos do Desenvolvimento Sustentável).

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

        - Catalogue a ODS de forma PERTINENTE com o assunto.
        - Caso haja mais que uma, responda em formato de lista.
        - Responda apenas o número e nome da ODS.

        '''
        response = self.model.generate_content([prompt, arquivo])
        return response.text