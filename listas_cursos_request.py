import pandas as pd
import requests 

url_base = 'https://sisu-api-pcr.apps.mec.gov.br/api/v1/oferta/'

resposta = requests.get(url_base + 'instituicoes/')
todas_instituicoes = resposta.json()

print(f">> Requisição para {url_base + 'instituicoes/'}")

instituicoes = []

for instituicao in todas_instituicoes:
    instituicoes.append(instituicao['co_ies'])

# Fazendo o scrapping no site https://sisu-api-pcr.apps.mec.gov.br/api/v1/oferta/instituicao/{} sendo {} substituido
# pelo valor do códico da insituição
# - O retorno do json corresponde a lista de instituições de ensino superior e suas informações 
# - Particionamos e colocamos em uma lista vários dicionários, em que cada corresponde a uma oferta 
ofertas = []
for i, instituicao in enumerate(instituicoes):
    requisicao = requests.get(url_base + 'instituicao/' + instituicao)
    
    print('[{:>3} / {}] ID instituição: #{}'.format(i + 1, len(instituicoes), instituicao))
    
    while True:
        try:
            requisicao = requests.get(url_base + 'instituicao/' + instituicao)
            break
        except:
            print(f"Requição feita para {url_base + 'instituicao/' + instituicao} falhou.\nTentando novamente")

    dado_instituicao = requisicao.json() 
    
    for i in range(len(dado_instituicao) - 1):
        dado_instituto = dado_instituicao[str(i)]
        
        dados_relevantes_instituto = {
            # Dados do curso
            'codigo_oferta':  dado_instituto['co_oferta'],
            'codigo_curso': dado_instituto['co_curso'],
            'nome_curso': dado_instituto['no_curso'],
            'grau_curso': dado_instituto['no_grau'],
            'turno_curso': dado_instituto['no_turno'],
            'numero_vagas': dado_instituto['qt_vagas_sem1'],
            
            # Dados do insituto
            'nome_campus': dado_instituto['no_campus'],
            'cidade_campus': dado_instituto['no_municipio_campus'],
            'uf_campus': dado_instituto['sg_uf_campus'],
            'nome_ies': dado_instituto['no_ies'],
            'sigla_ies': dado_instituto['sg_ies'],

            # Notas do curso
            'min_ciencias_natureza': dado_instituto['nu_nmin_cn'],
            'peso_ciencias_natureza': dado_instituto['nu_peso_cn'],
            'min_ciencias_humanas': dado_instituto['nu_nmin_ch'],
            'peso_ciencias_humanas': dado_instituto['nu_peso_ch'],
            'min_linguagens': dado_instituto['nu_nmin_l'],
            'peso_linguagens': dado_instituto['nu_peso_l'],
            'min_matematica': dado_instituto['nu_nmin_m'],
            'peso_matematica': dado_instituto['nu_peso_m'],
            'min_redacao': dado_instituto['nu_nmin_r'],
            'peso_redacao': dado_instituto['nu_peso_r'],
            'media_minima': dado_instituto['nu_media_minima']
        }

        ofertas.append(dados_relevantes_instituto)

# Criando um dataframe e o salvando em um arquivo CSV
df = pd.DataFrame(ofertas)
df.to_csv('lista_cursos.csv', sep = ';', index=False)