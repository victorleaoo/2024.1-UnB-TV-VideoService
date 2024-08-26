import csv
import pickle

# Carrega o arquivo CSV em uma lista de dicionários, ignorando a primeira coluna
def load_csv_as_dict(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        return [{'ID': row['ID'], 'Título': row['Título'], 'Descrição': row['Descrição'], 'Categoria': row['Categoria']} for row in reader]

# Cria um dicionário indexado por ID
def create_indexed_dict(data):
    return {item['ID']: index for index, item in enumerate(data)}

# Obtém uma lista de vídeos recomendados a partir de um ID
def get_recommendations(video_id):
    import sys
    print(sys.path)
    
    with open('/app/src/recommendation_model/cosine_similarity.pkl', 'rb') as f:
        cosine_sim = pickle.load(f)

    data = load_csv_as_dict('/app/src/recommendation_model/df_videos.csv')
    id_index = create_indexed_dict(data)

    # Verifica se o ID está presente no dicionário
    if str(video_id) not in id_index:
        raise ValueError(f"ID {video_id} não encontrado no dicionário.")

    # Encontra os índices dos vídeos similares
    sim_scores = sorted(list(enumerate(cosine_sim[id_index[str(video_id)]])), key=lambda x: x[1], reverse=True)[1:8]

    # Retorna uma lista de IDs recomendados
    video_indices = [i[0] for i in sim_scores]
    return [int(data[i]['ID']) for i in video_indices]
