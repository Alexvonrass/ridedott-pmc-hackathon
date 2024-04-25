from dataclasses import dataclass

language_dict = {
    "kk-KZ": "Kazakh (Kazakhstan)",
    "ko-KR": "Korean (South Korea)",
}

language_dropdown_options = [
    {"label": label, "value": value} for value, label in language_dict.items()
]
