from googletrans import Translator
# from PyQt5.QtGui import QFont
import logging

languages = {
    "en": {"name": "English", "script": "latin"},
    "bn": {"name": "Bengali", "script": "bangla"},
    "hi": {"name": "Hindi", "script": "devanagari"},
    "or": {"name": "Odia", "script": "odia"},
    "de": {"name": "German", "script": "latin"},
    "fr": {"name": "French", "script": "latin"},
    "ur": {"name": "Urdu", "script": "nashtaliq"},
    "es": {"name": "Spanish", "script": "latin"},
    "gj": {"name": "Gujarati", "script": "gujarati"},
    "te": {"name": "Telugu", "script": "telugu"},
    "ta": {"name": "Tamil", "script": "tamil"},
    "ml": {"name": "Malayalam", "script": "malayalam"},
    "kn": {"name": "Kannada", "script": "kannada"},
    "mr": {"name": "Marathi", "script": "devanagari"},
    "pa": {"name": "Punjabi", "script": "gurmukhi"},
}

numbers = {
    "latin": "0123456789",
    "bangla": "০১২৩৪৫৬৭৮৯",
    "devanagari": "०१२३४५६७८९",
    "odia": "୧୨୩୪୫୬୭୮୯",
    "gujarati": "૦૧૨૩૪૫૬૭૮૯",
}

def get_respective_number(number_text, src, dest):
    res = ""
    if languages[src]["script"] == languages[dest]["script"]:
        res = number_text
    else:
        for char in number_text:
            if char in numbers[languages[src]["script"]]:
                res += numbers[languages[dest]["script"]][
                    numbers[languages[src]["script"]].index(char)
                ]
            else:
                res += char
    return res

# fonts = {
#     "en": QFont("Baloo", 12),
#     "bn": QFont("Baloo Da", 12),
#     "hi": QFont("Baloo", 12),
#     "od": QFont("Baloo Bhaina", 12),
#     "de": QFont("Baloo", 12),
#     "fr": QFont("Baloo", 12),
#     "es": QFont("Baloo", 12),
#     "te": QFont("Baloo Tammudu", 12),
#     "ur": QFont("Baloo Bhaijaan", 12),
#     "ta": QFont("Baloo Thambi", 12),
# }


def translate(text, src, dest):
    res = ""
    try:
        translator = Translator()
        translation = translator.translate(text, src=src, dest=dest)
        res = translation.text 
        # Check if the text has numbers
        res = get_respective_number(translation.text, src, dest)
        logging.info(
            f"{translation.origin} ({translation.src}) --> {res} ({translation.dest})"
        )
    except ConnectionError as e:
        print(e)
        res = "*** Connection Error ***"
    return res
