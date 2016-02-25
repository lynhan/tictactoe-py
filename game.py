# game.py

import heapq

class TicTacToe:

    valid_cell_inputs = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    marks = ["X", "O"]
    rows = [(r, c) for r in range(3) for c in range(3)]
    cols = [(r, c) for c in range(3) for r in range(3)]
    d1 = [(x, x) for x in range(3)]  # top left to bottom right
    d2 = [(2-x, x) for x in range(3)] # bottom left to top right


    def __init__(self):

        self.first_player = 1
        self.current_player = self.first_player
        self.AI_num = 0
        self.player_count = 1
        self.move_count = 0

        from data import Cell
        self.board = [ [ Cell() for i in range(3)]  for j in range(3)]
        self.classify_cells()

        self.over = False
        self.queue = []
        self.init_queue()

    def classify_cells(self):

        from data import DefaultPriority, Coords
        from math import coords_to_num

        for row_index, row in enumerate(self.board):
            for col_index, cell in enumerate(row):

                if (row_index, col_index) == (1, 1):
                    cell.type = DefaultPriority.center
                elif row_index == 1 or col_index == 1:
                    cell.type = DefaultPriority.side
                else:
                    cell.type = DefaultPriority.corner

                cell.coords = Coords(row=row_index, col=col_index, num=coords_to_num(row_index, col_index))

    def init_queue(self):

        from data import Priority

        for row_index, row in enumerate(self.board):
            for col_index, cell in enumerate(row):
                heapq.heappush(self.queue, Priority(cell.type, cell))

    def print_board(self):

        print("\n")
        for row in self.board:
            print(*row, sep=' ', end='')
            print("\n")

    def start(self):

        p = self.get_valid_player_count()
        while not p:
            p = self.get_valid_player_count()

        if self.player_count == 1:
            a = self.is_AI_first()
            while not a:
                a = self.is_AI_first()

        print("\nGame started!\n")
        self.print_board()

    def valid_num(self, num):

        return num in ["1", "2"]

    def get_valid_player_count(self):

        print("\n1 or 2 player? (Type 1 or 2)")
        num = input()
        if self.valid_num(num):
            self.player_count = int(num)
            return True
        return False

    def is_AI_first(self):

        print("\nDoes the computer go first or second? (Type 1 or 2)")
        num = input()

        if self.valid_num(num):
            self.AI_num = int(num) - 1
            return True
        return False

    def turn(self):

        self.current_player = (0 if self.current_player == 1 else 1)
        print("Player {} => type a number 1 through 9".format(self.current_player+1, self.marks[self.current_player]))

        turn_done = self.choose_cell()
        while not turn_done:
            turn_done = self.choose_cell()


    def choose_cell(self):

        if self.player_count == 1 and self.current_player == self.AI_num:

            print("Computer is thinking...")

            c = heapq.heappop(self.queue).cell.coords
            row, col = c.row, c.col
            num = c.num
            self.valid_cell_inputs.remove(str(num))

        else:

            # get valid user input

            num = input()
            if num not in self.valid_cell_inputs:
                return False

            self.valid_cell_inputs.remove(num)

            from math import num_to_coords
            row, col = num_to_coords(int(num))

            # remove option from queue
            # so AI doesn't consider it anymore

            for item in self.queue:
                if item.cell.coords.num == num:
                    c = item.cell.coords
                    self.queue.remove(item)
                    heapq.heapify(self.queue)
                    break

        self.board[row][col].display = self.marks[self.current_player]
        if self.player_count == 1: # depends on updated board state
            self.update_queue()

        self.print_board()
        self.move_count += 1
        self.check_win()

        return True

    def my_count(self, three_cells):
        return sum(1 for coord in three_cells if self.board[coord[0]][coord[1]] == self.marks[self.current_player])

    def enemy_count(self, three_cells):
        return sum(1 for coord in three_cells if self.board[coord[0]][coord[1]] == self.marks[int(not self.current_player)])

    def update_queue(self):

        for item in self.queue:

            coords = item.cell.coords

            from data import DefaultPriority

            if item.cell.type == DefaultPriority.center:
                me = map(self.my_count, [self.rows, self.cols, self.d1, self.d2])
                enemy = map(self.enemy_count, [self.rows, self.cols, self.d1, self.d2])

            elif item.cell.type == DefaultPriority.corner:
                if coords.row == coords.col:
                    me = map(self.my_count, [self.rows, self.cols, self.d1])
                    enemy = map(self.enemy_count, [self.rows, self.cols, self.d1])
                else:
                    me = map(self.my_count, [self.rows, self.cols, self.d2])
                    enemy = map(self.enemy_count, [self.rows, self.cols, self.d2])

            elif item.cell.type == DefaultPriority.side:
                me = map(self.my_count, [self.rows, self.cols])
                enemy = map(self.enemy_count, [self.rows, self.cols])

            me = list(me)
            enemy = list(enemy)

            from data import DefaultPriority
            near_win = 2

            if near_win in me:
                item.num = DefaultPriority.win

            elif near_win in enemy:
                item.num = DefaultPriority.block

            else:
                diff = (e - m for e in enemy for m in me)
                item.num = min((DefaultPriority(item.cell.type) + d) for d in diff)

        heapq.heapify(self.queue)

    def check_three(self, three_cells):

        win = True
        for cell in three_cells:
            row, col = cell
            if self.board[row][col].display != self.marks[self.current_player]:
                win = False
                break

        from data import Status

        if win:
            return Status.win
        elif not win and self.move_count == 9:
            return Status.tie
        elif not win:
            return Status.ongoing

    def check_win(self):
        if self.move_count < 5:
            return False

        result = list(map(self.check_three, [self.rows, self.cols, self.d1, self.d2]))
        from data import Status

        if Status.win in result:
            self.over = True
            print("Player {} wins!".format(self.marks[self.current_player]))

        elif Status.tie in result:
            self.over = True
            print("It's a tie!")
