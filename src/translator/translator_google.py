import re

from googletrans import Translator

from .text_translator import TextTranslator

"""
TranslatorGoogle is a wrapper around google translate API.

Known issues:
 1. from time to time, google translate does not respond correctly and thus returns the following errors
      File "D:\workplace\changsin\pytranslator\venv\lib\site-packages\googletrans\client.py", line 182, in translate
        data = self._translate(translator, dest, src, kwargs)
      File "D:\workplace\changsin\pytranslator\venv\lib\site-packages\googletrans\client.py", line 78, in _translate
        token = self.token_acquirer.do(translator)
      File "D:\workplace\changsin\pytranslator\venv\lib\site-packages\googletrans\gtoken.py", line 194, in do
        self._update()
      File "D:\workplace\changsin\pytranslator\venv\lib\site-packages\googletrans\gtoken.py", line 62, in _update
        code = self.RE_TKK.search(r.translator).group(1).replace('var ', '')
    AttributeError: 'NoneType' object has no attribute 'group'
    
    If this happens, just rerun it till you get the correct response.
"""

MAX_RETRIES = 5


class TranslatorGoogle(TextTranslator):
    def __init__(self, from_language, to_language):
        super(TranslatorGoogle, self).__init__(from_language, to_language)
        self.translator = Translator()

    def translate(self, text):
        text_translated = self.dictionary.get(text)
        if (not text_translated or text == text_translated) and not re.match("^[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)?$", text):
            text_translated = self.translator.translate(text, dest=self.to_language, src=self.from_language).text
            detected_language = self.translator.detect(text)

            # if not translated, try again
            retries = 0
            if detected_language.lang == self.from_language and text_translated == text:

                for i in range(MAX_RETRIES):
                    if text_translated != text:
                        break

                    print("{} not translated. Detected as {}. Trying again".format(text, detected_language.lang))
                    text_translated = self.translator.translate(text, self.to_language, self.from_language).text
                    retries += 1

            if retries < MAX_RETRIES:
                self.dictionary[text] = text_translated
        else:
            print("known string")

        # if text_translated[0].islower():
        #     text_translated = text_translated[0].upper() + text_translated[1:]
        #     self.dictionary[translator] = text_translated

        return text_translated
