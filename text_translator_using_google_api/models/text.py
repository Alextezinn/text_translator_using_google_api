from typing import Optional

from .content import Content
from text_translator_using_google_api.enums.type_content import TypeContent


class Text(Content):

    def __init__(self, type_content: TypeContent, lang: str, origin_text: str, translate_text: str, name: Optional[str]=None):
        super().__init__(type_content, lang)
        self._origin_text = origin_text
        self._translate_text = translate_text
        self._name = name

    @property
    def origin_text(self) -> str:
        return self._origin_text

    @origin_text.setter
    def origin_text(self, origin_text) -> None:
        self._origin_text = origin_text

    @property
    def translate_text(self) -> str:
        return self._translate_text

    @translate_text.setter
    def translate_text(self, translate_text) -> None:
        self._translate_text = translate_text

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, name) -> None:
        self._name = name

    def __eq__(self, other):
        return self is other

    def __hash__(self):
        return hash((self._type_content, self._lang, self._origin_text, self._translate_text, self._name))

    def __str__(self):
        return f"Text: {self._type_content}, {self._lang}, {self._origin_text}, {self._translate_text}, {self._name}"

    def __repr__(self):
        f"Text({self._type_content}, {self._lang}, {self._origin_text}, {self._translate_text}, {self._name})"