import re

from sentence_transformers import util

from app.services.drug_classifier import has_drug_context
from app.services.embedding_model import model


def _u(value: str) -> str:
    return value.encode("utf-8").decode("unicode_escape")


CRIME_CLASSES = {
    "sale": ["selling drugs", "drug dealer", "drug sale"],
    "usage": ["using drugs", "drug addiction", "smoking drugs"],
    "transport": ["transporting drugs", "carrying drugs", "drug delivery"],
    "storage": ["storing drugs", "hidden drugs"],
    "production": ["manufacturing drugs", "making drugs"],
}

CRIME_KEYWORDS = {
    "sale": [
        "selling", "sale", "supply", "supplying", "suply", "supplier", "dealer",
        "deal", "packets", "shop", "close pannunga", "supply panna", "selling panna",
        _u(r"\u0bb5\u0bbf\u0b95\u0bcd\u0b95\u0bbf\u0bb1\u0bbe\u0b99\u0bcd\u0b95"),
        _u(r"\u0bb5\u0bbf\u0b95\u0bcd\u0b95\u0bbf\u0bb0\u0b99\u0bcd\u0b95\u0bbe"),
        _u(r"\u0bb5\u0bbf\u0b95\u0bcd\u0b95\u0bc1\u0bb1\u0bbe\u0b99\u0bcd\u0b95"),
        _u(r"\u0bb5\u0bbf\u0b95\u0bcd\u0b95\u0bb1\u0bbe\u0b99\u0bcd\u0b95"),
        _u(r"\u0bb5\u0bbf\u0b95\u0bcd\u0b95\u0bc1\u0ba4\u0bc1"),
        _u(r"\u0bb5\u0bbf\u0bb1\u0bcd\u0b95\u0bbf\u0bb1\u0bbe\u0bb0\u0bcd\u0b95\u0bb3\u0bcd"),
        _u(r"\u0bb5\u0bbf\u0bb1\u0bcd\u0b95\u0bc1\u0bb1\u0bbe\u0b99\u0bcd\u0b95"),
        _u(r"\u0bb5\u0bbf\u0bb1\u0bcd\u0b95\u0bc1\u0bb1"),
        _u(r"\u0bb5\u0bbf\u0bb1\u0bcd\u0baa\u0ba9\u0bc8"),
        _u(r"\u0bb5\u0bbf\u0bb1\u0bcd\u0bb1\u0bc1"),
    ],
    "usage": [
        "using", "use", "smoking", "addict", "taking", "smell", "disturbance",
        "use pann", "daily fight", "fight", "roaming",
        _u(r"\u0b85\u0b9f\u0bbf\u0b95\u0bcd\u0b95\u0bbf\u0bb1\u0bbe\u0b99\u0bcd\u0b95"),
        _u(r"\u0b85\u0b9f\u0bbf\u0b95\u0bcd\u0b95\u0bc1\u0bb1\u0bbe\u0b99\u0bcd\u0b95"),
        _u(r"\u0b95\u0bc1\u0b9f\u0bbf\u0b95\u0bcd\u0b95\u0bbf\u0bb1\u0bbe\u0b99\u0bcd\u0b95"),
        _u(r"\u0b95\u0bc1\u0b9f\u0bbf\u0b95\u0bcd\u0b95\u0bc1\u0bb1\u0bb5\u0b99\u0bcd\u0b95"),
        _u(r"\u0baa\u0bc1\u0b95\u0bc8\u0b95\u0bcd\u0b95\u0bbf\u0bb1\u0bbe\u0b99\u0bcd\u0b95"),
        _u(r"\u0baa\u0bc1\u0b95\u0bc8\u0b95\u0bcd\u0b95\u0bc1\u0bb1\u0bbe\u0b99\u0bcd\u0b95"),
        _u(r"\u0baa\u0baf\u0ba9\u0bcd\u0baa\u0b9f\u0bc1\u0ba4\u0bcd\u0ba4\u0bc1\u0bb1\u0bbe\u0b99\u0bcd\u0b95"),
        _u(r"\u0b89\u0baa\u0baf\u0bcb\u0b95\u0bae\u0bcd"),
    ],
    "transport": [
        "transport", "carrying", "delivery",
        _u(r"\u0b95\u0b9f\u0ba4\u0bcd\u0ba4\u0bb2\u0bcd"),
        _u(r"\u0b95\u0b9f\u0ba4\u0bcd\u0ba4\u0bc1\u0bb1\u0bbe\u0b99\u0bcd\u0b95"),
        _u(r"\u0b95\u0bca\u0ba3\u0bcd\u0b9f\u0bc1 \u0baa\u0bcb\u0bb1\u0bbe\u0b99\u0bcd\u0b95"),
    ],
    "storage": [
        "store", "storing", "hidden",
        _u(r"\u0bae\u0bb1\u0bc8\u0ba4\u0bcd\u0ba4\u0bc1"),
        _u(r"\u0bb5\u0bc8\u0ba4\u0bcd\u0ba4\u0bbf\u0bb0\u0bc1\u0b95\u0bcd\u0b95\u0bbf\u0bb1\u0bbe\u0bb0\u0bcd\u0b95\u0bb3\u0bcd"),
        _u(r"\u0bb5\u0b9a\u0bcd\u0b9a\u0bbf\u0bb0\u0bc1\u0b95\u0bcd\u0b95\u0bbe\u0b99\u0bcd\u0b95"),
    ],
    "production": [
        "manufacturing", "making", "producing",
        _u(r"\u0ba4\u0baf\u0bbe\u0bb0\u0bbf\u0b95\u0bcd\u0b95\u0bbf\u0bb1\u0bbe\u0bb0\u0bcd\u0b95\u0bb3\u0bcd"),
    ],
}

crime_embeddings = {
    k: model.encode(v, normalize_embeddings=True)
    for k, v in CRIME_CLASSES.items()
}


def _is_ascii_wordish(value: str) -> bool:
    return bool(re.fullmatch(r"[a-z0-9][a-z0-9 ]*[a-z0-9]", value))


def _contains_term(text: str, term: str) -> bool:
    term = term.lower().strip()
    if not term:
        return False
    if _is_ascii_wordish(term):
        pattern = r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])"
        return re.search(pattern, text) is not None
    return term in text


def detect_crime(text: str, has_detected_drug: bool = False):
    text = text or ""
    text_lower = text.lower()

    for crime, keywords in CRIME_KEYWORDS.items():
        for keyword in keywords:
            if not _contains_term(text_lower, keyword):
                continue
            if _is_ascii_wordish(keyword) and not (has_detected_drug or has_drug_context(text)):
                continue
            return {
                "label": crime,
                "confidence": 1.0
            }

    text_emb = model.encode(text, normalize_embeddings=True)

    best_match = "unknown"
    best_score = 0

    for crime, emb in crime_embeddings.items():
        score = util.cos_sim(text_emb, emb).max().item()
        if score > best_score:
            best_score = score
            best_match = crime

    if best_score < 0.68 or not (has_detected_drug or has_drug_context(text)):
        best_match = "unknown"

    return {
        "label": best_match,
        "confidence": round(best_score, 3)
    }
