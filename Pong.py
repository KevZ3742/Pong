import pygame
import sys
import subprocess
import pyttsx3

pygame.init()

# opens Instructions.txt with notepad 
try:
    subprocess.Popen(['notepad.exe', "Instructions.txt"])
except Exception as e:
    print(f"Error: {e}")

# Set up pygame screen
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
    """
    ### Description:
    Read and speak the text content from a file.

    This function uses the pyttsx3 library to initialize a text-to-speech engine,
    reads the content of a specified file, and then speaks the text aloud.

    ### Parameters:
    - filePath (str): The path to the text file to be read.

    ### Raises:
    - FileNotFoundError: If the specified file is not found.
    - Exception: If there is an error during the text-to-speech process.

    ### Note:
    The function sets the speech rate to 150, and the pyttsx3 engine is stopped
    after speaking the text.
    """
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)

    try:
        with open(filePath, 'r') as file:
            text = file.read()

        engine.say(text)
        engine.runAndWait()

    except FileNotFoundError as e:
        print(f"Error: {e}. Please provide a valid file path.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        engine.stop()

def checkScore():
    """
    ### Description
    Check the scores of the left and right players in a game and declare a winner if the score limit is reached.

    This function examines the scores of the left and right players. If either player's score reaches 10 or more,
    the function declares the corresponding player as the winner, displays a winning message on the game screen,
    waits for 5 seconds, and then exits the game.

    ### Global Variables:
    - winner (str): The variable to store the winner's name.

    ### Note:
    The function uses the Pygame library for rendering text on the screen. Make sure Pygame is initialized
    before calling this function.
    """
    global winner

    if leftScore >= 10:
        winner = "Left Player"
    elif rightScore >= 10:
        winner = "Right Player"

    # If winner exists, display winner text and close application after 5 seconds
    if winner:
        font = pygame.font.Font(None, 72)
        winner_text = font.render(f"{winner} wins!", True, white)
        winner_rect = winner_text.get_rect(center=(width // 2, height // 2))
        screen.blit(winner_text, winner_rect)
        pygame.display.flip()
        pygame.time.wait(5000)
        pygame.quit()
        print("Game Successfully Ended.")
        sys.exit()
 
def checkPaddleBallCollision():
    """
    ### Description
    Check for collisions between the ball and the paddles, updating the ball's speed accordingly.

    This function checks whether the ball has collided with the left or right paddles. If a collision is detected,
    it updates the horizontal speed of the ball, making it bounce off the paddle. The speed is modified by
    multiplying it by the `ballSpeedMultiplier` factor.

    ### Global Variables:
    - initialSpeed (list): A list representing the initial speed of the ball in the form [x_speed, y_speed].

    ### Note:
    - The function relies on global variables for ball and paddle positions, paddle dimensions, and the speed multiplier.
    - Ensure that the `ballSpeedMultiplier` is set appropriately before calling this function.
    """
    global initialSpeed

    # Flips ball movement direction on collision and increases speed with each bounce
    if (leftPaddlePos[0] < pos[0] - radius < leftPaddlePos[0] + paddleWidth and leftPaddlePos[1] < pos[1] < leftPaddlePos[1] + paddleHeight):
        initialSpeed[0] = abs(initialSpeed[0]) * ballSpeedMultiplier
    if (rightPaddlePos[0] < pos[0] + radius < rightPaddlePos[0] + paddleWidth and rightPaddlePos[1] < pos[1] < rightPaddlePos[1] + paddleHeight):
        initialSpeed[0] = -abs(initialSpeed[0]) * ballSpeedMultiplier

def updatePaddlePositions():
    """
    ### Description:
    Update the positions of the left and right paddles based on their current speeds.

    This function modifies the vertical positions of the left and right paddles based on their respective speeds.
    It ensures that the paddles stay within the valid height range of the game window, preventing them from going
    beyond the top or bottom edges.

    ### Global Variables:
    - leftPaddleSpeed (int): The speed of the left paddle.
    - rightPaddleSpeed (int): The speed of the right paddle.
    - leftPaddlePos (list): A list representing the position of the left paddle in the form [x_position, y_position].
    - rightPaddlePos (list): A list representing the position of the right paddle in the form [x_position, y_position].
    - height (int): The height of the game window.
    - paddleHeight (int): The height of the paddles.
    """
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
    """
    ### Description:
    Draw the main menu screen for a Pong game.

    This function fills the game screen with a black background and displays the Pong title along with menu options
    for 1 Player, 2 Players, and Online play. The currently selected menu option is highlighted with a red border.

    ### Global Variables:
    - screen: The Pygame display surface.
    - width (int): The width of the game window.
    - height (int): The height of the game window.
    - menuChoice (int): The index of the currently selected menu option.

    ### Note:
    The function uses Pygame for rendering text and rectangles on the screen. Ensure that Pygame is initialized
    before calling this function.
    """
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

    # Draw red box around current choice
    pygame.draw.rect(screen, red if menuChoice == 0 else black, textRect1, 2)
    pygame.draw.rect(screen, red if menuChoice == 1 else black, textRect2, 2)
    pygame.draw.rect(screen, red if menuChoice == 2 else black, textRect3, 2)

    screen.blit(titleText, titleRect)
    screen.blit(text1, textRect1)
    screen.blit(text2, textRect2)
    screen.blit(text3, textRect3)

    pygame.display.flip()

def drawGame():
    """
    ### Description:
    Draw the game elements on the screen for a Pong game.

    This function fills the game screen with a black background and draws the game elements, including the center line,
    the ball, and the left and right paddles. It also displays the current scores for both players.

    ### Global Variables:
    - screen: The Pygame display surface.
    - width (int): The width of the game window.
    - height (int): The height of the game window.
    - pos (list): A list representing the position of the ball in the form [x_position, y_position].
    - radius (int): The radius of the ball.
    - leftPaddlePos (list): A list representing the position of the left paddle in the form [x_position, y_position].
    - rightPaddlePos (list): A list representing the position of the right paddle in the form [x_position, y_position].
    - paddleWidth (int): The width of the paddles.
    - paddleHeight (int): The height of the paddles.
    - leftScore (int): The score of the left player.
    - rightScore (int): The score of the right player.

    ### Note:
    The function uses Pygame for drawing shapes and rendering text on the screen. Ensure that Pygame is initialized
    before calling this function.
    """
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
    """
    ### Description
    Draw the difficulty selection screen for a game.

    This function fills the game screen with a black background and displays the title, current difficulty,
    and instructions for starting or going back. The difficulty level is dynamically displayed based on the
    selected difficulty index.

    ### Global Variables:
    - screen: The Pygame display surface.
    - width (int): The width of the game window.
    - height (int): The height of the game window.
    - difficultyValues (list): A list of available difficulty values.
    - selectedDifficultyIndex (int): The index of the currently selected difficulty.

    ### Note:
    The function uses Pygame for rendering text on the screen. Ensure that Pygame is initialized
    before calling this function.
    """
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

        # State machine
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