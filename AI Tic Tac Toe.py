import sys
import pygame
import numpy as np
import random
import copy

WIDTH = 600
HEIGHT = 600

ROWS = 3
COLS = 3

SQSIZE = WIDTH // COLS

LINE_WIDTH = 15
CIRC_WIDTH = 15
CROSS_WIDTH = 20
OFSET = 50

RADIUS = SQSIZE // 4

# COLOURS
BG_COLOUR = (28, 170, 150)
LINE_COLOUR = (23, 145, 135)
CIR_COLOUR = (239, 231, 200)
CROSS_COLOUR = (66, 66, 66)

# PYGAME SETUP
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ai Tic Tac Toe")
screen.fill(BG_COLOUR)


class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.empty_sqrs = self.squares
        self.marked_sqrs = 0

    def final_state(self, show=False):
        """
        @ Return 0 if there is no wine
        @ Return 1 if player 1 wins
        @ Return 2 if player 2 wins
        """
        # Vertical win
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    colour = CIR_COLOUR if self.squares[1][col] == 2 else CROSS_COLOUR
                    iPos = (col * SQSIZE + SQSIZE // 2, 20)
                    fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, colour, iPos, fPos, CROSS_WIDTH)
                return self.squares[0][col]

        # Horizontal win
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    colour = CIR_COLOUR if self.squares[row][0] == 2 else CROSS_COLOUR
                    iPos = (20, row * SQSIZE + SQSIZE // 2)
                    fPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, colour, iPos, fPos, CROSS_WIDTH)
                return self.squares[row][0]

        # Disc diagonal win
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                colour = CIR_COLOUR if self.squares[1][1] == 2 else CROSS_COLOUR
                iPos = (20, 20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, colour, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                colour = CIR_COLOUR if self.squares[1][1] == 2 else CROSS_COLOUR
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen, colour, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        return 0

    def mark_sqr(self, row, col, player):
        self.squares[row, col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_squs(self):
        empty_squs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_squs.append((row, col))
        return empty_squs

    def is_full(self):
        return self.marked_sqrs == 9

    def is_empty(self):
        return self.marked_sqrs == 0


class AI:
    def __init__(self, lavel=1, player=2):
        self.lavel = lavel
        self.player = player

    def rnd(self, board):
        empty_sqre = board.get_empty_squs()
        idx = random.randrange(0, len(empty_sqre))
        return empty_sqre[idx]  # give row & col

    def minimax(self, board, maximizing):
        # terminal cas
        case = board.final_state()

        # player 1 wins
        if case == 1:
            return 1, None
        if case == 2:
            return -1, None

        # Drow
        elif board.is_full():
            return 0, None

        if maximizing:
            max_eval = -100
            bast_move = None
            empty_sqrs = board.get_empty_squs()
            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    bast_move = (row, col)
            return max_eval, bast_move

        elif not maximizing:
            min_eval = 100
            bast_move = None
            empty_sqrs = board.get_empty_squs()
            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    bast_move = (row, col)
            return min_eval, bast_move

    def eval(self, main_board):
        if self.lavel == 0:
            # random choice
            eval = "random"
            move = self.rnd(main_board)
        else:
            # minimax algo choice
            eval, move = self.minimax(main_board, False)

        # print(f"AI has chosen to mark the square in pos {move} with an eval of {eval}")

        return move  # give row & col


class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1  # 1 = cross # 2 = circles
        self.game_mode = "ai"
        self.running = True
        self.show_lines()

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.drow_fig(row, col)
        self.next_turn()

    def show_lines(self):
        # Reset background colour
        screen.fill(BG_COLOUR)

        # vertical lines
        pygame.draw.line(screen, LINE_COLOUR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOUR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)

        # horizontal lines
        pygame.draw.line(screen, LINE_COLOUR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOUR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    def drow_fig(self, row, col):
        if self.player == 1:
            # Drow cross
            # Desc line
            start_disc = (col * SQSIZE + OFSET, row * SQSIZE + OFSET,)
            end_disc = (col * SQSIZE + SQSIZE - OFSET, row * SQSIZE + SQSIZE - OFSET,)
            pygame.draw.line(screen, CROSS_COLOUR, start_disc, end_disc, CROSS_WIDTH)
            # Asc line
            start_disc = (col * SQSIZE + OFSET, row * SQSIZE + SQSIZE - OFSET,)
            end_disc = (col * SQSIZE + SQSIZE - OFSET, row * SQSIZE + OFSET,)
            pygame.draw.line(screen, CROSS_COLOUR, start_disc, end_disc, CROSS_WIDTH)

        elif self.player == 2:
            # Drow circle
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIR_COLOUR, center, RADIUS, CIRC_WIDTH)

    def next_turn(self):
        self.player = self.player % 2 + 1

    def change_game_mode(self):
        self.game_mode = "ai" if self.game_mode == "pvp" else "pvp"

    def is_over(self):
        return self.board.final_state(show=True) != 0 or self.board.is_full()

    def reset(self):
        self.__init__()


# Main loop
def main():
    # Game object
    game = Game()
    board = game.board
    ai = game.ai

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:

                # prac g is change the game mode
                if event.key == pygame.K_g:
                    game.change_game_mode()

                # r = reset
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

                # 0 is random ai
                if event.key == pygame.K_0:
                    ai.lavel = 0

                # 1 is random ai
                if event.key == pygame.K_1:
                    ai.lavel = 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE

                if board.empty_sqr(row, col):
                    game.make_move(row, col)

                    if game.is_over():
                        game.running = False

        if game.game_mode == "ai" and game.player == ai.player and game.running:
            # update the screen
            pygame.display.update()
            # AI methods
            row, col = ai.eval(board)
            game.make_move(row, col)

            if game.is_over():
                game.running = False

        pygame.display.update()


main()
