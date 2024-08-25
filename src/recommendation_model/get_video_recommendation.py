import pandas as pd
import pickle

# Obtém uma lista de vídeos recomendados a partir de um ID
def get_recommendations(id):
    with open('/app/src/recommendation_model/cosine_similarity.pkl', 'rb') as f:
        cosine_sim = pickle.load(f)

    df = pd.read_csv('/app/src/recommendation_model/df_videos.csv')

    indices = pd.Series(df.index, index=df['ID']).drop_duplicates()

    sim_scores = sorted(list(enumerate(cosine_sim[indices[id]])), key=lambda x: x[1], reverse=True)[
                 1:8]  # Pega os 7 melhores

    video_indices = [i[0] for i in sim_scores]
    return list(df.iloc[video_indices][['ID']]['ID'])