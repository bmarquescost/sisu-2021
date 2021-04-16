import pandas as pd
import requests 
import os

diretorio = "Data"
url_base = "https://sisu-api-pcr.apps.mec.gov.br/api/v1/oferta/{}/selecionados"

cursos = pd.read_csv("lista_cursos.csv", sep=";")

todos_alunos = []
for codigo_oferta, index in zip(cursos["codigo_oferta"], cursos.index):
    while True:
        try:
            resposta = requests.get(url_base.format(codigo_oferta))
            break
        except:
            print("[{}] Requisição Falhou, tentando novamente".format(codigo_oferta))
    
    if resposta.status_code != 200:
        print("[{}] Erro {}".format(codigo_oferta, resposta.status_code))
        continue
    
    print(f"[{index + 1} / {cursos['codigo_oferta'].shape[0]}] {cursos.loc[index, 'nome_ies']} ({cursos.loc[index, 'sigla_ies']}) {cursos.loc[index, 'nome_curso']}")
   
    resposta = resposta.json()

    for aluno in resposta:
        dados_aluno = {
            'nome': aluno['no_inscrito'],
            'codigo_inscricao_enem': aluno['co_inscricao_enem'],
            'codigo_oferta': codigo_oferta,
            'bonus': aluno['qt_bonus_perc'],
            'classificacao': aluno['nu_classificacao'],
            'nota': aluno['nu_nota_candidato'],
            'codigo_modalidade': aluno['co_mod_concorrencia'],
            'modalidade': aluno['no_mod_concorrencia']
        }

        todos_alunos.append(dados_aluno)

df = pd.DataFrame(todos_alunos)
df.to_csv(diretorio + '/alunos_selecionados.csv', sep=';', index=False)