import itertools
import timeit

# Параметры задачи
K = 5  # Количество фильмов
N = 3  # Количество фильмов в программе

# Генерация данных о фильмах
movies = [f"{i + 1}" for i in range(K)]


# 1. Алгоритмический способ (рекурсивный)
def generate_programs_recursive(movies, N, current=[], result=[]):
    if len(current) == N:
        result.append(current.copy())
        return
    for movie in movies:
        if movie not in current:
            current.append(movie)
            generate_programs_recursive(movies, N, current, result)
            current.pop()
    return result


# 2. Использование itertools
def generate_with_itertools(movies, N):
    return list(itertools.permutations(movies, N))


# Сравнение и вывод всех вариантов
def compare_and_show_all():
    print(f"Все возможные программы просмотра из {N} фильмов из {K} доступных:\n")

    # Генерация вариантов
    programs_recursive = generate_programs_recursive(movies, N, [], [])
    programs_itertools = generate_with_itertools(movies, N)

    # Проверка корректности
    assert len(programs_recursive) == len(programs_itertools)
    assert set(tuple(p) for p in programs_recursive) == set(programs_itertools)

    # Вывод всех вариантов с нумерацией
    print("Список всех возможных программ:")
    for i, program in enumerate(programs_recursive, 1):
        print(f"{i:2d}. {','.join(program)}")

    # Сравнение времени выполнения
    print("\nСравнение методов генерации:")
    recursive_time = timeit.timeit(lambda: generate_programs_recursive(movies, N, [], []), number=100)
    itertools_time = timeit.timeit(lambda: generate_with_itertools(movies, N), number=100)

    print(f"Алгоритмический способ: {recursive_time:.6f} сек (100 запусков)")
    print(f"Способ с itertools: {itertools_time:.6f} сек (100 запусков)")
    print(f"Разница: {abs(recursive_time - itertools_time):.6f} сек")


if __name__ == "__main__":
    compare_and_show_all()
