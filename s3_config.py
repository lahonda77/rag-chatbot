import boto3
import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv

# charge les var d'environnement
load_dotenv(".env")

# configuration AWS
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name='eu-north-1'
)

bucket_name = "local-rag"  # nom du bucket S3
file_key = "pdf-exemple.pdf"  # clé du fichier dans le bucket

def get_file_from_s3(bucket_name, file_key):
    """
    Ici, récupère le contenu d'un fichier depuis un bucket S3 et le convertit en texte.
    """
    try:
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        content = response['Body'].read()

        # identifie le type de fichier en fonction de son extension
        if file_key.lower().endswith('.pdf'):
            # sauvegarde temporaire pour lire avec PyPDF2
            temp_file_path = "/tmp/exposure-temp.pdf"
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(content)
            
            # lecture du texte du PDF
            reader = PdfReader(temp_file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()

            # supprimer le fichier temporaire
            os.remove(temp_file_path)
            return text
        else:
            # supposer que c'est un fichier texte
            return content.decode('utf-8')
    except Exception as e:
        print(f"Erreur lors de la récupération ou du traitement du fichier S3 : {e}")
        return None




