import time
import socket
import pygame
from net import Network
from message import Message

pygame.font.init()

WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("game_a")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

DISCONNECT_MESSAGE = "!DISCONNECT"
n = Network(socket.gethostbyname(socket.gethostname()))
name = "PGCLIENT"
first = Message(name, "CONNECTED", "default", time.time())
n.connect(first)


def main():
    run = True
    FPS = 60

    main_font = pygame.font.SysFont("Arial", 24)

    clock = pygame.time.Clock()

    server_response = None

    def redraw_window():
        WIN.fill(BLACK)

        fps_label = main_font.render(f"FPS: {int(clock.get_fps())}", 1, WHITE)
        WIN.blit(fps_label, (2, 2))

        if server_response:
            label = main_font.render(f"S: {server_response.get_message()}", 1, WHITE)
            WIN.blit(label, (2, 26))

        pygame.display.flip()

    def send_msg(msg):
        m = Message(name, str(msg), "default", time.time())
        return n.send(m)

    while run:
        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                send_msg(DISCONNECT_MESSAGE)
                n.disconnect()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # send(pygame.mouse.get_pos())
                server_response=send_msg(pygame.mouse.get_pos())
                

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:  # left
            pass
        if keys[pygame.K_d]:  # right
            pass
        if keys[pygame.K_w]:  # up
            pass
        if keys[pygame.K_s]:  # down
            pass


if __name__ == "__main__":
    main()