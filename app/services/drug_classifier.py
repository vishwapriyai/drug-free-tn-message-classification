import re
from difflib import SequenceMatcher

from sentence_transformers import util
import os
from app.services.embedding_model import get_model

try:
    import spaces
except ImportError:
    class MockSpaces:
        def GPU(self, fn=None):
            if fn: return fn
            return lambda f: f
    spaces = MockSpaces()


try:
    from rapidfuzz import fuzz
except ImportError:
    class fuzz:
        @staticmethod
        def ratio(left, right):
            return SequenceMatcher(None, left, right).ratio() * 100

        @staticmethod
        def partial_ratio(left, right):
            if len(left) > len(right):
                left, right = right, left
            if not left:
                return 0
            best = 0
            for index in range(0, max(1, len(right) - len(left) + 1)):
                window = right[index:index + len(left)]
                best = max(best, fuzz.ratio(left, window))
            return best


def _u(value: str) -> str:
    return value.encode("utf-8").decode("unicode_escape")


DRUG_KEYWORDS = {
    "ganja": [
        "ganja", "kanja", "khanja", "kancha", "kannaja", "kanaja", "kannja",
        "kannacha", "ganga", "marijuana", "marihuana",
        "weed", "pot", "grass", "joint", "smoke", "hashish", "hash", "charas",
        "cannabis", "cannabis oil", "thc oil", "edibles",
        _u(r"\u0b95\u0b9e\u0bcd\u0b9a\u0bbe"),
        _u(r"\u0b95\u0ba9\u0bcd\u0b9c\u0bbe"),
        _u(r"\u0b95\u0b9e\u0bcd\u0b9a\u0bbe\u0bb5"),
        _u(r"\u0b95\u0b9e\u0bcd\u0b9a\u0bbe\u0bb5\u0bc8"),
    ],
    "cocaine": [
        "cocaine", "cocain", "cocane", "crack cocaine", "crack", "coke",
        _u(r"\u0b95\u0bcb\u0b95\u0bc8\u0ba9\u0bcd"),
    ],
    "heroin": [
        "heroin", "brown sugar", "smack",
        _u(r"\u0bb9\u0bc6\u0bb0\u0bbe\u0baf\u0bbf\u0ba9\u0bcd"),
        _u(r"\u0baa\u0bbf\u0bb0\u0bb5\u0bc1\u0ba9\u0bcd \u0b9a\u0bc1\u0b95\u0bb0\u0bcd"),
    ],
    "opium": ["opium", _u(r"\u0b85\u0baa\u0bbf\u0ba9\u0bcd")],
    "morphine": ["morphine"],
    "fentanyl": ["fentanyl", "fentanil"],
    "codeine": ["codeine", "codeine abuse"],
    "oxycodone": ["oxycodone", "oxycodone abuse", "oxy"],
    "tramadol": ["tramadol", "tramadol abuse"],
    "lsd": ["lsd", "acid", _u(r"\u0b8e\u0bb2\u0bcd\u0b8e\u0bb8\u0bcd\u0b9f\u0bbf")],
    "mdma": ["mdma", "ecstasy", "extasy", "molly"],
    "ketamine": ["ketamine", "ketamin", "keta"],
    "meth": ["meth", "methamphetamine", "methamfetamine", "crystal meth", "ice", _u(r"\u0bae\u0bc6\u0ba4\u0bcd")],
    "amphetamine": ["amphetamine", "amphetamin"],
    "magic_mushrooms": ["magic mushrooms", "mushrooms", "psilocybin", "psilocin"],
    "pcp": ["pcp"],
    "dmt": ["dmt"],
    "inhalants": [
        "whitener", "whitener", "glue", "thinner", "petrol sniffing", "correction fluid",
        "aerosol spray", "aerosol sprays", "solution sniffing",
    ],
    "cigarettes": ["cigarette", "cigarettes", "cigar", "cigars", "cig"],
    "beedi": ["beedi", "bidi", _u(r"\u0baa\u0bc0\u0b9f\u0bbf")],
    "vape": ["vape", "vaping", "e-cigarette", "e cigarette", "ecigarette"],
    "hookah": ["hookah", "hooka", "shisha", "hookah pipe"],
    "gutka": ["gutka", "gutkha", "pan parag", "pan masala", "hans", "snuff", "nicotine pouch", "chewing tobacco"],
    "cool_lip": ["coolip", "cool lip", "cool lips", "coollip"],
    "liquor": [
        "liquor", "alcohol", "beer", "whisky", "whiskey", "brandy", "rum", "vodka",
        "wine", "arrack", "illegal liquor", "illicit liquor", "country liquor",
        "tasmac", "tasmac bottle", "tasmac bottles", "liquor shop",
        _u(r"\u0b9a\u0bbe\u0bb0\u0bbe\u0baf\u0bae\u0bcd"),
        _u(r"\u0b95\u0bb3\u0bcd\u0bb3\u0b9a\u0bcd\u0b9a\u0bbe\u0bb0\u0bbe\u0baf\u0bae\u0bcd"),
        _u(r"\u0bae\u0ba4\u0bc1"),
    ],
    "sleeping_pills": ["sleeping pills", "sleeping pill", "sedatives", "sedative", "diazepam", "alprazolam", "nitrazepam"],
    "cough_syrup": ["cough syrup", "cough syrup abuse"],
    "painkillers": ["painkiller", "painkillers", "painkiller abuse"],
    "steroids": ["steroid", "steroids", "steroid misuse"],
    "rolling_paper": ["rolling paper", "rolling papers"],
    "bong": ["bong"],
    "pipe": ["pipe"],
    "syringe": ["syringe", "needle", "injection needle"],
    "grinder": ["grinder"],
    "lighter": ["lighter"],
    "foil_paper": ["foil paper", "foil"],
    "capsules": ["capsule", "capsules"],
    "powder_packets": ["powder packet", "powder packets", "white powder"],
    "drug_packaging": [
        "small packets", "small packet", "zip lock", "zip lock cover", "zip lock covers",
        "sachets", "sachet", "drug pouch", "drug pouches", "plastic covers",
        "brown packets", "brown packet",
    ],
    "drug_production_material": ["chemical bottles", "chemical bottle", "mixing powder", "injection vials", "injection vial"],
    # "synthetic_drug": [
    #     "synthetic drug", "party drug", "drug tablet", "drug tablets", "tablets",
    #     "pills", "tabs", "trip", "high material", "crystal",
    #     _u(r"\u0baa\u0bcb\u0ba4\u0bc8 \u0bae\u0bbe\u0ba4\u0bcd\u0ba4\u0bbf\u0bb0\u0bc8"),
    #     _u(r"\u0bae\u0bbe\u0ba4\u0bcd\u0ba4\u0bbf\u0bb0\u0bc8"),
    # ],
    # "suspected_drug": [
    #     "drug", "drugs", "narcotic", "narcotics", "stuff", "powder", "item", "dope",
    #     _u(r"\u0baa\u0bcb\u0ba4\u0bc8"),
    #     _u(r"\u0baa\u0bcb\u0ba4\u0bc8\u0baa\u0bcd \u0baa\u0bca\u0bb0\u0bc1\u0b9f\u0bcd\u0b95\u0bb3\u0bcd"),
    # ],
}

