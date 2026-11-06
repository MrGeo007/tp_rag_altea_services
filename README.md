## Installation
```
git clone https://github.com/MrGeo007/tp_rag_altea_services.git
cd tp_rag_altea_services
uv venv
.venv\Scripts\activate
uv pip install -r requirements.txt
```
LLM local : installer Ollama, puis `ollama pull llama3.2`.

Créer un fichier `.env` à la racine :
```
OPENAI_BASE_URL=http://localhost:11434/v1
OPENAI_API_KEY=ollama
MODELE=llama3.2
```

## Lancement
1. Ouvrir `notebook/TP_RAG_Altea.ipynb` et exécuter l'exercice 1 : collecte, nettoyage,
   découpage et indexation (crée `base_vectorielle/` à la racine).
2. Exécuter l'exercice 2 : recherche, génération et évaluation.
3. Lancer l'interface depuis la racine : `streamlit run app.py`

## Exemple
Question : « Combien de jours de télétravail par semaine ? »
Réponse : « Le télétravail est autorisé jusqu'à 2 jours par semaine [1]. »
Source : teletravail.pdf, page 1

## Résultats (étape 7)
- Recherche : bon document trouvé dans … % des cas (k = 3)
- Réponses justes : … %
- Réponses correctement sourcées : … %

## Limites connues
- Pas de gestion des droits d'accès : tout salarié voit tous les documents.
- En-têtes et numéros de page des PDF encore présents dans les chunks.
- Réponses plus lentes et moins précises avec un petit modèle local (llama3.2).
- Base à réindexer à la main quand un document change.

## Auteur
Geoffrey Ndissa — Master 1, INSTA
