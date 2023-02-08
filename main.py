import sys
from random import choice, randint

import pygame
from affichage import *
from commun import *
from algo_mini_max import ia

LVL_IA = 7


def select_player():
    name = ("JcJ (1)", "JcIA (2)", "IAcIA (3)", "IA commence (4)", "J commence (5)", "full random (6)")
    p = randint(1,2)
    players = {
        pygame.K_1: ("Bleu", "Rouge"), 
        pygame.K_2: ("Bleu" if p == 1 else "IA Bleu", "Rouge" if p == 2 else "IA Rouge"),
        pygame.K_3: ("IA Bleu", "IA Rouge"),
        pygame.K_4: ("IA Bleu", "Rouge"),
        pygame.K_5: ("Bleu", "IA Rouge"),
        pygame.K_6: (choice, ["Bleu", "Rouge", "IA Bleu", "Rouge"])
    }

    def affichage(select: int):
        select -= pygame.K_1
        screen.fill(black)
        for i in range(6):
            mx, my = i%3, i//3
            width, x = (200, 10) if my else (160, 70)
            x += (width + 10) * mx
            y = 162 + 80 * my
            rect = pygame.Rect(x, y, width, 50)
            pygame.draw.rect(screen, gris if select == i else gris_2, rect, 0, 99999)
            pygame.draw.rect(screen, gris_2 if select == i else gris, rect, 5, 99999)

            size = button_font.size(name[i])
            surface = button_font.render(name[i], True, (255, 255, 255) if select == i else (0, 0, 0))
            screen.blit(surface, (x + (width - size[0]) // 2, y + (50 - size[1]) // 2))

    def change_select(select):
        if select > pygame.K_6:
            select -= 6
        elif select < pygame.K_1:
            select += 6
        affichage(select)
        return select

    select = pygame.K_1
    affichage(select)
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if e.key == pygame.K_UP:
                    select = change_select(select - 3)
                elif e.key == pygame.K_DOWN:
                    select = change_select(select + 3)
                elif e.key == pygame.K_LEFT:
                    select = change_select(select - 1)
                elif e.key == pygame.K_RIGHT:
                    select = change_select(select + 1)
                elif e.key in range(pygame.K_1,pygame.K_6+1):
                    return players[e.key]
                elif e.key == 13:
                    return players[select]
        pygame.display.flip()
        clock.tick(60)

def ask_col():
    keys = {pygame.K_1: 0,
        pygame.K_2: 1,
        pygame.K_3: 2,
        pygame.K_4: 3,
        pygame.K_5: 4,
        pygame.K_6: 5,
        pygame.K_7: 6}
    col = None
    while col is None:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if e.key in keys.keys():
                    col = keys[e.key]
        pygame.display.flip()
        clock.tick(60)
    return col

def det_player(turn, players):
    if type(players[1]) == list:
        player = players[0](players[1])
    else:
        player = players[0] if turn % 2 else players[1]
    pice = 1 if "Bleu" in player else 2
    return player, pice

def play_turn(player, pice, board, turn):
    if "IA" in player:
        coup = False
        while not coup:
            if LVL_IA >= 6:
                limit = 2 * (LVL_IA + (-1  if turn <= 8 else 0 if 8 <= turn <= 14 else 1 if 14 <= turn <= 18 else 2 if 18 <= turn <= 20 else 3))
                #if turn >= 0:
                #    limit = 42
            else:
                limit = 2 * LVL_IA
            print(limit)
            coup = calc_piece_pos(ia(board, pice, turn, limit), board)
    else:
        coup = False
        while not coup:
            coup = calc_piece_pos(ask_col(), board)
    board[coup[0]][coup[1]] = pice
    return board, coup

def infinit():
    b=False
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == 13:
                    b=True
        pygame.display.update()
        if b: break
        clock.tick(60)

def loop(board):
    end = False
    players = select_player()
    turn = 0
    fill_board(board)
    draw_num_col()
    player, pice = det_player(1, players)
    draw_txt("C'est au tour de " + player, get_color(pice))
    pygame.display.flip()
    while not end:
        pygame.event.clear()
        turn += 1
        for i in board:
            print(i)
        print("")
        board, pos = play_turn(player, pice, board, turn)
        fill_board(board)
        draw_num_col(pos[1], get_color(pice))
        if is_position_a_winner(board, 0, pos[0], pos[1]):
            end = True
            show_win(board)
            draw_txt("Victoir de " + player, get_color(pice))
        elif turn == 42:
            end = True
            draw_txt("Égalité")
        else:
            player, pice = det_player(turn + 1, players)
            draw_txt("C'est au tour de " + player, get_color(pice))
        pygame.display.flip()

if __name__ == "__main__":
    while True:
        board = [[0 for _ in range(7)] for _ in range(6)]
        loop(board)
        infinit()