DRUG_CLASSES = {
    drug: aliases[:8]
    for drug, aliases in DRUG_KEYWORDS.items()
}

GENERIC_DRUG_LABELS = {
    # "suspected_drug", "synthetic_drug", "drug_packaging", "drug_production_material",
    "rolling_paper", "bong", "pipe", "syringe", "grinder", "lighter", "foil_paper",
    "capsules", "powder_packets",
}

DRUG_CONTEXT_TERMS = sorted(
    {term for aliases in DRUG_KEYWORDS.values() for term in aliases},
    key=len,
    reverse=True,
)

_drug_embeddings = None

@spaces.GPU
def get_drug_embeddings():
    global _drug_embeddings
    if _drug_embeddings is None:
        model = get_model()
        _drug_embeddings = {
            k: model.encode(v, normalize_embeddings=True)
            for k, v in DRUG_CLASSES.items()
        }
    return _drug_embeddings



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


def _words(text: str):
    return re.findall(r"[a-z0-9]+|[\u0b80-\u0bff]+", text.lower())


def _candidate_phrases(text: str, max_words: int = 4):
    words = _words(text)
    candidates = set(words)
    for size in range(2, max_words + 1):
        for index in range(0, max(0, len(words) - size + 1)):
            candidates.add(" ".join(words[index:index + size]))
    return candidates


