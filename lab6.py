import numpy as np
import timeit
import matplotlib.pyplot as plt
import math

def F_rec(n):
    if n < 1:
        raise ValueError("n должно быть положительным целым числом")
    if n == 1:
        return 1
    sign = 1 if n % 2 else -1
    val = 2 * F_rec(n - 1) - G_rec(n - 1)
    return sign * val

def G_rec(n):
    if n < 1:
        raise ValueError("n должно быть положительным целым числом")
    if n == 1:
        return 1
    sign = 1 if n % 2 else -1
    val = F_rec(n - 1) / math.factorial(2 * n) + 2 * G_rec(n - 1)
    return sign * val

def iterative_calc(n):
    if n < 1:
        raise ValueError("n должно быть положительным целым числом")
    if n == 1:
        return 1.0, 1.0
    F_val, G_val = 1.0, 1.0
    sign = -1
    for i in range(2, n + 1):
        F_val_new = sign * (2 * F_val - G_val)
        G_val_new = sign * (F_val / math.factorial(2 * i) + 2 * G_val)
        F_val, G_val = F_val_new, G_val_new
        sign = -sign
    return F_val, G_val

def time_func(func, repeats=1):
    return timeit.timeit(func, number=repeats)

def main():
    ns = np.arange(1, 21)
    times_F_rec, times_G_rec = [], []
    times_F_it, times_G_it = [], []

    for n in ns:
        try:
            times_F_rec.append(time_func(lambda: F_rec(n)))
        except (RecursionError, OverflowError):
            times_F_rec.append(np.nan)
        try:
            times_G_rec.append(time_func(lambda: G_rec(n)))
        except (RecursionError, OverflowError):
            times_G_rec.append(np.nan)
        times_F_it.append(time_func(lambda: iterative_calc(n)[0]))
        times_G_it.append(time_func(lambda: iterative_calc(n)[1]))

    print("\n n |   F_rec    |   G_rec    |  F_iter    |  G_iter")
    for i, n in enumerate(ns):
        print(f"{n:2d} | {times_F_rec[i]:10.6f} | {times_G_rec[i]:10.6f} | {times_F_it[i]:10.6f} | {times_G_it[i]:10.6f}")

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
