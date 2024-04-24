from dotenv import load_dotenv, find_dotenv
import os


def load_secrets():
    secrets = dict()
    load_dotenv(find_dotenv())

    secrets["cluster_url"] = os.getenv("WCS_URL")
    if not secrets["cluster_url"]:
        raise Exception("Please set WCS_URL environment variable")
    secrets["wcs_api_key"] = os.getenv("WCS_API_KEY")
    if not secrets["wcs_api_key"]:
        raise Exception("Please set WCS_API_KEY environment variable")
    secrets["palm_api_key"] = os.getenv("PALM_API_KEY")
    if not secrets["palm_api_key"]:
        raise Exception("Please set PALM_API_KEY environment variable")
    secrets["gcloud_project_id"] = os.getenv("GCLOUD_PROJECT_ID")
    if not secrets["gcloud_project_id"]:
        raise Exception("Please set GCLOUD_PROJECT_ID environment variable")

    return secrets
