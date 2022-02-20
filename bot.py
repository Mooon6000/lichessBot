import re
import sys
import json
import time
import random
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
                         stockfish.set_fen_position(str(newFen)[1:-1]+' w')
                         print(stockfish.get_top_moves())
                         move = stockfish.get_top_moves()[0]["Move"]
                         if enable_automation:
                             driver.execute_script('lichess.socket.send("move",{"u":"' + move + '","s":' + str(random.randint(3, 10)) + '})')
                         print(move)
                         break
                     elif 'black manipulable' in driver.page_source:
                         stockfish.set_fen_position(str(newFen)[1:-1]+' b')
                         print(stockfish.get_top_moves())
                         move = stockfish.get_top_moves()[0]["Move"]
                         if enable_automation:
                             driver.execute_script('lichess.socket.send("move",{"u":"' + move + '","s": ' + str(random.randint(3, 10)) +'})')
                         print(move)
                         break
                     break 
