# # from app.services.junk_classifier import is_junk
# # from app.services.drug_classifier import detect_drug
# # from app.services.crime_classifier import detect_crime
# # from app.services.location_extractor import extract_location
# # from app.database.crud import insert_complaint
# # from app.services.ner_extractor import extract_entities

# # def process_complaint(complaint: str, address: str):

# #     junk = is_junk(complaint)

# #     # 🔴 HANDLE JUNK
# #     if junk:
# #         result = {
# #             "complaint_text": complaint,
# #             "is_junk": True,
# #             "drug_type": None,
# #             "crime_type": None,
# #             "address": address,
# #             "city": None,
# #             "location_detail": None
# #         }

# #         insert_complaint(result)

# #         return {
# #             "is_junk": True,
# #             "message": "Irrelevant complaint"
# #         }

# #     # 🧠 AI EXTRACTION
# #     drug = detect_drug(complaint)
# #     crime = detect_crime(complaint)
# #     location_data = extract_location(complaint, address)

# #     # fallback logic
# #     if drug == "unknown" and "drug" in complaint.lower():
# #         drug = "suspected_drug"

# #     if crime == "unknown":
# #         crime = "suspicious_activity"

# #     result = {
# #         "complaint_text": complaint,
# #         "is_junk": False,
# #         "drug_type": drug,
# #         "crime_type": crime,
# #         "address": location_data["address"],
# #         "city": location_data["city"],
# #         "location_detail": location_data["location_detail"]
# #     }

# #     insert_complaint(result)

# #     return result

from app.services.junk_classifier import is_junk

from app.services.drug_classifier import detect_drug
from app.services.crime_classifier import detect_crime
from app.services.location_extractor import extract_location, normalize_unknown
from app.services.ner_extractor import extract_entities
from app.database.crud import insert_complaint


# def process_complaint(complaint: str, address: str):
#     address = normalize_unknown(address)
#     # ✅ HUMAN-LIKE COMPLAINT CHECK
#     if not has_real_complaint_intent(complaint):

#         result = {
#             "complaint_text": complaint,
#             "is_junk": True,
#             "junk_confidence": 0.95,

#             "drug_type": None,
#             "drug_confidence": 0.0,

#             "crime_type": None,
#             "crime_confidence": 0.0,

#             "address": address,
#             "city": "unknown",
#             "location_detail": "unknown",

#             "entities": {
#                 "persons": [],
#                 "locations": [],
#                 "organizations": []
#             }
#         }

#         insert_complaint(result)
#         return result

#     drug = detect_drug(complaint)
#     crime = detect_crime(complaint, has_detected_drug=drug["label"] != "unknown")
#     junk = is_junk(complaint, drug_label=drug["label"], crime_label=crime["label"])

#     # 🚨 HARD STOP
#     if junk:
#         result = {
#             "complaint_text": complaint,
#             "is_junk": True,
#             "junk_confidence": 1.0,

#             "drug_type": None,
#             "drug_confidence": 0.0,

#             "crime_type": None,
#             "crime_confidence": 0.0,

#             "address": address,
#             "city": "unknown",
#             "location_detail": "unknown",

#             "entities": {
#                 "persons": [],
#                 "locations": [],
#                 "organizations": []
#             }
#         }

#         insert_complaint(result)
#         return result

#     # ✅ AI classification
#     location = extract_location(complaint, address)
#     entities = extract_entities(complaint)

#     result = {
#         "complaint_text": complaint,

#         "is_junk": False,
#         "junk_confidence": 0.0,

#         "drug_type": drug["label"],
#         "drug_confidence": drug["confidence"],

#         "crime_type": crime["label"],
#         "crime_confidence": crime["confidence"],

#         "address": location["address"],
#         "city": location["city"],
#         "location_detail": location["location_detail"],

#         "entities": entities
#     }

#     insert_complaint(result)
#     return result
from app.services.text_normalizer import normalize_text
from app.services.junk_classifier import is_junk

def process_complaint(complaint: str, address: str):

    complaint = normalize_text(complaint)

    junk = is_junk(complaint)

    if junk:

        result = {
            "complaint_text": complaint,
            "is_junk": True,
            "junk_confidence": 0.95,

            "drug_type": None,
            "drug_confidence": 0.0,

            "crime_type": None,
            "crime_confidence": 0.0,

            "address": address,
            "city": "unknown",
            "location_detail": "unknown",

            "entities": {
                "persons": [],
                "locations": [],
                "organizations": []
            }
        }

        insert_complaint(result)
        return result

    # NON-JUNK FLOW
    drug = detect_drug(complaint)

    crime = detect_crime(
        complaint,
        has_detected_drug=drug["label"] != "unknown"
    )

    location = extract_location(complaint, address)

    entities = extract_entities(complaint)

    result = {
        "complaint_text": complaint,

        "is_junk": False,
        "junk_confidence": 0.05,

        "drug_type": drug["label"],
        "drug_confidence": drug["confidence"],

        "crime_type": crime["label"],
        "crime_confidence": crime["confidence"],

        "address": location["address"],
        "city": location["city"],
        "location_detail": location["location_detail"],

        "entities": entities
    }

    insert_complaint(result)

    return result

# from app.services.junk_classifier import is_junk
# from app.services.drug_classifier import detect_drug
# from app.services.crime_classifier import detect_crime
# from app.services.location_extractor import (
#     extract_location,
#     normalize_unknown
# )
# from app.services.ner_extractor import extract_entities
# from app.database.crud import insert_complaint


# def process_complaint(complaint: str, address: str):

#     address = normalize_unknown(address)

#     # ---------------------------------------------------
#     # SEMANTIC JUNK DETECTION
#     # ---------------------------------------------------

#     junk = is_junk(complaint)

#     if junk:

#         result = {
#             "complaint_text": complaint,

#             "is_junk": True,
#             "junk_confidence": 1.0,

#             "drug_type": None,
#             "drug_confidence": 0.0,

#             "crime_type": None,
#             "crime_confidence": 0.0,

#             "address": address,
#             "city": "unknown",
#             "location_detail": "unknown",

#             "entities": {
#                 "persons": [],
#                 "locations": [],
#                 "organizations": []
#             }
#         }

#         insert_complaint(result)

#         return result

#     # ---------------------------------------------------
#     # DRUG + CRIME DETECTION
#     # ---------------------------------------------------

#     drug = detect_drug(complaint)

#     crime = detect_crime(
#         complaint,
#         has_detected_drug=drug["label"] != "unknown"
#     )

#     # ---------------------------------------------------
#     # LOCATION EXTRACTION
#     # ---------------------------------------------------

#     location = extract_location(
#         complaint,
#         address
#     )

#     entities = extract_entities(complaint)

#     # ---------------------------------------------------
#     # FINAL RESULT
#     # ---------------------------------------------------

#     result = {

#         "complaint_text": complaint,

#         "is_junk": False,
#         "junk_confidence": 0.0,

#         "drug_type": drug["label"],
#         "drug_confidence": drug["confidence"],

#         "crime_type": crime["label"],
#         "crime_confidence": crime["confidence"],

#         "address": location["address"],
#         "city": location["city"],
#         "location_detail": location["location_detail"],

#         "entities": entities
#     }

#     insert_complaint(result)

#     return result
