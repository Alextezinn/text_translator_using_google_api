from text_translator_using_google_api.models.content import Content
from text_translator_using_google_api.enums.type_content import TypeContent


class FileSubtitle(Content):

    def __init__(self, type_content: TypeContent, lang: str, origin_file_name: str, translate_file_name: str, extend: str):
        super().__init__(type_content, lang)
        self._origin_file_name = origin_file_name
        self._translate_file_name = translate_file_name
        self._extend = extend

    @property
    def origin_file_name(self) -> str:
        return self._origin_file_name

    @origin_file_name.setter
    def origin_file_name(self, origin_file_name) -> None:
        self._origin_file_name = origin_file_name

    @property
    def translate_file_name(self) -> str:
        return self._translate_file_name

    @translate_file_name.setter
    def translate_file_name(self, translate_file_name) -> None:
        self._translate_file_name = translate_file_name

    @property
    def extend(self) -> str:
        return self._extend

    @extend.setter
    def extend(self, extend) -> None:
        self._extend = extend

    def __eq__(self, other):
        return self is other

    def __hash__(self):
        return hash((self._type_content, self._lang, self._origin_file_name, self._translate_file_name, self._extend))

    def __str__(self):
        return f"FileSubtitle: {self._type_content}, {self._lang}, {self._origin_file_name}, {self._translate_file_name}, {self._extend}"

    def __repr__(self):
        f"FileSubtitle({self._type_content}, {self._lang}, {self._origin_file_name}, {self._translate_file_name}, {self._extend})"
