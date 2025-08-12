# Streamlit Frontend pour CSI API

Ce mini-front fait l'interface avec votre API CSI (FastAPI). Il permet :
- d'uploader un document pour analyse
- d'afficher les constats / stats
- de voir les poids de catégories
- de télécharger les exports CSV

## Utilisation en local
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
# Ouvrir: http://localhost:8501
```

## Paramétrage de l'URL de l'API
Par défaut: `http://localhost:8080`. Modifiez-le dans l'UI.
En production, vous pouvez définir un secret Streamlit `API_BASE_URL`.

## Déploiement sur Streamlit Cloud
- Déposez ce dossier dans un repo GitHub (ou sous-dossier).
- Lors de la création de l'app :
  - **Main file path** : `streamlit_app.py`
  - (Optionnel) Secrets → `API_BASE_URL` = URL publique de votre API (ex. Render/Railway).