def _fuzzy_alias_match(text: str, include_generic: bool = False):
    candidates = _candidate_phrases(text)
    best_label = "unknown"
    best_score = 0

    for label, aliases in DRUG_KEYWORDS.items():
        if include_generic != (label in GENERIC_DRUG_LABELS):
            continue
        for alias in aliases:
            alias_lower = alias.lower().strip()
            if len(alias_lower) < 4:
                continue
            if label in GENERIC_DRUG_LABELS and len(alias_lower) < 6:
                continue

            alias_words = len(_words(alias_lower))
            possible = [c for c in candidates if abs(len(_words(c)) - alias_words) <= 1]
            if not possible:
                possible = candidates

            for candidate in possible:
                if abs(len(candidate) - len(alias_lower)) > max(3, len(alias_lower) // 2):
                    continue
                score = max(
                    fuzz.ratio(alias_lower, candidate),
                    fuzz.partial_ratio(alias_lower, candidate),
                )
                threshold = 88 if len(alias_lower) <= 6 else 82
                if score >= threshold and score > best_score:
                    best_label = label
                    best_score = score

    return best_label, best_score / 100


def has_drug_context(text: str) -> bool:
    text_lower = (text or "").lower()
    return any(_contains_term(text_lower, term) for term in DRUG_CONTEXT_TERMS)


@spaces.GPU
def detect_drug(text: str):
    text = text or ""
    text_lower = text.lower()

    MEDICAL_CONTEXT = [
        "doctor",
        "hospital",
        "prescribed",
        "medicine",
        "treatment",
        "therapy",
    ]

    if any(word in text_lower for word in MEDICAL_CONTEXT):
        return {
            "label": "unknown",
            "confidence": 0.0
        }

    for drug, keywords in DRUG_KEYWORDS.items():
        if drug in GENERIC_DRUG_LABELS:
            continue
        if any(_contains_term(text_lower, keyword) for keyword in keywords):
            return {
                "label": drug,
                "confidence": 1.0
            }

    fuzzy_label, fuzzy_score = _fuzzy_alias_match(text_lower)
    if fuzzy_label != "unknown":
        return {
            "label": fuzzy_label,
            "confidence": round(fuzzy_score, 3)
        }

    for drug, keywords in DRUG_KEYWORDS.items():
        if drug not in GENERIC_DRUG_LABELS:
            continue
        if any(_contains_term(text_lower, keyword) for keyword in keywords):
            return {
                "label": drug,
                "confidence": 1.0
            }

    fuzzy_label, fuzzy_score = _fuzzy_alias_match(text_lower, include_generic=True)
    if fuzzy_label != "unknown":
        return {
            "label": fuzzy_label,
            "confidence": round(fuzzy_score, 3)
        }

    model = get_model()
    drug_embeddings = get_drug_embeddings()
    text_emb = model.encode(text, normalize_embeddings=True)

    best_match = "unknown"
    best_score = 0

    for drug, emb in drug_embeddings.items():
        score = util.cos_sim(text_emb, emb).max().item()
        if score > best_score:
            best_score = score
            best_match = drug

    if best_score < 0.68 or not has_drug_context(text):
        best_match = "unknown"

    return {
        "label": best_match,
        "confidence": round(best_score, 3)
    }

