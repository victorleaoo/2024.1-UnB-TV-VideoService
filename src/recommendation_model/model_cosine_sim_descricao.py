from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd
import string

from utils.constants import PORTUGUESE_STOP_WORDS

from utils.model import Catalog

from utils.get_videos import find_all_videos, videos_to_dataframe, add_title_to_file
from utils.categorize_videos import categorize_videos

# Calcula similaridade dos vídeos a partir da distância dos cossenos (cosine distance)
def calculate_similarity(df):
    tfidf = TfidfVectorizer(stop_words=PORTUGUESE_STOP_WORDS)
    tfidf_matrix = tfidf.fit_transform(df['Descrição'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    return cosine_sim