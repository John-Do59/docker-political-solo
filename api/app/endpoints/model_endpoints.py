from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.train import TrainingService

router = APIRouter(prefix="/model", tags=["model"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_model_info():
    """Retourne les informations sur le modèle ML actuellement chargé.

    Returns:
        dict: Métadonnées du modèle (features, classes, version).
    """
    return TrainingService.get_model_metadata()


@router.post("/train", status_code=status.HTTP_201_CREATED)
async def train_model(db: Session = Depends(get_db)):
    """Déclenche l'entraînement du modèle ML à partir des données en base.

    Returns:
        dict: Résultats de l'entraînement (accuracy, classes, nb_samples).
    """
    return TrainingService.train(db)
