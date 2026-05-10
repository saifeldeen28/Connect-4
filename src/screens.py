import math
import random
import sys
import pygame

from .constants import COLUMN_COUNT, SQUARE_SIZE, RADIUS, width, ORANGE
from .display import screen, font, rules, main_bg, dark_bg
from .board import create_board, drop_piece, valid_location, get_next_open_row, check_win, check_draw, print_board
from .renderer import draw_board, pause_page
from .persistence import check_name, save_game, load_game


def main_menu():
    while True:
        pygame.display.set_caption('Main Menu')
        screen.blit(main_bg, (0, 0))
        play_button = pygame.draw.rect(screen, ORANGE, (30, 280, 200, 50), 0, 30)
        rules_button = pygame.draw.rect(screen, ORANGE, (30, 380, 200, 50), 0, 30)
        credits_button = pygame.draw.rect(screen, ORANGE, (30, 480, 200, 50), 0, 30)
        exit_button = pygame.draw.rect(screen, ORANGE, (30, 580, 200, 50), 0, 30)

        screen.blit(font.render('Play', True, 'black'), (90, 275))
        screen.blit(font.render('Rules', True, 'black'), (75, 375))
        screen.blit(font.render('Credits', True, 'black'), (55, 475))
        screen.blit(font.render('Exit', True, 'black'), (90, 575))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    name_page()
                if rules_button.collidepoint(event.pos):
                    rules_page()
                if credits_button.collidepoint(event.pos):
                    credits_page()
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()


def rules_page():
    run = True
    while run:
        pygame.display.set_caption('Rules')
        screen.blit(rules, (0, 0))
        back_button = pygame.draw.rect(screen, 'black', (275, 640, 150, 50), 0, 30)
        screen.blit(font.render('Back', True, 'white'), (300, 635))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and back_button.collidepoint(event.pos):
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False

        pygame.display.flip()


def credits_page():
    run = True
    while run:
        pygame.display.set_caption('Credits')
        screen.blit(dark_bg, (0, 0))
        screen.blit(font.render('CREDITS', True, 'white'), (260, 80))
        screen.blit(font.render('Made by:', True, 'white'), (10, 150))
        screen.blit(font.render('Karim Wael', True, 'white'), (100, 200))
        back_button = pygame.draw.rect(screen, ORANGE, (275, 600, 150, 50), 0, 30)
        screen.blit(font.render('Back', True, 'black'), (300, 595))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and back_button.collidepoint(event.pos):
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False

        pygame.display.flip()


def name_page():
    active = False
    error = False
    user_input = ''
    run = True

    while run:
        screen.blit(dark_bg, (0, 0))
        pygame.display.set_caption('Welcome to Connect 4!')

        continue_button = pygame.draw.rect(screen, ORANGE, (450, 600, 190, 50), 0, 30)
        back_button = pygame.draw.rect(screen, ORANGE, (50, 600, 160, 50), 0, 30)
        text_width, _ = font.size(user_input)

        if active:
            text_box = pygame.draw.rect(screen, ORANGE, (220, 300, max(250, text_width + 40), 50), 0, 30)
        else:
            text_box = pygame.draw.rect(screen, 'grey', (220, 300, max(250, text_width + 40), 50), 0, 30)

        if error:
            screen.blit(font.render('You need to enter a name', True, 'red'), (110, 400))

        screen.blit(font.render('Enter your name:', True, 'white'), (190, 100))
        screen.blit(font.render(user_input, True, 'black'), (240, 295))
        screen.blit(font.render('Continue', True, 'black'), (470, 595))
        screen.blit(font.render('Back', True, 'black'), (75, 595))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    else:
                        user_input += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if text_box.collidepoint(event.pos):
                    active = True
                    error = False
                else:
                    active = False
                if continue_button.collidepoint(event.pos):
                    if user_input == '':
                        error = True
                    else:
                        check_game(user_input)
                if back_button.collidepoint(event.pos):
                    main_menu()

        pygame.display.flip()


