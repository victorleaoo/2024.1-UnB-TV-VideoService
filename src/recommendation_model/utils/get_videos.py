import requests
import re
from typing import List
import pandas as pd
import string

from utils.model import IVideo

from utils.constants import *

# Função para buscar todos os vídeos
def find_all_videos() -> List[IVideo]:
    HEADERS = {"clientkey": EDUPLAY_CLIENT_KEY}

    params = {
        "institution": UNB_ID,
        "limit": VIDEOS_LIMIT,
        "order": VIDEOS_ORDER
    }

    try:
        response = requests.get(f"{EDUPLAY_API_URL}video", headers=HEADERS, params=params)
        response.raise_for_status()
        videos_data = response.json()
        
        # print("Resposta da API:", videos_data)

        # Acesse a lista de vídeos
        video_list = videos_data.get('videoList', [])

        # Filtra vídeos pelo canal da UNB_TV
        filtered_videos = [video for video in video_list if video.get('channels') and video['channels'][0]['id'] == UNB_TV_CHANNEL_ID]

        return [IVideo(video['id'], video['title'], video.get('description', '')) for video in filtered_videos]
    except requests.HTTPError as err:
        print(f"Erro ao acessar a API: {err}")
        return []
    except ValueError as err:
        print(f"Erro ao processar o JSON: {err}")
        return []

def clean_text(videos: List[IVideo]):
    html_pattern = re.compile('<.*?>')

    for video in videos:
        # remover html
        video.description = re.sub(html_pattern, '', video.description)

        # minusculo
        video.description = video.description.lower()
        video.title = video.title.lower()
        video.catalog = video.catalog.lower()

        # Remover pontuação
        video.description = video.description.translate(str.maketrans('', '', string.punctuation))
        video.title = video.title.translate(str.maketrans('', '', string.punctuation))

    return videos

# Função para transformar a lista de vídeos em um dataframe
def videos_to_dataframe(videos: List[IVideo]) -> pd.DataFrame:
    videos = clean_text(videos)

    # Converte a lista de objetos IVideo para uma lista de dicionários
    video_dicts = [
        {
            'ID': video.id,
            'Título': video.title,
            'Descrição': video.description,
            'Categoria': video.catalog
        }
        for video in videos
    ]
    
    df = pd.DataFrame(video_dicts)
    
    return df

def add_title_to_file(file_path, title):
    # Abra o arquivo CSV para leitura e obtenha as linhas existentes
    with open(file_path, 'r') as file:
        linhas = file.readlines()

    # Adicione a linha com o título no início da lista de linhas
    linhas.insert(0, f'TITLE: {title}\n')

    # Escreva todas as linhas de volta no arquivo CSV
    with open(file_path, 'w') as file:
        file.writelines(linhas)