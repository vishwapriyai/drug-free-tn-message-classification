# # """
# # app/services/shared_models.py
# # ==============================
# # Single source of truth for heavy ML model instances.
# # Models are loaded ONCE on first call (lazy singleton).
# # Both complaint_intent.py and junk_classifier.py import from here.
# # """

# # from __future__ import annotations
# # from typing import List

# # # _nli_model       = None
# # _embedder_model  = None
# # _valid_emb_cache = None
# # _junk_emb_cache  = None

# # # ─────────────────────────────────────────────────────────────────────────────
# # # Anchor sentences — used by BOTH classifiers for cosine similarity.
# # # Includes English, Tamil, and Tanglish so the multilingual model
# # # can match any input language.
# # # ─────────────────────────────────────────────────────────────────────────────

# # VALID_ANCHORS: List[str] = [
# #     # English
# #     "students smoking ganja behind college canteen",
# #     "drug selling happening near bus stand",
# #     "some boys smoking weed near public park",
# #     "dealer supplying drugs near college gate",
# #     "illegal liquor sale in the area",
# #     "drug trafficking spotted near railway station",
# #     "person storing drugs in the house",
# #     "ganja packets being sold near school",
# #     "guys selling brown sugar packets in evening near bus stand",
# #     "narcotic peddler operating near residential area",
# #     "here school near ganja selling",          # translated Tamil complaint
# #     "school near ganja smoking",               # translated Tamil complaint
# #     "college near ganja selling",              # translated Tamil complaint
# #     "school near drugs selling",               # translated Tamil complaint
# #     "students drug substance using",           # translated Tamil complaint
# #     # Tamil (original script — for similarity model)
# #     "கல்லூரி பக்கத்தில் கஞ்சா விக்கிறாங்க",
# #     "பஸ் ஸ்டாண்ட் பக்கம் போதை பொருள் விற்பனை",
# #     "பள்ளி அருகில் போதைப்பொருள் விற்கிறாங்க",
# #     "இங்க ஸ்கூல் பக்கத்துல கஞ்சா விக்கிரங்கா",
# #     "மாணவர்கள் போதை பொருள் உபயோகிக்கிறார்கள்",
# #     # Tanglish
# #     "enna panrathu drug addict ah irukaan police ku sollunga",
# #     "school pakkam ganja vilkuranga kitta ponga",
# #     "college canteen back side la ganja smoke panranga daily",
# #     "park la late night la drugs use panranga complain pannunga",
# # ]

# # JUNK_ANCHORS: List[str] = [
# #     # English
# #     "doctor prescribed mental drug for my depression",
# #     "I am addicted to cricket it is like a drug",
# #     "testing app hello ignore this message",
# #     "love is my drug I cannot live without you",
# #     "painkiller tablets after surgery prescribed by doctor",
# #     "that movie was so good it felt like a drug",
# #     "drugs are bad for society general awareness",
# #     "mental health medicine tablet doctor help",
# #     "my friend taking tablets for depression prescribed",
# #     "music is addictive like a drug to me",
# #     # Tamil junk (medical / metaphor)
# #     "doctor prescription tablet saapidu sonnanga",
# #     "மருத்துவர் மருந்து எழுதி கொடுத்தார்",
# #     # Tanglish junk
# #     "cricket pathi pesrom adhu ennakku drug maari",
# #     "app test panrom evvalavo ignore pannunga",
# #     "kadhal oru drug maari irukku life la",
# #     "mental health ku doctor tablet kuduthaanga saapidren",
# #     "movie patha appuram drug feel achu super ah irunthuchu",
# # ]


# # # ─────────────────────────────────────────────────────────────────────────────
# # # Lazy getters
# # # # ─────────────────────────────────────────────────────────────────────────────

