import base64
import json

from google.cloud import speech, storage
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech


def audio_to_text(
    project_id: str,
    audio_file: str,
    gcs_uri: str,
    language: str,
) -> cloud_speech.RecognizeResponse:
    """Transcribe an audio file."""
    # Instantiates a client

    client = SpeechClient()

    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=[language],
        model="long",
    )

    file_metadata = cloud_speech.BatchRecognizeFileMetadata(uri=gcs_uri)

    request = cloud_speech.BatchRecognizeRequest(
        recognizer=f"projects/{project_id}/locations/global/recognizers/_",
        config=config,
        files=[file_metadata],
        recognition_output_config=cloud_speech.RecognitionOutputConfig(
            inline_response_config=cloud_speech.InlineOutputConfig(),
        ),
    )

    # Transcribes the audio into text
    operation = client.batch_recognize(request=request)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=120)

    print("Response")
    print(response)
    for result in response.results[gcs_uri].transcript.results:
        print(f"Transcript: {result.alternatives[0].transcript}")

    return response.results[gcs_uri].transcript

    # client = SpeechClient()

    # audio = speech.RecognitionAudio(uri=gcs_uri)
    # config = speech.RecognitionConfig(
    #     encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
    #     sample_rate_hertz=44100,
    #     language_code=language,
    # )

    # operation = client.long_running_recognize(config=config, audio=audio)

    # print("Waiting for operation to complete...")
    # response = operation.result(timeout=90)

    # transcript_builder = []
    # # Each result is for a consecutive portion of the audio. Iterate through
    # # them to get the transcripts for the entire audio file.
    # for result in response.results:
    #     # The first alternative is the most likely one for this portion.
    #     transcript_builder.append(f"\nTranscript: {result.alternatives[0].transcript}")
    #     transcript_builder.append(f"\nConfidence: {result.alternatives[0].confidence}")

    # transcript = "".join(transcript_builder)
    # print(transcript)

    # return transcript

    # config = cloud_speech.RecognitionConfig(
    #     auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
    #     # Language codes is optional
    #     language_codes=[language],
    #     model="long",
    # )

    # request = cloud_speech.RecognizeRequest(
    #     recognizer=f"projects/{project_id}/locations/global/recognizers/_",
    #     config=config,
    #     content=audio_file,
    # )

    # # Transcribes the audio into text
    # response = client.recognize(request=request)
    # #language = response.results
    # #print(response)
    # for result in response.results:
    #     print(f"Transcript: {result.alternatives[0].transcript}")

    # return response


def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = json.loads(
        base64.b64decode(event["data"]).decode("utf-8")
    )

    src_bucket = pubsub_message["bucket"]
    src_fname = pubsub_message["name"]
    print("Processing file:", src_fname)
    print("Processing bucket:", src_bucket)
    print(type(src_fname))

    storage_client = storage.Client()
    language = src_fname[src_fname.find("_") + 1 : src_fname.find(".")]
    print("LANGUAGE")
    print(language)

    bucket = storage_client.bucket(src_bucket)
    blob = bucket.blob(src_fname)
    contents = blob.download_as_bytes()

    gcs_uri = f"gs://{src_bucket}/{src_fname}"
    print(gcs_uri)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    print("Contents")
    print(type(contents))
    print(contents)

    audio_to_text("qwiklabs-gcp-02-08a8c713b151", contents, gcs_uri, language)
