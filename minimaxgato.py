"""
Juego de Gato (Tic-Tac-Toe) con Pygame y visualización del árbol Minimax

Características:
- Menú de inicio gráfico con Pygame
- Juego visual con interfaz gráfica
- Impresión en consola del árbol de estados de Minimax con indentación
- IA óptima usando el algoritmo Minimax

Controles:
- Click en el menú para elegir X o O
- Click en las casillas del tablero para jugar
- Botón "Nueva Partida" para reiniciar
"""

import pygame
import math
import sys

# Constantes del juego
WIN_COMBINATIONS = [
    (0,1,2), (3,4,5), (6,7,8),  # filas
    (0,3,6), (1,4,7), (2,5,8),  # columnas
    (0,4,8), (2,4,6)            # diagonales
]

# Constantes de Pygame
WINDOW_SIZE = 600
GRID_SIZE = 3
CELL_SIZE = WINDOW_SIZE // GRID_SIZE
LINE_WIDTH = 15
CIRCLE_RADIUS = CELL_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = CELL_SIZE // 4

# Colores
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (100, 100, 200)
BUTTON_HOVER = (150, 150, 255)

# Variables globales para visualización
PRINT_TREE = True  # Activar/desactivar impresión del árbol

def print_board_state(board, depth, prefix=""):
    """Imprime el estado del tablero con formato ASCII para visualización"""
    if not PRINT_TREE:
        return
    print(f"{prefix}Tablero (depth={depth}):")
    for i in range(3):
        row = board[i*3:(i+1)*3]
        print(f"{prefix}  {' | '.join([c if c != ' ' else '·' for c in row])}")

def available_moves(board):
    return [i for i, c in enumerate(board) if c == ' ']

def check_winner(board):
    for a, b, c in WIN_COMBINATIONS:
        if board[a] == board[b] == board[c] and board[a] != ' ':
            return board[a]
    if ' ' not in board:
        return 'Tie'
    return None

def minimax(board, depth, is_maximizing, ai_player, hu_player, print_tree=False):
    """
    Algoritmo Minimax con visualización del árbol de estados
    """
    indent = "  " * depth
    winner = check_winner(board)
    
    if winner == ai_player:
        score = 10 - depth
        if print_tree:
            print(f"{indent}├─ Nodo terminal: IA gana, score={score}")
        return score
    elif winner == hu_player:
        score = depth - 10
        if print_tree:
            print(f"{indent}├─ Nodo terminal: Humano gana, score={score}")
        return score
    elif winner == 'Tie':
        if print_tree:
            print(f"{indent}├─ Nodo terminal: Empate, score=0")
        return 0

    moves = available_moves(board)
    
    if is_maximizing:
        best_score = -math.inf
        if print_tree:
            print(f"{indent}├─ Nodo MAX (IA={ai_player}) depth={depth}, {len(moves)} movimientos")
        
        for i, move in enumerate(moves):
            board[move] = ai_player
            if print_tree:
                print(f"{indent}│  ├─ Probando movimiento {move+1}:")
            score = minimax(board, depth+1, False, ai_player, hu_player, print_tree)
            board[move] = ' '
            
            if print_tree:
                print(f"{indent}│  │  └─ Score recibido: {score}")
            
            if score > best_score:
                best_score = score
        
        if print_tree:
            print(f"{indent}│  └─ Mejor score MAX: {best_score}")
        return best_score
    else:
        best_score = math.inf
        if print_tree:
            print(f"{indent}├─ Nodo MIN (Humano={hu_player}) depth={depth}, {len(moves)} movimientos")
        
        for i, move in enumerate(moves):
            board[move] = hu_player
            if print_tree:
                print(f"{indent}│  ├─ Probando movimiento {move+1}:")
            score = minimax(board, depth+1, True, ai_player, hu_player, print_tree)
            board[move] = ' '
            
            if print_tree:
                print(f"{indent}│  │  └─ Score recibido: {score}")
            
            if score < best_score:
                best_score = score
        
        if print_tree:
            print(f"{indent}│  └─ Mejor score MIN: {best_score}")
        return best_score

