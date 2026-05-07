from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Resume:
    filename: str
    raw_text: str = ""
    clean_text: str = ""
    tfidf_score: float = 0.0
    bert_score: Optional[float] = None
    final_score: float = 0.0
    rank: int = 0
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            'filename': self.filename,
            'tfidf_score': round(self.tfidf_score * 100, 2),
            'bert_score': round(self.bert_score * 100, 2) if self.bert_score else None,
            'final_score': round(self.final_score * 100, 2),
            'rank': self.rank,
            'error': self.error,
            'raw_text_preview': self.raw_text[:300] + '...' if len(self.raw_text) > 300 else self.raw_text
        }
