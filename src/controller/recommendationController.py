from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from src.domain import recordSchema
from src.database import get_db
from src.repository import recordRepository

from src.recommendation_model.get_video_recommendation import get_recommendations

Recommendation = APIRouter(
    prefix="/recommendation"
)

@Recommendation.get("/get_recommendation_record")
def get_recommendation_from_record(user_id: str =Query(...) , db: Session = Depends(get_db)):
    record = recordSchema.RecordGet(user_id = user_id)
    videos_record = recordRepository.get_record(db=db, record=record)

    recommendations = []
    final_recommendations = []

    # Gera lista de recomendações para cada vídeo no histórico
    for video in videos_record:
        videos_recommend = get_recommendations(int(video))
        recommendations.append(videos_recommend)

    try:
        for i in range(7):
            for list_recommendation in recommendations:
                video = list_recommendation[i]

                if len(final_recommendations) > 20:
                    break

                if (str(video) not in videos_record) and (video not in final_recommendations):
                    final_recommendations.append(video)
    except:
        print("Não há vídeos recomendados suficientes!")
        return {"recommend_videos": final_recommendations}

    return {"recommend_videos": final_recommendations}


@Recommendation.get("/get_recommendation_video")
def get_recommendation_from_video(video_id: str =Query(...) , db: Session = Depends(get_db)):
    videos_recommend = get_recommendations(int(video_id))

    return {"recommend_videos": videos_recommend}
