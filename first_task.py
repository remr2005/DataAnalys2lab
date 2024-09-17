from math import erf, sqrt, pi, exp, log
from statistics import mean
from random import randint

# нормальное распределение функции
def f_norm(x, mu=0, s=1):
    return (1+erf((x-mu)/sqrt(2)/s))/2

# нормальное распределение плотность
def rho_norm(x, mu=0,s=1):
    return 1/sqrt(2*pi*s)*exp(-(x-mu)**2/2/s**2)

# вероятность ошибки первого рода
def p_value(x, mu=0, s=1):
    return 2*(1-f_norm(x,mu,s)) if x >= mu else 2*f_norm(x,mu,s)

def p_value_z_test(z):
    return 2 * (1 - normal_cdf(abs(z)))

# Кумулятивная функция распределения нормального распределения (CDF)
def normal_cdf(x):
    return 0.5 * (1 + erf(x / sqrt(2)))

# дисперсия
def disp(x:list) -> float:
    return mean([i*i for i in x])-mean(x)**2

# стандартное отклонение
def stand_otk(x: list) -> float:
    return sqrt(disp(x))

# Размах
def razm(x: list) -> float:
    return max(x)-min(x)

# Обратная функция распределения
def inv_f_norm(p, mu, s, t=0.001):
    if mu != 0 or s != 1:
        return mu + s *inv_f_norm(p,0,1,t)
    low_x, low_p = -100, 0
    hi_x, hi_p = 100, 1
    while hi_x - low_x > t:
        mid_x = (low_x + hi_x)/2
        mid_p = f_norm(mid_x)
        if mid_p < p:
            low_x, low_p = mid_x, mid_p
        elif mid_p>p:
            hi_x,hi_p = mid_x,mid_p
        else:
            break
    return mid_x

# z-тест
def z_test(x:list, mu: float, s: float) -> float:
    return ((mean(x)-mu)*sqrt(len(x)))/s

# решение
def first_task(data:list):
    # считаем стандартное отклонение
    s = stand_otk(data)
    # выбираем уровень значимости
    alpha = 0.05
    # составляем разные выборки и находим минимальную
    for i in range(2, len(data)):
        buf = []
        for j in range(i):
            buf.append(data[randint(0,len(data)-1)])
        z_t = z_test(buf, 4, s)
        p = p_value_z_test(z_t)
        if alpha<p:
            # стандартная ошибка
            se = s/sqrt(i)
            # квант/критическая граница альфы
            z_a = inv_f_norm(p,4,s)
            print(f"Количество часов: {i}, мощность проверки: {((z_a*se+4)-3)/se}")
            return
            
    print("Нулевая теория не верна")

print(p_value(3,4))