"""Helper file to transcribe audio and video"""

import whisper
import os
from dotenv import load_dotenv
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

from pyannote.audio import Pipeline
import torchaudio
import torchaudio.transforms as T
import subprocess
import io

import cv2
import numpy as np
import base64
import imageio
from io import BytesIO

# def extract_audio_with_ffmpeg(video_file: bytes):
#     """Helper function to extract audio from video using ffmpeg and return as a waveform tensor."""
#     video_file.seek(0)
#     command = [
#         'ffmpeg',
#         '-i', 'pipe:0',  # Read input from stdin
#         '-f', 'wav',
#         '-acodec', 'pcm_s16le',
#         '-'
#     ]
#     process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     out, err = process.communicate(input=video_file.read())
#     if process.returncode != 0:
#         raise RuntimeError(f"ffmpeg error: {err.decode()}")
#     audio_buffer = io.BytesIO(out)
#     waveform, sample_rate = torchaudio.load(audio_buffer)
#     return waveform, sample_rate

def extract_audio_with_ffmpeg(video_file: bytes):
    """Helper function to extract audio from video using ffmpeg and return as a waveform tensor."""
    video_file.seek(0)
    command = [
        'ffmpeg',
        '-i', 'pipe:0',  # Read input from stdin
        '-vn',           # Ignore video stream
        '-acodec', 'pcm_s16le',  # Use PCM audio codec (WAV format)
        '-ar', '16000',  # Set sample rate to 16kHz
        '-ac', '1',      # Mono channel
        '-f', 'wav',
        '-'              # Output to stdout
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate(input=video_file.read())
    if process.returncode != 0:
        raise RuntimeError(f"ffmpeg error: {err.decode()}")
    audio_buffer = io.BytesIO(out)
    waveform, sample_rate = torchaudio.load(audio_buffer)
    return waveform, sample_rate


def transcribe_audio(video_file: bytes):
    """Function to process video, get transcription with diarization"""
    load_dotenv()
    waveform, sample_rate = extract_audio_with_ffmpeg(video_file)   # Extract audio from the video as a waveform, 

    if sample_rate != 16000:                                        # Resample the audio to 16kHz (the expected input for Whisper)
        resampler = T.Resample(orig_freq=sample_rate, new_freq=16000)
        waveform = resampler(waveform)
        sample_rate = 16000

    audio_data = waveform.squeeze().numpy()
    # diarization pipeline
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=os.environ.get('HUGGINGFACE_API_KEY'))

    diarization = pipeline({"waveform": waveform, "sample_rate": sample_rate})
    diarization_list = []
    for segment, _, speaker in diarization.itertracks(yield_label=True):
        diarization_list.append([speaker, segment.start, segment.end])

    model = whisper.load_model("base")
    transcription = model.transcribe(audio_data)
    transcription_segments = transcription['segments']


    # final generation point
    pointer = 0
    final_result = []
    for segment in diarization_list:
        if pointer == len(transcription_segments):
            break
        speaker = segment[0]
        segment_start = segment[1]
        segment_end = segment[2]
        whisper_start = transcription_segments[pointer]['start']
        whisper_end = transcription_segments[pointer]['end']
        while pointer < len(transcription_segments) and (max(segment_start, whisper_start) < min(segment_end, whisper_end)):
            final_result.append({'speaker': speaker, 'segment_start':whisper_start, 'segment_end': whisper_end, 'segment_transcription': transcription_segments[pointer]['text']})
            pointer += 1
            if pointer == len(transcription_segments):
                break
            whisper_start = transcription_segments[pointer]['start']
            whisper_end = transcription_segments[pointer]['end']
    return final_result

# def process_video(video_path, fps=1):
#     # Open the video file using the provided file path
#     cap = cv2.VideoCapture(video_path)

#     if not cap.isOpened():
#         raise ValueError("Error opening video file or stream")

#     frame_rate = int(cap.get(cv2.CAP_PROP_FPS))  # Get original FPS of the video
#     interval = max(1, int(frame_rate / fps))  # Ensure interval is at least 1

#     base64_frames = []
#     count = 0

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         if count % interval == 0:
#             _, buffer = cv2.imencode('.jpg', frame)
#             frame_base64 = base64.b64encode(buffer).decode('utf-8')
#             base64_frames.append(frame_base64)

#         count += 1

#     cap.release()
#     return base64_frames

# def describe_video(video_path, processed_transcript: str, fps=0.1):
#     """Function to generate description with GPT-4 from video at 0.1 fps (for price reasons)"""
#     base64Frames = process_video(video_path, fps=fps)
    
#     prompt_content = (
#         "These are frames from a video of an appointment between a physician and a patient. "
#         "Generate an accurate description of the patient, using the transcript to help: " 
#         + processed_transcript
#     )

#     frames_list = [{"image": frame, "resize": 768} for frame in base64Frames[::50]]
    
#     PROMPT_MESSAGES = [
#         {
#             "role": "user",
#             "content": prompt_content,
#             "frames": frames_list
#         }
#     ]
    
#     params = {
#         "model": "gpt-4o",
#         "messages": PROMPT_MESSAGES,
#         "max_tokens": 200,
#     }

#     result = openai.ChatCompletion.create(**params)
#     print(result)
#     return result.choices[0].message.content