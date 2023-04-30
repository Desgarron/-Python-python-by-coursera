"""
Сумма цифр в строке
Давайте начнем с несложной задачи.
Ваша цель написать программу (скрипт),
которая будет запускаться из командной строки.
Программа принимает в качестве аргумента строку, состоящую из цифр.
Гарантируется, что других символов в переданном параметре нет
и на вход всегда подается не пустая строка.
Программа должна вычислить сумму цифр из которых состоит строка
и вывести полученный результат на печать в стандартный вывод.
"""


import sys


digit_string = sys.argv[1]
total = 0
for i in digit_string:
    total += int(i)
print(total)

