import requests
import json

def query_ollama(prompt, temperature, model="llama3.2"):
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": model,
        "prompt": prompt,
        "temperature": temperature,
        "stream": False
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        result = response.json()
        return result.get("response", "Aucune réponse reçue du modèle.")
    except requests.exceptions.RequestException as e:
        return f"Erreur lors de l'appel à Ollama : {e}"
