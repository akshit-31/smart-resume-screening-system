from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine
import numpy as np

def cosine_similarity_score(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Compute cosine similarity between two numpy vectors.
    Returns a float between 0 and 1.
    """
    vec1 = vec1.reshape(1, -1)
    vec2 = vec2.reshape(1, -1)
    return float(sklearn_cosine(vec1, vec2)[0][0])
