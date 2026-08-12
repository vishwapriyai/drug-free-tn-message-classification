# """
# app/services/tamil_preprocessor.py
# ====================================
# Translates Tamil (and Tanglish) drug-complaint vocabulary into English
# so that the English-only NLI model (bart-large-mnli) can understand it.

# Also provides:
#   - is_tamil_text()        → detect if input is primarily Tamil script
#   - instant_complaint_win()→ fast-path: returns True if translated text
#                              has clear drug + crime signal (skips NLI)
#   - instant_junk_win()     → fast-path: returns True for obvious medical/
#                              metaphor/spam patterns

# Design principle:
#   We do NOT need a perfect translator.
#   We only need to convert the ~50 most common Tamil words used in drug
#   complaints into their English equivalents so the NLI model can score
#   them correctly.
#   Unknown Tamil words are left as-is (the similarity model handles them).
# """

# from __future__ import annotations
# import re

# # ─────────────────────────────────────────────────────────────────────────────
# # Core Tamil → English word map
# # Covers colloquial spellings, slang, and common variants
# # ─────────────────────────────────────────────────────────────────────────────

# TAMIL_TO_EN: dict[str, str] = {

#     # ── Drugs & substances ────────────────────────────────────────────────────
#     "கஞ்சா":             "ganja",
#     "போதை":              "drug",
#     "போதைப்பொருள்":      "drugs",
#     "போதைப்":            "drugs",
#     "போதைப்பொருட்கள்":   "drugs",
#     "நார்கோட்டிக்ஸ்":   "narcotics",
#     "ஹெராயின்":          "heroin",
#     "கோகெய்ன்":          "cocaine",
#     "எல்எஸ்டி":          "lsd",
#     "சாராயம்":           "liquor",
#     "மதுபானம்":          "alcohol",
#     "குடி":              "drinking alcohol",
#     "புகையிலை":          "tobacco",
#     "வீட்":              "weed",
#     "ப்ரவுன் சுகர்":     "brown sugar",
#     "கெமிக்கல்":         "chemical drug",
#     "டேப்லெட்":          "tablet",
#     "மாத்திரை":          "tablet",       # could be medical — context decides

#     # ── Crime actions (selling / using / trafficking) ─────────────────────────
#     "விக்கிரங்கா":       "selling",      # colloquial present tense
#     "விக்கிறாங்க":       "selling",
#     "விற்கிறாங்க":       "selling",
#     "விற்கின்றனர்":      "selling",
#     "விக்குறாங்க":       "selling",
#     "விற்பனை":           "sale",
#     "விற்கிறார்கள்":     "selling",
#     "வித்துறாங்க":       "selling",
#     "வாங்குறாங்க":       "buying",
#     "வாங்கிறாங்க":       "buying",
#     "வாங்கிக்குறாங்க":   "buying",
#     "கடத்துறாங்க":       "trafficking",
#     "கடத்துகிறார்கள்":   "trafficking",
#     "கடத்துகின்றனர்":    "trafficking",
#     "கடத்துறான்":        "trafficking",
#     "கடத்துறாள்":        "trafficking",
#     "வச்சிருக்காங்க":    "storing drugs",
#     "வைத்திருக்கிறார்கள்": "storing drugs",
#     "சேமிக்கிறாங்க":    "storing drugs",
#     "புகைக்குறாங்க":     "smoking",
#     "புகைக்கிறார்கள்":   "smoking",
#     "புகைக்கின்றனர்":    "smoking",
#     "புகைக்குறான்":      "smoking",
#     "சாப்பிடுறாங்க":     "consuming",
#     "சாப்பிடுகிறார்கள்": "consuming",
#     "உபயோகிக்கிறார்கள்": "using",
#     "உபயோகிக்கின்றனர்":  "using",
#     "உபயோகிக்குறாங்க":   "using",
#     "பயன்படுத்துகிறார்கள்": "using",
#     "தயாரிக்கிறார்கள்":  "manufacturing",
#     "தயாரிக்குறாங்க":    "manufacturing",
#     "சப்ளை":             "supply",
#     "டீல்":              "deal",
#     "டீலர்":             "dealer",
#     "நடக்குது":          "happening",
#     "நடக்கிறது":         "happening",
#     "நடக்குதுன்னு":      "happening reportedly",

