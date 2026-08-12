import re
from difflib import SequenceMatcher

from app.services.ner_extractor import extract_entities


def _u(value: str) -> str:
    return value.encode("utf-8").decode("unicode_escape")


PLACEHOLDER_VALUES = {"", "string", "unknown", "none", "null", "n/a", "na", "test", "testing", "xyz"}

CITY_MAPPING = {
    "chennai city": "Chennai",
    "chennai railway": "Chennai",
    "chennai": "Chennai",
    "madras": "Chennai",
    "avadi city": "Avadi",
    "avadi": "Avadi",
    "ambattur": "Chennai",
    "tambaram city": "Tambaram",
    "tambaram": "Tambaram",
    "chrompet": "Chennai",
    "pallavaram": "Chennai",
    "velachery": "Chennai",
    "porur": "Chennai",
    "perambur": "Chennai",
    "medavakkam": "Chennai",
    "sholinganallur": "Chennai",
    "trichy city": "Trichy",
    "trichy railway": "Trichy",
    "trichy": "Trichy",
    "coimbatore city": "Coimbatore",
    "coimbatore": "Coimbatore",
    "tiruppur city": "Tiruppur",
    "tiruppur": "Tiruppur",
    "salem city": "Salem",
    "salem": "Salem",
    "madurai city": "Madurai",
    "madurai": "Madurai",
    "tirunelveli city": "Tirunelveli",
    "tirunelveli": "Tirunelveli",
    _u(r"\u0b9a\u0bc6\u0ba9\u0bcd\u0ba9\u0bc8"): "Chennai",
    _u(r"\u0bae\u0bc6\u0b9f\u0bcd\u0bb0\u0bbe\u0bb8\u0bcd"): "Chennai",
    _u(r"\u0b85\u0ba3\u0bcd\u0ba3\u0bbe \u0ba8\u0b95\u0bb0\u0bcd"): "Chennai",
    _u(r"\u0ba4\u0bbe\u0bae\u0bcd\u0baa\u0bb0\u0bae\u0bcd"): "Tambaram",
    _u(r"\u0b85\u0bae\u0bcd\u0baa\u0ba4\u0bcd\u0ba4\u0bc2\u0bb0\u0bcd"): "Chennai",
    _u(r"\u0bb5\u0bc7\u0bb3\u0b9a\u0bcd\u0b9a\u0bc7\u0bb0\u0bbf"): "Chennai",
    _u(r"\u0baa\u0bb2\u0bcd\u0bb2\u0bbe\u0bb5\u0bb0\u0bae\u0bcd"): "Chennai",
    _u(r"\u0b85\u0bb5\u0b9f\u0bbf"): "Avadi",
    _u(r"\u0b85\u0bb5\u0b9f\u0bc0"): "Avadi",
    _u(r"\u0bae\u0bc6\u0b9f\u0bb5\u0bbe\u0b95\u0bcd\u0b95\u0bae\u0bcd"): "Chennai",
    _u(r"\u0baa\u0bcb\u0bb0\u0bc2\u0bb0\u0bcd"): "Chennai",
    _u(r"\u0b9a\u0bcb\u0bb4\u0bbf\u0b99\u0bcd\u0b95\u0ba8\u0bb2\u0bcd\u0bb2\u0bc2\u0bb0\u0bcd"): "Chennai",
    _u(r"\u0baa\u0bc6\u0bb0\u0bae\u0bcd\u0baa\u0bc2\u0bb0\u0bcd"): "Chennai",
}

BASE_CITIES = [
    "ariyalur", "chengalpattu", "chennai", "coimbatore", "cuddalore",
    "dharmapuri", "dindigul", "erode", "kallakurichi", "kancheepuram",
    "kanyakumari", "karur", "krishnagiri", "madurai", "mayiladuthurai",
    "nagapattinam", "namakkal", "perambalur", "pudukottai",
    "ramanathapuram", "ranipet", "salem", "sivagangai", "tenkasi",
    "thanjavur", "the nilgiris", "theni", "thirupathur", "thiruvallur",
    "thiruvarur", "thoothukudi", "tirunelveli", "tiruppur",
    "tiruvannamalai", "trichy", "vellore", "viluppuram", "virudhunagar",
]

