import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BongoCat Alternativo - Símbolos")
clock = pygame.time.Clock()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
GREEN = (50, 200, 50)
RED = (200, 50, 50)
BLUE = (50, 100, 200)
YELLOW = (255, 220, 50)
PURPLE = (150, 50, 200)
ORANGE = (255, 150, 50)
CYAN = (50, 200, 200)
PINK = (255, 100, 150)

# Fuentes
font_large = pygame.font.SysFont("consolas", 48, bold=True)
font_medium = pygame.font.SysFont("consolas", 28)
font_small = pygame.font.SysFont("consolas", 20)
font_tiny = pygame.font.SysFont("consolas", 16)

# Estado del juego
clicks = 0
current_costume = 0  # 0 = normal (siempre disponible)
shop_open = False
hand_up = False  # Para animación de golpe

# Disfraces: (nombre, umbral de desbloqueo, color principal, símbolos de orejas/ojos/boca)
COSTUMES = [
    {
        "name": "Gatito Normal",
        "unlock": 0,
        "color": (255, 200, 150),
        "ears": "^ ^",
        "eyes": "o o",
        "mouth": "ω",
        "body": "(=^･ω･^=)"
    },
    {
        "name": "Gatito Ninja",
        "unlock": 100,
        "color": (40, 40, 40),
        "ears": "^ ^",
        "eyes": "> <",
        "mouth": "─",
        "body": "(=^>ω<^=)"
    },
    {
        "name": "Gatito Magico",
        "unlock": 1000,
        "color": (180, 100, 255),
        "ears": "* *",
        "eyes": "★ ★",
        "mouth": "◇",
        "body": "(=^★ω★^=)"
    },
    {
        "name": "Gatito Robot",
        "unlock": 1500,
        "color": (100, 180, 255),
        "ears": "[ ]",
        "eyes": "◉ ◉",
        "mouth": "═",
        "body": "[=^◉ω◉^=]"
    },
    {
        "name": "Gatito Rey",
        "unlock": 2000,
        "color": (255, 215, 0),
        "ears": "♔ ♔",
        "eyes": "◎ ◎",
        "mouth": "ω",
        "body": "(=^◎ω◎^=)"
    },
    {
        "name": "Gatito Dragon",
        "unlock": 5000,
        "color": (255, 80, 50),
        "ears": "Λ Λ",
        "eyes": "◆ ◆",
        "mouth": "▽",
        "body": "(=^◆ω◆^=)"
    }
]

def is_unlocked(index):
    return clicks >= COSTUMES[index]["unlock"]

def draw_text(text, font, color, x, y, center=False):
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surface, rect)
    return rect

def draw_cat(costume_idx, x, y, scale=1.0, hands_up=False):
    """Dibuja el gatito usando solo símbolos / texto ASCII estilizado"""
    costume = COSTUMES[costume_idx]
    color = costume["color"]

    # Cuerpo principal (cara grande)
    face_font = pygame.font.SysFont("consolas", int(60 * scale), bold=True)
    face_surf = face_font.render(costume["body"], True, color)
    face_rect = face_surf.get_rect(center=(x, y))
    screen.blit(face_surf, face_rect)

    # Orejas encima
    ear_font = pygame.font.SysFont("consolas", int(36 * scale), bold=True)
    ears_surf = ear_font.render(costume["ears"], True, color)
    ears_rect = ears_surf.get_rect(center=(x, y - 55 * scale))
    screen.blit(ears_surf, ears_rect)

    # Manos / patas (animación)
    hand_font = pygame.font.SysFont("consolas", int(40 * scale), bold=True)
    if hands_up:
        left_hand = hand_font.render("ﾉ", True, color)
        right_hand = hand_font.render("ヽ", True, color)
        screen.blit(left_hand, left_hand.get_rect(center=(x - 80 * scale, y + 10 * scale)))
        screen.blit(right_hand, right_hand.get_rect(center=(x + 80 * scale, y + 10 * scale)))
    else:
        left_hand = hand_font.render("つ", True, color)
        right_hand = hand_font.render("⊂", True, color)
        screen.blit(left_hand, left_hand.get_rect(center=(x - 70 * scale, y + 40 * scale)))
        screen.blit(right_hand, right_hand.get_rect(center=(x + 70 * scale, y + 40 * scale)))

    # Mesa / bongo
    table_font = pygame.font.SysFont("consolas", int(30 * scale))
    table = table_font.render("═══════", True, DARK_GRAY)
    table_rect = table.get_rect(center=(x, y + 70 * scale))
    screen.blit(table, table_rect)

