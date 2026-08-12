# import re

# MEDICAL_TERMS = [
#     "doctor",
#     "prescribed",
#     "prescription",
#     "medicine",
#     "tablet for",
#     "treatment",
#     "hospital",
#     "mental",
#     "depression",
#     "anxiety",
#     "therapy",
# ]

# NON_COMPLAINT_PATTERNS = [
#     "i am addicted to",
#     "naan use pannuren",
#     "i use",
#     "for my health",
#     "for treatment",
#     "doctor gave",
#     "doctor prescribed",
#     "cricket drug",
# ]

# COMPLAINT_TERMS = [
#     "selling",
#     "dealer",
#     "near school",
#     "near college",
#     "public disturbance",
#     "smoking",
#     "using drugs",
#     "drug sale",
#     "supply",
#     "gang",
#     "illegal",
#     "please take action",
#     "kindly investigate",
# ]

# def has_real_complaint_intent(text: str) -> bool:

#     text = (text or "").lower().strip()

#     # ❌ medical/personal usage
#     for term in MEDICAL_TERMS:
#         if term in text:
#             return False

#     # ❌ casual/self statements
#     for pattern in NON_COMPLAINT_PATTERNS:
#         if pattern in text:
#             return False

#     # ✅ actual complaint indicators
#     for term in COMPLAINT_TERMS:
#         if term in text:
#             return True

#     # ❌ first-person self statements
#     if re.search(r"\b(i am|i use|my drug|for me|naan|enaku)\b", text):
#         return False

#     return False