#     # ── Places ────────────────────────────────────────────────────────────────
#     "ஸ்கூல்":            "school",
#     "பள்ளி":             "school",
#     "கல்லூரி":           "college",
#     "கேம்பஸ்":           "campus",
#     "பல்கலைக்கழகம்":    "university",
#     "பஸ்":               "bus",
#     "ஸ்டாண்ட்":          "stand",
#     "பேருந்து":          "bus",
#     "நிலையம்":           "station",
#     "ரயில்":             "railway",
#     "ரெயில்":            "railway",
#     "ரயில்வே":           "railway",
#     "பார்க்":            "park",
#     "பூங்கா":            "park",
#     "தெரு":              "street",
#     "சாலை":              "road",
#     "பகுதி":             "area",
#     "இடம்":              "place",
#     "அருகில்":           "near",
#     "பக்கத்தில்":        "near",
#     "பக்கத்துல":         "near",
#     "பக்கம்":            "near",
#     "அடுத்து":           "next to",
#     "கிட்ட":             "near",
#     "கிட்டே":            "near",
#     "இங்க":              "here",
#     "இங்கே":             "here",
#     "இந்த":              "this",
#     "அந்த":              "that",
#     "வீட்டில்":          "at home",
#     "வீட்டுல":           "at home",
#     "கடையில்":           "in shop",
#     "கடையில":            "in shop",

#     # ── People ────────────────────────────────────────────────────────────────
#     "மாணவர்கள்":         "students",
#     "மாணவர்":            "student",
#     "இளைஞர்கள்":         "youth",
#     "பையன்கள்":          "boys",
#     "ஆட்கள்":            "people",
#     "ஒருத்தன்":          "a person",
#     "நபர்":              "person",
#     "நபர்கள்":           "persons",
#     "கும்பல்":           "gang",

#     # ── Complaint / action words ──────────────────────────────────────────────
#     "புகார்":            "complaint",
#     "நடவடிக்கை":         "action",
#     "போலீஸ்":            "police",
#     "போலீசார்":          "police",
#     "அதிகாரி":           "officer",
#     "கைது":              "arrest",
#     "தகவல்":             "information",
#     "தெரிவிக்கிறேன்":    "reporting",
#     "தெரியப்படுத்துகிறேன்": "reporting",
#     "செய்யுங்கள்":       "please take action",
#     "நிறுத்துங்கள்":     "please stop",
#     "கவனிங்க":           "please notice",
# }

# # ─────────────────────────────────────────────────────────────────────────────
# # Instant-win sets (applied on the TRANSLATED text, not the raw Tamil)
# # ─────────────────────────────────────────────────────────────────────────────

# _DRUG_WORDS = frozenset({
#     "ganja", "drug", "drugs", "narcotics", "heroin", "cocaine", "lsd",
#     "liquor", "alcohol", "weed", "substance", "brown", "sugar",
# })
# _CRIME_WORDS = frozenset({
#     "selling", "sale", "trafficking", "smoking", "using", "buying",
#     "storing", "manufacturing", "dealer", "supply", "deal", "happening",
# })
# _MEDICAL_WORDS = frozenset({
#     "doctor", "prescribed", "prescription", "hospital", "clinic",
#     "treatment", "therapy", "surgery", "painkiller",
# })
# _METAPHOR_PHRASES = (
#     "cricket is", "love is", "music is", "football is", "movie is",
#     "like a drug to me", "feels like a drug", "addicted to cricket",
#     "addicted to music",
# )


# # ─────────────────────────────────────────────────────────────────────────────
# # Public API
# # ─────────────────────────────────────────────────────────────────────────────

# def is_tamil_text(text: str) -> bool:
#     """Returns True if >30% of alphabetic chars are Tamil Unicode."""
#     tamil = sum(1 for c in text if "\u0b80" <= c <= "\u0bff")
#     alpha = sum(1 for c in text if c.isalpha())
#     return alpha > 0 and (tamil / alpha) > 0.30


# def translate_for_nli(text: str) -> str:
#     """
#     Word-by-word Tamil → English translation for NLI consumption.
#     Unknown Tamil words are kept as-is (similarity model handles them).
#     Non-Tamil text is returned unchanged.
#     """
#     if not is_tamil_text(text):
#         return text
#     words = text.split()
#     return " ".join(TAMIL_TO_EN.get(w, w) for w in words)


# def instant_complaint_win(translated: str) -> bool:
#     """
#     Returns True when translated text has clear drug + crime signal.
#     Bypasses the heavy NLI call — used as a fast-path for obvious complaints.

#     Requires BOTH a drug word AND a crime action word to prevent
#     "drug awareness campaign" from triggering.
#     """
#     words = set(translated.lower().split())
#     return bool(words & _DRUG_WORDS) and bool(words & _CRIME_WORDS)


# def instant_junk_win(original: str, translated: str) -> bool:
#     """
#     Returns True for obvious junk patterns that should skip NLI.
#     Only fires on very clear-cut cases.
#     """
#     t = original.lower()
#     # Metaphorical drug references
#     if any(p in t for p in _METAPHOR_PHRASES):
#         return True
#     # Pure medical context with NO crime words in translation
#     trans_words = set(translated.lower().split())
#     has_medical = bool(trans_words & _MEDICAL_WORDS)
#     has_crime   = bool(trans_words & _CRIME_WORDS)
#     if has_medical and not has_crime:
#         return True
#     return False