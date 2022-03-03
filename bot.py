# Imports
import re
import json
import time
import random
import shutil
from InquirerPy import inquirer
from selenium import webdriver
from stockfish import Stockfish
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException

# Temporary Variable
prevFen = ""
prevMoves = []
status = "Waiting..."

# Get User Configuration
threads = inquirer.number(message="Threads: ", default=8, max_allowed=256, min_allowed=1, long_instruction="Number of threads allocated to Stockfish").execute()
depth = inquirer.number(message="Depth: ", default=12, max_allowed=50, min_allowed=1, long_instruction="Depth Stockfish will analyze moves with").execute()
automated = inquirer.confirm(message = "Enable Automation", default=False, long_instruction="Enable a bot which will automatically play for you (beta)?").execute()

if automated:
    global minDelay
    global maxDelay
    minDelay = inquirer.number(message="Minimum Move Delay", default=0, min_allowed=0, max_allowed=60, long_instruction="The minimum time between moves that are automatically played").execute()
    maxDelay = inquirer.number(message="Maximum Move Delay", default=5, min_allowed=0, max_allowed=60, long_instruction="The maximum time between moves that are automatically played").execute()

# Configure StockFish
stockfish = Stockfish(parameters={"Threads" : threads})
stockfish.set_depth(depth)

# Configure WebDriver
capabilities = webdriver.DesiredCapabilities.CHROME.copy()
capabilities['goog:loggingPrefs'] = { 'performance':'ALL' }
driver = webdriver.Chrome(desired_capabilities=capabilities)
driver.get("https://lichess.org")

# Web Socket Log
def getWSLog():
    payloadCache = []
    for wsData in driver.get_log('performance'):
        wsJson = json.loads((wsData['message']))
        if wsJson["message"]["method"]== "Network.webSocketFrameReceived":
            payloadCache.append(wsJson["message"]["params"]["response"]["payloadData"])
    return payloadCache

# FEN
def getFen():
    for i in reversed(getWSLog()):
        newFen = re.findall(r'fen":"(.*?)"', i)
        if len(newFen) != 0:
            return str(newFen[0])
    return None
            
# Play Move (Uses data from arrow to find locations)
def playMove():
    try:
        # Get board and piece size!
        chessBoard = driver.find_element(By.TAG_NAME, "cg-container")
        boardSize = str(chessBoard.value_of_css_property("width"))
        boardSize = int(boardSize[0:len(boardSize) - 2:1])
        pieceSize = boardSize / 8

        # Find piece position from line
        line = driver.find_element(By.ID, "chessbot_line")
        startX = (float(line.get_attribute("x1")) + 3.5) * pieceSize
        startY = (float(line.get_attribute("y1")) + 3.5) * pieceSize

        # Find offset from piece
        endX = (float(line.get_attribute("x2")) + 3.5) * pieceSize
        endY = (float(line.get_attribute("y2")) + 3.5) * pieceSize
        endXOffset = endX - startX
        endYOffset = endY - startY

        # Find Piece
        pieces = driver.find_elements(By.TAG_NAME, "piece")
        for piece in pieces:
            if str(piece.value_of_css_property("transform")) == "matrix(1, 0, 0, 1, " + str(startX).strip(".0") + ", " + str(startY).strip(".0") + ")":
                # Move Piece
                action = ActionChains(driver)
                action.move_to_element_with_offset(piece, 0.5*pieceSize, 0.5*pieceSize)
                action.click()
                action.move_by_offset(endXOffset, endYOffset)
                action.click()
                action.perform()
    except StaleElementReferenceException as e:
        # Taking pieces causes them to become stale (as they have just been deleted)
        # This causes Selenium to create an error
        pass
    except Exception as e:
        print(e)

# Remove Arrow
def removeArrow():
    driver.execute_script("null!=document.getElementById('chessbot_line')&&(element=document.getElementById('chessbot_line'),element.parentNode.removeChild(element));")

# Draw Arrow
def drawArrow(move):
    g = driver.find_element(By.TAG_NAME ,"g")
    corr = -1 if 'orientation-black' in driver.page_source else 1
    coords = 'x1="c1" y1="c2" x2="c3" y2="c4"'
    coords = coords.replace("c1", str(corr*((ord(move[0]) & 31)-4.5)))
    coords = coords.replace("c2", str(corr*(4.5 - float(move[1]))))
    coords = coords.replace("c3", str(corr*((ord(move[2]) & 31)-4.5)))
    coords = coords.replace("c4", str(corr*(4.5 - float(move[3]))))
    arrow = '<line id="chessbot_line" stroke="#15781B" stroke-width="0.15625" stroke-linecap="round" marker-end="url(#arrowhead-g)" opacity="1" cgHash="288,288,green"' + coords + '></line>'
    script = "var ele=arguments[0]; ele.innerHTML = '" + arrow + "';"
    driver.execute_script(script, g)

# TUI
def refreshTUI():
    # Clear Terminal
    print(chr(27) + "[2J")
    # Print Status
    print(str("_" * (len(status) + 4)).center(shutil.get_terminal_size().columns))
    print(str("| " + status + " |").center(shutil.get_terminal_size().columns))
    print(str("¯" * (len(status) + 4)).center(shutil.get_terminal_size().columns))
    # Print Moves
    i = len(prevMoves) - (shutil.get_terminal_size().lines - 6)
    i = 0 if i < 0 else i
    print("\nPrevious Moves:")
    while i < len(prevMoves):
        print(prevMoves[i])
        i += 1


# Simple Checks
def inGame():
    return True if '<button class="fbt resign" title="Resign"><span' in driver.page_source else False

def isPlaying():
    return True if 'Your turn - Play' in driver.title else False

def getSide():
    return ' b' if 'black manipulable' in driver.page_source else ' w'

# Game Loop
while True:
    refreshTUI()
    try:
        # Make sure you are in a game
        newFen = getFen()
        status = "Waiting for a game to start... (Opening moves must be played manually)"
        if inGame():
            status = "Waiting for opponent to play"
            if newFen != None:
                # Make sure a move has been played
                if newFen != prevFen:
                    prevFen = newFen
                    # Remove Previous Arrow
                    removeArrow()
                    # Check if you are currently playing
                    if isPlaying():
                        status = "Calculating move..."
                        refreshTUI()
                        # Calculate and display best move
                        stockfish.set_fen_position(str(newFen)+ getSide())
                        optimalMove = stockfish.get_best_move()
                        prevMoves.append(optimalMove)
                        drawArrow(optimalMove)
                        # Run Move
                        if automated:
                            status = "Playing move..."
                            refreshTUI()
                            time.sleep(random.randint(int(minDelay), int(maxDelay)))
                            playMove()
            else:
                if isPlaying():
                    status = "Waiting for you to play..."
                    refreshTUI()
        else:
            prevMoves = []
    except Exception as e:
        print()
