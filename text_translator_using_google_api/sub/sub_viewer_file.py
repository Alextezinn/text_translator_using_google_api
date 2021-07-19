import datetime
import logging

from .sub_rip_file import SubRipFile
from collections import namedtuple


class SubViewerFile(SubRipFile):
    """
    Класс для файлов субтитров с расширением .sub

       Атрибуты:
       _______________________________________________________
           :param subtitles: список состоящий из строковых элеметов в которых
           находится информация о стилях и других параметрах файла субтитров и
           элементов типа SubViewItem в которых находится начало, конец и текст
           для каждой фразы.
           :param path: путь до файла вместе с именем и расширением файла
           :param encoding: кодировка файла

       Методы:
       _______________________________________________________
           :param open
           :param parse

       Пример структуры файла:
       _______________________________________________________
        [INFORMATION]
        [TITLE]
        [AUTHOR]
        [SOURCE]
        [PRG]
        [FILEPATH]
        [DELAY]0
        [CD TRACK]0
        [COMMENT]
        [END INFORMATION]
        [SUBTITLE]
        [COLF]&HFFFFFF,[STYLE]bd,[SIZE]24,[FONT]Tahoma
        00:00:41.87,00:00:44.20
        My name is Dalton Russell.

        00:00:45.01,00:00:46.94
        Pay strict attention[br]to what I say

        00:00:51.05,00:00:53.95
        I've told you my name.[br]That's the "who."
    """
    def __init__(self, path: str, encoding: str='utf_8'):
        super().__init__()
        self.path = path
        self.encoding = encoding

    def parse(self, source_file) -> None:

        SubViewItem = namedtuple('SubViewItem', 'start end text')
        SubView = namedtuple('SubView', 'dialoges')

        elements = []
        sub_view = []

        for line in source_file:
            if line[0] == "[":
                self.subtitles.append(line)
            else:
                try:
                    if datetime.datetime.strptime(line.split(",")[0], '%H:%M:%S.%f'):
                        # разбивает время формата %H:%M:%S.%f на часы, миниты, секунды и миллисекунды
                        start, end = line.split(",")
                        start = start.split(":")
                        end = end.split(":")
                        start[2] = start[2].split(".")
                        end[2] = end[2].split(".")
                        sec_start = int(start[0]) * 3600 + int(start[1]) * 60 + int(start[2][0])
                        sec_end = int(end[0]) * 3600 + int(end[1]) * 60 + int(end[2][0])

                        sec_start = datetime.timedelta(seconds=sec_start, milliseconds=int(start[2][1]) * 10)
                        sec_end = datetime.timedelta(seconds=sec_end, milliseconds=int(end[2][1]) * 10)

                        if elements != []:
                            item = SubViewItem(*elements[:-1])
                            sub_view.append(item)
                            elements = []

                        elements.extend([sec_start, sec_end])

                except Exception as err:
                    elements.append(line)

        item = SubViewItem(*elements)
        sub_view.append(item)

        sub_view = SubView(sub_view)
        self.subtitles.append(sub_view)

