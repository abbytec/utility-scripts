import pygame
import sys
import random
import string

# --- CONSTANTES Y CONFIGURACIÓN ---

# Pantalla
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

# Colores
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
GRAY = (200, 200, 200)
DARK_GRAY = (80, 80, 80)
GREEN = (70, 200, 70)
RED = (200, 70, 70)
BLUE = (60, 120, 240)

# --- Mapa de Dificultad (fácil de modificar) ---
# Cada nivel tiene su propia configuración
DIFFICULTY_LEVELS = {
    "FACIL": {
        "TIME": 75,          # Segundos para completar
        "TARGET_SCORE": 20,   # Items a completar
        "SHUFFLE_N": 0        # Aciertos para regenerar la clave (0 = nunca)
    },
    "MEDIO": {
        "TIME": 70,
        "TARGET_SCORE": 30,
        "SHUFFLE_N": 10
    },
    "DIFICIL": {
        "TIME": 65,
        "TARGET_SCORE": 40,
        "SHUFFLE_N": 5
    }
}

# --- INICIALIZACIÓN DE PYGAME ---
pygame.init()
pygame.font.init()

# Configuración de la pantalla y el reloj
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Traductor Rápido (Entrenamiento VP)")
clock = pygame.time.Clock()

# Fuentes
FONT_KEY = pygame.font.SysFont('Arial', 36, bold=True)
FONT_STIMULUS = pygame.font.SysFont('Arial', 64, bold=True)
FONT_UI = pygame.font.SysFont('Arial', 48)
FONT_INPUT = pygame.font.SysFont('Arial', 54)
FONT_MENU = pygame.font.SysFont('Arial', 50, bold=True)
FONT_MENU_DESC = pygame.font.SysFont('Arial', 24)


def generate_key():
    """
    Genera la clave de 9 combinaciones.
    Puede ser (Números -> Letras) o (Letras -> Números).
    """
    if random.choice(["num_to_letter", "letter_to_num"]) == "num_to_letter":
        # MODO: 1-F, 2-R, 3-A...
        source_items = [str(i) for i in range(1, 10)]
        all_letters = list(string.ascii_uppercase)
        random.shuffle(all_letters)
        target_items = all_letters[:9]
        
    else:
        # MODO: A-4, B-27, C-9...
        source_items = list(string.ascii_uppercase[:9])
        target_items = [str(n) for n in random.sample(range(1, 100), 9)]

    # Crea el mapa de diccionarios para la lógica del juego
    key_map = dict(zip(source_items, target_items))
    
    return key_map, source_items, target_items

