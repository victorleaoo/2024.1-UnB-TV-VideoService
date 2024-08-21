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