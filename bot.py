from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from stockfish import Stockfish
from fetchBoard import fetchLichessBoard

stockfish = Stockfish('/Users/morgan/Desktop/Stockfish/src/stockfish', parameters={"Threads": 8})
stockfish.set_depth(10)

driver = webdriver.Chrome()
driver.get("https://lichess.org")
#driver.maximize_window()

