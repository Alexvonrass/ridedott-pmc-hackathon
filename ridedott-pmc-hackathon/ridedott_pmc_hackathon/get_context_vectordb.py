import weaviate
import weaviate.classes as wvc
from weaviate.classes.config import DataType, Property

from ridedott_pmc_hackathon.parse_secrets import load_secrets


def get_context(question):
    secrets = load_secrets()
    print(secrets.keys())

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
    context = get_context(question)


if __name__ == "__main__":
    get_context("What do with glioma")
