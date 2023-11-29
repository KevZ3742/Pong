import pygame
import sys
import subprocess
import pyttsx3

pygame.init()

try:
    subprocess.Popen(['notepad.exe', "Instructions.txt"])
except Exception as e:
    print(f"Error: {e}")

width, height = 800, 450
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong")

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

radius, initialSpeed, ballSpeedMultiplier = 15, [5, 5], 1.1
pos = [width // 2, height // 2]
leftScore, rightScore = 0, 0
paddleWidth, paddleHeight = 10, 80
playerSpeed, leftPaddleSpeed, rightPaddleSpeed = 7, 0, 0
leftPaddlePos, rightPaddlePos = [20, height // 2 - paddleHeight // 2], [width - paddleWidth - 20, height // 2 - paddleHeight // 2]

gameState = "menu"
menuChoice = 0

difficultyValues = [1, 2, 3, 4, 5]
selectedDifficultyIndex = 0
winner = None

def SpeakText(filePath):
    engine = pyttsx3.init()

    engine.setProperty('rate', 150)

    try:
        with open(filePath, 'r') as file:
            text = file.read()

        engine.say(text)
        engine.runAndWait()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        engine.stop()

def checkScore():
    global winner

    if leftScore >= 10:
        winner = "Left Player"
    elif rightScore >= 10:
        winner = "Right Player"

    if winner:
        font = pygame.font.Font(None, 72)
        winner_text = font.render(f"{winner} wins!", True, white)
        winner_rect = winner_text.get_rect(center=(width // 2, height // 2))
        screen.blit(winner_text, winner_rect)
        pygame.display.flip()
        pygame.time.wait(5000)
        pygame.quit()
        sys.exit()
 
def checkPaddleBallCollision():
    global initialSpeed

    if (leftPaddlePos[0] < pos[0] - radius < leftPaddlePos[0] + paddleWidth and leftPaddlePos[1] < pos[1] < leftPaddlePos[1] + paddleHeight):
        initialSpeed[0] = abs(initialSpeed[0]) * ballSpeedMultiplier
    if (rightPaddlePos[0] < pos[0] + radius < rightPaddlePos[0] + paddleWidth and rightPaddlePos[1] < pos[1] < rightPaddlePos[1] + paddleHeight):
        initialSpeed[0] = -abs(initialSpeed[0]) * ballSpeedMultiplier

def updatePaddlePositions():
    global leftPaddleSpeed, rightPaddleSpeed

    leftPaddlePos[1] += leftPaddleSpeed
    if leftPaddlePos[1] < 0:
        leftPaddlePos[1] = 0
    elif leftPaddlePos[1] > height - paddleHeight:
        leftPaddlePos[1] = height - paddleHeight

    rightPaddlePos[1] += rightPaddleSpeed
    if rightPaddlePos[1] < 0:
        rightPaddlePos[1] = 0
    elif rightPaddlePos[1] > height - paddleHeight:
        rightPaddlePos[1] = height - paddleHeight

def drawMenu():
    screen.fill(black)
    fontTitle = pygame.font.Font(None, 72)
    fontMenu = pygame.font.Font(None, 36)
    titleText = fontTitle.render("Pong", True, white)
    titleRect = titleText.get_rect(center=(width // 2, height // 4))
    text1 = fontMenu.render("1 Player", True, white)
    text2 = fontMenu.render("2 Players", True, white)
    text3 = fontMenu.render("Online", True, white)
    textRect1 = text1.get_rect(center=(width // 2, height // 2 - 50))
    textRect2 = text2.get_rect(center=(width // 2, height // 2))
    textRect3 = text3.get_rect(center=(width // 2, height // 2 + 50))

    pygame.draw.rect(screen, red if menuChoice == 0 else black, textRect1, 2)
    pygame.draw.rect(screen, red if menuChoice == 1 else black, textRect2, 2)
    pygame.draw.rect(screen, red if menuChoice == 2 else black, textRect3, 2)

    screen.blit(titleText, titleRect)
    screen.blit(text1, textRect1)
    screen.blit(text2, textRect2)
    screen.blit(text3, textRect3)

    pygame.display.flip()

def drawGame():
    screen.fill(black)
    pygame.draw.line(screen, white, (width // 2, 0), (width // 2, height), 5)
    pygame.draw.circle(screen, white, (int(pos[0]), int(pos[1])), radius)
    pygame.draw.rect(screen, white, (leftPaddlePos[0], leftPaddlePos[1], paddleWidth, paddleHeight))
    pygame.draw.rect(screen, white, (rightPaddlePos[0], rightPaddlePos[1], paddleWidth, paddleHeight))

    font = pygame.font.Font(None, 36)
    leftNumberText = font.render(str(leftScore), True, white)
    rightNumberText = font.render(str(rightScore), True, white)

    screen.blit(leftNumberText, (width // 4, height // 15))
    screen.blit(rightNumberText, (width * 3 // 4, height // 15))

    pygame.display.flip()

def drawDifficultyScreen():
    screen.fill(black)
    fontTitle = pygame.font.Font(None, 72)
    fontMenu = pygame.font.Font(None, 36)

    titleText = fontTitle.render("Select Difficulty", True, white)
    titleRect = titleText.get_rect(center=(width // 2, height // 4))
    difficultyText = fontMenu.render(f"Difficulty: {difficultyValues[selectedDifficultyIndex]}", True, white)
    difficultyRect = difficultyText.get_rect(center=(width // 2, height // 2))
    startText = fontMenu.render("Press ENTER to Start", True, white)
    startRect = startText.get_rect(center=(width // 2, height // 2 + 50))
    backText = fontMenu.render("Press ESC to Go Back", True, white)
    backRect = backText.get_rect(center=(width // 2, height // 2 + 100))

    screen.blit(titleText, titleRect)
    screen.blit(difficultyText, difficultyRect)
    screen.blit(startText, startRect)
    screen.blit(backText, backRect)

    pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if gameState == "menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    menuChoice = (menuChoice + 1) % 3
                elif event.key == pygame.K_UP:
                    menuChoice = (menuChoice - 1) % 3
                elif event.key == pygame.K_RETURN:
                    if menuChoice == 0:
                        gameState = "difficulty screen"
                    elif menuChoice == 1:
                        gameState = "playing 2p"
                    elif menuChoice == 2:
                        executablePath = r'PongUnity.exe'
                        try:
                            subprocess.run([executablePath], check=True)
                        except subprocess.CalledProcessError as e:
                            print(f"Error: {e}")
                elif event.key == pygame.K_p:
                    executablePath = r'PythonLogo.py'
                    try:
                        subprocess.run(["python" ,executablePath], check=True)
                    except subprocess.CalledProcessError as e:
                        print(f"Error: {e}")
                elif event.key == pygame.K_i:
                    SpeakText("Instructions.txt")

        elif gameState == "difficulty screen":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selectedDifficultyIndex = (selectedDifficultyIndex + 1) % len(difficultyValues)
                elif event.key == pygame.K_UP:
                    selectedDifficultyIndex = (selectedDifficultyIndex - 1) % len(difficultyValues)
                elif event.key == pygame.K_RETURN:
                    gameState = "playing"

                elif event.key == pygame.K_ESCAPE:
                    gameState = "menu"

        elif gameState == "playing":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    leftPaddleSpeed = -playerSpeed
                elif event.key == pygame.K_s:
                    leftPaddleSpeed = playerSpeed

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    leftPaddleSpeed = 0

        elif gameState == "playing 2p":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    leftPaddleSpeed = -playerSpeed
                elif event.key == pygame.K_s:
                    leftPaddleSpeed = playerSpeed
                elif event.key == pygame.K_UP:
                    rightPaddleSpeed = -playerSpeed
                elif event.key == pygame.K_DOWN:
                    rightPaddleSpeed = playerSpeed

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    leftPaddleSpeed = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    rightPaddleSpeed = 0

    if gameState == "menu":
        drawMenu()
    elif gameState == "difficulty screen":
        drawDifficultyScreen()
    elif gameState == "playing":
        pos[0] += initialSpeed[0]
        pos[1] += initialSpeed[1]
        updatePaddlePositions()

        if pos[0] - radius < 0:
            rightScore += 1
            pos = [width // 2, height // 2]
            initialSpeed = [-5, -5]
        elif pos[0] + radius > width:
            leftScore += 1
            pos = [width // 2, height // 2]
            initialSpeed = [5, 5]

        if pos[1] - radius < 0 or pos[1] + radius > height:
            initialSpeed[1] = -initialSpeed[1]

        checkScore()
        checkPaddleBallCollision()

        cpuDifficulty = difficultyValues[selectedDifficultyIndex]
        if pos[1] > rightPaddlePos[1] + paddleHeight // 2:
            rightPaddleSpeed = playerSpeed / (6 - cpuDifficulty)
        elif pos[1] < rightPaddlePos[1] + paddleHeight // 2:
            rightPaddleSpeed = -playerSpeed / (6 - cpuDifficulty)
        else:
            rightPaddleSpeed = 0

        drawGame()
        pygame.time.Clock().tick(60)

    elif gameState == "playing 2p":
        pos[0] += initialSpeed[0]
        pos[1] += initialSpeed[1]

        updatePaddlePositions()

        if pos[0] - radius < 0:
            rightScore += 1
            pos = [width // 2, height // 2]
            initialSpeed = [-5, -5]
        elif pos[0] + radius > width:
            leftScore += 1
            pos = [width // 2, height // 2]
            initialSpeed = [5, 5]

        if pos[1] - radius < 0 or pos[1] + radius > height:
            initialSpeed[1] = -initialSpeed[1]

        checkScore()
        checkPaddleBallCollision()
        drawGame()
        pygame.time.Clock().tick(60)