Данная программа является CLI приложением, которое создает новый файл субтитров с качественно переведенным текстом с английского языка на русский язык, где каждый отдельный субтитр укладывался в отведенное ему время в случае озвучки переведенного субтитра.
Реализованная система предоставляет пользователю качественный перевод файла субтитров с расширением srt, sub, ass, обычный перевод текста с английского на русский и получение синонимичного текста из исходного от пользователя.


ИНСТРУКЦИЯ ПО ИСПОЛЬЗОВАНИЮ ПРОГРАММЫ


1. Установить интерпретатор Python версии 3.8, только 64-х битной версии.
2. Создание виртуального окружения. Для этого необходимо в директорию с исходными кодами проекта, в терминале, ввести следующую команду: python3.8 -m venv venv.
3. Для активации виртуального окружения необходимо ввести следующую команду в терминале: venv\Scripts\activate
Если команда выполнилась успешно, то перед приглашением в командной строке появиться дополнительная надпись, совпадающая с названием виртуального окружения.
4. Установка необходимых зависимостей. Для этого необходимо ввести следующую команду в командной строке: pip install -r requirements.txt


Работать с программой можто только через командную строку!!!


Общая сигнатура запуска программы:
python main.py <базовый метод> <расширяющий метод> <данные>

<базовые методы>
translate_text_use_google_api
translate_file_subtitle
synonymizer

<расширяющие методы>
translate_file_subtitle_ass
translate_file_subtitle_sub
translate_file_subtitle_srt

Данные вводятся последовательно через пробел, если, например, имя файла субтитров содержит пропуски, то передавать нужно в кавычках.


Примеры работы программы:

# перевод текста, предложения, слова с английского на русский
python main.py translate_text_use_google_api "hello world!"

# перевод файла субтитров с расширением srt с английского на русский
python main.py translate_file_subtitle translate_file_subtitle_srt "text_translator_using_google_api/resources/subtitles/Mr. Mrs. Smith (2005).en.srt" iso-8859-1

# перевод файла субтитров с расширением ass с английского на русский
python main.py translate_file_subtitle translate_file_subtitle_ass "text_translator_using_google_api/resources/subtitles/Dukes Of Hazzard S05E20 Big Brothers, Duke.720p.AMZN.WEB-DL.x264.HI.en.ass"

# перевод файла субтитров с расширением sub с английского на русский
python main.py translate_file_subtitle translate_file_subtitle_sub "text_translator_using_google_api/resources/subtitles/example.sub"

# синонимизация текста, предложения, слова
python main.py synonymizer get_synonymizer_text "я купил машину"

# получение 3 вариантов синонимичных текстов
python main.py synonymizer get_three_synonymizer_text "я пришел домой"


Для запуска на отработку всех тестов необходимо в корне проекта ввести следующую команду:

python -m unittest tests.api.test_translate_content_api
