import weaviate
import weaviate.classes as wvc
from weaviate.classes.config import DataType, Property

client = weaviate.connect_to_wcs(
    cluster_url=cluster_url,
    auth_credentials=weaviate.auth.AuthApiKey(wcs_api_key),
    headers={"X-PaLM-Api-Key": palm_api_key},
)


collection = client.collections.get("instructions_collection")

result = collection.query.hybrid("what is fertility", limit=10)

# can print format string: f"{e.properties.get("content")}" to get all contents of the file itself
for e in result.objects:
    print(e.properties.get("filename"))
