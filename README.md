# API de Chatbot Multitâche

Cette application est une API construite avec FastAPI qui expose un endpoint pour interagir avec un chatbot. L'API prend un texte en français, le traduit en anglais, analyse son sentiment, génère une réponse conversationnelle, et renvoie toutes ces informations.

## Fonctionnalités

- **Traduction** : Traduit le texte fourni (français) en anglais en utilisant le modèle `Helsinki-NLP/opus-mt-fr-en`.
- **Analyse de Sentiment** : Évalue le sentiment du texte traduit à l'aide du modèle `nlptown/bert-base-multilingual-uncased-sentiment`.
   **Génération de Réponse** : Génère une réponse conversationnelle en anglais basée sur le texte traduit avec le modèle `microsoft/DialoGPT-medium`.
- **Journalisation (Logging)** : Enregistre chaque requête reçue dans le fichier `logs/api.log`.

## Prérequis

- Python 3.8+
- Un compte Hugging Face
- Un token d'accès Hugging Face avec au moins le rôle `read`.

## Installation

1. **Clonez le dépôt du projet :**

    ```bash
    git clone <url-du-repo>
    cd <nom-du-repo>
    ```

2. **Créez et activez un environnement virtuel :**

    ```bash
    python -m venv venv
    source venv/bin/activate  # Sur Windows: venv\Scripts\activate
    ```

3. **Installez les dépendances :**

    Créez un fichier `requirements.txt` avec le contenu suivant :

    ```text
    fastapi
    uvicorn[standard]
    loguru
    pydantic
    torch
    transformers
    huggingface_hub
    ```

    Puis installez-les :
    ```bash
    pip install -r requirements.txt
    ```

4. **Configurez votre token Hugging Face :**

    L'application nécessite un token d'API Hugging Face pour communiquer avec les modèles d'inférence. Exportez ce token en tant que variable d'environnement.
    ```bash
    export HF_TOKEN="votre_token_hugging_face_ici"
    ```

## Utilisation

1. **Lancez le serveur d'application :**

    Depuis la racine du projet, exécutez la commande suivante :

    ```bash
    uvicorn api:app --host 0.0.0.0 --port 9000 --reload
    ```

    L'API sera accessible à l'adresse `http://localhost:9000`.

2. **Interagissez avec l'API :**
    Vous pouvez envoyer des requêtes à l'endpoint `/chat/` en utilisant un outil comme `curl` ou Postman.

    **Exemple avec `curl` :**

    ```bash
    curl -X 'POST' \
      'http://localhost:9000/chat/' \
      -H 'Content-Type: application/json' \
      -d '{
        "texte": "Je suis très content de découvrir cette nouvelle API !"
      }'
    ```

## Documentation de l'API

### Endpoint : `POST /chat/`

Cet endpoint est le cœur de l'application. Il traite le texte fourni et renvoie un objet JSON complet.

- **URL** : `/chat/`
- **Méthode** : `POST`
- **Corps de la requête** (`application/json`) :

    ```json
    {
      "texte": "string"
    }
    ```

- **Réponse (Succès `200 OK`)** :

    Un objet JSON contenant le message original, sa traduction, l'analyse de sentiment et la réponse du chatbot.

    **Exemple de réponse :**

    ```json
    {
      "message": "Je suis très content de découvrir cette nouvelle API !",
      "translation": "I am very happy to discover this new API!",
      "sentiment": [
        {
          "label": "5 stars",
          "score": 0.8833699226379395
        }
      ],
      "reply": " I'm glad you're enjoying it!"
    }
    ```

- **Réponse (Erreur `500 Internal Server Error`)** :
    En cas de problème lors du traitement (par exemple, un modèle indisponible), l'API renverra une erreur 500 avec des détails.

    ```json
    {
      "detail": "Description de l'erreur"
    }
    ```

## Technologies utilisées

- **Framework API** : FastAPI
- **Serveur ASGI** : Uvicorn
- **Validation de données** : Pydantic
- **Modèles NLP** : Hugging Face Transformers
  - Traduction : `Helsinki-NLP/opus-mt-fr-en`
  - Analyse de Sentiment : `nlptown/bert-base-multilingual-uncased-sentiment`
  - Chatbot : `microsoft/DialoGPT-medium`
- **Client d'inférence** : `huggingface_hub`
- **Logging** : Loguru
- **Deep Learning** : PyTorch
