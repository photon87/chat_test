import time
import socket
import pygame
from net import Network
from message import Message
from pod import Pod
from player import Player

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

    p = Player(WIN, int(WIDTH/2), int(HEIGHT/2), 20, WHITE, RED)

    def redraw_window():
        WIN.fill(BLACK)

        fps_label = main_font.render(f"FPS: {int(clock.get_fps())}", 1, WHITE)
        WIN.blit(fps_label, (2, 2))

        if server_response:
            label = main_font.render(
                f"S: {server_response.get_message()}", 1, WHITE)
            WIN.blit(label, (2, 26))

        p.draw()

        pygame.display.flip()

    def send_msg(msg, mtype="default"):
        m = Message(name, str(msg), mtype, time.time())
        return n.send(m)

    while run:
        clock.tick(FPS)
        redraw_window()

        p.update()
        send_msg(p, "player")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                send_msg(DISCONNECT_MESSAGE)
                n.disconnect()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # send(pygame.mouse.get_pos())
                server_response = send_msg(pygame.mouse.get_pos())

        acl = 0.3

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:  # left
            p.add_acl(pygame.Vector2(-acl, 0))
        if keys[pygame.K_d]:  # right
            p.add_acl(pygame.Vector2(acl, 0))
        if keys[pygame.K_w]:  # up
            p.add_acl(pygame.Vector2(0, -acl))
        if keys[pygame.K_s]:  # down
            p.add_acl(pygame.Vector2(0, acl))


if __name__ == "__main__":
    main()
