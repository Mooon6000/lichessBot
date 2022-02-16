import cv2
import numpy as np

# load piece img
bB_img = cv2.imread('./cburnettpng/bB.png')
bK_img = cv2.imread('./cburnettpng/bK.png')
bN_img = cv2.imread('./cburnettpng/bN.png')
bP_img = cv2.imread('./cburnettpng/bP.png')
bQ_img = cv2.imread('./cburnettpng/bQ.png')
bR_img = cv2.imread('./cburnettpng/bR.png')
wB_img = cv2.imread('./cburnettpng/wB.png')
wK_img = cv2.imread('./cburnettpng/wK.png')
wQ_img = cv2.imread('./cburnettpng/wQ.png')
wN_img = cv2.imread('./cburnettpng/wN.png')
wP_img = cv2.imread('./cburnettpng/wP.png')
wR_img = cv2.imread('./cburnettpng/wR.png')

def fetchBoard(screen):
    bB_result = cv2.matchTemplate(screen, bB_img, cv2.TM_CCOEFF_NORMED)
    bK_result = cv2.matchTemplate(screen, bK_img, cv2.TM_CCOEFF_NORMED)
    bB_result = cv2.matchTemplate(image, bB_img, cv2.TM_CCOEFF_NORMED)
    bB_result = cv2.matchTemplate(image, bB_img, cv2.TM_CCOEFF_NORMED)
    bB_result = cv2.matchTemplate(image, bB_img, cv2.TM_CCOEFF_NORMED)
    bB_result = cv2.matchTemplate(image, bB_img, cv2.TM_CCOEFF_NORMED)
    bB_result = cv2.matchTemplate(image, bB_img, cv2.TM_CCOEFF_NORMED)
    bB_result = cv2.matchTemplate(image, bB_img, cv2.TM_CCOEFF_NORMED)
    bB_result = cv2.matchTemplate(image, bB_img, cv2.TM_CCOEFF_NORMED)
    bB_result = cv2.matchTemplate(image, bB_img, cv2.TM_CCOEFF_NORMED)
    bB_result = cv2.matchTemplate(image, bB_img, cv2.TM_CCOEFF_NORMED)
    bB_result = cv2.matchTemplate(image, bB_img, cv2.TM_CCOEFF_NORMED)