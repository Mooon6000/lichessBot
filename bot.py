from cgitb import enable
import re
import sys
import json
import time
from hashlib import new
from tracemalloc import start
from selenium import webdriver
from stockfish import Stockfish
from selenium.webdriver.common.action_chains import ActionChains

enable_automation = "-a" in sys.argv

stockfish = Stockfish(parameters={"Threads": 8})
stockfish.set_depth(16)

prevFen = ""

chrm_caps = webdriver.DesiredCapabilities.CHROME.copy()
chrm_caps['goog:loggingPrefs'] = { 'performance':'ALL' }

driver = webdriver.Chrome(desired_capabilities=chrm_caps)
action = ActionChains(driver)
driver.get("https://lichess.org")

def WebSocketLog():
    payloadCache = []
    for wsData in driver.get_log('performance'):
        wsJson = json.loads((wsData['message']))
        if wsJson["message"]["method"]== "Network.webSocketFrameReceived":
            payloadCache.append(wsJson["message"]["params"]["response"]["payloadData"])
    return payloadCache

while True:
    if '<button class="fbt resign" title="Resign"><span' in driver.page_source:
        for i in reversed(WebSocketLog()):
            newFen = re.findall(r'fen":"(.*?)"', i)
            if len(newFen) != 0 and prevFen != newFen[0]:
                prevFen = newFen[0]
                if 'Your turn - Play' in driver.page_source:
                    if 'white manipulable' in driver.page_source:
                        start_time = time.time()
                        stockfish.set_fen_position(str(newFen)[1:-1]+' w')
                        moves = stockfish.get_top_moves()
                        end_time = time.time()
                        if enable_automation:
                            driver.execute_script('lichess.socket.send("move",{"u":"' + moves[0]["Move"] + '","s":' + str(int(end_time-start_time)) + '})')
                            print("Bot played move: " + moves[0]["Move"])
                        else:
                            print("Top 5 moves: " + str(moves))
                        break
                    elif 'black manipulable' in driver.page_source:
                        start_time = time.time()
                        stockfish.set_fen_position(str(newFen)[1:-1]+' b')
                        moves = stockfish.get_top_moves()
                        end_time = time.time()
                        if enable_automation:
                            driver.execute_script('lichess.socket.send("move",{"u":"' + moves[0]["Move"] + '","s": ' + str(int(end_time-start_time)) +'})')
                            print("Bot played move: " + moves[0]["Move"])
                        else:
                            print("Top 5 moves: " + str(moves))
                        break
                    break