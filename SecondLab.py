import sqlite3, math

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from statistics import mode

# df = sns.load_dataset('mpg')
# Словари для подсчета
rating_counter = {}#числовой - количество ограничений каждого из имеющихся (возрастных)
language_counter = {}#числовой - количество фильмов на каждом языке
rental_counter = {}#числовой - длина сезона проката (сколько каких сезонов было)
replacment_dict = {}#категориальный - количество денег на возвраты билетов каждого фильма
rating_duration = {}#ищем связь для рейтинга и месяцев аренды
rating_replace = {}#ищем связь для рейтинга и сумм возвратов

def threeTable(tableName):
    global rating_counter,language_counter,rental_counter, replacment_dict
    conn = sqlite3.connect('FirstLab.db')
    cursor = conn.cursor()
    # Объединенный запрос для получения информации о фильмах и языках
    cursor.execute("SELECT film.title, film.rating, language.name, film.rental_duration,"
                   "film.replacement_cost "
                   f"FROM {tableName} JOIN language ON film.language_id = "
                   "language.language_id")
    # Обработка результатов
    for row in cursor.fetchall():
        title, rating, language, rental_duration, replacement_cost = row  # явно указываем существующие
        # поля таблицы как имена переменных, python это понимает
        rating_counter[rating] = rating_counter.get(rating, 0) + 1
        language_counter[language] = language_counter.get(language, 0) + 1
        rental_counter[rental_duration] = rental_counter.get(rental_duration, 0) + 1
        replacment_dict[title] = replacment_dict.get(title,replacement_cost)
        rating_duration[rating] = rating_duration.get(rating,rental_duration)+1
        rating_replace[rating] = rating_replace.get(rating, 0) + replacement_cost

    # Вывод результатов
    print("Количество фильмов по рейтингам:")
    for rating, count in rating_counter.items():
        print(f"{rating}: {count}")

    print("\nКоличество фильмов по языкам:")
    for language, count in language_counter.items():
        print(f"{language}: {count}")

    print("\nКоличество фильмов по количеству месяцев аренды:")
    for duration, count in rental_counter.items():
        print(f"{duration} month: {count}")

    print("\nФильмы и суммы на возвраты билетов за них:")
    for title, count in replacment_dict.items():
        print(f"За {title} вернули: {count}")

    print("\nРейтинг и на сколько месяцев в сумме такие брали:")
    for title, count in rating_duration.items():
        print(f"Рейтинг {title} брали на: {count} месяцев")

    print("\nРейтинг и на сколько в сумме вовзратов его было:")
    for rating, sumi in rating_replace.items():
        print(f"Рейтинг {rating} навозвращали на: {round(sumi,2)} долларов")

    conn.close()

