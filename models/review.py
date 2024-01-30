#!/usr/bin/python3
"""Review class defined"""
from models.base_model import BaseModel


class Review(BaseModel):
    """Represent a review representation"""

    place_id = ""
    user_id = ""
    text = ""
