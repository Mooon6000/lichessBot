# Imports
from selenium import webdriver
import json

# Previous Fen
prevFen = ""

# Chrome Options
chrm_caps = webdriver.DesiredCapabilities.CHROME.copy()
chrm_caps['goog:loggingPrefs'] = { 'performance':'ALL' }

# Initiate Driver
driver = webdriver.Chrome(executable_path = '/Applications/chromedriver', desired_capabilities=chrm_caps)

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
    for i in reversed(WebSocketLog):
        # Check if a fen is found
        if