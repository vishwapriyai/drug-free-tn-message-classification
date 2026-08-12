NORMALIZATION_MAP = {

    # selling
    "vikkuranga": "selling drugs",
    "vikranga": "selling drugs",
    "vilkuranga": "selling drugs",

    # using
    "adikuranga": "using drugs",
    "smoke panranga": "smoking drugs",

    # drug names
    "saraku": "liquor",
    "ganja": "cannabis",

    # places
    "school pakkathula": "near school",
    "college pakkam": "near college",

    # actions
    "kudukranga": "supplying drugs",
}

def normalize_text(text: str):

    text = text.lower()

    for k, v in NORMALIZATION_MAP.items():
        text = text.replace(k, v)

    return text