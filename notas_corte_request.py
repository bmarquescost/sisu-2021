import os
import requests
import pandas as pd
from time import sleep


# A cada parcial, faremos requisições para o site obtenod informações sobre cada nota de corte
# Faremos requisições para o site https://sisu-api-pcr.apps.mec.gov.br/api/v1/oferta/{}/modalidades em que {} é substituido pelo código do oferecimento
try:
    dataframe_cursos = pd.read_csv("lista_cursos.csv", sep= ";")
except:
    print("Necessário gerar arquivo lista_cursos.csv\nPara isso, rode o programa lista_cursos.request.py")
    exit()

diretorio = "Data"
arquivo_final_csv = input("Digite o nome do arquivo em será guardado os dados finais (sem extensão): ")

url_modalidades = "https://sisu-api-pcr.apps.mec.gov.br/api/v1/oferta/{}/modalidades"

codigos_oferta = dataframe_cursos["codigo_oferta"]

dataframe_modalidades = pd.DataFrame()
for index, codigo_oferta in enumerate(codigos_oferta):

    # Fazendo requsição até que dê tudo certo
    while True:
        try:
            resposta = requests.get(url_modalidades.format(codigo_oferta))
            break
        except:
            print(f"[{codigo_oferta}] Erro ocorreu na requisição, tentando novamente")
    
    # Caso a resposta não seja 200 (OK) então vamos para o próximo código de oferta
    if resposta.status_code != 200:
        print(f"[{codigo_oferta}] Erro {resposta.status_code}")
        continue
    
    dados_modalidades = resposta.json()

    print(f"[{index + 1} / {codigos_oferta.shape[0]}] {dataframe_cursos.loc[index, 'nome_ies']} ({dataframe_cursos.loc[index, 'sigla_ies']}) {dataframe_cursos.loc[index, 'nome_curso']}")
    
    # A resposta é um json com várias modalidades, então para cada modalidade iremos guardar seus dados
    for modalidade in dados_modalidades["modalidades"]:   
        dados = {
            "codigo_oferta": codigo_oferta,
            "codigo_concorrencia": modalidade["co_concorrencia"],
            "quantidade_vagas": modalidade["qt_vagas"],
            "nota_corte": modalidade["nu_nota_corte"],
            "bonus_percentual": modalidade["qt_bonus_perc"],
            "data_nota_corte": modalidade["dt_nota_corte"]
        }
        for column in dataframe_cursos.columns.tolist():
            dados[column] = dataframe_cursos.loc[index, column]

        dataframe_modalidades = dataframe_modalidades.append(dados, ignore_index=True)
    
# Salvando os dados em um arquivo CSV
dataframe_modalidades.to_csv(os.path.join(diretorio, arquivo_final_csv + ".csv"), sep=";", index=False)