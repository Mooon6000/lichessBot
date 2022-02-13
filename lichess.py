import re
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from stockfish import Stockfish
from chessBoard import fetchLichessBoard

stockfish = Stockfish('/Users/morgan/Desktop/Stockfish/src/stockfish', parameters={"Threads": 8})
stockfish.set_depth(10)

driver = webdriver.Chrome()
driver.get("https://lichess.org")
#driver.maximize_window()

yourboard = []
theirBoard = []
turn = None

def cordToSq(position):
    output = ''
    for i in position:
        if i[3] == 0:
            output.join('a')
        elif i[3] == 1:
            output.join('a')
        elif i[3] == 2:
            output.join('a')
        elif i[3] == 3:
            output.join('a')
        elif i[3] == 5:
            output.join('a')
        elif i[3] == 6:
            output.join('a')
        elif i[3] == 7:
            output.join('a')
        elif i[3] == 8:
            output.join('a')
            

#for square in board: if square not in fetchLichessBoard, start= this
# for square in fetchLichessBoard, if square not in board, end = this
#start, end into stockfish

while True:
    if '<title>Your turn - Play' in driver.page_source and turn != 0:
       yourBoard = fetchLichessBoard(driver.page_source)
       #print(theirBoard, '\n', '\n', yourBoard)
       turn = 0
    
    if '<title>Waiting for opponent' in driver.page_source and turn != 1:
        theirBoard = fetchLichessBoard(driver.page_source)
        turn = 1
     
        #moves = stockfish.get_top_moves(10)
        #pieces = driver.find_elements_by_tag_name('piece') #use the pieces to find where they are and use the height and width to calculate each move. Then input moves into stockfish. Use action chains and context_click for arrows. 
        #   print('\n', fen)
        #for mate lines show multiple moves so each pattern could be premoved. Used builtin stockfish mate feature
        # = re.findall(r'translate(.*?);"><\/piece>')[1:]
        #to find intuitive moves, find moves that engine likes on very low depth (such that it relies on NNUE) and then checks those moves at higher depth to ensure they are accurate. This excludes moves that are good for high-depth, computeresque reasons.
