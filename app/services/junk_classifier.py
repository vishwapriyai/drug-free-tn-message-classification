from string import punctuation
import os
from transformers import pipeline

# Safe spaces import for local vs Hugging Face environments
try:
    import spaces
except ImportError:
    class MockSpaces:
        def GPU(self, fn=None):
            if fn: return fn
            return lambda f: f
    spaces = MockSpaces()

_classifier = None

def get_classifier():
    global _classifier
    if _classifier is None:
        _classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli",
            device=0 if os.getenv("SPACES_ZERO_GPU") else -1
        )
    return _classifier



# classifier = pipeline(
#     "zero-shot-classification",
#     model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli"
# )
labels = [
        # Valid complaints
        "real drug-related public complaint or self complaint that asks for action or reports an incident",
        "real public drug complaint",
        "drug trafficking complaint",
        "public drug usage complaint",
        "drug production complaint",
        "drug sale complaint",
        "drug storage complaint",
        "drug transportation complaint",
        "drug usage complaint",

        # Non-complaints / junk / irrelevant
        "medical discussion about prescribed medicine",
        "joke or fake statement",
        "self personal statement that does not related to any drug complaint",
        "spam or testing message",
    ]


JUNK_PHRASES = [
    "hello testing", "testing only", "test complaint", "just checking",
    "checking app", "app super", "no issue", "asdfghjkl",
    "selling something maybe not sure", "maybe not sure",
    _u(r"\u0bb9\u0bbe\u0baf\u0bcd"),
    _u(r"\u0b8e\u0ba4\u0bc1\u0bb5\u0bc1\u0bae\u0bcd \u0b87\u0bb2\u0bcd\u0bb2\u0bc8"),
    _u(r"\u0b87\u0ba4\u0bc1 \u0bb5\u0bc7\u0bb2\u0bc8 \u0b9a\u0bc6\u0baf\u0bcd\u0b95\u0bbf\u0bb1\u0ba4\u0bbe"),
]

GENERIC_ONLY_TERMS = {
    "drug", "drugs", "narcotic", "narcotics", "ganja", "weed", "liquor",
    "alcohol", "tablet", "tablets", "powder", "stuff", "item",
    _u(r"\u0baa\u0bcb\u0ba4\u0bc8"),
    _u(r"\u0b95\u0b9e\u0bcd\u0b9a\u0bbe"),
}


def _normalized_words(text: str):
    cleaned = text.lower().translate(str.maketrans({ch: " " for ch in punctuation}))
    return [word for word in cleaned.split() if word]


def _looks_like_noise(text: str) -> bool:
    compact = "".join(text.split())
    if not compact:
        return True
    if compact.isdigit():
        return True
    if len(compact) <= 2:
        return True
    alnum_count = sum(ch.isalnum() for ch in compact)
    if alnum_count == 0:
        return True
    return False


def _is_generic_only(text: str) -> bool:
    words = _normalized_words(text)
    if not words or len(words) > 3:
        return False
    return all(word in GENERIC_ONLY_TERMS for word in words)


def _u(value: str) -> str:
    return value.encode("utf-8").decode("unicode_escape")

