import sys
from types import ModuleType

# Mock 'spaces' locally before import to avoid errors outside of Hugging Face
try:
    import spaces
except ImportError:
    mock_spaces = ModuleType("spaces")
    mock_spaces.GPU = lambda fn=None: (fn if fn else lambda f: f)
    sys.modules["spaces"] = mock_spaces
    import spaces

from transformers import pipeline
import os


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
