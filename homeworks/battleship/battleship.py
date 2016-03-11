import string
import os


class Ship:
    def __init__(self, name, count, size):
        self.name = name
        self.count = count
        self.size = size


class Board():
    INITIAL_STATE = ' '
    SIZE = 10

    def __init__(self):
        self.size = self.__class__.SIZE
        self.board = [[] for _ in range(self.size)]
        for i in range(self.size):
            for _ in range(self.size):
                self.board[i].append(self.__class__.INITIAL_STATE)

    def cool_print(self, title='Helllo'):
        abc = string.ascii_lowercase[:self.size]
        print('{0:.^64}'.format(title))
        print()
        print('{0:>64}'.format((' ' * 5).join(abc) + ' ' * 3))
        separator = '{0:>64}'.format('_' * 61)
        print(separator)
        for i in range(10):
            beauty = ['{0:^5}'.format(k) for k in self.board[i]]
            print('{0:<3}'.format(i + 1) + '|' + '|'.join(beauty), end='|\n')
            print(separator)


class Player:
    def __init__(self):
        self.name = self.wait_for_name()
        self.field = Board()
        self.moves = Board()

    def greet_player(self):
        print("Hello ", self.name)

    def wait_for_name(self):
        return input("Player name: ")


class GameController:
    def __init__(self):
        self.ships = [Ship('Четырехпалубный', 1, 4)]
        # Ship('Трехпалубный', 2, 3),
        # Ship('Двухпалубный', 3, 2),
        # Ship('Однопалубный', 4, 1)]
        self.players = []
        for _ in range(2):
            self.players.append(Player())

    def take_coord(self):
        abc = string.ascii_lowercase[:10]
        while True:
            coord = input('Введите координаты слитно (например: a5 j7) в диапазоне a-j 1-10 -> ')
            try:
                x = abc.index(coord[0])
                y = int(coord[1:3]) - 1
            except (IndexError, ValueError):
                pass
            else:
                if y in range(10):
                    return x, y
            print('Неверно!!!')

    def place_ship(self, ship, board):
        # os.system('clear')
        for _ in range(ship.count):
            board.cool_print()
            print("Расположить ", ship.name)
            x, y = self.take_coord()
            orientation = 'h'
            print(x, y, ship.size)
            if ship.size != 1:
                while True:
                    orientation = input('Горизонтально или вертикально? (h или v): ')
                    if orientation in ('h', 'v'):
                        break
                    print('Неверно!!!')
            if orientation == 'h':
                for i in range(ship.size):
                    board.board[y][x + i] = '[ ]'
            elif orientation == 'v':
                for i in range(ship.size):
                    board.board[y + i][x] = '[ ]'
            os.system('clear')
        board.cool_print()

    def start_game(self):
        for player in self.players:
            player.greet_player()
            for ship in self.ships:
                self.place_ship(ship, player.field)
        self.perform_move(self.players)

    def perform_move(self, players):
        you, opponent = players
        while not self.check_win(opponent.field.board):
            os.system('clear')
            input('Игрок {}! Ваш ход.'.format(you.name))
            you.moves.cool_print()
            x, y = self.take_coord()
            if opponent.field.board[y][x] == '[ ]':
                you.moves.board[y][x] = '[X]'
                opponent.field.board[y][x] = '[X]'
            elif opponent.field.board[y][x] == ' ':
                you.moves.board[y][x] = 'X'
                you, opponent = opponent, you
        print('{} win!!!'.format(you.name))

    def check_win(self, board):
        for row in board:
            if '[ ]' in row:
                return False
        return True


a = GameController()
# a.init_players()
a.start_game()
