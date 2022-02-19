from hashlib import new
from selenium import webdriver
import json
import re

# Previous Fen
prevFen = ""

# Chrome Options
chrm_caps = webdriver.DesiredCapabilities.CHROME.copy()
chrm_caps['goog:loggingPrefs'] = { 'performance':'ALL' }

# Initiate Driver
driver = webdriver.Chrome(desired_capabilities=chrm_caps)

# Set URL
driver.get("https://lichess.org")

# Function to get all WebSocket Data
def WebSocketLog():
    payloadCache = []
    for wsData in driver.get_log('performance'):
        wsJson = json.loads((wsData['message']))
        if wsJson["message"]["method"]== "Network.webSocketFrameReceived":
            payloadCache.append(wsJson["message"]["params"]["response"]["payloadData"])
    return payloadCache

# Run fen every time move is played (and is in game)
while True:
    # Loop over log backwards (start with most recent data)
    if '<button class="fbt resign" title="Resign"><span' in driver.page_source:
        for i in reversed(WebSocketLog()):
            newFen = re.findall(r'fen":"(.*?)"', i)
            if len(newFen) != 0 and prevFen != newFen:
                prevFen = newFen
                print(newFen)
                break