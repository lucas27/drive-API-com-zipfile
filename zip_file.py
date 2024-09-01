from zipfile import ZipFile, ZIP_DEFLATED
import time
import os
from tkinter import filedialog
import logging
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)

def caminho_para_zip():
    caminho = filedialog.askdirectory()
    nome_do_arquivo = os.path.basename(caminho) + '.zip'

    return nome_do_arquivo, caminho

# ===============================================================

def zipando(nome_arquivo_zip, caminho, total):
    arquivos_compactados = 0

    with ZipFile(nome_arquivo_zip, 'w', ZIP_DEFLATED) as zip:
        for raiz, diretorios, arquivos in os.walk(caminho):       
            for arquivo in arquivos:       
                caminho_file_join = os.path.join(raiz, arquivo)
                caminho_file_relpath = os.path.relpath(caminho_file_join, caminho)
                zip.write(caminho_file_join , caminho_file_relpath)
                arquivos_compactados += 1
            

            progresso = (arquivos_compactados / total) * 100
            print(f'carregando {progresso:.2f}%')
            
            
def main_zip(nome_arquivo_zip, caminho):
    
    # nome_arquivo_zip, caminho = caminho_para_zip()

    tempo_inicial = time.time()
    total = sum([len(arquivos) for raiz, dirs, arquivos in os.walk(caminho)])
    

    zipando(nome_arquivo_zip, caminho, total)

    # progresso = (arquivos_compactados / total) * 100
    # print(f'carregando {progresso:.2f}%')
                
    logging.info('Arquivo comprimido com sucesso')
    logging.info(f'demorou: {round(time.time() - tempo_inicial)} segundos')

if __name__ == '__main__':
    main_zip()
    ...