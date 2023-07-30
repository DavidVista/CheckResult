from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from urllib.request import urlretrieve
from PIL import Image, ImageFilter
import numpy as np
from plyer import notification


import os
import time

import pytesseract as pts

from classes import *

EXAMS = [
    "Русский язык",
    "Математика профильная",
    "Математика базовая",
    "Физика",
    "Химия",
    "Информатика и ИКТ (КЕГЭ)",
    "Биология",
    "История",
    "География",
    "Английский язык",
    "Немецкий язык",
    "Французский язык",
    "Обществознание",
    "Испанский язык",
    "Китайский язык",
    "Литература",
]

headers = ["Дата экзамена", "Предмет", "Тестовый балл", "Минимальный балл", "Статус экзамена", "Апелляция"]


def search_forever(timeStep, data):
    while True:
        driver = init_driver()
        lookup(driver, data)
        subjects = []
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'table-container')))
        except TimeoutException:
            driver.quit()
            continue
        div = driver.find_element(By.ID, "table-container")
        soup = BeautifulSoup(div.get_attribute("innerHTML"), 'html.parser')
        table = soup.find("table")
        print(date())
        for row in table.findAll("tr"):
            subject = [''] * 6
            i = 0
            for elem in row.findAll("td"):
                subject[i] = elem.text.strip() if elem.text.strip() else '-'
                i += 1
            if subject[0]:
                subjects.append(subject)
        show_results(subjects)
        print("___________________Ожидание___________________")
        driver.quit()
        time.sleep(timeStep * 60)


def search_all(timeStep, examsCount, examsList, nE, data):
    while True:
        k = 0
        verdict = ''
        driver = init_driver()
        lookup(driver, data)
        subjects = []
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'table-container')))
        except TimeoutException:
            driver.quit()
            continue
        div = driver.find_element(By.ID, "table-container")
        soup = BeautifulSoup(div.get_attribute("innerHTML"), 'html.parser')
        table = soup.find("table")
        print(date())
        for row in table.findAll("tr"):
            subject = [''] * 6
            i = 0
            for elem in row.findAll("td"):
                subject[i] = elem.text.strip() if elem.text.strip() else '-'
                i += 1
                if elem.text.strip() in examsList:
                    k += 1
                    if k == examsCount:
                        verdict = f"Результаты по предметам {examsList} пришли!"
            if subject[0]:
                subjects.append(subject)
        show_results(subjects)
        if verdict:
            if nE:
                notify(verdict)
            print(verdict)
            break
        print("___________________Ожидание___________________")
        driver.quit()
        time.sleep(timeStep * 60)


def search_one(name, timeStep, nE, data):
    while True:
        verdict = ''
        subjects = []
        driver = init_driver()
        lookup(driver, data)
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'table-container')))
        except TimeoutException:
            driver.quit()
            continue
        div = driver.find_element(By.ID, "table-container")
        soup = BeautifulSoup(div.get_attribute("innerHTML"), 'html.parser')
        table = soup.find("table")
        print(date())
        for row in table.findAll("tr"):
            subject = [''] * 6
            i = 0
            for elem in row.findAll("td"):
                subject[i] = elem.text.strip() if elem.text.strip() else '-'
                i += 1
                if elem.text.strip() == name:
                    verdict = name
            if subject[0]:
                subjects.append(subject)
        show_results(subjects)
        if verdict:
            for subj in subjects:
                if subj[1] == name:
                    verdict = f'Результат по предмету {name} cоставляет {subj[2]}!'
            print(verdict)
            if nE:
                notify(verdict)
            break
        print("___________________Ожидание___________________")
        driver.quit()
        time.sleep(timeStep * 60)


def notify(message):
    notification.notify(
        title="Результаты ЕГЭ",
        message=message,
        timeout=10
    )


def show_results(array):
    for subject in array:
        print(f"________________{subject[1]}________________")
        for i in range(6):
            print(f"{headers[i]}: {subject[i]}")


def index(name):
    if name == "Нет":
        return 0
    if name == "Все":
        return 1
    return 2


def date():
    t = datetime.now()
    return f'{t.day}/{t.month}/{t.year} {t.hour}:{t.minute}'


def check_options(opt):
    if os.path.isfile(opt['TesseractOCRpath']):
        pts.pytesseract.tesseract_cmd = opt['TesseractOCRpath']
    else:
        raise TesseractError(opt['TesseractOCRpath'])
    if not (isinstance(opt['timeStep'], int) and 5 <= opt['timeStep'] <= 300):
        raise TimerError(str(opt['timeStep']))
    if not (isinstance(opt['examsCount'], int) and opt['examsCount'] == len(opt['examsList'])):
        raise ExamError("length")
    for exam in opt['examsList']:
        if exam not in EXAMS:
            raise ExamError("name")
    if not (opt['notificationEnabled'] in ("Да", "Нет")):
        raise NotificationError(opt['notificationEnabled'])
    if opt['expectedResult'] not in ("Нет", "Все"):
        if opt['expectedResult'] not in EXAMS:
            raise ExamError("name")
    print("Успешный запуск!")


def filter_image():
    fmg = Image.open("images/image.jpg")
    for i in range(8):
        fmg = fmg.filter(ImageFilter.DETAIL)
        fmg = fmg.filter(ImageFilter.SMOOTH)

    fmg = fmg.filter(ImageFilter.UnsharpMask(500, 70, 3))
    fmg = fmg.filter(ImageFilter.EDGE_ENHANCE_MORE)
    fmg.save("images/image.jpg")


def CleanImage(FilePath, valid_value):
    image = Image.open(FilePath)
    image = image.point(lambda x: 255 if x > valid_value else 0)
    return image


def confidence(image):
    data = pts.image_to_data(image, output_type=pts.Output.DICT)
    text = data["text"]
    conf = []
    numChar = []
    for i in range(len(text)):
        if data['conf'][i] > -1:
            conf.append(data['conf'][i])
            numChar.append(len(text[i]))
    if numChar in [[0], []]:
        return None
    return np.average(conf, weights=numChar), sum(numChar)


def approx():
    filter_image()
    data = []
    for valid_value in range(0, 256, 1):
        imgNew = CleanImage("images/image.jpg", valid_value)
        scores = confidence(imgNew)
        if scores:
            data.append([valid_value] + list(scores))
    maximum = max(filter(lambda x: x[2] == 6, data), key=lambda x: (x[1], x[2], x[0]))
    return CleanImage("images/image.jpg", maximum[0])


def translate():
    image = approx()
    image.save("images/new_image.jpg")
    return pts.image_to_string(image, config='outputbase digits')[:6]


def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    return webdriver.Chrome(service=Service(), options=chrome_options)


def lookup(driver, data):
    url = "https://checkege.rustest.ru/"
    driver.get(url)
    box = driver.find_element(By.ID, "captcha-img")
    img_link = box.get_attribute("style")[17:-1]
    path = os.path.abspath("images")
    urlretrieve(img_link, path+"\image.jpg")
    time.sleep(1)

    for key, value in data.items():
        if key != 'region':
            driver.find_element(By.ID, key).send_keys(value)

    driver.find_element(By.ID, "region_chosen").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/div/div/div[1]/form/div[10]/div/div/div/input").send_keys(data['region'])
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, "active-result").click()

    numbers = translate()
    driver.find_element(By.ID, "captcha").send_keys(numbers)

    btn = driver.find_element(By.XPATH, "/html/body/div/div/div[1]/form/button")
    btn.click()
