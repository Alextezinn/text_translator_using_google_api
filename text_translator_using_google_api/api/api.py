import time
import json
from typing import List, Dict, Union, Optional
import sys
import random

import requests
from bs4 import BeautifulSoup
from faker import Faker
from fake_useragent import UserAgent
from loguru import logger
import nltk
from nltk.tokenize import sent_tokenize
from textblob import TextBlob
from googletrans import Translator
import fake_proxy

import constants
from text_translator_using_google_api.sub.sub_viewer_file import SubViewerFile
from text_translator_using_google_api.utils.configuration_logger import config
from text_translator_using_google_api.models.text import Text
from text_translator_using_google_api.enums.type_content import TypeContent
from text_translator_using_google_api.models.translate_content import TranslateContent
from text_translator_using_google_api.models.file_subtitle import FileSubtitle
from text_translator_using_google_api.sub.sub_rip_srt_file import SubRipSrtFile
from text_translator_using_google_api.sub.sub_rip_ass_file import SubRipAssFile


nltk.download('punkt')


class Api():
    """
       Класс предоставляющий API приложения

       Атрибуты:
       _______________________________________________________
           :param _ua: юзер-агент для запросов
           :param _proxy: прокси для запросов

       Методы API:
       _______________________________________________________
           :param: translate_text_use_google_api
           :param: translate_file_subtitle
           :param: translate_file_subtitle_srt
           :param: translate_file_subtitle_ass
           :param: translate_file_subtitle_sub
           :param: synonymizer
           :param: get_three_synonymizer_text
           :param: get_synonymizer_text

       Вспомогательные методы:
       _______________________________________________________
           :param: _write_translate_phrases_in_file_subtitle_srt
           :param: _write_translate_phrases_in_file_subtitle_ass
           :param: _write_translate_phrases_in_file_subtitle_sub
           :param: _get_data_sent_by_user
           :param: _registration_fake_user
           :param: _get_three_type_synonymize_text
           :param: _tokenization
           :param: _google_translator
           :param: _checke_count_characters_in_text
           :param: _checking_text_fits_into_timing
       """
    logger.configure(**config)
    _ua = UserAgent()
    _proxy = fake_proxy.get_from_source(source_name='free-proxy-list.net',
                                        amount=1,
                                        proxy_type='https')[0]

    # API
    @logger.catch
    def translate_text_use_google_api(self, origin_text: str, text_title: Optional[str] = None) -> TranslateContent:
        """
        Метод который переводит текст используя google api.

        :param origin_text: исходный тескт который надо перевести
        :return: объект класса TranslateContent
        :rtype: TranslateContent
        """
        try:
            translate_text = ""
            checke_text, lang = self._checke_count_characters_in_text(origin_text)

            if checke_text is None:
                sentences, lang = self._tokenization(origin_text)
                # переводим все предложения используя google api
                translate_sentences = self._google_translator(sentences)

            else:
                translate_sentences = self._google_translator(checke_text)

            for sentence in translate_sentences:
                translate_text = " ".join([translate_text, sentence.text])

            txt = Text(TypeContent.TEXT, "en", origin_text, translate_text.strip(), text_title)
            translate_content = TranslateContent(txt, "ru")

            return translate_content

        except Exception as err:
            logger.error(err)
            return -1
            sys.exit(-1)

    def translate_file_subtitle(self, operation: str, filename: str, encoding: str = None):
        """
        Метод который вызывает другой метод который выбрал пользователь для
        работы с файлом субтитров.

        :param operation: выбранный метод пользователем для файла субтитров
        :param filename: название файла субтитров
        :param encoding: кодировка файла субтитров
        :return:
        :rtype:
        """
        try:
            if operation == "translate_file_subtitle_srt":
                return self.translate_file_subtitle_srt(filename, encoding)
            elif operation == "translate_file_subtitle_ass":
                return self.translate_file_subtitle_ass(filename, encoding)
            elif operation == "translate_file_subtitle_sub":
                return self.translate_file_subtitle_sub(filename, encoding)
            else:
                logger.error("Неправильный ввод данных. Нет такой команды")
                return -1
                sys.exit(-1)

        except Exception as err:
            return -1
            sys.exit(-1)

    @logger.catch
    def translate_file_subtitle_srt(self, filename: str, encoding: str = None) -> TranslateContent:
        """
        Метод который переводит файл субтитров с русского на английский с расширением .srt

        :param filename: имя файла субтитров который считывается
        :param encoding: кодировка файла субтитров с которого считываем информацию
        :return: объект класса TranslateContent
        :rtype: TranslateContent
        """
        try:
            translate_filename = "".join(["subfile", str(int(time.time())), ".srt"])
            subfile = open(translate_filename, "w+", encoding='utf-8')

            if encoding is not None:
                self._write_translate_phrases_in_file_subtitle_srt(subfile, filename, encoding)
            else:
                self._write_translate_phrases_in_file_subtitle_srt(subfile, filename)

            subfile.close()

            file_subtitle = FileSubtitle(TypeContent.FILE_SUBTITLE, "en", filename,
                                         translate_filename.split(".")[0], "srt")
            translate_content = TranslateContent(file_subtitle, "ru")
            return translate_content

        except Exception as err:
            logger.error(err)

    @logger.catch
    def translate_file_subtitle_ass(self, filename: str, encoding: str = None) -> TranslateContent:
        """
        Метод который переводит файл субтитров с русского на английский с расширением .ass

        :param filename: имя файла субтитров который считывается
        :param encoding: кодировка файла субтитров с которого считываем информацию
        :return: объект класса TranslateContent
        :rtype: TranslateContent
        """
        try:
            translate_filename = "".join(["subfile", str(int(time.time())), ".ass"])
            subfile = open(translate_filename, "w+", encoding='utf_8_sig')

            if encoding is not None:
                self._write_translate_phrases_in_file_subtitle_ass(subfile, filename, encoding)
            else:
                self._write_translate_phrases_in_file_subtitle_ass(subfile, filename)
                logger.info("here")

            subfile.close()

            file_subtitle = FileSubtitle(TypeContent.FILE_SUBTITLE, "en", filename,
                                         translate_filename.split(".")[0], "ass")
            translate_content = TranslateContent(file_subtitle, "ru")
            return translate_content

        except Exception as err:
            logger.error(err)

    @logger.catch
    def translate_file_subtitle_sub(self, filename: str, encoding: str = None) -> TranslateContent:
        """
        Метод который переводит файл субтитров с русского на английский с расширением .sub

        :param filename: имя файла субтитров который считывается
        :param encoding: кодировка файла субтитров с которого считываем информацию
        :return: объект класса TranslateContent
        :rtype: TranslateContent
        """
        try:
            translate_filename = "".join(["subfile", str(int(time.time())), ".sub"])
            subfile = open(translate_filename, "w+", encoding='utf_8')

            if encoding is not None:
                self._write_translate_phrases_in_file_subtitle_sub(subfile, filename, encoding)
            else:
                self._write_translate_phrases_in_file_subtitle_sub(subfile, filename)

            subfile.close()

            file_subtitle = FileSubtitle(TypeContent.FILE_SUBTITLE, "en", filename,
                                         translate_filename.split(".")[0], "sub")
            translate_content = TranslateContent(file_subtitle, "ru")
            return translate_content

        except Exception as err:
            logger.error(err)

    def synonymizer(self, operation: str, text: str):
        """
        Метод который вызывает другой метод который выбрал пользователь для поиска сининимизации к слову,
        предложению, тексту.

        :param operation: выбранный метод пользователем
        :param text: слово, предложение или текст к которому будет производиться синонимизация.
        :return:
        :rtype:
        """
        try:
            if operation == "get_three_synonymizer_text":
                return self.get_three_synonymizer_text(text)
            elif operation == "get_synonymizer_text":
                return self.get_synonymizer_text(text)
            else:
                logger.error("Неправильный ввод данных. Нет такой команды")
                return -1
                sys.exit(-1)

        except Exception as err:
            return -1
            sys.exit(-1)

    def get_three_synonymizer_text(self, text: str) -> List[str]:
        """
        Метод который делает 3 варианта синонимичных текстов из исходного текста.

        :param text: исходный текст к которому делаем синонимичный текст
        :return: возвращает список из 3 вариантов синонимизорованных текстов
        :rtype: List[str]
        """
        try:
            self._registration_fake_user()
            with requests.Session() as session:

                with open(constants.COOKIES_JSON) as cookies:
                    session.cookies.update(json.load(cookies))

                # Делаем GET запрос, для того чтобы получить id и lp со страницы.
                # id и lp - параметры, которые необходимы для отправки запроса на сервер.
                response_get = session.get(url=constants.URL_GET_INFORMATION_SEND_TEXT,
                                           headers=constants.HEADERS)

                data = {
                    'text': text,
                    'dem': 0,
                }

                data = self._get_data_sent_by_user(data, response_get)

                session.post(url=constants.URL_SEND_TEXT, headers=constants.HEADERS, data=data)

                response_data = {
                    'id': int(data['id']),
                }

                response = session.post(url=constants.URL_GET_TEXT, headers=constants.HEADERS,
                                        data=response_data)
                timeout = 0

                while not response.text:
                    if timeout > 120:
                        logger.error("Timeout requests error")
                        break

                    logger.info("No data")
                    response = session.post(url=constants.URL_GET_TEXT, headers=constants.HEADERS,
                                            data=response_data)
                    time.sleep(2)
                    timeout += 2

                content = response.json()[0]['text']
                three_synonymize_text = self._get_three_type_synonymize_text(content)

                return three_synonymize_text

        except Exception as err:
            logger.error(err)

    def get_synonymizer_text(self, text: str) -> str:
        """
        Метод который делает синонимичный текст из исходного текста.

        :param text: исходный текст к которому делаем синонимичный текст
        :return: возвращает синонимизорованный текст
        :rtype: str
        """
        try:
            with requests.Session() as session:
                response = session.post(constants.SITE_API_SYNONYMIZER, data={'method': 'getSynText', 'text': text})
            return response.json()['modified_text'][:-4]

        except Exception as err:
            logger.error(err)

    # Helper methods
    def _write_translate_phrases_in_file_subtitle_srt(self, subfile, filename: str, encoding: str=None) -> None:
        """
        Метод в котором проходимся по всем элементам файла субтитров с расширением .srt
        и записывается в новый файл переведенная версия.

        :param subfile: файловый объект (поток) куда будет записываться переведенную версию файла субтитров
        :param filename: имя файла субтитров который считывается
        :param encoding: кодировка файла субтитров с которого считываем информацию
        :return:
        :rtype:
        """
        # проходимся по элементам файла субтитров
        for sub_rip_item in SubRipSrtFile.open(filename, claimed_encoding=encoding):

            number_phrase = "".join([str(sub_rip_item.number_phrase), "\n"])
            line = self._google_translator(sub_rip_item.text)
            # засыпаем на время для того чтобы не отправлять запросы сразу а то google api может
            # на время не работать
            time.sleep(random.uniform(3, 5))
            # если список тегов для данной фразы не пуст
            if sub_rip_item.tags:
                # если кол-во строк в фразе равно 1
                if len(sub_rip_item.text) == 1:
                    logger.debug("number_phrase: " + str(number_phrase))
                    line[0].text = self._checking_text_fits_into_timing(line[0].text, sub_rip_item.text[0])
                    line = "".join([sub_rip_item.tags[0], line[0].text, sub_rip_item.tags[1], "\n"])

                else:
                    logger.debug("number_phrase: " + str(number_phrase))
                    text = sub_rip_item.tags[0]
                    for index, value in enumerate(line[:-1]):
                        value.text = self._checking_text_fits_into_timing(value.text, sub_rip_item.text[index])
                        text += "".join([value.text, "\n"])

                    line[-1].text = self._checking_text_fits_into_timing(line[-1].text, sub_rip_item.text[-1])
                    line = "".join([text, line[-1].text, sub_rip_item.tags[1], "\n"])

            else:
                logger.debug("number_phrase: " + str(number_phrase))
                text = ""
                for index, value in enumerate(line):
                    value.text = self._checking_text_fits_into_timing(value.text, sub_rip_item.text[index])
                    text += "".join([value.text, "\n"])

                line = text

            tm = "".join([sub_rip_item.time['start'], " --> ", sub_rip_item.time['end'], "\n"])
            subfile.writelines([number_phrase, tm, line, "\n"])

    def _write_translate_phrases_in_file_subtitle_ass(self, subfile, filename: str, encoding: str=None) -> None:
        """
        Метод в котором проходимся по всем элементам файла субтитров с расширением .ass
        и записывается в новый файл переведенная версия.

        :param subfile: файловый объект (поток) куда будет записываться переведенную версию файла субтитров
        :param filename: имя файла субтитров который считывается
        :param encoding: кодировка файла субтитров с которого считываем информацию
        :return:
        :rtype:
        """
        count = 0
        section_event = "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"

        # проходимся по элементам файла субтитров
        for sub_rip_item in SubRipAssFile.open(filename, claimed_encoding=encoding):
            try:
                if sub_rip_item.name == "Events":
                    subfile.write(section_event)

                    for dialog in sub_rip_item:
                        count += 1
                        type_event = "Dialogue: " + str(dialog.layer)
                        _text = ",".join([type_event, str(dialog.start),str(dialog.end),
                                         dialog.style, dialog.name, str(dialog.margin_l),
                                         str(dialog.margin_r), str(dialog.margin_v), dialog.effect])
                        text = dialog.text.split(r'\N')
                        line = self._google_translator(text)

                        translate_text = ""
                        if len(line) > 1:
                            logger.info("Number phrase: " + str(count))
                            for index, translate_line in enumerate(line):
                                translate_line.text = self._checking_text_fits_into_timing(translate_line.text, text[index])
                                translate_text += translate_line.text + r'\N'

                            text = _text + translate_text[:-2] + "\n"

                        else:
                            logger.info("Number phrase: " + str(count))
                            line[0].text = self._checking_text_fits_into_timing(line[0].text, text[0])
                            text = _text + line[0].text + "\n"

                        subfile.write(text)
                        # засыпаем на время для того чтобы не отправлять запросы сразу а то google api может
                        # на время не работать
                        time.sleep(random.uniform(3, 5))

            except AttributeError as e:
                subfile.write(sub_rip_item)

    def _write_translate_phrases_in_file_subtitle_sub(self, subfile, filename: str, encoding: str=None) -> None:
        """
        Метод в котором проходимся по всем элементам файла субтитров с расширением .sub
        и записывается в новый файл переведенная версия.

        :param subfile: файловый объект (поток) куда будет записываться переведенную версию файла субтитров
        :param filename: имя файла субтитров который считывается
        :param encoding: кодировка файла субтитров с которого считываем информацию
        :return:
        :rtype:
        """
        count = 0

        # проходимся по элементам файла субтитров
        for sub_rip_item in SubViewerFile.open(filename, claimed_encoding=encoding):
            try:
                if sub_rip_item.dialoges:
                    for dialog in sub_rip_item.dialoges:
                        count += 1
                        text = dialog.text.split("[br]")
                        line = self._google_translator(text)

                        translate_text = ""
                        if len(line) > 1:
                            logger.info("Number phrase: " + str(count))
                            for index, translate_line in enumerate(line):
                                translate_line.text = self._checking_text_fits_into_timing(translate_line.text, text[index])
                                translate_text += translate_line.text + "[br]"

                            text = translate_text[:-4]

                        else:
                            logger.info("Number phrase: " + str(count))
                            line[0].text = self._checking_text_fits_into_timing(line[0].text, text[0])
                            text = line[0].text

                        text = "".join([str(dialog.start), ",", str(dialog.end), "\n", text, "\n\n"])
                        subfile.write(text)
                        # засыпаем на время для того чтобы не отправлять запросы сразу а то google api может
                        # на время не работать
                        time.sleep(random.uniform(3, 5))

            except Exception as e:
                subfile.write(sub_rip_item)

    def _get_data_sent_by_user(self, data: Dict, response_get: requests.Response) -> Dict:
        """
        Получаем данные которые спрятаны на странице пользователя которые
        нужны для отправки запроса от конкретного пользователя.

        :param data: данные которые будут отправлены в запросе
        :param response_get: ответ текста на get запрос по сути страница html
        :return: обновленные данные которые будут отправлены в запросе
        :rtype: Dict
        """
        bs = BeautifulSoup(response_get.text, 'html.parser')

        # Получаем все теги div на странице
        tags = bs.find_all('div')

        for tag in tags:

            # Получаем данные параметров lp и lg
            data_lp = tag.get('lp')
            data_lg = tag.get('lg')

            # Если в div есть такие параметры, то тогда
            if data_lp is not None:
                data['id'] = data_lg
                data['lp'] = data_lp

        return data

    def _registration_fake_user(self) -> None:
        """
        Регистрация фейкогого пользователя на сайте https://sin-ai.ru/
        для отправки запросов на сервер

        :return:
        :rtype:
        """
        fake = Faker()
        user_agent = self._ua.chrome

        with requests.Session() as session:
            constants.HEADERS['User-Agent'] = user_agent
            password = fake.password()
            params = {
                'username': fake.user_name(),
                'email': fake.email(),
                'password1': password,
                'password2': password,
                'act': 'register'
            }
            session.post(url=constants.URL_REGISTER, headers=constants.HEADERS, params=params)
            session.cookies.update({'User-Agent': user_agent})

            with open(constants.COOKIES_JSON, 'w') as cookies:
                json.dump(requests.utils.dict_from_cookiejar(session.cookies), cookies)

    def _get_three_type_synonymize_text(self, content: str) -> List[str]:
        """
        Вытаскиваем 3 варианта перефразированного текста из html тегов который
        мы получили в качестве ответа от сервера

        :param content: ответа от сервера (3 варианта перефразированного
                        текста заключенный между тегами)
        :return: список из 3 вариантов перефразированного текста
        :rtype: List[str]
        """
        bs = BeautifulSoup(content, 'html.parser')
        return [bs.find('div', id=f'txt_cop_{i}').get_text() for i in range(1, 4)]

    def _tokenization(self, text: str) -> (Union[List[str], str], str):
        """
        Функция производящая токенизацию текста по предложениям

        :param text: текст над котором будет производится токенизация
        :return: список предложений текста и язык исходного текста
        :rtype: Union[List[str], str], str
        """
        lang_det = TextBlob(text)
        # определяем язык текста
        language = lang_det.detect_language()

        if language == 'en':
            sentences = sent_tokenize(text, language="english")
        elif language == 'ru':
            sentences = sent_tokenize(text, language="russian")
        else:
            logger.error("Language not found")
            sys.exit(0)

        return sentences, language

    def _google_translator(self, text: str) -> Union[List[str], str]:
        """
        Функция для перевода английского текста в русский
        используя Google API

        :param text: текст который надо перевести в виде строки либо списка
        :return: переведенный текст на русском языке в виде строки либо списка
        :rtype: Union[List[str], str]
        """
        user_agent = self._ua.chrome
        proxy = {'http': "".join([self._proxy['ip'], ":", self._proxy['port']])}
        translator = Translator(user_agent=user_agent, proxies=proxy)
        russian_text = translator.translate(text, src='en', dest='ru')
        return russian_text

    def _checke_count_characters_in_text(self, origin_text: str) -> (List[str], Optional[str]):
        """
        Проверка кол-ва символов в тексте, если их больше 2000, то разбиваем текст
        на части предложений, где кол-во символов меньше 2000.

        :param origin_text: исходный текст
        :return: список который состоит из частей предложений не более 2000 символов и
                 язык исходного текста или None, None
        :rtype: List[str], Optional[str]
        """
        translate_text = []
        if len(origin_text) > 2000:
            sentences, lang = self._tokenization(origin_text)
            text = ""

            for sentence in sentences:
                if len(text) < 1900:
                    text = " ".join([text, sentence])
                else:
                    translate_text.append(text)
                    text = ""

            if text != "":
                translate_text.append(text)

            return translate_text, lang

        return None, None

    def _checking_text_fits_into_timing(self, rus_line, en_line) -> str:
        """
        Метод проверящий будет ли переведенное предложение умещаться в тайминг в случае
        его озвучивания.

        :param rus_line: переведенное предложение
        :param en_line: исходное предложение
        :return: возращает предложение как оно было при переводе, либо предложение после синонимизации,
                 или как ввел пользователь.
        :rtype: str
        """
        # если разница между переведенной и исходной строкой больше 6 символов
        logger.info("".join(["Предложение после перевода: ", rus_line]))
        if abs(len(rus_line) - len(en_line)) > 10:
            # получаем синонимичное предложение
            sinonim_line = self.get_synonymizer_text(rus_line)
            logger.info("".join(["Предложение после синонимизации: ", sinonim_line]))
            choose = input("Выберете действие\n" \
                           "0 - оставить как есть после перевода\n"
                           "1 - оставить как есть после синонимизации\n"
                           "2 - предложить свой вариант\n")
            try:
                if int(choose) == 0:
                    return rus_line
                elif int(choose) == 1:
                    rus_line = sinonim_line
                elif int(choose) == 2:
                    rus_line = input()
                else:
                    logger.error("Неправильный ввод данных. Такого варианта выбора нет.")
            except ValueError as err:
                logger.error("Неправильный ввод данных. Должно быть число либо 0 либо 1")

            return rus_line

        return rus_line