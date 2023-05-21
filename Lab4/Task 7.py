#Пример функции:
#f(x) = \frac{x^2}{2} - \cos(x)
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

x = sp.Symbol('x')
f = (x**2)/2 - sp.cos(x) # функция
df = sp.diff(f, x) # производная
If = sp.integrate(f, x) # интеграл

x_range = np.linspace(-10, 10, 1000)

func = sp.lambdify(x, f, 'numpy')
dfunc = sp.lambdify(x, df, 'numpy')

plt.plot(x_range, func(x_range), label='f(x)')
plt.plot(x_range, dfunc(x_range), label='f\'(x)')
plt.legend()
plt.show()

#Пример решения нелинейного уравнения:
#x^3 - 2x - 5 = 0

x = sp.Symbol('x')
equation = x**3 - 2*x -5
result = sp.nsolve(equation, x, 1)
print(result)

#Пример решения системы нелинейных уравнений:
#x^2 + y^2 = 2 \\ x + y = 1

x, y = sp.symbols('x y')
equations = [x**2 + y**2 - 2, x + y - 1]
result = sp.nsolve(equations, (x, y), (-1, 1))
print(result)