import pygame
from .constants import ROW_COUNT, COLUMN_COUNT, SQUARE_SIZE, RADIUS, width, height, ORANGE
from .display import screen, surface, font

_banner_font = None


def _get_banner_font():
    global _banner_font
    if _banner_font is None:
        _banner_font = pygame.font.SysFont('Comic Sans MS', 60)
    return _banner_font


def result_banner(message):
    bf = _get_banner_font()
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(overlay, (0, 0, 0, 190), (40, height // 2 - 80, width - 80, 160), 0, 20)
    text_surf = bf.render(message, True, 'white')
    text_rect = text_surf.get_rect(center=(width // 2, height // 2))
    overlay.blit(text_surf, text_rect)
    screen.blit(overlay, (0, 0))
    pygame.display.flip()
    pygame.time.wait(5000)


def draw_board(board):
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            pygame.draw.rect(screen, 'blue', (col * SQUARE_SIZE, row * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, 'black', (int(col * SQUARE_SIZE + SQUARE_SIZE / 2), int(row * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)

    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            if board[row][col] == 1:
                pygame.draw.circle(screen, 'red', (int(col * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(row * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, 'yellow', (int(col * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(row * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)


def pause_page():
    pygame.draw.rect(surface, (128, 128, 128, 7), (0, 0, width, height))
    pygame.draw.rect(surface, 'black', (100, 100, 500, 500), 0, 10)

    continue_button = pygame.draw.rect(surface, ORANGE, (150, 250, 400, 50), 0, 30)
    save_button = pygame.draw.rect(surface, ORANGE, (150, 350, 400, 50), 0, 30)
    exit_button = pygame.draw.rect(surface, ORANGE, (150, 450, 400, 50), 0, 30)

    surface.blit(font.render('Game Paused', True, 'white'), (230, 150))
    surface.blit(font.render('Continue', True, 'black'), (270, 245))
    surface.blit(font.render('Save', True, 'black'), (300, 345))
    surface.blit(font.render('Exit', True, 'black'), (300, 445))

    screen.blit(surface, (0, 0))
    return continue_button, save_button, exit_button
