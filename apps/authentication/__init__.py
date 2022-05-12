# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Blueprint
from models.detector import face_detector
from models.verifier.face_verifier import FaceVerifier

blueprint = Blueprint(
    'authentication_blueprint',
    __name__,
    url_prefix=''
)