LANDMARK_KEYWORDS = {
    "bus stand": ["bus stand", "bus stop", _u(r"\u0baa\u0bb8\u0bcd \u0bb8\u0bcd\u0b9f\u0bbe\u0ba3\u0bcd\u0b9f\u0bcd"), _u(r"\u0baa\u0bc7\u0bb0\u0bc1\u0ba8\u0bcd\u0ba4\u0bc1 \u0ba8\u0bbf\u0bb2\u0bc8\u0baf\u0bae\u0bcd")],
    "railway station": ["railway station", _u(r"\u0bb0\u0baf\u0bbf\u0bb2\u0bcd \u0ba8\u0bbf\u0bb2\u0bc8\u0baf\u0bae\u0bcd")],
    "school": ["school", _u(r"\u0bb8\u0bcd\u0b95\u0bc2\u0bb2\u0bcd"), _u(r"\u0baa\u0bb3\u0bcd\u0bb3\u0bbf")],
    "college": ["college", _u(r"\u0b95\u0bbe\u0bb2\u0bc7\u0b9c\u0bcd"), _u(r"\u0b95\u0bb2\u0bcd\u0bb2\u0bc2\u0bb0\u0bbf")],
    "temple": ["temple", _u(r"\u0b95\u0bcb\u0bb5\u0bbf\u0bb2\u0bcd")],
    "market": ["market", _u(r"\u0bae\u0bbe\u0bb0\u0bcd\u0b95\u0bcd\u0b95\u0bc6\u0b9f\u0bcd"), _u(r"\u0b9a\u0ba8\u0bcd\u0ba4\u0bc8")],
    "park": ["park", _u(r"\u0baa\u0bbe\u0bb0\u0bcd\u0b95\u0bcd"), _u(r"\u0baa\u0bc2\u0b99\u0bcd\u0b95\u0bbe")],
    "hospital": ["hospital", _u(r"\u0bb9\u0bbe\u0bb8\u0bcd\u0baa\u0bbf\u0b9f\u0bb2\u0bcd"), _u(r"\u0bae\u0bb0\u0bc1\u0ba4\u0bcd\u0ba4\u0bc1\u0bb5\u0bae\u0ba9\u0bc8")],
}

NEAR_TOKENS = [
    "near", "nearby", "next to", "beside",
    _u(r"\u0baa\u0b95\u0bcd\u0b95\u0ba4\u0bcd\u0ba4\u0bbf\u0bb2\u0bcd"),
    _u(r"\u0baa\u0b95\u0bcd\u0b95\u0ba4\u0bcd\u0ba4\u0bc1\u0bb2"),
    _u(r"\u0b85\u0bb0\u0bc1\u0b95\u0bc7"),
    _u(r"\u0b85\u0bb0\u0bc1\u0b95\u0bbf\u0bb2\u0bcd"),
    _u(r"\u0b95\u0bbf\u0b9f\u0bcd\u0b9f"),
]


def normalize_unknown(value):
    cleaned = str(value or "").strip()
    if cleaned.lower() in PLACEHOLDER_VALUES:
        return "unknown"
    return cleaned


def _contains(text: str, term: str) -> bool:
    term = term.lower().strip()
    if not term:
        return False
    if re.fullmatch(r"[a-z0-9][a-z0-9 ]*[a-z0-9]", term):
        pattern = r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])"
        return re.search(pattern, text) is not None
    return term in text


def extract_city(address: str, text: str):
    address = normalize_unknown(address)
    haystack = " ".join(v for v in [address, text or ""] if v and v != "unknown").lower()

    for key, value in CITY_MAPPING.items():
        if _contains(haystack, key):
            return value

    for city in BASE_CITIES:
        if _contains(haystack, city):
            return city.title()

    return "unknown"


def _valid_ner_location(value: str) -> bool:
    value = normalize_unknown(value)
    if value == "unknown":
        return False
    if "##" in value:
        return False
    if len(value.strip()) < 3:
        return False
    return True


def _landmark_from_text(text_lower: str):
    for landmark, keywords in LANDMARK_KEYWORDS.items():
        if any(_contains(text_lower, keyword) for keyword in keywords):
            return landmark

    words = re.findall(r"[a-z0-9]+", text_lower)
    for landmark, keywords in LANDMARK_KEYWORDS.items():
        for keyword in keywords:
            if not re.fullmatch(r"[a-z0-9]+", keyword):
                continue
            for word in words:
                if SequenceMatcher(None, keyword, word).ratio() >= 0.84:
                    return landmark

    return "unknown"


def _near_phrase(text_lower: str):
    for token in NEAR_TOKENS:
        if token in text_lower:
            if token in {"near", "nearby", "next to", "beside"}:
                after = text_lower.split(token, 1)[-1].strip(" .,")
                return after or "unknown"
            before = text_lower.split(token, 1)[0].strip(" .,")
            words = before.split()
            return " ".join(words[-3:]) if words else "unknown"
    return "unknown"


def extract_location(text: str, address: str):
    text = text or ""
    address = normalize_unknown(address)
    text_lower = text.lower()

    city = extract_city(address, text)
    location_detail = _landmark_from_text(text_lower)

    if location_detail == "unknown":
        location_detail = _near_phrase(text_lower)

    try:
        ner_data = extract_entities(text)
    except Exception:
        ner_data = {"locations": []}

    if city == "unknown":
        for location in ner_data.get("locations", []):
            if _valid_ner_location(location):
                city = location
                break

    return {
        "city": normalize_unknown(city),
        "address": address,
        "location_detail": normalize_unknown(location_detail)
    }
