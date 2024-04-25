from enum import StrEnum

prompt_answer_with_context = """
        You are a doctor, having a conversation with the parent
        of a child with a disease. Using the above context, 
        in a concise and empathetic manner
        answer the patient's question:
        """


class Prompts(StrEnum):
    PROMPT_ANSWER = prompt_answer_with_context
