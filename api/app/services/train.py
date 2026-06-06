import pandas as pd
import joblib
import os
import json
from fastapi import HTTPException
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from app.schemas.train import TrainSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODELS_DIR = os.path.join(BASE_DIR, "saved_models")
DEFAULT_MODEL = "politique_model.joblib"


class TrainingService:
    @staticmethod
    def get_model_metadata() -> dict:
        """Retourne les métadonnées du modèle ML actuel (features, classes, accuracy).

        Raises:
            HTTPException: 404 si aucun modèle n'est encore entraîné.

        Returns:
            dict: Métadonnées du modèle (accuracy, features_order, feature_importances).
        """
        meta_path = os.path.join(MODELS_DIR, DEFAULT_MODEL.replace(".joblib", ".json"))
        if not os.path.exists(meta_path):
            raise HTTPException(
                status_code=404,
                detail="Aucun modèle trouvé. Lancez d'abord un entraînement via POST /model/train.",
            )
        with open(meta_path, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def train(db) -> dict:
        """Entraîne le modèle ML depuis la table 'training' en base.

        Args:
            db: Session SQLAlchemy.

        Raises:
            HTTPException: 400 si la table training est vide.
            HTTPException: 500 en cas d'erreur pendant l'entraînement.

        Returns:
            dict: Résultats (accuracy, nb_samples, model_path).
        """
        try:
            from sqlalchemy import text
            rows = db.execute(text("SELECT * FROM training")).fetchall()
            if not rows:
                raise HTTPException(status_code=400, detail="La table 'training' est vide.")

            df = pd.DataFrame([dict(r._mapping) for r in rows])
            df_clean = df[
                (df['Population_active'] > 0) &
                (df['Population avec enfants'] > 0)
            ].copy()

            X = df_clean.drop(columns=['Code_INSEE', 'Résultat'])
            y = df_clean['Résultat']
            feature_names = list(X.columns)

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            accuracy = float(model.score(X_test, y_test))

            os.makedirs(MODELS_DIR, exist_ok=True)
            model_path = os.path.join(MODELS_DIR, DEFAULT_MODEL)
            joblib.dump(model, model_path)

            importances = {n: float(i) for n, i in zip(feature_names, model.feature_importances_)}
            metadata = {
                "model_name": DEFAULT_MODEL,
                "accuracy": accuracy,
                "features_order": feature_names,
                "feature_importances": dict(sorted(importances.items(), key=lambda x: x[1], reverse=True)),
            }
            meta_path = model_path.replace(".joblib", ".json")
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=4, ensure_ascii=False)

            return {
                "status": "success",
                "accuracy": accuracy,
                "nb_samples": len(df_clean),
                "model_path": model_path,
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erreur d'entraînement : {str(e)}")

    # ── Compatibilité rétrograde avec train_endpoints ──────────────────────────
    @staticmethod
    def run_pipeline(settings: TrainSettings, db_engine):
        """Legacy : utilisé par train_endpoints. Conservé pour compatibilité."""
        try:
            query = "SELECT * FROM training"
            df = pd.read_sql(query, db_engine)

            if df.empty:
                print("--- ERROR: Table 'training' vide ---")
                return

            df_clean = df[
                (df['Population_active'] > 0) &
                (df['Population avec enfants'] > 0)
            ].copy()

            X = df_clean.drop(columns=['Code_INSEE', 'Résultat'])
            y = df_clean['Résultat']
            feature_names = list(X.columns)

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=settings.test_size, random_state=42
            )

            model = RandomForestClassifier(n_estimators=settings.n_estimators, random_state=42)
            model.fit(X_train, y_train)

            os.makedirs(MODELS_DIR, exist_ok=True)
            model_path = os.path.join(MODELS_DIR, settings.model_name)
            joblib.dump(model, model_path)

            importances = model.feature_importances_
            feat_imp = {name: float(imp) for name, imp in zip(feature_names, importances)}
            sorted_imp = dict(sorted(feat_imp.items(), key=lambda item: item[1], reverse=True))

            metadata = {
                "model_name": settings.model_name,
                "accuracy": float(model.score(X_test, y_test)),
                "features_order": feature_names,
                "feature_importances": sorted_imp,
            }

            meta_path = model_path.replace(".joblib", ".json")
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=4, ensure_ascii=False)

            print(f"--- TRAINING SUCCESS ---")
            print(f"Modèle sauvegardé : {model_path}")
            print(f"Précision : {metadata['accuracy']:.4f}")

        except Exception as e:
            print(f"--- TRAINING FAILED: {str(e)} ---")