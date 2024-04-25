from pathlib import Path

import vertexai
from google.api_core.client_options import ClientOptions
from vertexai.preview.generative_models import GenerativeModel, Image

if __name__ == "__main__":
    PROJECT_ID = "qwiklabs-gcp-02-08a8c713b151"
    REGION = "europe-west4"
    vertexai.init(project=PROJECT_ID, location=REGION)
    input_dir = Path(__file__).resolve().parents[1] / "input_data"
    with open(
        input_dir
        / "messages"
        / "client_questions"
        / "fake_question_glioma.txt",
        "r",
    ) as file:
        questions = file.read()

    with open(
        input_dir / "instructions" / "text" / "high_grade_glioma.txt", "r"
    ) as file:
        context = file.read()

    print(questions, context)

    generative_multimodal_model = GenerativeModel(
        "gemini-1.5-pro-preview-0409"
    )

    model_prompt = f"""
        {context}
        using the above context, answer the following question:
        {questions}"""

    generative_multimodal_model = GenerativeModel(
        "gemini-1.5-pro-preview-0409"
    )
    response = generative_multimodal_model.generate_content(model_prompt)
    print(response)
    # completion = await generative_multimodal_model.generate_content_async(
    #     stream=True, contents="hello"
    # )
    #
    # iter = completion.__aiter__()