def check_game(user_input):
    file_exists, file_name = check_name(user_input)

    if not file_exists:
        game_mode(file_name)
        return

    run = True
    while run:
        screen.blit(dark_bg, (0, 0))

        new_game_button = pygame.draw.rect(screen, ORANGE, (50, 500, 250, 50), 0, 30)
        load_button = pygame.draw.rect(screen, ORANGE, (400, 500, 250, 50), 0, 30)
        back_button = pygame.draw.rect(screen, ORANGE, (275, 600, 150, 50), 0, 30)

        screen.blit(font.render('New Game', True, 'black'), (80, 495))
        screen.blit(font.render('Load Game', True, 'black'), (420, 495))
        screen.blit(font.render('Back', True, 'black'), (300, 595))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    run = False
                if new_game_button.collidepoint(event.pos):
                    game_mode(file_name)
                if load_button.collidepoint(event.pos):
                    loaded = load_game(file_name)
                    continue_game(loaded, file_name)

        pygame.display.flip()


def game_mode(file_name):
    run = True
    while run:
        pygame.display.set_caption('Game Mode')
        screen.blit(dark_bg, (0, 0))
        back_button = pygame.draw.rect(screen, ORANGE, (275, 600, 150, 50), 0, 30)
        multiplayer_button = pygame.draw.rect(screen, ORANGE, (80, 300, 250, 50), 0, 30)
        computer_button = pygame.draw.rect(screen, ORANGE, (380, 300, 250, 50), 0, 30)

        screen.blit(font.render('Choose mode', True, 'white'), (220, 100))
        screen.blit(font.render('Back', True, 'black'), (300, 595))
        screen.blit(font.render('Multiplayer', True, 'black'), (100, 293))
        screen.blit(font.render('Computer', True, 'black'), (410, 293))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    name_page()
                if multiplayer_button.collidepoint(event.pos):
                    play_page(file_name)
                if computer_button.collidepoint(event.pos):
                    computer_page(file_name)

        pygame.display.flip()


def win_page(piece, file_name):
    run = True
    while run:
        screen.blit(dark_bg, (0, 0))
        pygame.display.set_caption('CONGRATULATIONS!')
        screen.blit(font.render(f'Player {piece} WINS!', True, 'white'), (200, 100))

        new_game_button = pygame.draw.rect(screen, ORANGE, (80, 400, 250, 50), 0, 30)
        main_menu_button = pygame.draw.rect(screen, ORANGE, (380, 400, 250, 50), 0, 30)

        screen.blit(font.render('New Game', True, 'black'), (100, 395))
        screen.blit(font.render('Main Menu', True, 'black'), (400, 395))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if new_game_button.collidepoint(event.pos):
                    play_page(file_name)
                if main_menu_button.collidepoint(event.pos):
                    main_menu()

        pygame.display.flip()


def draw_page(file_name):
    run = True
    while run:
        screen.blit(dark_bg, (0, 0))
        pygame.display.set_caption('DRAW!')
        screen.blit(font.render('NO ONE WON ITS A DRAW!', True, 'white'), (80, 100))

        new_game_button = pygame.draw.rect(screen, ORANGE, (80, 400, 250, 50), 0, 30)
        main_menu_button = pygame.draw.rect(screen, ORANGE, (380, 400, 250, 50), 0, 30)

        screen.blit(font.render('New Game', True, 'black'), (100, 395))
        screen.blit(font.render('Main Menu', True, 'black'), (400, 395))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if new_game_button.collidepoint(event.pos):
                    play_page(file_name)
                if main_menu_button.collidepoint(event.pos):
                    main_menu()

        pygame.display.flip()


