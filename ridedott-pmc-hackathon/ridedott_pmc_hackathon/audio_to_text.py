from pathlib import Path
from typing import ByteString

import vertexai
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
from google.oauth2 import service_account
from vertexai.preview.generative_models import GenerativeModel, Image

SERVICE_ACCOUNT_FILE = Path(__file__).resolve().parents[1] / "sa" / "sa.json"

# Authenticate using the service account key file
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)


def audio_to_text(
    project_id: str,
    audio_file: str,
    language_code: str,
) -> cloud_speech.RecognizeResponse:
    """Transcribe an audio file."""
    # Instantiates a client

    client = SpeechClient(credentials=credentials)

    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        # Language codes is optional
        language_codes=[language_code],
        model="long",
    )

    request = cloud_speech.RecognizeRequest(
        recognizer=f"projects/{project_id}/locations/global/recognizers/_",
        config=config,
        content=audio,
    )

    # Transcribes the audio into text
    response = client.recognize(request=request)
    # language = response.results
    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")

    return response.results[0].alternatives[0].transcript


if __name__ == "__main__":
    # Reads a file as bytes
    input_dir = Path(__file__).resolve().parents[1] / "input_data"
    with open(input_dir / "audio" / "download.wav", "rb") as f:
        audio = f.read()
    audio_to_text("qwiklabs-gcp-02-08a8c713b151", audio, language_code="en-GB")
