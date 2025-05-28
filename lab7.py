import tkinter as tk
from tkinter import scrolledtext, messagebox
import timeit
import itertools
import random

K = 5

def generate_movies(K):
    return [
        {
            "name": f"Фильм {i + 1}",
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

def show_all_programs(programs, movies_data, parent_window):
    all_programs_window = tk.Toplevel(parent_window)
    all_programs_window.title("Все возможные программы")
    all_programs_window.geometry("800x600")

    text_area = scrolledtext.ScrolledText(all_programs_window, width=100, height=35, wrap=tk.WORD)
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    text_area.insert(tk.END, f"Все возможные программы ({len(programs)} вариантов):\n\n")

    for i, program in enumerate(programs, 1):
        text_area.insert(tk.END, f"Программа #{i}:\n")
        total_duration = 0
        total_rating = 0

        for film_name in program:
            film = next(f for f in movies_data if f["name"] == film_name)
            text_area.insert(tk.END,
                             f"  • {film['name']} (Длительность: {film['duration']} мин, Рейтинг: {film['rating']})\n")
            total_duration += film['duration']
            total_rating += film['rating']

        text_area.insert(tk.END,
                         f"  Итого: Длительность = {total_duration} мин, Суммарный рейтинг = {total_rating:.1f}\n\n")

    text_area.config(state='disabled')

def run_analysis():
    try:
        N = int(entry_N.get())
        max_duration = int(entry_max_duration.get())
    except ValueError:
        messagebox.showerror("Ошибка ввода", "Пожалуйста, введите целые числа для N и максимальной длительности.")
        return
    if N > K or N <= 0:
        messagebox.showerror("Ошибка ввода", f"N должно быть от 1 до {K}.")
        return
    if max_duration <= 0:
        messagebox.showerror("Ошибка ввода", "Максимальная длительность должна быть положительным числом.")
        return

    movies_data = generate_movies(K)
    movie_names = [movie["name"] for movie in movies_data]

    # Создаем новое окно для результатов
    result_window = tk.Toplevel(root)
    result_window.title("Результаты анализа")
    result_window.geometry("800x600")

    output_textbox = scrolledtext.ScrolledText(result_window, width=90, height=30, wrap=tk.WORD)
    output_textbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Выводим информацию о фильмах
    output_textbox.insert(tk.END, "Сгенерированные фильмы:\n")
    for movie in movies_data:
        output_textbox.insert(tk.END, f"  • {movie['name']} — {movie['duration']} мин — рейтинг {movie['rating']}\n")
    output_textbox.insert(tk.END, "\n")

    start_algo = timeit.timeit()
    programs_algo = generate_programs_algo(movie_names, N, [], [])
    end_algo = timeit.timeit()
    output_textbox.insert(tk.END, f"[1] Алгоритмический способ:\n")
    output_textbox.insert(tk.END, f"    Количество программ: {len(programs_algo)}\n")
    output_textbox.insert(tk.END, f"    Время выполнения: {end_algo - start_algo:.6f} сек\n\n")

    start_lib = timeit.timeit()
    programs_lib = list(itertools.permutations(movie_names, N))
    end_lib = timeit.timeit()
    output_textbox.insert(tk.END, f"[2] Через itertools.permutations:\n")
    output_textbox.insert(tk.END, f"    Количество программ: {len(programs_lib)}\n")
    output_textbox.insert(tk.END, f"    Время выполнения: {end_lib - start_lib:.6f} сек\n\n")

    optimal_program, rating = find_optimal_program(movies_data, N, max_duration)
    output_textbox.insert(tk.END, f"[3] Оптимальная программа с ограничением по времени ({max_duration} мин):\n")
    if optimal_program:
        total_duration = sum(f["duration"] for f in optimal_program)
        for film in optimal_program:
            output_textbox.insert(tk.END, f"  • {film['name']} — {film['duration']} мин — рейтинг {film['rating']}\n")
        output_textbox.insert(tk.END, f"  Суммарный рейтинг: {rating:.1f}\n")
        output_textbox.insert(tk.END, f"  Суммарная длительность: {total_duration} мин\n")
    else:
        output_textbox.insert(tk.END, "  Нет подходящей программы в рамках ограничения.\n")

    # Добавляем кнопку для просмотра всех программ
    btn_frame = tk.Frame(result_window)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Показать все варианты программ",
              command=lambda: show_all_programs(programs_lib, movies_data, result_window)).pack(side=tk.LEFT, padx=5)

    output_textbox.config(state='disabled')


root = tk.Tk()
root.title("Лабораторная работа №7 — Анализ программ фильмов")

label_info = tk.Label(root, text="Введите количество фильмов в программе (N) и максимальную длительность (мин).")
label_info.pack(pady=10)

frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="N (число фильмов):").grid(row=0, column=0, sticky="e", padx=5, pady=5)
entry_N = tk.Entry(frame_inputs, width=10)
entry_N.grid(row=0, column=1, padx=5, pady=5)
entry_N.insert(0, "3")

tk.Label(frame_inputs, text="Макс. длительность (мин):").grid(row=1, column=0, sticky="e", padx=5, pady=5)
entry_max_duration = tk.Entry(frame_inputs, width=10)
entry_max_duration.grid(row=1, column=1, padx=5, pady=5)
entry_max_duration.insert(0, "300")

button_run = tk.Button(root, text="Выполнить анализ", command=run_analysis, padx=10, pady=5)
button_run.pack(pady=10)

root.mainloop()
