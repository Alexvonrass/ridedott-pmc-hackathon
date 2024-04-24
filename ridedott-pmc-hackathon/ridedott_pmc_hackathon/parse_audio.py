from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech


def audio_to_text(
    project_id: str,
    audio_file_path: str,
) -> cloud_speech.RecognizeResponse:
    """Transcribe an audio file."""
    # Instantiates a client
    client = SpeechClient()

    # Reads a file as bytes
    with open(audio_file_path, "rb") as f:
        content = f.read()

    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        # Language codes is optional
        # language_codes=["nl-NL", "ar-MA", "en-US", "tr-TR", "uk-UA"],
        model="long",
    )

    request = cloud_speech.RecognizeRequest(
        recognizer=f"projects/{project_id}/locations/global/recognizers/_",
        config=config,
        content=content,
    )

    # Transcribes the audio into text
    response = client.recognize(request=request)
    language = response.results

    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")

    return response
