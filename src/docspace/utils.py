from pathlib import Path
import string
import nltk
from nltk.corpus import stopwords
import docspace


try:
    stops = list(set(stopwords.words('english')))
except LookupError:
    nltk.download('stopwords')
    stops = list(set(stopwords.words('english')))

replace_chars = string.punctuation + '1234567890“’'
char_translator = str.maketrans(replace_chars, ' '*len(replace_chars))

def clean_text(text, keep_stops=False):
    text = text.lower()
    text = text.translate(char_translator)
    text = text.replace('\n', ' ')
    tokens = text.split()
    if not keep_stops:
        tokens = [x for x in tokens if x not in stops]
    text = ' '.join(tokens)
    return text
