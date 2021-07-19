import ass

from .sub_rip_file import SubRipFile


class SubRipAssFile(SubRipFile):
    """
       Класс для файлов субтитров с расширением .ass

       Атрибуты:
       _______________________________________________________
           :param subtitles: список состоящий из строковых элеметов из секции
           [Script Info] и [V4+ Styles] и объекта EventsSection в котором находится
           список объектов типа Dialogue в которых находится вся информация о каждой
           фразе
           :param path: путь до файла вместе с именем и расширением файла
           :param encoding: кодировка файла

       Методы:
       _______________________________________________________
           :param open
           :param parse

       Пример структуры файла:
       _______________________________________________________
            [Script Info]
            ScriptType: v4.00+
            Collisions: Normal
            PlayResX: 1920
            PlayResY: 1080
            Timer: 100.0
            WrapStyle: 0

            [V4+ Styles]
            Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
            Style: Default,sans-serif,71,&H00FFFFFF,&H00FFFFFF,&H000F0F0F,&H000F0F0F,0,0,0,0,100,100,0,0.00,1,2,3,2,20,20,20,0

            [Events]
            Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
            Dialogue: 0,0:00:05.50,0:00:08.76,Default,,0,0,0,,♪ Just the Good Ol' Boys ♪
            Dialogue: 0,0:01:36.29,0:01:38.42,Default,,0,0,0,,This looks like\\Nthe place, alright.
    """
    def __init__(self, path: str, encoding: str='utf_8_sig'):
        super().__init__()
        self.path = path
        self.encoding = encoding

    def parse(self, source_file) -> None:
        for i in source_file:
            if i.strip() != "[Events]":
                self.subtitles.append(i)
            else:
                break

        source_file.seek(0)
        doc = ass.parse(source_file)
        self.subtitles.append(doc.events)



