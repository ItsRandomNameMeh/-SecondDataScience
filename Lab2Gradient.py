import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import random
import SecondLab
import sqlite3

conn = sqlite3.connect('FirstLab.db')
cursor = conn.cursor()
# Объединенный запрос для получения информации о фильмах и языках
cursor.execute("SELECT film.rating, language.name, film.rental_duration,"
                                  "film.replacement_cost "
               f"FROM film JOIN language ON film.language_id = "
               "language.language_id")
rating_counter = []
language_counter = []
rental_counter = []

for row in cursor.fetchall():
        rating, language, rental_duration, notuse = row  # явно указываем существующие
        # поля таблицы как имена переменных, python это понимает
        rating_counter.append(rating)
        language_counter.append(language)
        rental_counter.append(rental_duration)

def makeRating():
    revers = {'G':0,'PG': 5, 'PG-13':13,'NC-17':18,'R':17}
    for i in range(len(rating_counter)):
        rating_counter[i] = revers[rating_counter[i]]


def makeLangugage():
        for i in range(len(language_counter)):
            language_counter[i] = random.randint(1,5)


makeLangugage()
makeRating()


print(len(rating_counter),len(language_counter),len(rental_counter),len(list(SecondLab.replacment_dict.values())))

df = pd.DataFrame({
    'целевой_признак\nвозвраты за фильм': SecondLab.replacment_dict.values(),
    'Возрастне рейтинги': rating_counter,
    'Язык фильма': language_counter,
    'Длина сезона проката фильма': rental_counter
})

# Вычисляем корреляционную матрицу
correlation_matrix = df.corr()

# Строим тепловую карту
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Корреляционная матрица')
plt.show()