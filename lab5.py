import time
import itertools
import random

K = 5
N = 3
MAX_DURATION = 300

movies_data = [
    {
        "name": f"Фильм {i+1}",
        "duration": random.randint(60, 150),
        "rating": round(random.uniform(5.0, 9.5), 1)
    }
    for i in range(K)
]

def generate_programs_algo(movies, N, current=[], all_programs=[]):
    if len(current) == N:
        all_programs.append(current.copy())
        return
    for i in range(len(movies)):
        if movies[i] not in current:
            current.append(movies[i])
            generate_programs_algo(movies, N, current, all_programs)
            current.pop()
    return all_programs

movie_names = [movie["name"] for movie in movies_data]

start_algo = time.time()
programs_algo = generate_programs_algo(movie_names, N, [], [])
end_algo = time.time()
print(f"[1] Алгоритмический способ:")
print(f"    Кол-во программ: {len(programs_algo)}")
print(f"    Время выполнения: {end_algo - start_algo:.6f} сек")

start_lib = time.time()
programs_lib = list(itertools.permutations(movie_names, N))
end_lib = time.time()
print(f"[2] Через itertools.permutations:")
print(f"    Кол-во программ: {len(programs_lib)}")
print(f"    Время выполнения: {end_lib - start_lib:.6f} сек")

def find_optimal_program(movies_data, N, max_duration):
    best_program = None
    best_rating = 0
    for combo in itertools.permutations(movies_data, N):
        total_duration = sum(f["duration"] for f in combo)
        if total_duration <= max_duration:
            total_rating = sum(f["rating"] for f in combo)
            if total_rating > best_rating:
                best_rating = total_rating
                best_program = combo
    return best_program, best_rating

optimal_program, rating = find_optimal_program(movies_data, N, MAX_DURATION)

print("\n[3] Оптимальная программа с ограничением по времени:")
if optimal_program:
    total_duration = sum(f["duration"] for f in optimal_program)
    for film in optimal_program:
        print(f"  {film['name']} — {film['duration']} мин — рейтинг {film['rating']}")
    print(f"  Суммарный рейтинг: {rating}")
    print(f"  Суммарная длительность: {total_duration} мин")
else:
    print("  Нет подходящей программы в рамках ограничения.")
