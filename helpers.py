from translator import Translator
from tts import TTS
from webdriver import Driver
import json
from audio_processor import Processor
import os


def run_sequence(video_url: str, lang_to: str, lang_from: str = "en", temp_path: str = "/temp/audio/") -> bool:
    """
    Runs all the helper functions needed to translate a video
    :param video_url: source video to scrape captions from
    :param lang_to: translation language code
    :param lang_from: original language code
    :param temp_path: path for storing temporary files
    :return: bool indicating whether the function completed
    """

    captions = get_transcription(video_url)
    print("\n\ncaptions ", captions)
    # sentences = separate_sentences(captions)
    sentences = captions
    print("\n\nsentences", sentences)
    translation = translate_captions(sentences, lang_to=lang_to, lang_from=lang_from)
    print("\n\ntranslation", translation)
    make_audios(translation, lang_to=lang_to, path=temp_path)
    ans = cut_audios(temp_path=temp_path)
    print("\n\nAudios are cut", ans)
    if ans is True:
        clean_files(path=temp_path)
        return True
    else:
        return False


def get_transcription(video_url: str) -> dict:
    """
    Scrapes video captions from YouTube
    :param video_url: url
    :return: Dict of captions with time codes as they appear on YouTube
    """
    driver = Driver()
    driver.open_url(video_url)
    return driver.find_captions()


def separate_sentences(captions: dict) -> dict:
    """
    If there is punctuation in the captions: groups captions into sentences for better translation.
    Leaves timecode for the beginning of each sentence.
    :param captions: Dict of captions from YouTube
    :return: Dict of sentences with their time codes
    """
    # Checks whether YouTube automatic captions are dot-separated. If not, returns the captions unchanged
    for val in captions.values():
        if "." in val:
            break
    else:
        return captions
    processed = {}
    sentence = ""
    timeframe = ""

    for key, line in captions.items():
        print(key, line)
        if sentence == "":
            timeframe = key
        sentence += line + " "
        if line.endswith("."):
            processed[timeframe] = sentence
            sentence = ""
    return processed


def translate_captions(captions: dict, lang_to: str, lang_from: str = "en") -> dict:
    """
    Translates the captions as one text and then rebuilds them back into dict with timecodes
    :param captions: Dict of captions (or sentences)
    :param lang_to: language code to translate into
    :param lang_from: original language
    :return: same dict of captions (or sentences), but translated
    """
    # Concatenate all transcript text to reduce number of translator API calls
    full_transcript = "".join(captions.values())

    response = Translator.translate(text=full_transcript, lang_to=lang_to, lang_from=lang_from)
    translation = response['data']['translations'][0]['translatedText']

    # Separate translated text back to sentences
    return dict(zip(captions.keys(), translation.split(". ")))


def make_audios(keyframes: dict, lang_to: str, path: str = "temp/audio/") -> None:
    """
    Runs TTS on each sentence from captions and saves it in a separate file named with the sentence's timecode
    :param keyframes: Dict of captions
    :param lang_to: Language code for TTS
    :param path: Directory for outputting audios
    """
    audio_format = ".mp3"
    for key, line in keyframes.items():
        filename = key.replace(":", "-") + audio_format
        TTS.convert(text=line, lang_to=lang_to, filename=filename, save_path=path)


def cut_audios(temp_path: str = "temp/audio/", out_path: str = "static/", filename: str = "full.mp3") -> bool:
    """
    Uses audio_processor.py to rebuild and join all audio files together
    :param temp_path: Directory with all audios to join
    :param out_path: Path for saving the resulting file
    :param filename: Filename of resulting file
    :return: Bool to indicate whether the file has been created
    """
    Processor.keyframes_to_audio(temp_path, out_path, filename)
    return os.path.isfile(out_path + filename)


def get_supported_langs() -> None:
    """Get a list of languages supported BOTH by translator and TTS APIs and save it as json file"""

    translator_langs = Translator.get_supported_langs()["data"]["languages"]
    translator_codes = [c["language"] for c in translator_langs]
    tts_codes = TTS.get_supported_langs()
    supported_langs = {}
    for code, name in tts_codes.items():
        if code in translator_codes:
            supported_langs[code] = name

    with open("static/supported_langs.json", 'w') as file:
        json.dump(supported_langs, file)


def clean_files(path: str = "temp/audio/"):
    """
    Clean all the temporary audio files
    :param path: Files directory
    """
    for f in os.listdir(path):
        os.remove(path + f)


if __name__ == "__main__":
    ...