# # # def get_nli():
# # #     global _nli_model
# # #     if _nli_model is None:
# # #         from transformers import pipeline
# # #         print("[shared_models] Loading NLI model (facebook/bart-large-mnli) …")
# # #         _nli_model = pipeline(
# # #             "zero-shot-classification",
# # #             model="facebook/bart-large-mnli",
# # #         )
# # #         print("[shared_models] NLI model ready.")
# # #     return _nli_model


# # # def get_embedder():
# # #     global _embedder_model
# # #     if _embedder_model is None:
# # #         from sentence_transformers import SentenceTransformer
# # #         print("[shared_models] Loading multilingual sentence-transformer …")
# # #         _embedder_model = SentenceTransformer(
# # #             "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
# # #         )
# # #         print("[shared_models] Sentence-transformer ready.")
# # #     return _embedder_model

# # def get_embedder():
# #     global _embedder_model

# #     if _embedder_model is None:
# #         from sentence_transformers import SentenceTransformer

# #         print("[shared_models] Loading multilingual semantic model...")

# #         _embedder_model = SentenceTransformer(
# #             "intfloat/multilingual-e5-small"
# #         )

# #         print("[shared_models] Semantic model ready.")

# #     return _embedder_model


# # def get_valid_emb():
# #     global _valid_emb_cache
# #     if _valid_emb_cache is None:
# #         _valid_emb_cache = get_embedder().encode(
# #             VALID_ANCHORS, convert_to_tensor=True, normalize_embeddings=True
# #         )
# #     return _valid_emb_cache


# # def get_junk_emb():
# #     global _junk_emb_cache
# #     if _junk_emb_cache is None:
# #         _junk_emb_cache = get_embedder().encode(
# #             JUNK_ANCHORS, convert_to_tensor=True, normalize_embeddings=True
# #         )
# #     return _junk_emb_cache










# """
# Fast multilingual semantic models shared across the app.
# Production optimized.
# """

# from sentence_transformers import SentenceTransformer

# _embedder_model = None

# VALID_ANCHORS = [

#     # English
#     "students smoking ganja behind college",
#     "drug selling near bus stand",
#     "dealer supplying drugs near school",
#     "illegal liquor sale in public area",
#     "public drug usage happening near park",
#     "drug trafficking near railway station",
#     "ganja packets selling near school",
#     "boys using drugs in campus",

#     # English + Tamil (for better multilingual matching)
#     "School அருகில் kanja விற்கிறார்கள்",
#     "College பக்கத்தில் drugs use panranga",
#     "Bus stand பக்கம் weed sale nadakuthu",
#     "Park லா drug use panranga",
    

#     # Tamil
#     "கல்லூரி அருகில் கஞ்சா விற்கிறார்கள்",
#     "பள்ளி அருகில் போதைப்பொருள் பயன்படுத்துகிறார்கள்",
#     "பஸ் ஸ்டாண்ட் பக்கம் போதை பொருள் விற்பனை",

#     # Tanglish
#     "school pakkam ganja vilkuranga",
#     "college la drugs use panranga",
#     "bus stand la weed sale nadakuthu",
#     "park la drug use panranga",
#     "students smoke panranga near school",
# ]

# JUNK_ANCHORS = [

#     # English
#     "doctor prescribed medicine",
#     "mental health tablet usage",
#     "cricket is like a drug",
#     "testing app ignore message",
#     "movie scene felt like a drug",
#     "painkiller after surgery",

#     # Tamil
#     "மருத்துவர் மருந்து எழுதி கொடுத்தார்",
#     "மனநல மருந்து சாப்பிடுகிறேன்",

#     # Tanglish
#     "doctor tablet kudutharu",
#     "cricket enakku drug maari",
#     "mental health ku medicine use panren",
#     "app testing only",
# ]


# def get_embedder():

#     global _embedder_model

#     if _embedder_model is None:

#         print("[AI] Loading multilingual semantic model...")

#         _embedder_model = SentenceTransformer(
#             "intfloat/multilingual-e5-base"
#         )

#         print("[AI] Semantic model loaded.")

#     return _embedder_model