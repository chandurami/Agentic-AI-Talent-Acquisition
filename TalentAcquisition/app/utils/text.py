from __future__ import annotations

import re
from typing import List

import nltk
from nltk.corpus import stopwords


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text: str) -> List[str]:
    tokens = nltk.word_tokenize(text)
    stops = set(stopwords.words("english"))
    return [t for t in tokens if t not in stops and t.isalnum()]

