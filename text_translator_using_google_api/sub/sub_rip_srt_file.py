from typing import Set
from collections import namedtuple

from loguru import logger

from .sub_rip_file import SubRipFile
from text_translator_using_google_api.utils.configuration_logger import config


class SubRipSrtFile(SubRipFile):
    """
    Класс для файлов субтитров с расширением .srt

    Атрибуты:
    _______________________________________________________
        :param subtitles: список SubRipItem (субтитров) считанных из файла
        :param path: путь до файла вместе с именем и расширением файла
        :param encoding: кодировка файла

    Методы:
    _______________________________________________________
        :param open
        :param parse
        :param _predict_encoding
        :param _parse_text_from_file_subtitle_xml

    Пример структуры файла:
    _______________________________________________________
        1
        00:00:26,613 --> 00:00:28,782
        OK, I'll go first.
    """
    logger.configure(**config)

    def __init__(self, path: str, encoding: str='iso-8859-1'):
        super().__init__()
        self.path = path
        self.encoding = encoding

    def parse(self, source_file) -> None:
        """
        Метод класса для парсинга данных из файла субтитров с
        расширением .srt

        :param source_file: файловый объект (поток)
        :return:
        :rtype:
        """
        try:
            SubRipItem = namedtuple('SubRipItem', 'number_phrase time text tags')
            subtitle = {}

            for line in source_file:

                if line not in ('\r\n', '\r', '\n'):
                    line = line.strip()
                    # проверка если это номер фразы (число)
                    if line.isdigit():
                        # если словарь о субтитре пуст
                        if not bool(subtitle):
                            subtitle['number_phrase'] = int(line)
                            all_tags = []

                        else:
                            item = SubRipItem(**subtitle)
                            self.subtitles.append(item)
                            subtitle = {}
                            all_tags = []
                            subtitle['number_phrase'] = int(line)

                    elif "-->" in line:
                        start, end = line.split("-->")
                        start = start.strip()
                        end = end.strip()
                        subtitle['time'] = {'start': start, 'end': end}
                        subtitle['text'] = []

                    else:
                        l, tags = self._parse_text_from_file_subtitle_xml(line)

                        if tags is not None:
                            all_tags.extend(tags)

                        subtitle['tags'] = all_tags
                        subtitle['text'].append(l.strip())

            item = SubRipItem(**subtitle)
            self.subtitles.append(item)

        except Exception as err:
            logger.error(err)
            logger.error("Неправильная структура файла субтитров с расширением .srt")

    def _parse_text_from_file_subtitle_xml(self, line: str) -> Set[str]:
        """
        Извлечение текста который находится между xml тегами файла субтитров

        :param line: строка файла субтитров
        :return: кортеж состоящий из текста строки и тега если он был в строке
        :rtype: Set[str]
        """
        tags = []

        while "<" and ">" in line:

            if "</" in line:
                start_close_tag = line.index("</")
                tag = line[start_close_tag:]
                tags.append(tag)
                line = line[:start_close_tag]

            else:
                end_open_tag = line.index(">")
                tag = line[line.index("<"):end_open_tag + 1]
                tags.append(tag)
                line = line[(end_open_tag + 1):]

        if len(tags) == 2:
            return line, tags[::-1]

        return line, tags