def play_page(file_name):
    board = create_board()
    draw_board(board)
    turn = 0
    pygame.display.flip()
    run = True
    pause = False

    while run:
        pygame.display.set_caption('Play')

        if pause:
            continue_button, save_button, exit_button = pause_page()
        else:
            draw_board(board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause = not pause

            if not pause:
                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, 'black', (0, 0, width, SQUARE_SIZE))
                    posx = event.pos[0]
                    color = 'red' if turn == 0 else 'yellow'
                    pygame.draw.circle(screen, color, (posx, int(SQUARE_SIZE / 2)), RADIUS)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARE_SIZE))
                    piece = 1 if turn == 0 else 2

                    if valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, piece)
                        print_board(board)
                        draw_board(board)

                        if check_win(board, piece):
                            pygame.display.flip()
                            win_page(piece, file_name)

                        if check_draw(board):
                            pygame.display.flip()
                            draw_page(file_name)

                        turn = (turn + 1) % 2

            if pause:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if continue_button.collidepoint(event.pos):
                        pause = False
                    if save_button.collidepoint(event.pos):
                        save_game(file_name, board)
                        main_menu()
                    if exit_button.collidepoint(event.pos):
                        main_menu()

        pygame.display.flip()


def computer_page(file_name):
    board = create_board()
    draw_board(board)
    turn = 0
    pygame.display.flip()
    run = True
    pause = False

    while run:
        pygame.display.set_caption('Play vs Computer')

        if pause:
            continue_button, save_button, exit_button = pause_page()
        else:
            draw_board(board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause = not pause

            if not pause:
                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, 'black', (0, 0, width, SQUARE_SIZE))
                    posx = event.pos[0]
                    pygame.draw.circle(screen, 'red', (posx, int(SQUARE_SIZE / 2)), RADIUS)

                if event.type == pygame.MOUSEBUTTONDOWN and turn == 0:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARE_SIZE))

                    if valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)
                        print_board(board)
                        draw_board(board)
                        pygame.display.flip()

                        if check_win(board, 1):
                            win_page(1, file_name)

                        if check_draw(board):
                            draw_page(file_name)

                        turn = 1

            if pause:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if continue_button.collidepoint(event.pos):
                        pause = False
                    if save_button.collidepoint(event.pos):
                        save_game(file_name, board)
                        main_menu()
                    if exit_button.collidepoint(event.pos):
                        main_menu()

        if turn == 1 and run and not pause:
            col = random.randint(0, COLUMN_COUNT - 1)
            if valid_location(board, col):
                pygame.time.wait(500)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)
                print_board(board)
                draw_board(board)

                if check_win(board, 2):
                    pygame.display.flip()
                    win_page(2, file_name)

                if check_draw(board):
                    pygame.display.flip()
                    draw_page(file_name)

                turn = 0

        pygame.display.flip()


def continue_game(board, file_name):
    draw_board(board)
    turn = 0
    pygame.display.flip()
    run = True
    pause = False

    while run:
        pygame.display.set_caption('Play')

        if pause:
            continue_button, save_button, exit_button = pause_page()
        else:
            draw_board(board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause = not pause

            if not pause:
                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, 'black', (0, 0, width, SQUARE_SIZE))
                    posx = event.pos[0]
                    color = 'red' if turn == 0 else 'yellow'
                    pygame.draw.circle(screen, color, (posx, int(SQUARE_SIZE / 2)), RADIUS)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARE_SIZE))
                    piece = 1 if turn == 0 else 2

                    if valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, piece)
                        print_board(board)
                        draw_board(board)

                        if check_win(board, piece):
                            pygame.display.flip()
                            win_page(piece, file_name)

                        if check_draw(board):
                            pygame.display.flip()
                            draw_page(file_name)

                        turn = (turn + 1) % 2

            if pause:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if continue_button.collidepoint(event.pos):
                        pause = False
                    if save_button.collidepoint(event.pos):
                        save_game(file_name, board)
                        main_menu()
                    if exit_button.collidepoint(event.pos):
                        main_menu()

        pygame.display.flip()
