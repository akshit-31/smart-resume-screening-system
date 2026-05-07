def compute_bert_similarity(jd_text: str, resume_text: str) -> float:
    """
    Compute semantic similarity using BERT sentence embeddings.
    Uses sentence-transformers library.
    Returns a score between 0 and 1.
    """
    try:
        from sentence_transformers import SentenceTransformer, util

        model = SentenceTransformer('all-MiniLM-L6-v2')

        # Truncate texts to avoid token limit issues
        jd_truncated = jd_text[:512]
        resume_truncated = resume_text[:512]

        embeddings = model.encode([jd_truncated, resume_truncated], convert_to_tensor=True)
        score = util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()

        # Normalize to 0-1 range (cosine similarity can be -1 to 1)
        score = (score + 1) / 2
        return float(score)

    except ImportError:
        raise ImportError(
            "sentence-transformers not installed. "
            "Run: pip install sentence-transformers"
        )
    except Exception as e:
        raise ValueError(f"BERT similarity failed: {str(e)}")
