import re
import sys
import json
import random
import asyncio
from matplotlib.pyplot import arrow
from selenium import webdriver
from stockfish import Stockfish
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.common.action_chains import ActionChains

depth = 10
stockfish = Stockfish('/Users/morgan/Desktop/Stockfish/src/stockfish', parameters={"Threads": 8})
stockfish.set_depth(depth)
stockfish.set_show_wdl_option(True)

prevFen = ""

chrm_caps = webdriver.DesiredCapabilities.CHROME.copy()
chrm_caps['goog:loggingPrefs'] = { 'performance':'ALL' }

driver = webdriver.Chrome(desired_capabilities=chrm_caps)
actions = ActionChains(driver)
driver.get("https://lichess.org")
driver.fullscreen_window()

def WebSocketLog():
    payloadCache = []
    for wsData in driver.get_log('performance'):
        wsJson = json.loads((wsData['message']))
        if wsJson["message"]["method"]== "Network.webSocketFrameReceived":
            payloadCache.append(wsJson["message"]["params"]["response"]["payloadData"])
    return payloadCache

def drawArrow(move, color = 'g'):
    corr = 1
    if 'orientation-black manipulable' in driver.page_source:
        corr = -1
    coords = 'x1="c1" y1="c2" x2="c3" y2="c4"'
    coords = coords.replace("c1", str(corr*((ord(move[0]) & 31)-4.5)))
    coords = coords.replace("c2", str(corr*(4.5 - float(move[1]))))
    coords = coords.replace("c3", str(corr*((ord(move[2]) & 31)-4.5)))
    coords = coords.replace("c4", str(corr*(4.5 - float(move[3]))))
    
    if color == 'g' or color == 'green':
        arrow = '<line stroke="#15781B" stroke-width="0.15625" stroke-linecap="round" marker-end="url(#arrowhead-g)" opacity="1" cgHash="288,288,green"' + coords + '></line>'
    if color == 'y' or color == 'yellow':
        arrow = '<line stroke="#e68f00" stroke-width="0.15625" stroke-linecap="round" marker-end="url(#arrowhead-y)" opacity="1" cgHash="288,288,yellow"' + coords + '></line>'
    if color == 'r' or color == 'red':
        arrow = '<line stroke="#882020" stroke-width="0.15625" stroke-linecap="round" marker-end="url(#arrowhead-r)" opacity="1" cgHash="288,288,red"' + coords + '></line>'
    if color == 'b' or color == 'blue':
        arrow = '<line stroke="#003088" stroke-width="0.15625" stroke-linecap="round" marker-end="url(#arrowhead-b)" opacity="1" cgHash="288,288,blue"' + coords + '></line>'
    
    return arrow

while True:
    if '<button class="fbt resign" title="Resign"><span' in driver.page_source:
        count = -1
        evalcount = 0
        script = "var ele=arguments[0]; ele.innerHTML = '"
        arrowcolors = []
        g = driver.find_element(By.TAG_NAME ,"g")
        for i in reversed(WebSocketLog()):
            newFen = re.findall(r'fen":"(.*?)"', i)
            if len(newFen) != 0 and prevFen != newFen[0]:
                prevFen = newFen[0]
                
                if 'Your turn - Play' in driver.page_source:
                    moves = []
                    mate = False
                    if 'white manipulable' in driver.page_source:
                        stockfish.set_fen_position(str(newFen)[1:-1]+' w')

                        for move in stockfish.get_top_moves(6):
                            evalcount += 1
                            if evalcount == 1:
                                eval = move.get('Centipawn')
                                moves.append(move.get('Move'))
                                arrowcolors.append('g') 
                                continue
                            if type(move.get('Mate')) == type(1):
                                moves.append(move.get('Move'))
                                arrowcolors.append('g') 
                                continue
                            if eval == None:
                                if move.get('Centipawn') != None:
                                    continue
                            elif move.get('Centipawn') + 15 > eval:
                                moves.append(move.get('Move'))
                                arrowcolors.append('g') 
                                continue
                            elif move.get('Centipawn') + 30 > eval:
                                moves.append(move.get('Move'))
                                arrowcolors.append('b') 
                                continue
                            elif move.get('Centipawn') + 55 > eval:
                                moves.append(move.get('Move'))
                                arrowcolors.append('y') 
                                continue
                            elif move.get('Centipawn') + 100 > eval:
                                moves.append(move.get('Move'))
                                arrowcolors.append('r')
                                continue
                        
                        for move in moves:
                            count += 1
                            script = script + drawArrow(move, arrowcolors[count])
                        script = script + "';"
                        print(script)
                        driver.execute_script(script, g)
                        break
                    elif 'black manipulable' in driver.page_source:
                        stockfish.set_fen_position(str(newFen)[1:-1]+' b')
                        
                        for move in stockfish.get_top_moves(6):
                            evalcount += 1
                            if evalcount == 1:
                                eval = move.get('Centipawn')
                                moves.append(move.get('Move'))
                                arrowcolors.append('g') 
                                continue
                            if type(move.get('Mate')) == type(1):
                                moves.append(move.get('Move'))
                                arrowcolors.append('g') 
                                continue
                            elif move.get('Centipawn') - 15 < eval:
                                moves.append(move.get('Move'))
                                arrowcolors.append('g') 
                                continue
                            elif move.get('Centipawn') - 30 < eval:
                                moves.append(move.get('Move'))
                                arrowcolors.append('b') 
                                continue
                            elif move.get('Centipawn') - 55 < eval:
                                moves.append(move.get('Move'))
                                arrowcolors.append('y') 
                                continue
                            elif move.get('Centipawn') - 100 < eval:
                                moves.append(move.get('Move'))
                                arrowcolors.append('r')
                                continue
                        
                        for move in moves:
                            count += 1
                            script = script + drawArrow(move, arrowcolors[count])
                        script = script + "';"
                        print(script)
                        driver.execute_script(script, g)
                        break
                    break
