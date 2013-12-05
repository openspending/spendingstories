"""
Utility script to display as json the list of supported languages

Usage: `python scripts/get_supported_languages.py`
"""
from webapp import settings
import json

iso_codes = map(lambda el: el[0], settings.LANGUAGES)
print json.dumps(iso_codes)