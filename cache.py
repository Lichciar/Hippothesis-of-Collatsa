#!/usr/bin/env python3

# --------------- комментарий 72 символа -------------------------------
# ----------------------- код 79 символов -------------------------------------

# Задание:
"""
Скрипт-класс, описывающий кэш.

Начало: 29 мая 2024 г. 11:26.
Обновлена: 30 мая 2024 г. 00:38."""

# Версия скрипта.
version = '0.1'

# Исправлено в ver. 0.1:
"""
1. Создан прототип класса.
2. Создана функция "add" для добавления данных в кэш.
3. Создана функция "show_all" для вывода всего кэша.
4. Создана функция "ldid" (loading data into database)
   для загрузки кэша в БД."""

# План работ на ver. 0.X:
""" """

# Подключение модулей.
import settings # Файл настройки.
import sqlite3  # Модуль работы с БД SQLite3.
from time import strftime, localtime, time, gmtime  # Модуль времени.

# Описание классов.
class Cache:
    """ Класс описывающий кэш с данными для работы главного скрипта.
    1. Как только количество элементов кэша будет равно верхнему
       предела, будет открываться БД и весь кэш будет записан в БД"""

    def __init__(self, size = settings.CACHE_SIZE_DEFAULT):
        """ Конструктор класса. Определяет объём кэша.
        1. По умолчанию глубина кэша будет состовлять 100 элементов."""

        self.size = size  # Размер кэша.
        self.index = 0    # Текущий элемент кэша
        self.data = []    # Массив с данными.

    def add(self, data):
        """ Функция добавления данных в кэш."""

        # Проверяем индекс кэша.
        if self.index == self.size:
            self.ldid()         # Весь кэш загружаем в БД.
            self.index = 0      # Обнуляем индекс текущего элемента
            self.data.clear()   # Очищаем кэш.
        # Вносим данные в кэш и увеличиваем индекс кэша на 1.
        self.data.append(data)
        self.index += 1

    def ldid(self):
        """ Функция загрузки данных из кэша в базу данных.
        Справка: ldid == loading data into database"""

        con = sqlite3.connect(settings.DB_FILENAME) # Подлкюч-ся к БД.
        cur = con.cursor() # Создаём курсор для работы с БД.

        # Сохраняем данные в базу данных.
        for loop in self.data:
            query = ('INSERT INTO Result_tables VALUES (NULL, ' +
            str(loop['natural_number']) + ', \"' +
            loop['chain_results'] + '\", ' +
            str(loop['time']) + ')')
            cur.execute(query)  # Выполняем запрос.
        # Последнее натуральное число в кэше записываем в БД.
        query = ('UPDATE CN_tables SET natural_number = ' +
            str(self.data[self.size - 1]['natural_number']) + ' WHERE id = 1')
        cur.execute(query)      # Выполняем запрос.
        con.commit()            # Применяем изменения в БД.
        con.close()             # Закрываем соединение с БД.

    def show_all(self):
        """ Функция вывода всего содержимого кэша."""

        print('Размер кэша: ' + str(self.size))
        print('Текущий индекс кэша:' + str(self.index))
        print('Содержание кэша:')
        for loop in self.data:
            print(loop)

# Тестирование класса.
if __name__ == '__main__':

    # Приветствие.
    print('Тестирование класса Cache v. ' + version)

    # Создаём экземпляр класса.
    a = Cache()
    print('Создан класс-кэш \"a\" с размером по умолчанию: ' +
        str(a.size) + ' элементов.')

    # Создаём экземпляр класса.
    b = Cache(25)
    print('Создан класс-кэш \"b\" с заданным размером: ' +
        str(b.size) + ' элементов.')

    # Добавляем данные в кэш.
    for loop in range (0, 102):
        data = { 'natural_number': loop,
                 'chain_results': '1-2-3-' + str(loop),
                 'time': 10 + loop}
        b.add(data)

    # Выводим содержимое кэша "a".
    b.show_all()