@spaces.GPU
def is_junk(text: str, drug_label: str = "unknown", crime_label: str = "unknown") -> bool:
    text_lower = (text or "").lower().strip()

    if _looks_like_noise(text_lower):
        return True

    if any(phrase in text_lower for phrase in JUNK_PHRASES):
        return True

    if _is_generic_only(text_lower):
        return True

    has_drug_signal = bool(drug_label and drug_label != "unknown")
    has_crime_signal = bool(crime_label and crime_label != "unknown")

    if has_drug_signal and has_crime_signal:
        return False

    # labels = [
    #     "real drug-related public complaint that asks for action or reports an incident",
    #     "irrelevant, test, vague, or non-complaint message"
    # ]

    
    classifier_instance = get_classifier()

    result = classifier_instance(
        text,
        labels,
        multi_label=True
    )

    scores = dict(zip(result["labels"], result["scores"]))

    # -----------------------------
    # VALID COMPLAINT LABELS
    # -----------------------------
    complaint_labels = [
        "real public drug complaint",
        "drug trafficking complaint",
        "public drug usage complaint",
        "drug production complaint",
        "drug sale complaint",
        "drug storage complaint",
        "drug transportation complaint",
        "drug usage complaint",
    ]

    # -----------------------------
    # JUNK LABELS
    # -----------------------------
    junk_labels = [
        "medical discussion about prescribed medicine",
        "joke or fake statement",
        "self personal statement that does not related to any drug complaint",
        "spam or testing message",
    ]

    complaint_score = max(
        [scores.get(label, 0) for label in complaint_labels]
    )

    junk_score = max(
        [scores.get(label, 0) for label in junk_labels]
    )

    # ------------------------------------------------
    # CONTEXT UNDERSTANDING BOOST
    # ------------------------------------------------

    text_lower = text.lower()

    public_place_keywords = [
        "school",
        "college",
        "campus",
        "public",
        "bus stand",
        "railway station",
        "park",
        "street",
        "area",
        "near school",
    ]

    crime_keywords = [
        "drug",
        "drugs",
        "ganja",
        "weed",
        "selling",
        "using",
        "smoking",
        "dealer",
        "supply",
        "trafficking",
    ]

    medical_keywords = [
        "doctor",
        "prescribed",
        "hospital",
        "treatment",
        "medicine",
        "mental health",
    ]

    has_public_context = any(
        word in text_lower for word in public_place_keywords
    )

    has_crime_context = any(
        word in text_lower for word in crime_keywords
    )

    has_medical_context = any(
        word in text_lower for word in medical_keywords
    )

    # 🔥 IMPORTANT
    # Public + crime = likely real complaint
    if has_public_context and has_crime_context:
        complaint_score += 0.25

    # ------------------------------------------------
    # STRONG PUBLIC SAFETY BOOST
    # ------------------------------------------------

    danger_locations = [
        "school",
        "college",
        "campus",
        "children",
        "students",
    ]

    if any(word in text_lower for word in danger_locations):
        complaint_score += 0.40

    # Medical context = likely junk
    if has_medical_context:
        junk_score += 0.25

    print("\\n--------------------------")
    print("TEXT:", text)
    print("TOP LABEL:", max(scores, key=scores.get))
    print("COMPLAINT SCORE:", complaint_score)
    print("JUNK SCORE:", junk_score)
    print("ALL SCORES:", scores)
    print("--------------------------\\n")

    # FINAL DECISION
    return junk_score > complaint_score
    # result = classifier(text, labels)
    # scores = dict(zip(result["labels"], result["scores"]))

    # complaint_score = scores.get(
    #     "real drug-related public complaint that asks for action or reports an incident", 0
    # )
    # junk_score = scores.get("irrelevant, test, vague, or non-complaint message", 0)

    # print("DEBUG -> complaint:", complaint_score, "junk:", junk_score)

    # if junk_score >= complaint_score:
    #     return True

    # if complaint_score < 0.72:
    #     return True

    # return False
@spaces.GPU
def classify_complaint(text: str):

    classifier_instance = get_classifier()
    result = classifier_instance(
        text,
        labels,
        multi_label=True
    )

    scores = dict(zip(result["labels"], result["scores"]))

    # -----------------------------
    # VALID COMPLAINT CATEGORIES
    # -----------------------------
    complaint_labels = [
        "real public drug complaint",
        "drug trafficking complaint",
        "public drug usage complaint",
        "drug production complaint",
        "drug sale complaint",
        "drug storage complaint",
        "drug transportation complaint",
        "drug usage complaint",
    ]

    # -----------------------------
    # JUNK / NON-COMPLAINT
    # -----------------------------
    junk_labels = [
        "medical discussion about prescribed medicine",
        "joke or fake statement",
        "spam or testing message",
    ]

    complaint_score = max(
        [scores.get(label, 0) for label in complaint_labels]
    )

    junk_score = max(
        [scores.get(label, 0) for label in junk_labels]
    )

    # ------------------------------------------------
    # EXTRA SAFETY CHECKS
    # ------------------------------------------------
    text_lower = text.lower()

    strong_complaint_keywords = [
        "selling drugs",
        "drug sale",
        "drug selling",
        "ganja sale",
        "selling ganja",
        "drug transport",
        "transporting drugs",
        "drug storage",
        "stored drugs",
        "drug manufacturing",
        "drug production",
        "using drugs publicly",
        "public drug use",
        "drug trafficking",
        "smuggling",
        "dealer",
        "peddler",
        "lsd",
        "cocaine",
        "heroin",
        "mdma",
        "ganja",
        "weed packets",
        "narcotics"
    ]

    medical_context_keywords = [
        "doctor prescribed",
        "prescribed by doctor",
        "medical shop",
        "hospital",
        "medicine",
        "tablet",
        "prescription",
        "treatment",
        "mental health medicine",
        "painkiller"
    ]

    # If strong illegal-drug complaint indicators exist,
    # force it toward complaint category
    keyword_hit = any(k in text_lower for k in strong_complaint_keywords)

    # If clearly medical context, avoid false complaint
    medical_hit = any(k in text_lower for k in medical_context_keywords)

    if keyword_hit and not medical_hit:
        complaint_score += 0.15

    # Final decision
    is_junk = junk_score > complaint_score

    return {
        "is_junk": is_junk,
        "predicted_type": max(scores, key=scores.get),
        "complaint_score": round(complaint_score, 3),
        "junk_score": round(junk_score, 3),
        "scores": scores
    }