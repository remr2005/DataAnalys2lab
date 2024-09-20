from math import erf, sqrt, pi, exp, log
from statistics import mean
from random import randint
from scipy import integrate

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

def test(x,n, p0=4/8, pa=3/8):
    alpha = 0.05
    # вычисляю mu
    mu0 = n*p0
    mu1 = n*pa
    # нахожу стандартное отклонение
    sigma0=sqrt(n*p0*(1-p0))
    sigmaa=sqrt(n*pa*(1-pa))
    # нахожу нижнюю и верхнюю критическую точку 
    slow = inv_f_norm(alpha/2,mu0,sigma0)
    shigh=2*mu0-slow
    # формула из методы
    mosh_prov, error = integrate.quad(rho_norm, slow, shigh, args=(mu1, sigmaa))
    mosh_prov = 1 - mosh_prov
    if p_value(x/8,mu0,sigma0)>alpha and mosh_prov>0.8:
        print("Нулевая гипотеза не опровергнута")
        print(f"Мощность опроверки равна {mosh_prov}")
        return True
    return False

def first_task(j):
    # находим идеально кол-во чассов для заданного количетсва плитки
    for i in range(100,10000):
        if test(j,i,3/8,4/8):
            print("Плиточник кладет 3 кв.м")
            print(f"Потребовалось {i} часов")
            break
        if test(j,i):
            print("Плиточник кладет 4 кв.м")
            print(f"Потребовалось {i} часов")
            break

def main():
    first_task(700)

if __name__ == "__main__":
    main()