import pdb
from pathlib import Path

import vertexai
import weaviate
import weaviate.classes as wvc
from google.oauth2 import service_account
from vertexai.preview.generative_models import GenerativeModel, Image
from weaviate.classes.config import DataType, Property

from ridedott_pmc_hackathon.parse_secrets import load_secrets

REGION = "europe-west4"
SERVICE_ACCOUNT_FILE = Path(__file__).resolve().parents[1] / "sa" / "sa.json"

# Authenticate using the service account key file
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)
secrets = load_secrets()
print(secrets.keys())


def get_context(question):
    """
    Gets the context (most relevant instructions) from our vector database
    :param question:
    :return:
    """
    client = weaviate.connect_to_wcs(
        cluster_url=secrets["cluster_url"],
        auth_credentials=weaviate.auth.AuthApiKey(secrets["wcs_api_key"]),
        headers={"X-PaLM-Api-Key": secrets["palm_api_key"]},
    )

    collection = client.collections.get("instructions_collection")

    result = collection.query.hybrid(question, limit=5)
    for e in result.objects:
        print(e.properties.get("filename"))
    print(result)
    return result


def answer_text_using_context(question):
    vertexai.init(
        project=secrets["gcloud_project_id"],
        location=REGION,
        credentials=credentials,
    )
    context = get_context(question)
    generative_multimodal_model = GenerativeModel(
        "gemini-1.5-pro-preview-0409"
    )

    model_prompt = f"""
        {context}
        You are a doctor treating a patient at the princess Maxima hospital,
        using the above context, answer the following question,
        be empathetic but focus on being informative and concise:
        {question}"""

    response = generative_multimodal_model.generate_content(model_prompt)
    print(response.candidates[0].content.parts[0].text)
    return response.candidates[0].content.parts[0].text


if __name__ == "__main__":
    answer_text_using_context(
        "My daughter is about to undergo a glioma treatment, what should I expect"
    )
    answer_text_using_context(
        "Мою дочь будут лечить от глиомы, чего стоит ожидать?"
    )
