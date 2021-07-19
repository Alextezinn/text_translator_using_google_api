from abc import ABC, abstractmethod
from typing import Optional, Iterator

import chardet
from loguru import logger

from text_translator_using_google_api.utils.configuration_logger import config


class SubRipFile(ABC):
    """
    Абстрактный класс для файлов субтитров разных форматов

    Атрибуты:
    _______________________________________________________
        :param subtitles: список SubRipItem (субтитров) считанных из файла

    Методы:
    _______________________________________________________
        :param open
        :param parse
        :param _predict_encoding
    """
    logger.configure(**config)

    def __init__(self):
        self.subtitles = []

    @classmethod
    def open(cls, path: str, claimed_encoding: Optional[str]=None) -> Iterator:
        """
        Метод открывающий файл субтитров

        :param path: путь до файла вместе с именем и расширением файла
        :param claimed_encoding: ожидаемая кодировка файла
        :return: итератор списка субтитров
        :rtype: object list_iterator
        """
        # если задана кодировка файла то она и будет использоваться иначе
        # пытаемся предсказать кодировку файла
        try:
            encoding = claimed_encoding or cls._predict_encoding(path)
            source_file = open(path, encoding=encoding)
            new_file = cls(path=path, encoding=encoding)
            new_file.parse(source_file)
            source_file.close()
        except UnicodeDecodeError as err:
            logger.error(err)

        return iter(new_file.subtitles)

    @abstractmethod
    def parse(self, source_file) -> None:
        """
        Абстрактный метод класса который должен быть переопределен в дочерних классах
        для парсинга данных из файла субтитров в зависимости от формата

        :param source_file: файловый объект (поток)
        :return:
        :rtype:
        """
        pass

    @classmethod
    def _predict_encoding(cls, file_path: str, lines: int = 20) -> str:
        """
        Метод предсказывающий кодировку файла с помощью библиотеки chardet

        :param file_path: путь до файла вместе с именем и расширением файла
        :param lines: кол-во строк для предсказания какая кодировка у файла
        :return: кодировку файла
        :rtype: str
        """
        with open(file_path, 'rb') as f:
            # Соединяем двоичные строки на указанное количество строк
            raw_data = b''.join([f.readline() for _ in range(lines)])

        return chardet.detect(raw_data)['encoding']

