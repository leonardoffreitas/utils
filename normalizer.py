import re
from unicodedata import normalize
from html.parser import HTMLParser
from html.entities import name2codepoint


#https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def unescape(text):
    '''
    Removes HTML or XML character references and entities from a text string.

    @param text The HTML (or XML) source text.
    @return The plain text, as a Unicode string, if necessary.
    http://effbot.org/zone/re-sub.htm#unescape-html
    '''
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return chr(int(text[3:-1], 16))
                else:
                    return chr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = chr(name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text  # leave as is
    return re.sub("&#?\w+;", fixup, text)


class Normalizer():

    def __init__(self):
        self.alfanum_only = re.compile(r'\W+')

    def translate_html_entities(self, text):
        return unescape(text)

    #https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
    def strip_tags(self, html):
        s = MLStripper()
        s.feed(html)
        return s.get_data()

    def normalize_html(self, text):
        return self.strip_tags(
            self.translate_html_entities(text)
        )

    def normalize_accents(self, text, lowcase=True):
        normalized_text = text
        normalized_text = normalize(
            'NFKD', normalized_text
        ).encode('ASCII', 'ignore').decode("utf-8")
        if lowcase:
            return normalized_text.lower()
        else:
            return normalized_text

    def normalize_text(self, text):
        return self.alfanum_only.sub(' ', self.normalize_accents(text))


if __name__ == "__main__":
    text = 'Jogo de Furar e Parafusar 16 Peças R&ocirc;mulo - Black&amp;Decker'
    print('text: ', text)

    print('\n+translate_html_entities')
    text = Normalizer().translate_html_entities(text)
    print('text: ', text)

    print('\n+normalize_accents')
    text = Normalizer().normalize_accents(text)
    print('text: ', text)

    print('\n+normalize_text')
    text = Normalizer().normalize_text(text)
    print('text: ', text)

    text ='<a href="../../../../articles/w/a/d/Waddinxveen.html" title="Waddinxveen">Waddinxveen</a> | 79&#160;'
    print('\ntext: ', text)
    print('\n+normalize_html')
    text = Normalizer().normalize_html(text)
    print('text: ', text)

    print('\n+normalize_text')
    text = Normalizer().normalize_text(text)
    print('text: ', text)
