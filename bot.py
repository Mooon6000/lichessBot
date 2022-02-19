import re
import json
from hashlib import new
from selenium import webdriver
from stockfish import Stockfish
from selenium.webdriver.common.action_chains import ActionChains

stockfish = Stockfish('/Users/morgan/Desktop/Stockfish/src/stockfish', parameters={"Threads": 8})
stockfish.set_depth(10)

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
                        break
                    elif 'black manipulable' in driver.page_source:
                        stockfish.set_fen_position(str(newFen)[1:-1]+' b')
                        print(stockfish.get_top_moves())
                        break
                    break