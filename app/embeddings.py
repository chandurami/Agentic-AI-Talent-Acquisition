from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class EmbeddingIndex:
    vectorizer: TfidfVectorizer
    matrix: np.ndarray
    ids: List[str]

    def query(self, texts: List[str]) -> np.ndarray:
        q = self.vectorizer.transform(texts)
        return cosine_similarity(q, self.matrix)


def build_index(ids: List[str], texts: List[str]) -> EmbeddingIndex:
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(texts)
    return EmbeddingIndex(vectorizer=vectorizer, matrix=matrix, ids=ids)

