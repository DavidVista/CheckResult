class TesseractError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'Некорректный полный путь к tesseract.exe!\nУстановите TesseractOCR и укажите полный путь до исполняемого файла!\n' \
                   'Вы указали следующий путь: ' + self.message
        return 'Некорректный полный путь к tesseract.exe!'


class TimerError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'Неправильный временной интервал!\nДолжно приниматься число в пределах от 5 до 300! (Вводите целое число)\nВы указали: ' + self.message
        return 'Неправильный временной интервал!'


class ExamError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            if self.message == "length":
                return 'Неправильное число предметов!\nУкажите точное количество экзаменов! (Вводите целое число)'
            elif self.message == "name":
                EXAMS = 'Русский язык\nМатематика профильная\nМатематика базовая\nФизика\nХимия\nИнформатика и ИКТ (' \
                        'КЕГЭ)\nБиология\nИстория\nГеография\nАнглийский язык\nНемецкий язык\nФранцузский ' \
                        'язык\nОбществознание\nИспанский язык\nКитайский язык\nЛитература'
                return 'Неправильное название предмета! Проверьте названия предметов! Список допустимых:\n' + EXAMS

        else:
            return 'Ошибка при указании экзаменов!'


class NotificationError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'Ошибка в учёте уведомления! Допустимые значения: Да, Нет. Вы указали: ' + self.message
        else:
            return 'Ошибка в учёте уведомления!'
