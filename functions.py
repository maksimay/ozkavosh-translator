import csv
from pydub import AudioSegment

def csv_to_list(filepath,listname):
    """
    reads a csv file and appends the words to a list object
    """
    with open(filepath) as csvfile:
        dictionary = csv.reader(csvfile, delimiter=' ')
        for row in dictionary:
            listname.append(','.join(row))


def audio_export(audiofile,filename):
    """
    exports a pydub audioobject to a .wav file with the given filename
    """
    return audiofile.export(filename , format="wav")


def detect_silence(sound, silence_threshold=-50.0, chunk_size=10):
    # silence_threshold in dB
    # chunk_size in ms
    # iterate over chunks until you find the first one with sound
    trim_ms = 0
        # to avoid infinite loop
    assert chunk_size > 0
    while sound[trim_ms:trim_ms + chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms

def remove_silence(src_audio):
    start_trim = detect_silence(src_audio)
    end_trim = detect_silence(src_audio.reverse())
    trimmed_audio = src_audio[start_trim:duration - end_trim]

    return trimmed_audio