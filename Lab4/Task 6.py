import numpy as np

print("Умножение произвольных матриц А (размерности 3х5) и В (5х2)")
A = np.random.rand(3, 5)
B = np.random.rand(5, 2)

C = np.dot(A, B)
print(C, "\n")

print("Умножение матрицы (5х3) на трехмерный вектор")
A = np.random.rand(5, 3)
B = np.random.rand(3)

C = np.dot(A, B)
print(C, "\n")

print("Решение произвольной системы линейных уравнений")
A = np.array([[6, 8, 5], [44, 67, 4], [4, 6, 88]])
B = np.array([6, 15, 24])

X = np.linalg.solve(A, B)
print(X, "\n")

print("Расчет определителя матрицы")
A = np.array([[6, 8, 5], [44, 67, 4], [4, 6, 88]])

det = np.linalg.det(A)
print(det, "\n")

print("Получение обратной и транспонированной матриц")
A = np.array([[6, 8, 5], [44, 67, 4], [4, 6, 88]])

print("Обратная матрица")
inv_A = np.linalg.inv(A)
print(inv_A)

print("Транспонированная матрица")
tr_A = A.T
print(tr_A)

print("Демонстрация того факта, что определитель равен произведению собственных значений матрицы")
A = np.random.rand(5, 5)

print("Расчет определителя матрицы")
det = np.linalg.det(A)
print(det)

print("Расчет собственных значений матрицы")
eig = np.linalg.eigvals(A)
print(eig)

print("Расчет произведения собственных значений матрицы")
prod_eig = np.prod(eig)
print(prod_eig)

# Проверка равенства определителя и произведения собственных значений с точность до машинной погрешности
assert np.isclose(det, prod_eig, rtol=1e-10)