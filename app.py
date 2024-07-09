import json
from flask import Flask, render_template, request, flash
import re
from helpers import run_sequence

app = Flask(__name__)
app.secret_key = 'super secret key'

video_id_re = r".+\?v=(.+)"
TEMP_PATH = "temp/audio/"


@app.route("/", methods=["GET", "POST"])
def index():
    """
    The one route that contains a form to get video url and desired language, triggers the translation and then redirects
    to video page, passing the translated audio
    """
    with open("static/supported_langs.json", "r") as f:
        langs = json.load(f)

    if request.method == "POST":
        video_url = request.form.get("link")
        lang = request.form.get("language")
        if video_url and lang:
            if lang not in langs:
                flash("Please select a language")
            else:
                if re.match(video_id_re, video_url):
                    video_id = re.match(video_id_re, video_url).group(1)

                    result = run_sequence(video_url, lang_to=lang, temp_path=TEMP_PATH)
                    if result:
                        audio_path = "static/full.mp3"
                        return render_template("watch.html", video_id=video_id, audio_path=audio_path)
                    else:
                        flash("Server error :(")
                else:
                    flash("Please enter YouTube video url")
        elif not video_url:
            flash("Please enter a url")
        elif not lang:
            flash("Please select a language")

    return render_template("index.html", langs=langs)
