import pygame
from commun import is_position_a_winner

pygame.init()

reso = (640, 444)
screen = pygame.display.set_mode(reso)
pygame.display.set_caption("Puissance 4")

nbr_font = pygame.font.SysFont("franklin gothic heavy", 25)
button_font = pygame.font.SysFont("impact", 25)

clock = pygame.time.Clock()


red = (221, 47, 69)
green = (56, 146, 46)
blue = (85, 172, 238)
black = (54, 57, 63)
gris = (100, 100, 100)
gris_2 = (200,200,200)

def show_win(board):
    for row in range(len(board)):
        for col in range(len(board[row])):
            if is_position_a_winner(board, 0, row, col):
                draw_cercle(col, row, 28, green, 5)

def get_color(pice):
    if pice == 1: return blue
    if pice == 2: return red

def draw_cercle(col, row, radius, color, width=30):
    x, y = 141 + 60 * col, 31 + 60 * row
    pygame.draw.circle(screen,color, (x,y), radius, width)

def draw_num_col(last_col=None, color=None):
    y = 380
    for i in range(7):
        x = 140 + i * 60
        txt = str(i+1)
        size = nbr_font.size(txt)
        surface = nbr_font.render(txt, True, color if last_col == i else gris_2)
        screen.blit(surface, (x - size[0] // 2, y - size[1] // 2))

def draw_txt(txt, color=gris_2):
    x, y = 320, 420
    size = nbr_font.size(txt)
    surface = nbr_font.render(txt, True, color)
    screen.blit(surface, (x - size[0] // 2, y - size[1] // 2))

def fill_board(board):
    screen.fill(black)
    for i in range(7):
        pygame.draw.line(screen, gris, (110, i * 60), (530, i * 60))
        pygame.draw.line(screen, gris, (110 + i * 60, 0), (110 + i * 60, 360))
    pygame.draw.line(screen, gris, (530, 0), (530, 360))
    for row in range(6):
        for col in range(7):
            pice = board[row][col]
            if pice in (1,2):
                color = get_color(pice)
                draw_cercle(col, row, 28, color)
