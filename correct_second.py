import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import solve as gauss
from statistics import mean
from math import sqrt
from first_task import f_norm, inv_f_norm, p_value
from statistics import mean

def GetData(data=[]):
    url = 'https://cryptocharts.ru/bitcoin-dollar/'
    response = requests.get(url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    table_class = 'TableRates'
    table = soup.find('table', class_=table_class)

    rows = table.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        for cell in cells[1::2]:
            data.insert(0, cell.text.strip())

# дисперсия
def variance(x):
    return mean(list(map(lambda t: t ** 2, x)))

# стандартное отклонение
def standard_deviation(x):
    return sqrt(variance(x))

def find_max_by_abs(nums: list[float]) -> float:
    max_num = 0
    for num in nums:
        if abs(num) > abs(max_num):
            max_num = num
    return abs(max_num)

# Полиномиальная аппроксимация
def approx_poly(x, t, r):
    M = [[] for _ in range(r + 1)]
    b = []
    for l in range(r + 1):
        for q in range(r + 1):
            M[l].append(sum(list(map(lambda z: z ** (l + q), t))))
        b.append(sum(xi * ti ** l for xi, ti in zip(x, t)))
    a = gauss(np.array(M, dtype="float64"), np.array(b, dtype="float64"))
    return a

def test(x, n):
    alpha =0.05
    dataset = x.copy()
    t = list(range(len(dataset)))
    # Аппроксимация
    A_0 = approx_poly(dataset, t, n)
    A_1 = approx_poly(dataset,t,n)
    # Вычисляем аппроксимированные значения
    x_0_approx = [sum(A_0[i] * ti ** i for i in range(len(A_0))) for ti in t]
    x_1_approx = [sum(A_1[i] * ti ** i for i in range(len(A_0))) for ti in t]
    # Вычисление остатков (ошибок аппроксимации)
    epsilon0 = [x_0_approx[i]-dataset[i] for i in range(len(dataset))]
    epsilon1 = [x_1_approx[i]-dataset[i] for i in range(len(dataset))]
    # Средние значения и стандартные отклонения
    mu0 = mean(epsilon0)
    mu1 = mean(epsilon1)
    # стандартное отклонение
    sigma0 = standard_deviation(epsilon0)
    sigma1 = standard_deviation(epsilon1)
    # Наибольшее отклонение
    max_dev0 = find_max_by_abs([i - mu0 for i in epsilon0])
    # Вычисление p-значения
    slow = inv_f_norm(alpha/2,mu0,sigma0)
    shigh=2*mu0-slow
    return p_value(max_dev0+mu0, 0,sigma0), x_0_approx, 1-f_norm(shigh,mu1,sigma1)+f_norm(slow,mu1,sigma1)
# f_norm118 - f_norm82

def main():
    # Получение данных
    dataset = []
    GetData(dataset)
    dataset = [float(value.replace(',', '.')) for value in dataset]  # Преобразуем строки в числа
    max_p = -1
    max_n = 0
    max_w=0
    x_appr = []
    for i in range(5,50):
        p, x_appr, w = test(dataset,i)
        if max_p<p:
            max_p=p
            max_w = w
            max_n=i
    t = list(range(len(dataset)))
    print(f"Лучшее p_value:{max_p}")
    print(f"Его w:{max_w}")
    # Визуализация данных и аппроксимаций
    plt.figure(figsize=(10, 6))
    plt.plot(t, dataset, label='Исходные данные', marker='o')
    plt.plot(t, x_appr, label=f'Аппроксимированная кривая {max_n} степени', linestyle='-')
    plt.xlabel('Время')
    plt.ylabel('Значение')
    plt.title('Аппроксимация полиномом')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
