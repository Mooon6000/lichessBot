from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import json
import time
#from stockfish import Stockfish
#
#stockfish = Stockfish('/Users/morgan/Desktop/Stockfish/src/stockfish', parameters={"Threads": 8})
#stockfish.set_depth(10)

chrm_caps = webdriver.DesiredCapabilities.CHROME.copy()
chrm_caps['goog:loggingPrefs'] = { 'performance':'ALL' }
driver = webdriver.Chrome(executable_path = '/Applications/chromedriver', desired_capabilities=chrm_caps)
driver.get("https://lichess.org")

def WebSocketLog():
    for wsData in driver.get_log('performance'):
        #print(wsData) 
        wsJson = json.loads((wsData['message']))
        if wsJson["message"]["method"]== "Network.webSocketFrameReceived":
            print ("Rx :"+ str(wsJson["message"]["params"]["timestamp"]) + wsJson["message"]["params"]["response"]["payloadData"])
        if wsJson["message"]["method"] =="Network.webSocketFrameSent":
            print ("Tx :"+ wsJson["message"]["params"]["response"]["payloadData"])
time.sleep(30)
WebSocketLog()