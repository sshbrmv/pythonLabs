import tkinter as tk
from tkinter import scrolledtext, messagebox
import time
import itertools
import random

K = 5

def generate_movies(K):
    return [
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

    output_textbox.config(state='normal')
    output_textbox.delete(1.0, tk.END)

    start_algo = time.time()
    programs_algo = generate_programs_algo(movie_names, N, [], [])
    end_algo = time.time()
    output_textbox.insert(tk.END, f"[1] Алгоритмический способ:\n")
    output_textbox.insert(tk.END, f"    Кол-во программ: {len(programs_algo)}\n")
    output_textbox.insert(tk.END, f"    Время выполнения: {end_algo - start_algo:.6f} сек\n\n")

    start_lib = time.time()
    programs_lib = list(itertools.permutations(movie_names, N))
    end_lib = time.time()
    output_textbox.insert(tk.END, f"[2] Через itertools.permutations:\n")
    output_textbox.insert(tk.END, f"    Кол-во программ: {len(programs_lib)}\n")
    output_textbox.insert(tk.END, f"    Время выполнения: {end_lib - start_lib:.6f} сек\n\n")

    optimal_program, rating = find_optimal_program(movies_data, N, max_duration)
    output_textbox.insert(tk.END, f"[3] Оптимальная программа с ограничением по времени ({max_duration} мин):\n")
    if optimal_program:
        total_duration = sum(f["duration"] for f in optimal_program)
        for film in optimal_program:
            output_textbox.insert(tk.END, f"  {film['name']} — {film['duration']} мин — рейтинг {film['rating']}\n")
        output_textbox.insert(tk.END, f"  Суммарный рейтинг: {rating}\n")
        output_textbox.insert(tk.END, f"  Суммарная длительность: {total_duration} мин\n")
    else:
        output_textbox.insert(tk.END, "  Нет подходящей программы в рамках ограничения.\n")

    output_textbox.config(state='disabled')

root = tk.Tk()
root.title("Лабораторная работа №7 — Анализ программ фильмов")

label_info = tk.Label(root, text="Введите количество фильмов в программе (N) и максимальную длительность (мин).")
label_info.pack(pady=5)

frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=5)

tk.Label(frame_inputs, text="N (число фильмов):").grid(row=0, column=0, sticky="e")
entry_N = tk.Entry(frame_inputs, width=10)
entry_N.grid(row=0, column=1)
entry_N.insert(0, "3")

tk.Label(frame_inputs, text="Макс. длительность (мин):").grid(row=1, column=0, sticky="e")
entry_max_duration = tk.Entry(frame_inputs, width=10)
entry_max_duration.grid(row=1, column=1)
entry_max_duration.insert(0, "300")

button_run = tk.Button(root, text="Выполнить анализ", command=run_analysis)
button_run.pack(pady=5)

output_textbox = scrolledtext.ScrolledText(root, width=70, height=20, state='disabled')
output_textbox.pack(pady=5)

root.mainloop()