def readTable(tableName):
    conn = sqlite3.connect('FirstLab.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {tableName};")
    payment_rows = cursor.fetchall()
    cursor.execute("PRAGMA table_info(film)")
    payment_columns_info = cursor.fetchall()
    payment_columns = [info[1] for info in payment_columns_info]
    print(payment_columns)
    # for row in payment_rows:
    #     print(row)
    conn.close()

def shareOfPaces():
    # replacment_dict['Test'] = None #Проверка, что пустые значения прога видит
    paceCounter = len([value for key, value in rating_counter.items() if value is None])
    paceCounter += len([value for key, value in language_counter.items() if value is None])
    paceCounter += len([value for key, value in rental_counter.items() if value is None])
    paceCounter += len([value for key, value in replacment_dict.items() if value is None])
    print(f"В полученных данных (суммарно) {paceCounter} пропусков")

def maxAndmin():
    global rating_counter, replacment_dict, rental_counter
    ratingMassi = list(rating_counter.values())
    replaceMassi = list(replacment_dict.values())
    rentMassi = list(rental_counter.values())
    print(f"У списка рейтинга фильмов максимум - {find_key_by_value(rating_counter,max(ratingMassi))} "
          f"и минимум - {find_key_by_value(rating_counter,min(ratingMassi))}")
    print(f"У списка возвратов максимум - {find_key_by_value(replacment_dict,max(replaceMassi))}"
          f" и минимум - {find_key_by_value(replacment_dict,min(replaceMassi))}")
    print(f"У списка временных периодов аренды максимум - {find_key_by_value(rental_counter,max(rentMassi))} месяц"
          f" и минимум - {find_key_by_value(rental_counter,min(rentMassi))} месяц")

def uniq():
    global replacment_dict
    print(f"Количество уникальный фильмов из списка возвратов: "
          f"{len(set(replacment_dict.keys()))}")

def midd():
    global rating_counter,language_counter,rental_counter
    sumi = sum(rating_counter.values())
    print(f"Среднее значение фильмов каждого рейтинга: {sumi/len(rating_counter)}")
    sumi = sum(language_counter.values())
    print(f"Среднее значение фильмов на каждом из "
          f"имеющихся языков: {sumi/len(language_counter)}")
    sumi = sum(replacment_dict.values())
    print(f"Среднея сумма возвратов за фильм: {sumi/len(replacment_dict)}")

def find_key_by_value(dict_, value):
    """Метод используемый для поиска ключа,
    когда у нас уже есть значения этого ключа из
    словаря. Нужно в методе поиска медианы (иногда нам
    нужен клбч, помимо значения)"""
    for key, val in dict_.items():
        if val == value:
            return key
    return None
def median():
    global rating_counter,replacment_dict,rental_counter
    sortedRating = sorted(rating_counter.values())
    sortedRental = sorted(rental_counter.values())
    sortedReplacement = sorted(replacment_dict.values())
    print(f"Медиана для возрастных рейтингов: {find_key_by_value(rating_counter,sortedRating[len(sortedRating)//2])},\n"
          f"Медиана для временных периодов аренды фильмов: {find_key_by_value(rental_counter,sortedRental[len(sortedRental)//2])} месяцев,\n"
          f"Медиана для сумм возвращенных билетов: {sortedReplacement[len(sortedReplacement)//2]} долларов")


def dispers():
    global rating_counter, replacment_dict, rental_counter
    ratingMassi = list(rating_counter.values())
    print(f"Дисперсия рейтингов: {round(np.var(ratingMassi),3)}")

    replaceMassi = list(replacment_dict.values())
    print(f"Дисперсия суммы возвратов: {round(np.var(replaceMassi),3)}")

    rentMassi = list(rental_counter.values())
    print(f"Дисперсия месяцев аренды: {round(np.var(rentMassi),3)} ")


def qwant():
    global rating_counter,replacment_dict,rental_counter
    sumi = sum(rating_counter.values()) #в данном случаи это количество всех значений
    sumi1 = sumi//10
    generalSum = 0
    for key1, val1 in rating_counter.items():
        generalSum += val1
        if sumi1 > generalSum:
            continue
        else:
            print(f"Квантиль рейтингов 0.1: {key1};")
            generalSum = 0
            break
    sumi9 = 9*sumi//10
    for key9, val9 in rating_counter.items():
        generalSum += val9
        if sumi9 > generalSum:
            continue
        else:
            print( f"Квантиль рейтингов 0.9: {key9}.")
            break

    sumi = sum(rental_counter.values()) #в данном случаи это количество всех значений
    sumi1 = sumi//10
    generalSum = 0
    for key1, val1 in rental_counter.items():
        generalSum += val1
        if sumi1 > generalSum:
            continue
        else:
            print(f"Квантиль месяцев аренды 0.1: {key1} month;")
            generalSum = 0
            break
    sumi9 = 9*sumi//10
    for key9, val9 in rental_counter.items():
        generalSum += val9
        if sumi9 > generalSum:
            continue
        else:
            print( f"Квантиль месяцев аренды 0.9: {key9} month.")
            break

    sumi = len(replacment_dict)
    sumi1 = sumi//10
    generalSum = 0
    for key1, val1 in replacment_dict.items():
        generalSum += 1
        if sumi1 == generalSum:
            print(f"Квантиль суммы возвратов 0.1: {key1,val1};")
            generalSum = 0
            break
    sumi9 = 9*sumi//10
    for key9, val9 in replacment_dict.items():
        generalSum += 1
        if sumi9 == generalSum:
            print(f"Квантиль суммы возвратов 0.9: {key9,val9};")
            break
def qwart():
    global rating_counter, replacment_dict, rental_counter
    ratingMassi = list(rating_counter.values())
    print(f"Квартиль 1 рейтингов: {find_key_by_value(rating_counter,np.percentile(ratingMassi,25))}")
    print(f"Квартиль 3 рейтингов: {find_key_by_value(rating_counter,np.percentile(ratingMassi,75))}")

    replaceMassi = list(replacment_dict.values())
    print(f"Квартиль 1 суммы возвратов: {find_key_by_value(replacment_dict,np.percentile(replaceMassi,25))}")
    print(f"Квартиль 3 суммы возвратов: {find_key_by_value(replacment_dict,np.percentile(replaceMassi,75))}")

    rentMassi = list(rental_counter.values())
    print(f"Квартиль 1 месяцев аренды: {find_key_by_value(rental_counter,np.percentile(rentMassi,25))} месяц")
    print(f"Квартиль 3 месяцев аренды: {find_key_by_value(rental_counter,np.percentile(rentMassi,75))} месяц")


def fashion():
    global replacment_dict
    print(f"Мода для суммы возвратов по фильмам: "
          f"{mode(list(replacment_dict.values()))} самая часто встречающаяся сумма")


def lastTask():
    global rating_counter, language_counter, rental_counter, replacment_dict
    conn = sqlite3.connect('FirstLab.db')
    cursor = conn.cursor()
    # Объединенный запрос для получения информации о фильмах и языках
    cursor.execute("SELECT film.title, film.rating, film.rental_duration,"
                   "film.replacement_cost "
                   f"FROM film JOIN language ON film.language_id = "
                   "language.language_id")
    # Обработка результатов
    for row in cursor.fetchall():
        title, rating, rental_duration, replacement_cost = row  # явно указываем существующие
        # поля таблицы как имена переменных, python это понимает
        print(f"{title}, {rating}, {rental_duration}, {replacement_cost}")

    conn.close()

# threeTable("film")
# readTable("film")
# maxAndmin()
# shareOfPaces()
# midd()
# median()
# qwant()
# qwart()
# dispers()
# maxAndmin()
# uniq()
# fashion()
# lastTask()