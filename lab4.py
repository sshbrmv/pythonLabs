import numpy as np
import matplotlib.pyplot as plt
def print_matrix(matrix, title="Matrix"):
    print(f"\n{title}:")
    print(matrix)

def load_matrix_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        matrix = []
        for line in lines:
            row = list(map(int, line.strip().split()))
            matrix.append(row)
        return np.array(matrix)

def create_matrix_f(A):
    F = A.copy()
    n = F.shape[0]
    half = n // 2

    #Выделение матриц
    B = F[half:, half:]
    C = F[half:, :half]
    E = F[:half, half:]

    #Подсчет нулей
    zeros_B = np.count_nonzero(B == 0)
    zeros_E = np.count_nonzero(E == 0)

    if zeros_B > zeros_E:
        #Симметричная перестановка
        original_B = B.copy()
        original_C = C.copy()
        #Отражение и замена
        F[half:, half:] = np.fliplr(original_C)
        F[half:, :half] = np.fliplr(original_B)
    else:
        #Несимметричная перестановка
        F[half:, half:], F[:half, half:] = E.copy(), B.copy()
    return F

def plot_matrices(F):
    plt.figure(figsize=(15, 5))

    plt.subplot(131)
    plt.imshow(F, cmap='coolwarm', interpolation='nearest')
    plt.colorbar()

    plt.subplot(132, projection='3d')
    x, y = np.meshgrid(range(F.shape[1]), range(F.shape[0]))
    plt.gca().plot_surface(x, y, F, cmap='viridis')

    plt.subplot(133)
    for i in range(min(5, F.shape[0])):
        plt.plot(F[i], label=f'Строка {i + 1}')
    plt.legend()

    plt.tight_layout()
    plt.show()

def main():
    K = int(input("Введите число K: "))
    N = int(input("Введите размер матрицы N (четное число): "))
    print("\nВыберите способ заполнения матрицы A:")
    print("1 - Случайное заполнение")
    print("2 - Загрузить из файла")
    print("3 - Ввести вручную")
    choice = int(input("Ваш выбор (1/2/3): "))

    if choice == 1:
        A = np.random.randint(-10, 11, size=(N, N))
    elif choice == 2:
        filename = input("Введите имя файла: ")
        A = load_matrix_from_file(filename)
    elif choice == 3:
        print(f"Введите {N}x{N} элементов матрицы построчно (через пробел):")
        A = []
        for _ in range(N):
            row = list(map(int, input().split()))
            A.append(row)
        A = np.array(A) # Преобразование в массив NumPy
    else:
        print("Ошибка: неверный выбор")
        return

    # Вывод и преобразование
    print_matrix(A, "Исходная матрица A")
    F = create_matrix_f(A)
    print_matrix(F, "Преобразованная матрица F")
    plot_matrices(F)

    det_A = np.linalg.det(A) # Определитель
    sum_diag_F = np.trace(F) # Сумма элементов главной диагонали матрицы

    if det_A > sum_diag_F:
        result = A @ A.T - K * F
        print("\nРезультат: A*A^T - K*F")
    else:
        G = np.tril(A) # Нижняя треугольная матрица
        try:
            A_inv = np.linalg.inv(A) #Обратная матрица
            F_inv = np.linalg.inv(F)
            result = (A_inv + G - F_inv) * K
            print("\nРезультат: (A⁻¹ + G - F⁻¹)*K")
        except np.linalg.LinAlgError:
            print("\nОшибка: матрица A или F вырождена, невозможно вычислить обратную матрицу")
            return
    print_matrix(result, "Итоговый результат")

if __name__ == "__main__":
    main()