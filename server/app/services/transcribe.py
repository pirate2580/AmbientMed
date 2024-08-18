import whisper
import os
from dotenv import load_dotenv
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate

from pyannote.audio import Pipeline
import torchaudio
import subprocess
import io

def extract_audio_with_ffmpeg(video_path):
    """Extract audio from video using ffmpeg and return as a waveform tensor."""
    # Use ffmpeg to extract the audio directly to a bytes buffer
    command = [
        'ffmpeg',
        '-i', video_path,
        '-f', 'wav',
        '-acodec', 'pcm_s16le',
        '-'
    ]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()

    if process.returncode != 0:
        raise RuntimeError(f"ffmpeg error: {err.decode()}")

    audio_buffer = io.BytesIO(out)
    waveform, sample_rate = torchaudio.load(audio_buffer)

    return waveform, sample_rate

def process_video(video_path):
    """Function to process video, get transcription, make SOAP note"""
    load_dotenv()

    # Extract audio from the video as a waveform
    waveform, sample_rate = extract_audio_with_ffmpeg(video_path)

    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=os.environ.get('HUGGINGFACE_API_KEY'))

    diarization = pipeline({"waveform": waveform, "sample_rate": sample_rate})
    diarization_list = []
    for segment, _, speaker in diarization.itertracks(yield_label=True):
        diarization_list.append([speaker, segment.start, segment.end])

    model = whisper.load_model("base")
    transcription = model.transcribe(video_path)
    transcription_segments = transcription['segments']
    pointer = 0
    final_result = []
    for segment in diarization_list:
        print(segment)
        if pointer == len(transcription_segments):
            break
        speaker = segment[0]
        segment_start = segment[1]
        segment_end = segment[2]
        whisper_start = transcription_segments[pointer]['start']
        whisper_end = transcription_segments[pointer]['end']
        while pointer < len(transcription_segments) and (max(segment_start, whisper_start) < min(segment_end, whisper_end)):
            final_result.append([speaker, segment_start, segment_end, transcription_segments[pointer]['text']])
            pointer += 1
            if pointer == len(transcription_segments):
                break
            whisper_start = transcription_segments[pointer]['start']
            whisper_end = transcription_segments[pointer]['end']
            print(segment, pointer)
    return final_result

    # for segment in transcription['segments']:
    # return transcription
    # return diarization, transcription

# video_path = '../../test_audio/neurotechsoftware.mp4'

# Usage
# diarization, transcription = process_video(video_path)
# transcription = process_video(video_path)
# print(diarization)
# Print out detailed information about each segment
# for segment, _, speaker in diarization.itertracks(yield_label=True):
#     print(f"Speaker {speaker} spoke from {segment.start} to {segment.end}")

# print()
# print(transcription)