import requests
import os
import dotenv


class Translator:
    """Runs Google Translate API"""
    dotenv.load_dotenv()
    API_KEY = os.getenv('API_KEY')

    @classmethod
    def translate(cls, text: str, lang_to: str, lang_from: str = "en") -> dict:
        """
        Translates a text
        :param text: target text
        :param lang_to: language to translate into
        :param lang_from: origin language
        :return: json API response
        """
        translate_url = "https://google-translator9.p.rapidapi.com/v2"
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": cls.API_KEY,
            "X-RapidAPI-Host": "google-translator9.p.rapidapi.com"
        }
        payload = {
            "q": text,
            "source": lang_from,
            "target": lang_to,
            "format": "text"
        }
        response = requests.post(translate_url, json=payload, headers=headers)
        return response.json()

    @classmethod
    def get_supported_langs(cls) -> dict:
        """Returns a json of languages and their codes supported by this API"""
        langs_url = "https://google-translator9.p.rapidapi.com/v2/languages"
        headers = {
            "X-RapidAPI-Key": cls.API_KEY,
            "X-RapidAPI-Host": "google-translator9.p.rapidapi.com"
        }
        response = requests.get(langs_url, headers=headers)
        return response.json()
