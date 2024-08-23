import pytest
from fastapi.testclient import TestClient
import os, sys
import pandas as pd
import pickle
from unittest.mock import patch, mock_open

from src.repository import recordRepository
from src.domain import recordSchema
from src.recommendation_model.get_video_recommendation import get_recommendations
from src.main import app

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

client = TestClient(app)

# Mock para o DataFrame
mock_df = pd.DataFrame({
    'ID': [1, 2, 3, 4, 5],
    'Título': ['Video 1', 'Video 2', 'Video 3', 'Video 4', 'Video 5'],
    'Descrição': ['Descrição 1', 'Descrição 2', 'Descrição 3', 'Descrição 4', 'Descrição 5'],
    'Categoria': ['Entrevista', 'Entrevista', 'UnBTV', 'UnBTV', 'Jornalismo']
})

# Mock para a similaridade coseno
mock_cosine_sim = [
    [1.0, 0.9, 0.8, 0.4, 0.2],
    [0.9, 1.0, 0.85, 0.3, 0.1],
    [0.8, 0.85, 1.0, 0.2, 0.05],
    [0.4, 0.3, 0.2, 1.0, 0.7],
    [0.2, 0.1, 0.05, 0.7, 1.0]
]

# Mock para o retorno da função get_recommendations
mock_recommendations = [2, 3, 4, 5]

# Mock para o retorno de get_recommendations
mock_recommendations_for_video = {
    1: [2, 3, 4, 5, 6, 7, 8],
    2: [3, 4, 5, 6, 7, 8, 1],
    3: [4, 5, 6, 7, 8, 1, 2]
}

# Mock para o retorno do histórico de vídeos
mock_videos_record = [1, 2, 3]

def test_get_recommendations():
    # Patch para o método pd.read_csv
    with patch('pandas.read_csv', return_value=mock_df):
        # Patch para a função open e o carregamento do pickle
        with patch('builtins.open', mock_open(read_data=pickle.dumps(mock_cosine_sim))):
            # Patch para pickle.load
            with patch('pickle.load', return_value=mock_cosine_sim):
                recommendations = get_recommendations(1)
                assert recommendations == mock_recommendations

def test_get_recommendation_from_record():
    # Mock para a função get_recommendations
    def mock_get_recommendations(video_id):
        return mock_recommendations_for_video.get(video_id, [])

    # Patch para a função get_recommendations
    with patch('pandas.read_csv', return_value=mock_df):
        # Patch para a função open e o carregamento do pickle
        with patch('builtins.open', mock_open(read_data=pickle.dumps(mock_cosine_sim))):
            # Mock para o método recordRepository.get_record
            with patch('repository.recordRepository.get_record', return_value=mock_videos_record):
                # Patch para a função get_recommendations
                with patch('recommendation_model.get_video_recommendation.get_recommendations', side_effect=mock_get_recommendations):
                    response = client.get("/api/recommendation/get_recommendation_record/?user_id=1")
                    
                    assert response.status_code == 200 # ok
                    
                    assert response.json() == {"recommend_videos": [2, 1, 3, 4, 5]}

def test_get_recommendation_from_video():
    # Patch para a função get_recommendations
    with patch('pandas.read_csv', return_value=mock_df):
        # Patch para a função open e o carregamento do pickle
        with patch('builtins.open', mock_open(read_data=pickle.dumps(mock_cosine_sim))):
            with patch('recommendation_model.get_video_recommendation.get_recommendations', return_value=mock_recommendations):
                response = client.get("/api/recommendation/get_recommendation_video/?video_id=1")
                
                assert response.status_code == 200 # ok
                
                assert response.json() == {"recommend_videos": mock_recommendations}