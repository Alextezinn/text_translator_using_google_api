import unittest

from loguru import logger

from text_translator_using_google_api.api.api import Api
from text_translator_using_google_api.models.text import Text
from text_translator_using_google_api.enums.type_content import TypeContent
from text_translator_using_google_api.models.translate_content import TranslateContent
from text_translator_using_google_api.utils.configuration_logger import config


class TestTranslateContentApi(unittest.TestCase):

    logger.configure(**config)

    def setUp(self) -> None:
        self.api = Api()

    def test_translate_text_use_google_api_success(self):
        text = "Hello world!"
        translate_text = self.api.translate_text_use_google_api(text)

        txt = Text(TypeContent.TEXT, "en", text, "Привет мир!", None)
        translate_content = TranslateContent(txt, "ru")

        logger.debug(translate_text)
        logger.debug(translate_content)

        self.assertEqual(translate_content.content.translate_text, translate_text.content.translate_text)

    @unittest.expectedFailure
    def test_translate_text_use_google_api_fail(self):
        text = "Hello world!"
        translate_text = self.api.translate_text_use_google_api(text)

        txt = Text(TypeContent.TEXT, "en", text, "Hallo Welt!", None)
        expected_translate_content = TranslateContent(txt, "de")

        logger.debug(translate_text)
        logger.debug(expected_translate_content)

        self.assertEqual(translate_text.content.translate_text, expected_translate_content.content.translate_text, "broken")

    def test_translate_file_subtitle_srt_success(self):
        try:
            translate_obj = self.api.translate_file_subtitle_srt(filename="/home/alexander/PycharmProjects/text_translator_using_google_api/text_translator_using_google_api/resources/subtitles/Mr. Mrs. Smith (2005).en.srt")

        except Exception as err:
            pass

        print(translate_obj)
        self.assertIsNotNone(translate_obj)

    def test_translate_file_subtitle_srt_fail(self):
        translate_file = self.api.translate_file_subtitle_srt(filename="/home/alexander/PycharmProjects/text_translator_using_google_api/text_translator_using_google_api/resources/subtitles/example_srt.srt")
        self.assertIsNotNone(translate_file)

    def test_translate_file_subtitle_ass_success(self):
        try:
            translate_obj = self.api.translate_file_subtitle_ass("/home/alexander/PycharmProjects/text_translator_using_google_api/text_translator_using_google_api/resources/subtitles/Dukes Of Hazzard S05E20 Big Brothers, Duke.720p.AMZN.WEB-DL.x264.HI.en.ass")
        except Exception as err:
            pass

        print(translate_obj)
        self.assertIsNotNone(translate_obj)

    @unittest.expectedFailure
    def test_translate_file_subtitle_ass_fail(self):
        translate_file = self.api.translate_file_subtitle_ass("/home/alexander/PycharmProjects/text_translator_using_google_api/text_translator_using_google_api/resources/subtitles/example_ass.ass")
        self.assertIsNotNone(translate_file)

    def test_translate_file_subtitle_sub_success(self):
        try:
            translate_obj = self.api.translate_file_subtitle_sub("/home/alexander/PycharmProjects/text_translator_using_google_api/text_translator_using_google_api/resources/subtitles/example.sub")
        except Exception as err:
            pass

        print(translate_obj)
        self.assertIsNotNone(translate_obj)

    @unittest.expectedFailure
    def test_translate_file_subtitle_sub_fail(self):
        translate_file = self.api.translate_file_subtitle_sub("/home/alexander/PycharmProjects/text_translator_using_google_api/text_translator_using_google_api/resources/subtitles/example_ass.ass")
        self.assertIsNotNone(translate_file)

    def test_translate_file_subtitle_success(self):
        try:
            translate_obj = self.api.translate_file_subtitle("translate_file_subtitle_srt", "/home/alexander/PycharmProjects/text_translator_using_google_api/text_translator_using_google_api/resources/subtitles/example_srt.srt")
        except Exception as err:
            pass

        print(translate_obj)
        self.assertIsNotNone(translate_obj)

    def test_translate_file_subtitle_fail(self):
        translate_obj = self.api.translate_file_subtitle("translate_file_subtitle_srts", "/home/alexander/PycharmProjects/text_translator_using_google_api/text_translator_using_google_api/resources/subtitles/example_srt.srt")
        logger.info(translate_obj)
        self.assertEqual(-1, translate_obj)

    def test_get_synonymizer_text_success(self):
        text = self.api.get_synonymizer_text("я купил машину")
        logger.info(text)
        self.assertIsInstance(text, str)
        self.assertIsNotNone(text)

    @unittest.expectedFailure
    def test_get_synonymizer_text_fail(self):
        text = self.api.get_synonymizer_text("я купил машину")
        logger.info(text)
        self.assertEqual(text, "я купил машину")

    def test_get_three_synonymizer_text_success(self):
        text = "Парсер — это программа, сервис или скрипт, который собирает данные с " \
               "указанных веб-ресурсов, анализирует их и выдает в нужном формате. С помощью " \
               "парсеров можно делать много полезных задач: Цены. Актуальная задача для " \
               "интернет-магазинов."

        synonymize_text = self.api.get_three_synonymizer_text(text)
        logger.info(synonymize_text)
        self.assertIsInstance(synonymize_text[0], str)
        self.assertNotEqual(text, synonymize_text[0])

    @unittest.expectedFailure
    def test_get_three_synonymizer_text_fail(self):
        text = "Парсер — это программа, сервис или скрипт, который собирает данные с " \
               "указанных веб-ресурсов, анализирует их и выдает в нужном формате. С помощью " \
               "парсеров можно делать много полезных задач: Цены. Актуальная задача для " \
               "интернет-магазинов."

        synonymize_text = self.api.get_three_synonymizer_text(text)
        logger.info(synonymize_text)
        self.assertEquals(text, synonymize_text[0])

    def test_synonymizer_success(self):
        text = "я купил машину"
        synonymize_text = self.api.synonymizer("get_synonymizer_text", text)
        logger.info(synonymize_text)
        self.assertIsNotNone(synonymize_text)
        self.assertNotEqual(text, synonymize_text)

    def test_synonymizer_fail(self):
        text = "я купил машину"
        synonymize_text = self.api.synonymizer("get_synonymizer_texts", text)
        self.assertEqual(-1, synonymize_text)


if __name__ == '__main__':
    unittest.main()
