from functions import *

# ------------Здесь указывается информация об абитуриенте------------

data = {
    "surname": "",  # Имя
    "name": "",  # Фамилия
    "patr": "",  # Отчество
    "passNum": "",  # Серия паспорта
    "region": ""  # Регион
}

# ------------Здесь указываюся настройки------------

options = {
    "TesseractOCRpath": r"...",  # Путь до исполняемого файла tesseract.exe
    "timeStep": 5,  # Временной интервал (целое от 5 до 300)
    "examsCount": 0,  # Количество предметов (целое)
    "examsList": [],  # Список экзаменов (строк) через запятую
    "notificationEnabled": "Да",  # Наличие уведомлений
    "expectedResult": "Все"  # Ожидаемый результат
}

# ------------Программная часть------------

check_options(options)

if index(options['expectedResult']) == 0:
    search_forever(options['timeStep'], data)
elif index(options['expectedResult']) == 1:
    search_all(options['timeStep'], options['examsCount'], options['examsList'], options['notificationEnabled'], data)
else:
    search_one(options['expectedResult'], options['timeStep'], options['notificationEnabled'], data)
