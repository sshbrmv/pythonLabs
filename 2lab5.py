import itertools
import random

# Параметры задачи
K = 5  # Количество фильмов
N = 3  # Количество фильмов в программе
MAX_DURATION = 200  # Максимальная суммарная длительность

# Генерация данных о фильмах
movies = [
    {
        "id": str(i + 1),
        "duration": random.randint(40, 90),
        "rating": round(random.uniform(5.0, 9.5), 1),
        "genre": random.choice(["боевик", "комедия", "драма", "фантастика", "триллер"])
    }
    for i in range(K)
]

# 1. Сначала отбираем фильмы, которые могут быть в программе (по длительности)
valid_movies = [m for m in movies if m["duration"] <= MAX_DURATION]

# 2. Генерация программ только из подходящих фильмов
def generate_programs(movies, N):
    programs = []
    for combo in itertools.permutations(movies, N):
        total_duration = sum(m["duration"] for m in combo)
        if total_duration <= MAX_DURATION:
            programs.append(combo)
    return programs

# 3. Поиск оптимальной программы (максимальный рейтинг)
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

# Вывод результатов
def show_results():
    print("Доступные фильмы (длительность ≤ 200 мин):")
    for movie in valid_movies:
        print(f"Фильм {movie['id']}: {movie['duration']} мин, рейтинг {movie['rating']}, жанр: {movie['genre']}")

    programs = generate_programs(valid_movies, N)
    optimal, max_rating = find_optimal_program(programs)

    print("\nОптимальная программа:")
    if optimal:
        print("Фильмы:", ", ".join(m["id"] for m in optimal))
        print("Суммарная длительность:", sum(m["duration"] for m in optimal), "мин")
        print("Суммарный рейтинг:", max_rating)
    else:
        print("Нет программ, удовлетворяющих ограничению.")

if __name__ == "__main__":
    show_results()
