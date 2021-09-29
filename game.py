from CONSTANTS import *
import pygame
import socket
import threading
from networking import send, recieve


def main():
    PORT = 5050
    SERVER = "176.58.109.37" #socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER, PORT)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    print("[ESTABLISHED CONNECTION] \n\n")

    pygame.init()
    clock = pygame.time.Clock()
    fps = 60
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    bg = [255, 255, 255]

    screen = pygame.display.set_mode(size)
    player_id = recieve(client)
    data = {
        "id" : player_id,
        "enemy_id" : 1 if player_id == "2" else 2,
        "game_over" : False,
        "next_player_turn" : False if player_id == "1" else True,
        "waiting" : False,
        "running" : True,
        "disconnected_first" : True 
    }

    BUTTON_SIZE = (SCREEN_WIDTH // BOARD_SIZE, SCREEN_HEIGHT // BOARD_SIZE)
    board = [[Button(BUTTON_SIZE[0]*j, BUTTON_SIZE[1]*i, BUTTON_SIZE[0], BUTTON_SIZE[1], 5, (100, 100, 100)) for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]

    
    while data["running"]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                data["running"] = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position
                for i, row in enumerate(board):
                    for j, button in enumerate(row):
                        if button.colliding(mouse_pos):
                            if data["game_over"] and not data["next_player_turn"]:
                                reset_board(board)
                                data["game_over"] = False
                            elif not button.value and not data["next_player_turn"]:
                                new_board = move(data, board, i , j)
                                send(f"{data['enemy_id']}|{new_board}", client)

        # Draw
        screen.fill(bg)
        mouse_pos = pygame.mouse.get_pos()
        for row in board:
            for button in row:
                button.draw(screen, mouse_pos)


        pygame.display.update()
        clock.tick(fps)

        if data["next_player_turn"] and not data["waiting"]:
            data["waiting"] = True
            thread = threading.Thread(target=next_player_move, args=[client, board, data])
            thread.start()

    return data, client
    
def next_player_move(client, board, data):
    msg = recieve(client)
    if msg == DISCONNECT_MESSAGE or not data["running"]:
        data["disconnected_first"] = False
        data["running"] = False
        return
    
    if data["game_over"]:
        reset_board(board)
        data["game_over"] = False


    new_board = [[x for x in row.split()] for row in msg.split(",")]
    for i, row in enumerate(new_board):
        for j, x in enumerate(row):
            if x == "X":
                board[i][j].value = "X"
            elif x == "O":
                board[i][j].value = "O"
            else:
                board[i][j].value = ""

    result = check_board(board)
    data["game_over"] = result
    data["next_player_turn"] = not data["next_player_turn"]
    if result == 1:
        print("player 1 won")
    elif result == 2:
        print("player 2 won")
    elif result == 3:
        print("Tie")

    data["waiting"] = False

def move(data, board, i, j):
    board[i][j].value = "X" if data["id"] == "1" else "O"
    result = check_board(board)
    data["game_over"] = result
    if result == 1:
        print("player 1 won")
    elif result == 2:
        print("player 2 won")
    elif result == 3:
        print("Tie")

    data["next_player_turn"] = not data["next_player_turn"]

    new_board = ""
    for row in board:
        for button in row:
            if button.value:
                new_board += button.value + " "
            else:
                new_board += "e "
        new_board = new_board[:-1]
        new_board += ","
    return new_board[:-1]

def check_board(board):
    # check rows
    for i in range(BOARD_SIZE):
        player_1_sum = 0
        player_2_sum = 0
        for j in range(BOARD_SIZE):
            if board[i][j].value == "X":
                player_1_sum += 1
            elif board[i][j].value == "O":
                player_2_sum += 1

        if player_1_sum >= BOARD_SIZE:
            return 1
        elif player_2_sum >= BOARD_SIZE:
            return 2
    
    # check columns
    for j in range(BOARD_SIZE):
        player_1_sum = 0
        player_2_sum = 0
        for i in range(BOARD_SIZE):
            if board[i][j].value == "X":
                player_1_sum += 1
            elif board[i][j].value == "O":
                player_2_sum += 1

        if player_1_sum >= BOARD_SIZE:
            return 1
        elif player_2_sum >= BOARD_SIZE:
            return 2
    
    # check for full board
    full = True
    for row in board:
        for button in row:
            if button.value == "":
                full = False
                break
    if full:
        return 3

    # check left diagonal
    player_1_sum = 0
    player_2_sum = 0
    for i in range(BOARD_SIZE):
        if board[i][i].value == "X":
            player_1_sum += 1
        elif board[i][i].value == "O":
            player_2_sum += 1

    if player_1_sum >= BOARD_SIZE:
        return 1
    elif player_2_sum >= BOARD_SIZE:
        return 2

    
    # check right diagonal
    player_1_sum = 0
    player_2_sum = 0
    for i in range(BOARD_SIZE):
        if board[i][BOARD_SIZE - (1 + i)].value == "X":
            player_1_sum += 1
        elif board[i][BOARD_SIZE - (1 + i)].value == "O":
            player_2_sum += 1

    if player_1_sum >= BOARD_SIZE:
        return 1
    elif player_2_sum >= BOARD_SIZE:
        return 2


    return 0

def reset_board(board):
    for row in board:
        for button in row:
            button.value = ""

class Button():
    def __init__(self, x, y, width, height, border_size, color):
        self.value = ""
        self.color = color
        self.button = pygame.Rect(x, y, width, height)
        self.inside_button = pygame.Rect(x + border_size, y + border_size, width - (border_size*2), height - (border_size*2))
        self.font = pygame.font.Font(None, width)
        self.text = self.font.render(f"{self.value}", True, (255, 255, 255))
        self.text_pos = (x + (width//2), 5 + y + (width//2))
        self.text_rect = self.text.get_rect(center=self.text_pos)

    def colliding(self, pos):
        if self.inside_button.collidepoint(pos):
            return True

    def draw(self, screen, mouse_pos):
        pygame.draw.rect(screen, (0, 0, 0), self.button)
        color = (150, 150 ,150) if self.colliding(mouse_pos) else self.color
        pygame.draw.rect(screen, color, self.inside_button)

        self.text = self.font.render(f"{self.value}", True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center=self.text_pos)
        screen.blit(self.text, self.text_rect)

if __name__ == '__main__':
    data, client = main()
    if data["disconnected_first"]:
        send(f"{data['enemy_id']}|{DISCONNECT_MESSAGE}", client)
    
    print("[DISCONNECTED]")