def draw_shop():
    # Fondo semi-transparente
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    # Panel de la tienda
    panel_rect = pygame.Rect(100, 60, 600, 480)
    pygame.draw.rect(screen, (30, 30, 40), panel_rect, border_radius=15)
    pygame.draw.rect(screen, YELLOW, panel_rect, 3, border_radius=15)

    draw_text("TIENDA DE DISFRACES", font_medium, YELLOW, WIDTH // 2, 90, center=True)
    draw_text(f"Clicks actuales: {clicks}", font_small, WHITE, WIDTH // 2, 125, center=True)

    # Lista de disfraces
    start_y = 160
    for i, costume in enumerate(COSTUMES):
        y = start_y + i * 55
        unlocked = is_unlocked(i)
        selected = (current_costume == i)

        # Fondo de la fila
        row_rect = pygame.Rect(130, y - 5, 540, 48)
        if selected:
            pygame.draw.rect(screen, (80, 60, 20), row_rect, border_radius=8)
            pygame.draw.rect(screen, YELLOW, row_rect, 2, border_radius=8)
        else:
            pygame.draw.rect(screen, (50, 50, 60), row_rect, border_radius=8)

        # Nombre y estado
        name_color = GREEN if unlocked else GRAY
        status = "✓ DESBLOQUEADO" if unlocked else f"Bloqueado ({costume['unlock']} clicks)"
        draw_text(f"{i}. {costume['name']}", font_small, name_color, 150, y + 5)
        draw_text(status, font_tiny, name_color if unlocked else RED, 150, y + 25)

        # Botón seleccionar (solo si está desbloqueado)
        if unlocked:
            btn_rect = pygame.Rect(550, y + 5, 100, 35)
            btn_color = GREEN if selected else BLUE
            pygame.draw.rect(screen, btn_color, btn_rect, border_radius=6)
            label = "USANDO" if selected else "USAR"
            draw_text(label, font_tiny, WHITE, btn_rect.centerx, btn_rect.centery, center=True)

    # Instrucciones
    draw_text("Clic en 'USAR' para equipar  |  ESC o botón Cerrar para salir", font_tiny, LIGHT_GRAY, WIDTH // 2, 510, center=True)

    # Botón cerrar
    close_rect = pygame.Rect(350, 525, 100, 35)
    pygame.draw.rect(screen, RED, close_rect, border_radius=6)
    draw_text("CERRAR", font_tiny, WHITE, close_rect.centerx, close_rect.centery, center=True)
    return close_rect

def main():
    global clicks, current_costume, shop_open, hand_up

    hand_timer = 0
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if shop_open:
                        shop_open = False
                    else:
                        running = False
                elif event.key == pygame.K_SPACE and not shop_open:
                    # Golpe con espacio
                    clicks += 1
                    hand_up = True
                    hand_timer = 8
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True

        # Actualizar animación de manos
        if hand_timer > 0:
            hand_timer -= 1
            if hand_timer == 0:
                hand_up = False

        # Dibujar fondo
        screen.fill((20, 20, 30))

        if not shop_open:
            # --- Pantalla principal ---
            # Título
            draw_text("BONGO CAT - SÍMBOLOS", font_large, YELLOW, WIDTH // 2, 40, center=True)
            draw_text("Haz clic en el gato o pulsa ESPACIO", font_small, LIGHT_GRAY, WIDTH // 2, 90, center=True)

            # Contador de clicks
            draw_text(f"CLICKS: {clicks}", font_medium, WHITE, WIDTH // 2, 130, center=True)

            # Área del gato (clicable)
            cat_x, cat_y = WIDTH // 2, 300
            draw_cat(current_costume, cat_x, cat_y, scale=1.4, hands_up=hand_up)

            # Rectángulo invisible para detectar clic en el gato
            cat_hitbox = pygame.Rect(cat_x - 150, cat_y - 100, 300, 220)

            # Botón de tienda
            shop_btn = pygame.Rect(WIDTH // 2 - 80, 500, 160, 45)
            pygame.draw.rect(screen, PURPLE, shop_btn, border_radius=10)
            pygame.draw.rect(screen, WHITE, shop_btn, 2, border_radius=10)
            draw_text("TIENDA", font_medium, WHITE, shop_btn.centerx, shop_btn.centery, center=True)

            # Info del disfraz actual
            costume = COSTUMES[current_costume]
            draw_text(f"Disfraz: {costume['name']}", font_small, costume["color"], WIDTH // 2, 460, center=True)

            # Manejo de clics
            if mouse_clicked:
                if cat_hitbox.collidepoint(mouse_pos):
                    clicks += 1
                    hand_up = True
                    hand_timer = 8
                elif shop_btn.collidepoint(mouse_pos):
                    shop_open = True

        else:
            # --- Pantalla de tienda ---
            close_rect = draw_shop()

            if mouse_clicked:
                # Cerrar
                if close_rect.collidepoint(mouse_pos):
                    shop_open = False
                else:
                    # Seleccionar disfraz
                    start_y = 160
                    for i, costume in enumerate(COSTUMES):
                        if is_unlocked(i):
                            btn_rect = pygame.Rect(550, start_y + i * 55 + 5, 100, 35)
                            if btn_rect.collidepoint(mouse_pos):
                                current_costume = i

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()