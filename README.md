# YouTranslate

#### Video Demo:  https://www.loom.com/share/e6ba1fe4e6aa4093844cac0dcadd1be3

#### Description: A web application that translates YouTube videos into 59 languages

By ***Anton Moroz***

Github: **morozanton**

## Requirements:

- [flask](https://flask.palletsprojects.com/en/2.3.x/) ~= 2.3.2
- [selenium](https://www.selenium.dev/) ~= 4.11.2
- [gTTS](https://gtts.readthedocs.io/en/latest/) ~= 2.5.1
- [requests](https://requests.readthedocs.io/en/latest/) ~= 2.31.0
- [python-dotenv](https://pypi.org/project/python-dotenv/) ~= 1.0.0
- [pydub](https://pypi.org/project/pydub/) ~= 0.25.1

`audio_processor.py` requires "FFmpeg (Essentials Build)" which has to be installed separately.

# app.py

The Flask application file contains only one "/" route.
Uses three templates:

1. *layout.html* contains the `<head>` and `<footer>`
2. *index.html* contains a `post` request form for passing the video URL and desired translation language. This page
   handles form errors with Flask [flash](https://flask.palletsprojects.com/en/2.3.x/patterns/flashing/)
3. *watch.html* embeds the YouTube video into `<iframe>` and contains the Javascript code for controlling the translated
   audio.
   It makes sure the audio timing matches with the video even upon rewinding.

**TODO:** I tried passing "status messages" describing each translation step to *index.html*
using [SocketIo](https://flask-socketio.readthedocs.io/en/latest/) because video translation takes considerable time,
but did not succeed.

The TTS part could have been done better voice-wise, but Google's API is free and supports many languages. In general,
the resulting audios are very slow and require additional processing.

## index

The `index` function is the main route handler for this Flask application. It contains a form to input a video URL and
select a desired language for translation. After submitting the form, the function triggers the translation process and
redirects the user to a video page where the translated audio is available.

# helpers.py

Contains all the necessary functions to retrieve YouTube captions, translate them, convert to speech and adjust the
playback time to match the original audio.

## run_sequence

Runs all the helper functions needed to translate a video

### Parameters

- `video_url` (str): Source video URL to scrape captions from.
- `lang_to` (str): Translation language code.
- `lang_from` (str, optional): Original language code (default is "en").
- `temp_path` (str, optional): Path for storing temporary files (default is "/temp/audio/").

### Returns

bool: Indicates whether the function completed successfully.

## get_transcription

Scrapes video captions from YouTube.

### Parameters

- `video_url` (str): Video URL.

### Returns

dict: Dictionary of captions with time codes as they appear on YouTube.

## separate_sentences

Groups captions into sentences for better translation if there is punctuation in the captions.

### Parameters

- `captions` (dict): Dictionary of captions from YouTube.

### Returns

dict: Dictionary of sentences with their time codes.

## translate_captions

Translates captions as one text and then rebuilds them back into a dictionary with time codes.

### Parameters

- `captions` (dict): Dictionary of captions (or sentences).
- `lang_to` (str): Language code to translate into.
- `lang_from` (str, optional): Original language code (default is "en").

### Returns

dict: Same dictionary of captions (or sentences), but translated.

## make_audios

Runs text-to-speech (TTS) on each sentence from captions and saves it in a separate file named with the sentence's
timecode.

### Parameters

- `keyframes` (dict): Dictionary of captions.
- `lang_to` (str): Language code for TTS.
- `path` (str, optional): Directory for outputting audios (default is "temp/audio/").

## cut_audios

Rebuilds and joins all audio files together.

### Parameters

- `temp_path` (str, optional): Directory with all audios to join (default is "temp/audio/").
- `out_path` (str, optional): Path for saving the resulting file (default is "static/").
- `filename` (str, optional): Filename of resulting file (default is "full.mp3").

### Returns

bool: Indicates whether the file has been created.

## get_supported_langs

Get a list of languages supported by both the translator and TTS APIs and save it as a JSON file for quick access in the
Flask application

## clean_files

Clean all the temporary audio files.

### Parameters

- `path` (str, optional): Files directory (default is "temp/audio/").

# webdriver.py

This class provides methods to interact with Selenium WebDriver for scraping YouTube video captions. The `open_url`
method loads a given URL, while the `find_captions` method opens video captions on YouTube and returns them as a
dictionary of time-text pairs.

## Driver class

Uses Selenium to scrape YouTube video captions. All methods are `@classmethod`s.

### Attributes

- `WAIT_TIME` (int): Response waiting threshold (default is 10 seconds).

### Methods

## \__init__()

Initializes the Driver class by running the web driver in headless mode.

## open_url

Loads the given URL in the web driver.

### Parameters:

- `url` (str): URL to load.

## find_captions

Opens video captions on YouTube and saves all of them in a dictionary of `{time : text}` pairs.

### Returns

The resulting dictionary of captions.

# translator.py

## Translator Class

Provides methods to interact with the Google Translate API for translating text.
Uses own `API_KEY` that is loaded from a **.env** file.

### Methods

## translate

- Translates a text.

### Parameters:

- `text` (str): The target text to translate.
- `lang_to` (str): The **language code** to translate into.
- `lang_from` (str, optional): The origin language. Defaults to "en".

### Returns

`dict`: API response in JSON format.

## get_supported_langs

- Get a JSON of languages and their codes supported by this API.

### Returns

`dict`: JSON containing supported languages and their codes.

# tts.py

Provides methods to interact with the gTTS (Google text to speech) API for converting text to speech.

## Class: TTS

All methods are `@classmethod`s.

### Methods:

## get_supported_langs

Returns a `dict` of supported languages with their codes.

## convert

Converts text to speech.

### Parameters:

- `text` (str): The original text.
- `lang_to` (str): The language of the text.
- `filename` (str): The resulting filename.
- `save_path` (str, optional): A path to save the audio file. Defaults to "temp/audio/".

## playback

- Plays an audio file.

# audio_processor.py

Provides methods to process audio files, adjust their playback time, and join them together into one complete audio.

## Class: Processor

All methods are `@classmethod`s.

## load_file

Makes a pydub AudioSegment out of .mp3 file.

### Parameters:

- `path` (str): File path.

### Returns

The segment.

## keyframes_to_audio

The main method that adjusts playback length of all files according to specified keyframes and joins them into one
complete audio. Saves the resulting file.

### Parameters:

- `temp_path` (str, optional): Path with temporary separate audios to work with. Defaults to "temp/audio/".
- `out_path` (str, optional): Output file path. Defaults to "static/".
- `filename` (str, optional): Output file name. Defaults to "full.mp3".

## check_pairs

Checks filenames of two files to get their keyframes, decides whether the first file needs to be extended or sped-up to
match the beginning of the second file. Then modifies and saves the first file.

### Parameters:

- `f1`: File to modify.
- `f2`: File to match timing with.
- `path`: Path to files location. File is saved (rewritten) in the same directory.
- `time_format` (str, optional): Datetime format to parse file names into keyframes. Defaults to "%M-%S".
- `audio_format` (str, optional): Format of the audios to exclude it from name. Defaults to ".mp3".

## get_len_sec

Returns length of AudioSegment in seconds.

### Parameters:

- `seg`: The AudioSegment.

### Returns

Length of the segment in seconds.

## add_pause

Adds silence to the end of the file (makes the audio longer).

### Parameters:

- `segment`: Target AudioSegment.
- `pause_sec`: Pause length.

### Returns

Modified AudioSegment.

## shorten

Makes an audio shorter. First removes pauses between words. If not enough, speeds up by a calculated factor.

### Parameters:

- `segment`: Target AudioSegment.
- `goal_time`: Target playback time of this segment.

### Returns

Modified AudioSegment.

## speed_up

Uses pydub to speed the audio up.

### Parameters:

- `segment`: Target AudioSegment.
- `factor`: Speeding-up factor.

### Returns

Modified AudioSegment.

## strip_silence

Uses pydub to delete silent parts of audio.

### Parameters:

- `segment`: Target AudioSegment.

### Returns

Modified AudioSegment.