def best_move(board, ai_player, hu_player):
    """Encuentra el mejor movimiento para la IA e imprime el árbol de búsqueda"""
    print("\n" + "="*60)
    print("ÁRBOL DE BÚSQUEDA MINIMAX")
    print("="*60)
    
    best_score = -math.inf
    move_choice = None
    moves = available_moves(board)
    
    print(f"Evaluando {len(moves)} movimientos posibles desde el estado actual:")
    print_board_state(board, 0, "")
    print()
    
    for move in moves:
        board[move] = ai_player
        print(f"\n┌─ Evaluando movimiento en posición {move+1} (IA juega {ai_player}):")
        score = minimax(board, 0, False, ai_player, hu_player, print_tree=True)
        board[move] = ' '
        
        print(f"└─ Score final para movimiento {move+1}: {score}")
        
        if score > best_score:
            best_score = score
            move_choice = move
    
    print(f"\n{'='*60}")
    print(f"DECISIÓN: Mejor movimiento = posición {move_choice+1}, score = {best_score}")
    print(f"{'='*60}\n")
    
    return move_choice

class TicTacToeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption('Gato - Minimax')
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 74)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        
        self.state = 'menu'  # 'menu', 'playing', 'game_over'
        self.board = [' '] * 9
        self.hu_player = None
        self.ai_player = None
        self.hu_turn = False
        self.winner = None
        self.button_rect = None
    
    def draw_menu(self):
        """Dibuja el menú de inicio"""
        self.screen.fill(BG_COLOR)
        
        # Título
        title = self.font_large.render('GATO - MINIMAX', True, TEXT_COLOR)
        title_rect = title.get_rect(center=(WINDOW_SIZE//2, 100))
        self.screen.blit(title, title_rect)
        
        # Subtítulo
        subtitle = self.font_small.render('Elige tu símbolo:', True, TEXT_COLOR)
        subtitle_rect = subtitle.get_rect(center=(WINDOW_SIZE//2, 200))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Botones X y O
        mouse_pos = pygame.mouse.get_pos()
        
        # Botón X
        x_button = pygame.Rect(150, 280, 120, 120)
        x_color = BUTTON_HOVER if x_button.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(self.screen, x_color, x_button, border_radius=10)
        x_text = self.font_large.render('X', True, TEXT_COLOR)
        x_text_rect = x_text.get_rect(center=x_button.center)
        self.screen.blit(x_text, x_text_rect)
        
        # Botón O
        o_button = pygame.Rect(330, 280, 120, 120)
        o_color = BUTTON_HOVER if o_button.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(self.screen, o_color, o_button, border_radius=10)
        o_text = self.font_large.render('O', True, TEXT_COLOR)
        o_text_rect = o_text.get_rect(center=o_button.center)
        self.screen.blit(o_text, o_text_rect)
        
        # Nota
        note = self.font_small.render('(X juega primero)', True, TEXT_COLOR)
        note_rect = note.get_rect(center=(WINDOW_SIZE//2, 450))
        self.screen.blit(note, note_rect)
        
        return x_button, o_button
    
    def draw_lines(self):
        """Dibuja las líneas del tablero"""
        # Líneas horizontales
        pygame.draw.line(self.screen, LINE_COLOR, (0, CELL_SIZE), 
                        (WINDOW_SIZE, CELL_SIZE), LINE_WIDTH)
        pygame.draw.line(self.screen, LINE_COLOR, (0, 2 * CELL_SIZE), 
                        (WINDOW_SIZE, 2 * CELL_SIZE), LINE_WIDTH)
        
        # Líneas verticales
        pygame.draw.line(self.screen, LINE_COLOR, (CELL_SIZE, 0), 
                        (CELL_SIZE, WINDOW_SIZE), LINE_WIDTH)
        pygame.draw.line(self.screen, LINE_COLOR, (2 * CELL_SIZE, 0), 
                        (2 * CELL_SIZE, WINDOW_SIZE), LINE_WIDTH)
    
    def draw_figures(self):
        """Dibuja X y O en el tablero"""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                idx = row * GRID_SIZE + col
                if self.board[idx] == 'O':
                    center = (col * CELL_SIZE + CELL_SIZE // 2, 
                             row * CELL_SIZE + CELL_SIZE // 2)
                    pygame.draw.circle(self.screen, CIRCLE_COLOR, center, 
                                     CIRCLE_RADIUS, CIRCLE_WIDTH)
                elif self.board[idx] == 'X':
                    start_desc = (col * CELL_SIZE + SPACE, 
                                 row * CELL_SIZE + SPACE)
                    end_desc = (col * CELL_SIZE + CELL_SIZE - SPACE, 
                               row * CELL_SIZE + CELL_SIZE - SPACE)
                    pygame.draw.line(self.screen, CROSS_COLOR, start_desc, 
                                   end_desc, CROSS_WIDTH)
                    
                    start_asc = (col * CELL_SIZE + SPACE, 
                                row * CELL_SIZE + CELL_SIZE - SPACE)
                    end_asc = (col * CELL_SIZE + CELL_SIZE - SPACE, 
                              row * CELL_SIZE + SPACE)
                    pygame.draw.line(self.screen, CROSS_COLOR, start_asc, 
                                   end_asc, CROSS_WIDTH)
    
    def draw_game_over(self):
        """Dibuja la pantalla de game over"""
        # Semi-transparente overlay
        overlay = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
        overlay.set_alpha(200)
        overlay.fill(BG_COLOR)
        self.screen.blit(overlay, (0, 0))
        
        # Mensaje de ganador
        if self.winner == 'Tie':
            msg = '¡EMPATE!'
        else:
            msg = f'¡Gana {self.winner}!'
        
        text = self.font_large.render(msg, True, TEXT_COLOR)
        text_rect = text.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//2 - 50))
        self.screen.blit(text, text_rect)
        
        # Botón de nueva partida
        mouse_pos = pygame.mouse.get_pos()
        button = pygame.Rect(150, 400, 300, 60)
        button_color = BUTTON_HOVER if button.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(self.screen, button_color, button, border_radius=10)
        
        button_text = self.font_medium.render('Nueva Partida', True, TEXT_COLOR)
        button_text_rect = button_text.get_rect(center=button.center)
        self.screen.blit(button_text, button_text_rect)
        
        self.button_rect = button
    
    def handle_click_menu(self, pos):
        """Maneja clicks en el menú"""
        x_button = pygame.Rect(150, 280, 120, 120)
        o_button = pygame.Rect(330, 280, 120, 120)
        
        if x_button.collidepoint(pos):
            self.hu_player = 'X'
            self.ai_player = 'O'
            self.hu_turn = True  # X empieza
            self.start_game()
        elif o_button.collidepoint(pos):
            self.hu_player = 'O'
            self.ai_player = 'X'
            self.hu_turn = False  # IA (X) empieza
            self.start_game()
    
    def start_game(self):
        """Inicia una nueva partida"""
        self.board = [' '] * 9
        self.state = 'playing'
        self.winner = None
        print(f"\n{'='*60}")
        print(f"NUEVA PARTIDA: Humano={self.hu_player}, IA={self.ai_player}")
        print(f"{'='*60}\n")
        
        # Si la IA empieza, hace su movimiento
        if not self.hu_turn:
            self.ai_move()
    
    def handle_click_game(self, pos):
        """Maneja clicks durante el juego"""
        if not self.hu_turn:
            return
        
        col = pos[0] // CELL_SIZE
        row = pos[1] // CELL_SIZE
        idx = row * GRID_SIZE + col
        
        if self.board[idx] == ' ':
            self.board[idx] = self.hu_player
            print(f"\nJugador humano ({self.hu_player}) juega en posición {idx+1}")
            
            winner = check_winner(self.board)
            if winner:
                self.winner = winner
                self.state = 'game_over'
            else:
                self.hu_turn = False
                # IA juega después de un pequeño delay
                pygame.time.set_timer(pygame.USEREVENT, 500)
    
    def ai_move(self):
        """La IA hace su movimiento"""
        if available_moves(self.board):
            move = best_move(self.board, self.ai_player, self.hu_player)
            if move is not None:
                self.board[move] = self.ai_player
                print(f"\nIA ({self.ai_player}) juega en posición {move+1}")
                
                winner = check_winner(self.board)
                if winner:
                    self.winner = winner
                    self.state = 'game_over'
                else:
                    self.hu_turn = True
    
    def handle_click_game_over(self, pos):
        """Maneja clicks en la pantalla de game over"""
        if self.button_rect and self.button_rect.collidepoint(pos):
            self.state = 'menu'
    
    def run(self):
        """Loop principal del juego"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == 'menu':
                        self.handle_click_menu(event.pos)
                    elif self.state == 'playing':
                        self.handle_click_game(event.pos)
                    elif self.state == 'game_over':
                        self.handle_click_game_over(event.pos)
                
                elif event.type == pygame.USEREVENT:
                    # Timer para que la IA juegue
                    pygame.time.set_timer(pygame.USEREVENT, 0)  # Desactiva timer
                    if self.state == 'playing' and not self.hu_turn:
                        self.ai_move()
            
            # Dibujar
            if self.state == 'menu':
                self.draw_menu()
            elif self.state == 'playing' or self.state == 'game_over':
                self.screen.fill(BG_COLOR)
                self.draw_lines()
                self.draw_figures()
                
                if self.state == 'game_over':
                    self.draw_game_over()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = TicTacToeGame()
    game.run()