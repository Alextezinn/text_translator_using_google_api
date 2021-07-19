from .content import Content


class TranslateContent(object):

    def __init__(self, content: Content, lang: str):
        self._content = content
        self._lang = lang

    @property
    def content(self) -> Content:
        return self._content

    @content.setter
    def content(self, content) -> None:
        self._content = content

    @property
    def lang(self) -> str:
        return self._lang

    @lang.setter
    def lang(self, lang) -> None:
        self._lang = lang

    def __eq__(self, other):
        return self is other

    def __hash__(self):
        return hash((self._content, self._lang))

    def __str__(self):
        return f"TranslateContent: {self._content}, {self._lang}"

    def __repr__(self):
        f"TranslateContent({self._content}, {self._lang})"