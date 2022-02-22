import re
import json
from hashlib import new
from selenium import webdriver
from stockfish import Stockfish
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

stockfish = Stockfish('/Users/morgan/Desktop/Stockfish/src/stockfish', parameters={"Threads": 8})
stockfish.set_depth(10)

prevFen = ""

chrm_caps = webdriver.DesiredCapabilities.CHROME.copy()
chrm_caps['goog:loggingPrefs'] = { 'performance':'ALL' }

driver = webdriver.Chrome(desired_capabilities=chrm_caps)
actions = ActionChains(driver)
driver.get("https://lichess.org")


def WebSocketLog():
    payloadCache = []
    for wsData in driver.get_log('performance'):
        wsJson = json.loads((wsData['message']))
        if wsJson["message"]["method"]== "Network.webSocketFrameReceived":
            payloadCache.append(wsJson["message"]["params"]["response"]["payloadData"])
    return payloadCache

def drawArrow(board, move):
    corr = 1
    if 'orientation-black' in driver.page_source:
        corr = -1
    coords = 'x1="c1" y1="c2" x2="c3" y2="c4"'
    coords = coords.replace("c1", str(corr*((ord(move[0]) & 31)-4.5)))
    coords = coords.replace("c2", str(corr*(4.5 - float(move[1]))))
    coords = coords.replace("c3", str(corr*((ord(move[2]) & 31)-4.5)))
    coords = coords.replace("c4", str(corr*(4.5 - float(move[3]))))
    arrow = '<line stroke="#15781B" stroke-width="0.15625" stroke-linecap="round" marker-end="url(#arrowhead-g)" opacity="1" cgHash="288,288,green"' + coords + '></line>'
    script = "var ele=arguments[0]; ele.innerHTML = '" + arrow + "';"
    driver.execute_script(script, board)


while True:
    if '<button class="fbt resign" title="Resign"><span' in driver.page_source:
        g = driver.find_element(By.TAG_NAME ,"g")
        for i in reversed(WebSocketLog()):
            newFen = re.findall(r'fen":"(.*?)"', i)
            if len(newFen) != 0 and prevFen != newFen[0]:
                prevFen = newFen[0]
                if 'Your turn - Play' in driver.page_source:
                    moves = []
                    if 'white manipulable' in driver.page_source:
                        stockfish.set_fen_position(str(newFen)[1:-1]+' w')
                        '''for i in stockfish.get_top_moves():
                            moves.append(i['Move'])
                            if i['Centipawn'] != None:
                                moves.append(i['Centipawn'])
                            else:
                                moves.append('m' + moves['Mate'])
                        for i in moves:

                        print(moves)'''
                        drawArrow(g, stockfish.get_best_move())
                        break
                    elif 'black manipulable' in driver.page_source:
                        stockfish.set_fen_position(str(newFen)[1:-1]+' b')
                        '''for i in stockfish.get_top_moves():
                            moves.append(i['Move'])
                            if i['Centipawn'] != None:
                                moves.append(i['Centipawn'])
                            else:
                                moves.append('m' + moves['Mate'])
                        print(moves)'''
                        drawArrow(g, stockfish.get_best_move())
                        break
                    break
