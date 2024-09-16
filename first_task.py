from math import erf, sqrt, pi, exp, log
from statistics import mean

# нормальное распределение функции
def f_norm(x, mu=0, s=1):
    return (1+erf((x-mu)/sqrt(2)/s))/2

# нормальное распределение плотность
def rho_norm(x, mu=0,s=1):
    return 1/sqrt(2*pi*s)*exp(-(x-mu)**2/2/s**2)

# вероятность ошибки первого рода
def p_value(x, mu=0, s=1):
    return 2*(1-f_norm(x,mu,s)) if x >= mu else 2*f_norm(x,mu,s)

# дисперсия
def disp(x:list) -> float:
    return mean([i*i for i in x])-mean(x)**2

# стандартное отклонение
def stand_otk(x: list) -> float:
    return sqrt(disp(x))

# Размах
def razm(x: list) -> float:
    return max(x)-min(x)

# Квантиль?
def approximate_quantile(p):
    # Коэффициенты для аппроксимации
    c0, c1, c2 = 2.515517, 0.802853, 0.010328
    d1, d2, d3 = 1.432788, 0.189269, 0.001308
    
    # Вычисляем t
    t = sqrt(-2 * log(1 - p))
    
    # Вычисляем квантиль по аппроксимации
    numerator = c0 + c1 * t + c2 * t**2
    denominator = 1 + d1 * t + d2 * t**2 + d3 * t**3
    z = t - (numerator / denominator)
    
    return z

# решение
def first_task():
    print()