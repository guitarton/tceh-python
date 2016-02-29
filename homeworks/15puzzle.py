#!/usr/bin/python
# -*- coding: utf-8 -*-
# Для запуска: python 15puzzle.py
# Протестировано на python2 и 3 windows и linux
import os
import random
import copy
import sys

try:
    from getch import getch
except ImportError:

    # Взято отсюда http://code.activestate.com/recipes/134892/

    class _Getch:
        """Gets a single character from standard input.  Does not echo to the
    screen."""

        def __init__(self):
            try:
                self.impl = _GetchWindows()
            except ImportError:
                self.impl = _GetchUnix()

        def __call__(self):
            return self.impl()

    class _GetchUnix:
        def __init__(self):
            import tty, sys

        def __call__(self):
            import sys, tty, termios

            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

    class _GetchWindows:
        def __init__(self):
            import msvcrt

        def __call__(self):
            import msvcrt

            return msvcrt.getch().decode()

    getch = _Getch()

# Дальше собственный код

clear = 'cls' if sys.platform.startswith("win") else 'clear'

# Ширина и высота игрового поля
W = 5
H = 5

# Задаем глобальные переменные
matrix = []  # Двумерный list матрица - наше игровое полное
coord = ()  # координаты пустой ячейки
count_movements = 0  # будем считать ходы


def main():
    global coord
    global count_movements
    global matrix
    matrix = matrix_generator(W, H)  # генерируем начальное "правильное" поле
    clear = copy.deepcopy(matrix)  # и копируем его для дальнейшего сравнения
    coord = find_coord(matrix)  # ищем координаты пустой ячейки
    random_mix()  # перемешиваем чтобы наша головоломка имела стопроцентное решение (подробнее в вики)
    count_movements = 0
    while matrix != clear:
        cool_print()
        ch = getch()
        get_choice(ch)
    cool_print()
    print("Conratulations!!! You win!!! with {} movies".format(count_movements))


def matrix_generator(width, heigth):
    l = [[] for _ in range(heigth)]
    for j in range(heigth):
        for i in range(width):
            l[j].append(i + 1 + width * j)
    l[-1][-1] = " "
    # print(l)
    return l


def find_coord(m, elem=' '):
    x, y = None, None
    for j in range(len(m)):
        try:
            x = m[j].index(elem)
        except ValueError:
            pass
        else:
            y = j
    return x, y


def move_right(x, y):
    global count_movements
    if x > 0:
        try:
            ch = matrix[y][x]
            matrix[y][x] = matrix[y][x - 1]
            matrix[y][x - 1] = ch
            count_movements += 1
            return x - 1, y
        except IndexError:
            pass
    return x, y


def move_left(x, y):
    global count_movements
    try:
        ch = matrix[y][x]
        matrix[y][x] = matrix[y][x + 1]
        matrix[y][x + 1] = ch
        count_movements += 1
        return x + 1, y
    except IndexError:
        pass
    return x, y


def move_up(x, y):
    global count_movements
    if y > 0:
        try:
            ch = matrix[y][x]
            matrix[y][x] = matrix[y - 1][x]
            matrix[y - 1][x] = ch
            count_movements += 1
            return x, y - 1
        except IndexError:
            pass
    return x, y


def move_down(x, y):
    global count_movements
    try:
        ch = matrix[y][x]
        matrix[y][x] = matrix[y + 1][x]
        matrix[y + 1][x] = ch
        count_movements += 1
        return x, y + 1
    except IndexError:
        pass
    return x, y


def cool_print():
    os.system(clear)
    print("Use a,w,s,d for movements, q for quit")
    print("-" * 5 * W)
    s = ''
    for j in matrix:
        s += "  ".join(["{0:{1}}".format(a, len(str(H * W)) + 1) for a in j])
        s += '\n'
    print(s)
    print("Move: ", count_movements)


def get_choice(ch):
    global coord
    if ch == "d":
        coord = move_right(*coord)
    elif ch == "a":
        coord = move_left(*coord)
    elif ch == "s":
        coord = move_up(*coord)
    elif ch == "w":
        coord = move_down(*coord)
    elif ch == "q":
        sys.exit(1)
    else:
        return


def random_mix(count=1000):
    for _ in range(count):
        ch = random.choice(['s', 'a', 'd', 'w'])
        get_choice(ch)


if __name__ == '__main__':
    main()
