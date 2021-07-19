import sys

from loguru import logger

from text_translator_using_google_api.api.api import Api
from text_translator_using_google_api.utils.configuration_logger import config


class Main():

    @staticmethod
    def main():
        logger.configure(**config)
        api = Api()
        args = sys.argv[1:]

        if args[0] == "translate_file_subtitle":
            if len(args) == 3:
                logger.info(api.translate_file_subtitle(args[1], args[2]))
            elif len(args) == 4:
                logger.info(api.translate_file_subtitle(args[1], args[2], args[3]))
            else:
                logger.error("Error args")

        elif args[0] == "synonymizer":
            logger.info(api.synonymizer(args[1], args[2]))

        elif args[0] == "translate_text_use_google_api":
            if len(args) == 2:
                logger.info(api.translate_text_use_google_api(args[1]))
            elif len(args) == 3:
                logger.info(api.translate_text_use_google_api(args[1], args[2]))
            else:
                logger.error("Error args")

        else:
            logger.error("Error args")


if __name__ == "__main__":
    try:
        Main.main()
    except Exception as err:
        logger.error(err)