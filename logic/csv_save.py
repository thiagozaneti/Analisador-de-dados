import csv
import os
from datetime import datetime

def salvar_dados_csv(nome_maquina, dados, timestamp=None):
    # Cria um diretório para os arquivos CSV se não existir
    diretorio = "dados_aquisicao"
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)
    
    # Se não for fornecido um timestamp, cria um novo
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Cria o nome do arquivo com o nome da máquina e o timestamp
    nome_arquivo = f"{diretorio}/{nome_maquina}_{timestamp}.csv"
    
    # Abre o arquivo em modo de append e escreve os dados
    with open(nome_arquivo, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(dados)

    return nome_arquivo  # Retorna o nome do arquivo para referência 