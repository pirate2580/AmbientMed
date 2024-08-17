"""
Route(s) for transcription with basic diarization endpoint
"""

from flask import Blueprint, request
import os
import sys

transcribe_bp = Blueprint('transcribe', __name__)

@transcribe_bp.route("/transcribe", methods=["POST"])
def transcribe():
  