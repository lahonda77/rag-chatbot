from s3_config import get_file_from_s3
from ollama_interaction import query_ollama

bucket_name = "local-rag"
file_key = "pdf-exemple.pdf"

def process_user_query(user_query, use_rag, temperature):
    if use_rag:
        print("Utilisation de RAG...")
        s3_text = get_file_from_s3(bucket_name="local-rag", file_key="pdf-exemple.pdf")
        if s3_text:
            prompt = f"Voici un document de référence : {s3_text}\nRépondez à cette question : {user_query}"
        else:
            prompt = f"Je n'ai pas pu récupérer le document de référence, mais répondez à cette question : {user_query}"
    else:
        print("Pas d'utilisation de RAG...")
        prompt = f"Répondez à cette question sans document de référence : {user_query}"

    response = query_ollama(prompt, temperature=temperature, model="llama3.2")
    return response


if __name__ == "__main__":
    user_query = input("Rédigez votre question : ")
    use_rag_input = input("Souhaitez-vous utiliser RAG ? (oui/non) ").strip().lower()
    use_rag = use_rag_input == "oui"
    
    temperature = float(input("Entrez la température (0.0 à 1.0) : ").strip())

    result = process_user_query(user_query, use_rag, temperature=temperature)
    print("\nRéponse du modèle :")
    print(result)
