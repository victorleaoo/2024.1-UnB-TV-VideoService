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
    tfidf_matrix = tfidf.fit_transform(df['Categoria'] + ' ' + df['Título'] + ' ' + df['Descrição'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    return cosine_sim


# Obtém uma lista de vídeos recomendados a partir de um título
def get_recommendations(title, cosine_sim, df):
    indices = pd.Series(df.index, index=df['Título']).drop_duplicates()

    sim_scores = sorted(list(enumerate(cosine_sim[indices[title]])), key=lambda x: x[1], reverse=True)[
                 1:11]  # Pega os 5 melhores

    video_indices = [i[0] for i in sim_scores]
    return df.iloc[video_indices]


if __name__ == "__main__":
    catalog = Catalog()
    videos = find_all_videos()

    if videos:
        # Categorização dos vídeos
        categorize_videos(videos, catalog)

        # Cria o DataFrame com as categorias
        df = videos_to_dataframe(videos)

        # Calcula a similaridade
        cosine_sim = calculate_similarity(df)

        # Obtém recomendações
        ##### MODIFICAR NOME DO TITULO #####
        title = 'IAgora Entrevista: IA, Ciência de Dados e perspectivas'  # Substitua pelo título desejado
        title = title.lower().translate(str.maketrans('', '', string.punctuation))
        recommendations = get_recommendations(title, cosine_sim, df)

        ##### MODIFICAR NOME DO ARQUIVO #####
        file_path = './model_cosine_sim_results/3COSINE_SUSTENTAVEIS_TODOS.csv'
        recommendations.to_csv(file_path)
        add_title_to_file(file_path, title)

        print("Recomendações:\n", recommendations)
    else:
        print("Nenhum vídeo encontrado.")