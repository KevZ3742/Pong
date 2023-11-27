import pygame
import sys

pygame.init()
width, height = 800, 450
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong")

white = (255, 255, 255)
black = (0, 0, 0)

radius = 15
speed = [5, 5]

pos = [width // 2, height // 2]

leftScore = 0
rightScore = 0

def checkScore():
    if leftScore >= 10 or rightScore >= 10:
        print("Game Over!")
        pygame.quit()

        # do the turtle thing here cause this is where the game ends
        sys.exit()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pos[0] += speed[0]
    pos[1] += speed[1]

    if pos[0] - radius < 0:
        rightScore += 1
        pos = [width // 2, height // 2]
        speed[0] = abs(speed[0])
    elif pos[0] + radius > width:
        leftScore += 1
        pos = [width // 2, height // 2]
        speed[0] = -abs(speed[0])

    if pos[1] - radius < 0 or pos[1] + radius > height:
        speed[1] = -speed[1]

    checkScore()

    screen.fill(black)

    lineThickness = 5
    pygame.draw.line(screen, white, (width // 2, 0), (width // 2, height), lineThickness)
    pygame.draw.circle(screen, white, (int(pos[0]), int(pos[1])), radius)

    font = pygame.font.Font(None, 36)

    leftNumberText = font.render(str(leftScore), True, white)
    rightNumberText = font.render(str(rightScore), True, white)

    screen.blit(leftNumberText, (width // 4, height // 15))
    screen.blit(rightNumberText, (width * 3 // 4, height // 15))

    pygame.display.flip()
    pygame.time.Clock().tick(30)