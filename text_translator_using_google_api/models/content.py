from text_translator_using_google_api.enums.type_content import TypeContent


class Content(object):

    def __init__(self, type_content: TypeContent, lang: str):
        self._type_content = type_content
        self._lang = lang

    @property
    def type_content(self) -> TypeContent:
        return self._type_content

    @type_content.setter
    def type_content(self, type_content) -> None:
        self._type_content = type_content

    @property
    def lang(self) -> str:
        return self._lang

    @lang.setter
    def lang(self, lang) -> None:
        self._lang = lang