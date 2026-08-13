from transformers import pipeline
import os

# Safe spaces import for local vs Hugging Face environments
try:
    import spaces
except ImportError:
    class MockSpaces:
        def GPU(self, fn=None):
            if fn: return fn
            return lambda f: f
    spaces = MockSpaces()

# Global cache to avoid reloading the model on every call
_ner_pipeline = None

@spaces.GPU
def extract_entities(text: str):
    global _ner_pipeline
    if _ner_pipeline is None:
        _ner_pipeline = pipeline(
            "ner",
            model="dslim/bert-base-NER",
            aggregation_strategy="simple",
            device=0 if os.getenv("SPACES_ZERO_GPU") else -1 # Use GPU if on Hugging Face ZeroGPU
        )

    entities = _ner_pipeline(text)

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
