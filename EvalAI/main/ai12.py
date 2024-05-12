from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from django.shortcuts import render, redirect
import re
from EvalAI import urls

from urllib3 import request


def process_images(url1, url2):
    # Настройка драйвера
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    # Списки для сохранения результатов
    results1 = []
    results2 = []

    # Обработка первого изображения
    driver.get("https://rehand.ru")
    upload = driver.find_element(By.ID, 'file')
    upload.send_keys(url1)
    driver.implicitly_wait(10)
    time.sleep(5)
    result1 = driver.find_element(By.ID, 'output').text
    results1.append(result1)
    asd = result1.split('\n')
       # Обработка второго изображения
    driver.get("https://rehand.ru")
    upload = driver.find_element(By.ID, 'file')
    upload.send_keys(url2)
    driver.implicitly_wait(20)
    time.sleep(5)
    result2 = driver.find_element(By.ID, 'output').text
    results2.append(result2)

    driver.quit()

    return results1, results2, asd

def process_images1(url):
    # Настройка драйвера
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    # Обработка изображения
    driver.get("https://rehand.ru")
    upload = driver.find_element(By.ID, 'file')
    upload.send_keys(url)
    driver.implicitly_wait(10)
    time.sleep(3)
    result = driver.find_element(By.ID, 'output').text
    print(result)
    driver.quit()

    # Разделение текста на строки
    lines = result.split('\n')

    # Использование первой строки в качестве значения ключа 'name'
    results_dict = {'name': lines[0]}

    i = 0  # начальное значение переменной i
    for line in lines[1:]:  # Начинаем с 1, так как первая строка уже использована
        i += 1
        # Если знак "-" присутствует в строке
        if '-' in line:
            # Разделяем строку на ключ и значение по знаку "-"
            key, value = line.split('-', 1)
            # Добавляем элемент в словарь, преобразуя ключ в int
            results_dict[i] = value.strip().lower()  # Увеличиваем ключ на 1
        elif ' ' in line:
            # Если в строке есть пробел, разделяем строку по пробелу
            key, value = line.split(' ', 1)
            # Добавляем элемент в словарь, преобразуя ключ в int
            results_dict[i] = value.strip().lower()  # Увеличиваем ключ на 1
        else:
            # Если в строке нет "-" и нет пробела, принимаем её за значение словаря
            # Используем переменную i в качестве ключа
            results_dict[i] = line.strip().lower()  # Увеличиваем ключ на 1

    return results_dict












