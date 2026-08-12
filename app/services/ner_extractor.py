from transformers import pipeline

# Load NER model
ner_pipeline = pipeline(
    "ner",
    model="dslim/bert-base-NER",
    aggregation_strategy="simple"
)

def extract_entities(text: str):
    entities = ner_pipeline(text)

    result = {
        "persons": [],
        "locations": [],
        "organizations": []
    }

    def clean_entity(value):
        value = str(value or "").replace("##", "").strip()
        return value if len(value) >= 3 else ""

    for ent in entities:
        label = ent["entity_group"]
        value = clean_entity(ent["word"])
        if not value:
            continue

        if label == "PER":
            result["persons"].append(value)
        elif label == "LOC":
            result["locations"].append(value)
        elif label == "ORG":
            result["organizations"].append(value)

    return result
