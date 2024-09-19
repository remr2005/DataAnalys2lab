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

def test(x,n):
    x= x/(8*n) * 100
    alpha = 0.05
    # задаю p0 и pa
    p0 = 4/8
    pa = 3/8
    # вычисляю mu
    mu0 = n*p0
    mu1 = n*pa
    # нахожу стандартное отклонение
    sigma0=sqrt(n*p0*(1-p0))
    sigmaa=sqrt(n*pa*(1-pa))
    # нахожу нижнюю и верхнюю критическую точку 
    slow = inv_f_norm(alpha/2,mu0,sigma0)
    shigh=2*mu0-slow
    # по сути это тоже самое, но я просто делал по книге)))0
    f_first_error = True if shigh >= x >= slow else False
    p_value_test = True if p_value(x,mu0,sigma0) > alpha else False
    # формула из методы
    mosh_prov = 1 - rho_norm(x,mu1,sigmaa)
    if f_first_error:
        print(x, slow, shigh)
        print("без p_value")
        print("Нулевая гипотеза не опровергнута")
        print(f"Мощность опроверки равна {mosh_prov}")
        return True
    if p_value_test:
        print(x, slow, shigh)
        print("c p_value")
        print("Нулевая гипотеза не опровергнута")
        print(f"Мощность опроверки равна {mosh_prov}")
        return True
    return False

def first_task(j):
    # находим идеально кол-во чассов для заданного количетсва плитки
    for i in range(100,10000):
        if test(j,i):
            print(f"Потребовалось {i} часов")
            break

def main():
    first_task(700)

if __name__ == "__main__":
    main()