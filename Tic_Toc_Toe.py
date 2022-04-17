USER_1 = 'X'
USER_2 = '0'
QUES_1 = ("Нажмите - Y чтобы поиграть, \
    \nНажмите - N для выхода.\n\033[1;32m Ваш выбор: \033[0m")
QUES_2 = ("\nСыграем ещё партию - Y, \
    \nДля выхода из игры - N \n\033[1;32m Ваш выбор: \033[0m")
QUES_3 = ("Согласны с очевидным - Y, \
    \nесть желание убедиться - N \n\033[1;32m Ваш выбор: \033[0m")


def greet():
    """
    Эта функция выводит табло приветствия при заходе в игру.
    """

    print("----------------------")
    print("|  Приветствуем Вас  |")
    print("|       в игре       |")
    print("|  крестики и нолики |")
    print("|--------------------|")
    print("| формат ввода: х у  |")
    print("| х - номер строки   |")
    print("| у - номер столбца  |")
    print("----------------------")


def show():
    """
    Эта функция формирует вид игрового поля.
    """

    print()
    print("   | 0 | 1 | 2 | ")
    print(" --------------- ")
    for i, row in enumerate(field):
        row_str = f" {i} | {' | '.join(map(str, row))} | "
        print(row_str)
        print(" --------------- ")
    print()


def ask():
    """
    Эта функция запрашивает у пользователя координаты хода,
    а потом делает проверки на корректность вводимых данных и
    отсутствие в данной точке ранее поставленного символа.
    """

    while True:
        cords = input("            Ваш ход: ").split()

        if len(cords) != 2:
            print("\033[1;31m Введите 2 координаты! \033[0m")
            continue

        x, y = cords

        if not(x.isdigit()) or not(y.isdigit()):
            print("\033[1;31m Введите числа! \033[0m")
            continue

        x, y = int(x), int(y)

        if 0 > x or x > 2 or 0 > y or y > 2:
            print("\033[1;31m Координаты вне диапазона! \033[0m")
            continue

        if field[x][y] != " ":
            print("\033[1;31m Клетка занята! \033[0m")
            continue

        return x, y


def yes_no(question):
    """
    Эта функция возвращает True либо False в зависимости от ответа
    пользователя на вопрос блока программы.
    """

    ans = input(question)

    while True:
        yes_ = ('Y', 'y', 'Н', 'н')
        no_ = ('N', 'n', 'Т', 'т')

        if ans not in yes_ and ans not in no_:
            ans = input(str("\033[1;31m Введите Y или N !!! : \033[0m"))
            continue

        if ans in yes_:
            return True

        if ans in no_:
            return False


def check_win():
    """
    Эта функция проверяет наличие выигрышной комбинации,
    а так же реализует досрочное завершение игры на 7 ходу
    в случае очевидного ничейного исхода.
    """

    win_cord = (((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)),
                ((2, 0), (2, 1), (2, 2)), ((0, 2), (1, 1), (2, 0)),
                ((0, 0), (1, 1), (2, 2)), ((0, 0), (1, 0), (2, 0)),
                ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)))

    mask = list()
    q = 0
    r = 0
    
    for cord in win_cord:
        symbols = []

        for c in cord:
            symbols.append(field[c[0]][c[1]])

        if symbols == [USER_1, USER_1, USER_1]:
            print(f"\033[1;33m Выиграл Игрок 1 '{USER_1}' !!! \033[0m")
            return True

        if symbols == [USER_2, USER_2, USER_2]:
            print(f"\033[1;33m Выиграл Игрок 2 '{USER_2}' !!! \033[0m")
            return True

        if count == 7 and q == 3 and r < 2:
            print((("\033[1;31m В этой партии уже никто не выиграет - "
                    "редкая комбинация вничью!!! \033[0m")))

            a = yes_no(QUES_3)
            return a

        mask.extend([symbols])
        
        q = mask.count([USER_2, USER_1, USER_1]) \
            + mask.count([USER_1, USER_1, USER_2])
        
        r = mask.count([USER_1, USER_1, ' ']) + \
            mask.count([' ', USER_1, USER_1]) + \
            mask.count([' ', USER_2, USER_2]) + \
            mask.count([USER_2, USER_2, ' '])
        
    return False


greet()
field = [[" "] * 3 for i in range(3)]
count = 0
start = yes_no(QUES_1)
while start:

    count += 1
    show()
    if count % 2 == 1:
        print(f"\033[3;36m Ходит Игрок 1 - '{USER_1}' \033[0m")
    else:
        print(f"\033[3;36m Ходит Игрок 2 - '{USER_2}' \033[0m")

    x, y = ask()

    if count % 2 == 1:
        field[x][y] = "X"

    else:
        field[x][y] = "0"

    if check_win():
        start = yes_no(QUES_2)
        field = [[" "] * 3 for i in range(3)]  # Очищаем игровое поле для нового раунда игры.
        count = 0  # обнуляем счётчик ходов для нового раунда игры.
        continue

    if count == 9:
        print("\033[1;33m Ничья! \033[0m")
        start = yes_no(QUES_2)
        field = [[" "] * 3 for i in range(3)]
        count = 0
        continue
