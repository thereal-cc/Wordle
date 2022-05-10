import pygame
import random

from words import answers

pygame.init()
pygame.font.init()

# Window
WIDTH, HEIGHT = 700, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wordle")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (120, 119, 119)
YELLOW = (252, 199, 23)
GREEN = (4, 189, 53)

# Utils
FPS = 60
ROWS = 5
COLS = 5
LETTER_SIZE = 100
LETTER_SPACING = 25

# Target Word
daily_Word = answers[random.randint(0, len(answers) - 1)]

# Fonts
TITLE_FONT = pygame.font.SysFont('BabelStone Modern', 75)
LOWER_FONT = pygame.font.SysFont('BabelStone Modern', 35)
Title = TITLE_FONT.render("Wordle", 1, WHITE)

TURN = 0
BOARD = [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "]]

game_over = False
letters = 0
turn_active = True

# Draw Window
def draw_window():
    WIN.fill(BLACK)
    WIN.blit(Title, (WIDTH / 2 - Title.get_width() / 2, 10))

# Set Default Values On Restart
def set_defaults():
    global TURN, letters, game_over, daily_Word, BOARD

    TURN = 0
    letters = 0
    game_over = False
    daily_Word = answers[random.randint(0, len(answers) - 1)]
    BOARD = [[" ", " ", " ", " ", " "],
             [" ", " ", " ", " ", " "],
             [" ", " ", " ", " ", " "],
             [" ", " ", " ", " ", " "],
             [" ", " ", " ", " ", " "],
             [" ", " ", " ", " ", " "]]

# Draw Game Board
def draw_board():
    global TURN, BOARD

    for col in range(0, 5):
        for row in range(0, 6):
            pygame.draw.rect(WIN, WHITE, [col * 100 + 100, row * 100 + 100, 100, 100], 1)
            letter_text = TITLE_FONT.render(BOARD[row][col], True, WHITE)
            WIN.blit(letter_text, (col * 100 + 125, row * 100 + 100))

# Check User Guess
def check_guess():
    global TURN, BOARD, daily_Word

    for col in range(0, 5):
        for row in range(0, 6):
            if daily_Word[col] == BOARD[row][col] and TURN > row:
                pygame.draw.rect(WIN, GREEN, [col * 100 + 100, row * 100 + 100, LETTER_SIZE, LETTER_SIZE], 0, 5)
            elif BOARD[row][col] in daily_Word and TURN > row:
                pygame.draw.rect(WIN, YELLOW, [col * 100 + 100, row * 100 + 100, LETTER_SIZE, LETTER_SIZE], 0, 5)
            elif BOARD[row][col] not in daily_Word and TURN > row: 
                pygame.draw.rect(WIN, GREY, [col * 100 + 100, row * 100 + 100, LETTER_SIZE, LETTER_SIZE], 0, 5)

def main():
    global letters, game_over, TURN

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(FPS)

        draw_window()
        check_guess()
        draw_board()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.QUIT()
            if event.type == pygame.TEXTINPUT and turn_active and not game_over:
                entry = event.__getattribute__('text')
                if entry != " " and entry.isalpha():
                    entry = entry.lower()
                    BOARD[TURN][letters] = entry
                    letters += 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and letters > 0:
                    BOARD[TURN][letters - 1] = " "
                    letters -= 1
                if event.key == pygame.K_RETURN and not game_over:
                    guess = BOARD[TURN][0] + BOARD[TURN][1] + BOARD[TURN][2] + BOARD[TURN][3] + BOARD[TURN][4]
                    if letters == 5 and guess in answers:
                        TURN += 1
                        letters = 0
                if event.key == pygame.K_RETURN and game_over:
                    set_defaults()

        # End turn based on amount of letters
        if letters == 5:
            turn_active = False
        if letters < 5:
            turn_active = True

        # End game if all letters are guessed
        for row in range(0, 6):
            guess = BOARD[row][0] + BOARD[row][1] + BOARD[row][2] + BOARD[row][3] + BOARD[row][4]
            if guess == daily_Word and row < TURN:
                game_over = True

        if TURN >= 6:
            game_over = True
            loser_text = LOWER_FONT.render("You Lose! The Word Was " + daily_Word, 1, WHITE)
            WIN.blit(loser_text, (WIDTH / 2 - loser_text.get_width() / 2, HEIGHT - 75))
        
        if game_over and TURN < 6:
            winner_text = LOWER_FONT.render("You Win! Press Enter To Play Again", 1, WHITE)
            WIN.blit(winner_text, (WIDTH / 2 - winner_text.get_width() / 2, HEIGHT - 75))

        pygame.display.update()

if __name__ == "__main__":
    main()