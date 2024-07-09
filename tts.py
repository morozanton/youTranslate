from gtts import gTTS
import gtts
import os


class TTS:
    """Runs gTTS (Google text to speech) API"""
    FILE_PATH = "temp/audio"
    FILENAME = "speech.mp3"

    @classmethod
    def get_supported_langs(cls) -> dict:
        """Returns supported languages with their codes"""
        return gtts.lang.tts_langs()

    @classmethod
    def convert(cls, text: str, lang_to: str, filename: str, save_path: str = "temp/audio/") -> None:
        """
        Converts text to speech
        :param text: original text
        :param lang_to: text language
        :param filename: resulting filename
        :param save_path: a path to save
        """
        myobj = gTTS(text=text, lang=lang_to, slow=False)
        myobj.save(save_path + filename)

    @classmethod
    def playback(cls):
        """
        Plays an audio file
        """
        audio = cls.FILE_PATH + cls.FILENAME
        os.system(f"start {audio}")


if __name__ == "__main__":
    ...
