Задана рекуррентная функция. Область определения функции – натуральные числа. Написать программу сравнительного вычисления данной функции рекурсивно и итерационно. Определить границы применимости рекурсивного и итерационного подхода. Результаты сравнительного исследования времени вычисления представить в табличной и графической форме в виде отчета по лабораторной работе.
Варианты:
F(1) = 2; G(1) = 1; F(n) = (-1)n*( (n–1)! – G(n–1)), G(n) = F(n–1) + G(n–1), при n >=2

import numpy as np
import timeit
import matplotlib.pyplot as plt
import math

def F_rec(n):
    if n < 1:
        raise ValueError("n должно быть положительным целым числом")
    if n == 1:
        return 2
    return -1 * ((math.factorial(n - 1) - G_rec(n - 1)))

def G_rec(n):
    if n < 1:
        raise ValueError("n должно быть положительным целым числом")
    if n == 1:
        return 1
    return F_rec(n - 1) + G_rec(n - 1)

def iterative_calc(n):
    if n < 1:
        raise ValueError("n должно быть положительным целым числом")
    if n == 1:
        return 2, 1
    F_prev, G_prev = 2, 1
    sign = -1  
    fact = 1    
    for i in range(2, n + 1):
        sign *= -1
        fact *= (i - 1) 
        F_current = sign * (fact - G_prev)
        G_current = F_prev
        F_prev, G_prev = F_current, G_current
    return F_prev, G_prev
    
def time_func(func, repeats=1):
    return timeit.timeit(func, number=repeats)
def main():
    ns = np.arange(1, 21)
    times_F_rec, times_G_rec = [], []
    times_F_it, times_G_it = [], []
    values_F_rec, values_G_rec = [], []
    values_F_it, values_G_it = [], []
    for n in ns:
        try:
            # Измерение времени и получение значений для рекурсивных функций
            F_val = F_rec(n)
            values_F_rec.append(F_val)
            times_F_rec.append(time_func(lambda: F_rec(n)))
        except (RecursionError, OverflowError):
            values_F_rec.append(np.nan)
            times_F_rec.append(np.nan)
        try:
            G_val = G_rec(n)
            values_G_rec.append(G_val)
            times_G_rec.append(time_func(lambda: G_rec(n)))
        except (RecursionError, OverflowError):
            values_G_rec.append(np.nan)
            times_G_rec.append(np.nan)
        # Итеративный метод
        F_it, G_it = iterative_calc(n)
        values_F_it.append(F_it)
        values_G_it.append(G_it)
        times_F_it.append(time_func(lambda: iterative_calc(n)[0]))
        times_G_it.append(time_func(lambda: iterative_calc(n)[1]))
    # Вывод таблицы времени выполнения
    print("\n n |   F_rec (s) |   G_rec (s) |  F_iter (s) |  G_iter (s)")
    for i, n in enumerate(ns):
        print(
            f"{n:2d} | {times_F_rec[i]:10.6f} | {times_G_rec[i]:10.6f} | {times_F_it[i]:10.6f} | {times_G_it[i]:10.6f}")
    # Построение графиков
    valid_idxs = [i for i, x in enumerate(times_F_rec) if not np.isnan(x)]
    ns_valid = ns[valid_idxs]
    f_rec_valid = [times_F_rec[i] for i in valid_idxs]
    g_rec_valid = [times_G_rec[i] for i in valid_idxs]
    plt.figure(figsize=(12, 6))
    plt.plot(ns_valid, f_rec_valid, 'r--', label='F recursive')
    plt.plot(ns_valid, g_rec_valid, 'b--', label='G recursive')
    plt.plot(ns, times_F_it, 'r-', label='F iterative')
    plt.plot(ns, times_G_it, 'b-', label='G iterative')
    plt.xlabel('n')
    plt.ylabel('Time (s)')
    plt.title('Время выполнения функций F и G')
    plt.legend()
    plt.grid(True)
    plt.yscale('log')
    plt.show()
if __name__ == "__main__":
    main()
