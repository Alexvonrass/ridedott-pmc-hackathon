from dataclasses import dataclass

language_dict = {
    "kk-KZ": "Kazakh (Kazakhstan)",
    "ko-KR": "Korean (South Korea)",
    "en-GB": "English (United Kingdom)",
    "ru-RU": "Russian (Russia)",
}

language_dropdown_options = [
    {"label": label, "value": value} for value, label in language_dict.items()
]