def draw_text(text, font, color, x, y, center=True):
    """Función helper para dibujar texto centrado."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def draw_key(source_items, target_items):
    """Dibuja la clave de 9 casillas en la parte superior."""
    box_width = 80
    box_height = 60
    start_x = (SCREEN_WIDTH - (9 * (box_width + 10))) // 2
    y_source = 20
    y_target = y_source + box_height + 5
    
    for i in range(9):
        current_x = start_x + i * (box_width + 10)
        
        # Casilla superior (Fuente ordenada)
        pygame.draw.rect(screen, BLUE, (current_x, y_source, box_width, box_height))
        pygame.draw.rect(screen, WHITE, (current_x+2, y_source+2, box_width-4, box_height-4))
        draw_text(source_items[i], FONT_KEY, BLACK, current_x + box_width // 2, y_source + box_height // 2)
        
        # Casilla inferior (Target desordenado)
        pygame.draw.rect(screen, DARK_GRAY, (current_x, y_target, box_width, box_height))
        pygame.draw.rect(screen, WHITE, (current_x+2, y_target+2, box_width-4, box_height-4))
        draw_text(target_items[i], FONT_KEY, BLACK, current_x + box_width // 2, y_target + box_height // 2)

def main_menu(game_buttons):
    """Dibuja el menú principal y maneja la selección de dificultad."""
    screen.fill(BLACK)
    draw_text("Selecciona la dificultad", FONT_MENU, WHITE, SCREEN_WIDTH // 2, 80)
    
    y_pos = 180
    for level, config in DIFFICULTY_LEVELS.items():
        # Dibuja el botón
        button_rect = pygame.Rect((SCREEN_WIDTH // 2) - 200, y_pos, 400, 100)
        game_buttons[level] = button_rect
        
        # Lógica de hover (cambio de color)
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, BLUE, button_rect)
        else:
            pygame.draw.rect(screen, DARK_GRAY, button_rect)
            
        pygame.draw.rect(screen, WHITE, button_rect, 3) # Borde
        
        # Texto del botón (Título)
        draw_text(level, FONT_UI, WHITE, SCREEN_WIDTH // 2, y_pos + 40)
        
        # Texto del botón (Descripción)
        time = config["TIME"]
        target = config["TARGET_SCORE"]
        shuffle_n = config["SHUFFLE_N"]
        
        shuffle_text = f"shuffle c/{shuffle_n}" if shuffle_n > 0 else "sin shuffle"
        desc_text = f"{time}s | {target} aciertos | {shuffle_text}"
        draw_text(desc_text, FONT_MENU_DESC, GRAY, SCREEN_WIDTH // 2, y_pos + 75)
        
        y_pos += 130
        
    pygame.display.flip()

def game_over_screen(win):
    """Dibuja la pantalla de victoria o derrota."""
    screen.fill(BLACK)
    if win:
        draw_text("¡GANASTE!", FONT_MENU, GREEN, SCREEN_WIDTH // 2, 200)
    else:
        draw_text("¡SE ACABÓ EL TIEMPO!", FONT_MENU, RED, SCREEN_WIDTH // 2, 200)
    
    # Botón para volver al menú
    menu_button = pygame.Rect((SCREEN_WIDTH // 2) - 200, 350, 400, 80)
    
    mouse_pos = pygame.mouse.get_pos()
    if menu_button.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BLUE, menu_button)
    else:
        pygame.draw.rect(screen, DARK_GRAY, menu_button)
    
    pygame.draw.rect(screen, WHITE, menu_button, 3) # Borde
    draw_text("Volver al Menú", FONT_UI, WHITE, SCREEN_WIDTH // 2, 350 + 40)
    
    pygame.display.flip()
    return menu_button

def run_game():
    """Loop principal del juego."""
    
    game_state = "MENU"
    
    # --- Variables de Nivel (se cargan al elegir dificultad) ---
    current_time_limit = 0
    current_target_score = 0
    current_shuffle_n = 0
    
    # --- Variables de Partida (se resetean cada partida) ---
    key_map = {}
    source_items = []
    target_items = []
    stimuli_to_present = []
    current_stimulus_index = 0
    current_stimulus = ""
    correct_answer = ""
    user_input = ""
    score = 0
    start_time = 0
    win = False
    
    game_buttons = {}
    menu_button_rect = None

    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if game_state == "GAME":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        
                        # Comprobar respuesta
                        if user_input.upper() == correct_answer.upper():
                            score += 1
                            user_input = ""
                            
                            # --- LÓGICA DE VICTORIA Y BARAJADO ---
                            
                            # 1. ¿Ganó?
                            if score >= current_target_score:
                                game_state = "GAME_OVER"
                                win = True
                            
                            # 2. ¿Toca barajar? (y no es 0, y aún no ganó)
                            elif (current_shuffle_n > 0) and (score % current_shuffle_n == 0):
                                # ¡REGENERAR CLAVE COMPLETA!
                                key_map, source_items, target_items = generate_key()
                                stimuli_to_present = random.choices(source_items, k=current_target_score * 2)
                                current_stimulus_index = 0
                            
                            # 3. Siguiente estímulo (si no ganó ni barajó)
                            else:
                                current_stimulus_index += 1
                                if current_stimulus_index >= len(stimuli_to_present):
                                    # Recargar estímulos si se acaban
                                    stimuli_to_present = random.choices(source_items, k=current_target_score * 2)
                                    current_stimulus_index = 0
                        
                        else:
                            # Falló, solo limpiar input
                            user_input = ""

                        # Actualizar el estímulo (si no ha ganado)
                        if game_state == "GAME":
                            current_stimulus = stimuli_to_present[current_stimulus_index]
                            correct_answer = key_map[current_stimulus]

                    elif event.unicode.isalnum(): # Acepta letras y números
                        user_input += event.unicode
                        
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == "MENU":
                    for level, rect in game_buttons.items():
                        if rect.collidepoint(event.pos):
                            # --- INICIAR JUEGO ---
                            game_state = "GAME"
                            
                            # Cargar config del nivel
                            config = DIFFICULTY_LEVELS[level]
                            current_time_limit = config["TIME"]
                            current_target_score = config["TARGET_SCORE"]
                            current_shuffle_n = config["SHUFFLE_N"]
                            
                            # Generar primera clave
                            key_map, source_items, target_items = generate_key()
                            
                            # Generar lista de estímulos
                            stimuli_to_present = random.choices(source_items, k=current_target_score * 2)
                            
                            # Resetear variables de partida
                            current_stimulus_index = 0
                            current_stimulus = stimuli_to_present[0]
                            correct_answer = key_map[current_stimulus]
                            score = 0
                            user_input = ""
                            start_time = pygame.time.get_ticks()
                            
                elif game_state == "GAME_OVER":
                    if menu_button_rect and menu_button_rect.collidepoint(event.pos):
                        game_state = "MENU"
                        
        
        # --- Lógica de Estados y Dibujado ---
        
        if game_state == "MENU":
            main_menu(game_buttons)
            
        elif game_state == "GAME":
            # Lógica del tiempo
            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
            time_left = current_time_limit - elapsed_time
            
            if time_left <= 0:
                game_state = "GAME_OVER"
                win = False
                time_left = 0
                
            # --- Dibujar Interfaz del Juego ---
            screen.fill(BLACK)
            
            # 1. Dibujar la clave
            draw_key(source_items, target_items)
            
            # 2. Dibujar Estímulo
            draw_text("TRADUCE:", FONT_UI, GRAY, SCREEN_WIDTH // 2, 230)
            draw_text(current_stimulus, FONT_STIMULUS, WHITE, SCREEN_WIDTH // 2, 300)
            
            # 3. Dibujar Caja de Input
            input_box_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 380, 200, 70)
            pygame.draw.rect(screen, DARK_GRAY, input_box_rect)
            pygame.draw.rect(screen, WHITE, input_box_rect, 3) # Borde
            draw_text(user_input, FONT_INPUT, WHITE, SCREEN_WIDTH // 2, 415)
            
            # 4. Dibujar HUD (Score y Tiempo)
            score_text = f"Completados: {score} / {current_target_score}"
            draw_text(score_text, FONT_UI, GREEN, SCREEN_WIDTH // 2, 530)
            
            time_text = f"Tiempo: {int(time_left // 60)}:{int(time_left % 60):02d}"
            time_color = RED if time_left < 10 else WHITE
            draw_text(time_text, FONT_UI, time_color, SCREEN_WIDTH // 2, 570)
            
            pygame.display.flip()

        elif game_state == "GAME_OVER":
            menu_button_rect = game_over_screen(win)

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_game()
