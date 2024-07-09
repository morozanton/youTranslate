from pydub import AudioSegment, effects, silence
import os
import time
from datetime import timedelta


class Processor:
    """A class that processes audio files to adjust their playback time and join them together"""

    @classmethod
    def load_file(cls, path: str):
        """
        Makes a pydub AudioSegment out of .mp3 file
        :param path: File path
        :return: the segment
        """
        if not path.endswith(".mp3"):
            raise ValueError("Unsupported audio format")
        return AudioSegment.from_mp3(path)

    @classmethod
    def keyframes_to_audio(cls, temp_path: str = "temp/audio/", out_path: str = "static/",
                           filename: str = "full.mp3") -> None:
        """
        The main method that adjusts playback length of all files according to specified keyframes
        and joins them into one complete audio. Saves the resulting file.

        :param temp_path: Path with temporary separate audios to work with
        :param out_path: Output file path
        :param filename: Output file name
        :return: Saves the final file
        """

        files = os.listdir(temp_path)
        for i in range(len(files) - 1):
            f1 = files[i]
            f2 = files[i + 1]
            cls.check_pairs(f1, f2, temp_path)

        full_audio = sum((AudioSegment.from_mp3(temp_path + file) for file in files), AudioSegment.empty())
        full_audio.export(out_path + filename)

    @classmethod
    def check_pairs(cls, f1, f2, path, time_format: str = "%M-%S", audio_format: str = ".mp3"):
        """
        Checks filenames of two files to get their keyframes, decides whether the first file needs to be extended or
        sped-up to match the beginning of the second file. Then modifies and saves the first file.
        :param f1: file to modify
        :param f2:  file to match timing with
        :param path: path to files location. File is saved (rewritten) in the same directory.
        :param time_format: datetime format to parse file names into keyframes
        :param audio_format: format of the audios to exclude it from name
        """
        def get_time(filename: str) -> time.struct_time:
            """Converts filename into REQIIRED audio start time"""
            return time.strptime(filename.replace(audio_format, ""), time_format)

        t1 = get_time(f1)
        t2 = get_time(f2)
        seg1 = AudioSegment.from_mp3(os.path.join(path, f1))
        seg1_len = cls.get_len_sec(seg1)
        goal_len = timedelta(minutes=t2.tm_min - t1.tm_min,
                             seconds=t2.tm_sec - t1.tm_sec).seconds
        diff = goal_len - seg1_len
        if diff > 0:
            seg1 = cls.add_pause(seg1, diff)
        elif diff < 0:
            seg1 = cls.shorten(seg1, -diff)
        seg1.export(path + f1)

    @classmethod
    def get_len_sec(cls, seg: AudioSegment) -> float:
        """Returns length of AudioSegment in seconds"""
        return len(seg) / 1000

    @staticmethod
    def add_pause(segment: AudioSegment, pause_sec: float) -> AudioSegment:
        """
        Adds silence to the end of the file (makes the audio longer)
        :param segment: target AudioSegment
        :param pause_sec: pause length
        :return: modified AudioSegment
        """
        return segment + AudioSegment.silent(duration=pause_sec * 1000)

    @classmethod
    def shorten(cls, segment: AudioSegment, goal_time: float) -> AudioSegment:
        """
        Makes an audio last shorter. First removes pauses between words. If not enough, speeds up by a calculated factor
        :param segment: target AudioSegment
        :param goal_time: target playback time of this segment
        :return: modified AudioSegment
        """
        segment = cls.strip_silence(segment)
        new_len = cls.get_len_sec(segment)
        if new_len > goal_time:
            f = round(new_len / goal_time, 2)
            segment = cls.speed_up(segment, factor=f)
        return segment

    @staticmethod
    def speed_up(segment: AudioSegment, factor: float) -> AudioSegment:
        """
        Uses pydub to speed the audio up
        :param segment: target AudioSegment
        :param factor: speeding-up factor
        :return: modified AudioSegment
        """
        return effects.speedup(segment, playback_speed=factor, chunk_size=50)

    @staticmethod
    def strip_silence(segment: AudioSegment) -> AudioSegment:
        """
        Uses pydub to delete silent parts of audio
        :param segment: target AudioSegment
        :return: modified AudioSegment
        """
        split_list = silence.split_on_silence(segment, min_silence_len=50, seek_step=10, silence_thresh=-29)
        return sum(split_list, AudioSegment.empty())


if __name__ == "__main__":
    now = time.time()
    Processor.keyframes_to_audio("temp-2/audio/")
    print("Passed", time.time() - now)
