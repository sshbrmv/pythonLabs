import itertools
import timeit
import random

# Параметры задачи
K = 5  # Количество фильмов
N = 3  # Количество фильмов в программе
MAX_DURATION = 200  # Максимальная суммарная длительность программы (в минутах)

# Генерация данных о фильмах с дополнительными характеристиками
movies = [
    {
        "id": str(i + 1),
        "duration": random.randint(40, 90),  # Длительность фильма (40-90 минут)
        "rating": round(random.uniform(5.0, 9.5), 1),  # Рейтинг фильма (5.0-9.5)
        "genre": random.choice(["боевик", "комедия", "драма", "фантастика", "триллер"])
    }
    for i in range(K)
]


# 1. Алгоритмический способ с ограничениями
def generate_programs_recursive(movies, N, current=[], result=[], current_duration=0):
    if len(current) == N:
        result.append(current.copy())
        return
    for movie in movies:
        if (movie["id"] not in [m["id"] for m in current] and
                current_duration + movie["duration"] <= MAX_DURATION):
            current.append(movie)
            generate_programs_recursive(
                movies, N, current, result, current_duration + movie["duration"]
            )
            current.pop()
    return result


# 2. Использование itertools с ограничениями
def generate_with_itertools(movies, N):
    all_combinations = itertools.permutations(movies, N)
    valid_combinations = [
        combo for combo in all_combinations
        if sum(m["duration"] for m in combo) <= MAX_DURATION
    ]
    return valid_combinations


# Целевая функция для оптимизации (максимизация суммарного рейтинга)
def find_optimal_program(programs):
    if not programs:
        return None, 0
    max_rating = -1
    optimal = None
    for program in programs:
        total_rating = sum(m["rating"] for m in program)
        if total_rating > max_rating:
            max_rating = total_rating
            optimal = program
    return optimal, max_rating


# Сравнение и вывод результатов
def compare_and_show_optimal():
    print(f"Все возможные программы из {N} фильмов с ограничением по длительности ({MAX_DURATION} мин):\n")

    # Генерация вариантов
    programs_recursive = generate_programs_recursive(movies, N, [], [], 0)
    programs_itertools = generate_with_itertools(movies, N)

    # Проверка корректности
    assert len(programs_recursive) == len(programs_itertools)

    # Нахождение оптимальной программы
    optimal_recursive, max_rating_recursive = find_optimal_program(programs_recursive)
    optimal_itertools, max_rating_itertools = find_optimal_program(programs_itertools)

    # Вывод информации о фильмах
    print("Доступные фильмы:")
    for movie in movies:
        print(f"Фильм {movie['id']}: {movie['duration']} мин, рейтинг {movie['rating']}, жанр: {movie['genre']}")

    # Вывод оптимальной программы
    print("\nОптимальная программа (максимальный суммарный рейтинг):")
    if optimal_recursive:
        print("Фильмы:", ", ".join(m["id"] for m in optimal_recursive))
        print("Суммарная длительность:", sum(m["duration"] for m in optimal_recursive), "мин")
        print("Суммарный рейтинг:", max_rating_recursive)
        print("Состав:")
        for m in optimal_recursive:
            print(f" - Фильм {m['id']}: {m['duration']} мин, рейтинг {m['rating']}, жанр: {m['genre']}")
    else:
        print("Нет подходящих программ в рамках ограничений")

    # Сравнение времени выполнения
    print("\nСравнение методов генерации:")
    recursive_time = timeit.timeit(lambda: generate_programs_recursive(movies, N, [], [], 0), number=10)
    itertools_time = timeit.timeit(lambda: generate_with_itertools(movies, N), number=10)

    print(f"Алгоритмический способ: {recursive_time:.6f} сек (10 запусков)")
    print(f"Способ с itertools: {itertools_time:.6f} сек (10 запусков)")
    print(f"Разница: {abs(recursive_time - itertools_time):.6f} сек")
    print(f"Всего допустимых программ: {len(programs_recursive)}")


if __name__ == "__main__":
    compare_and_show_optimal()
