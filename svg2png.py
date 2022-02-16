# convert svg images to png to make fetchBoard compatible with other piece sets

import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

def svg2png(file: str, output_name: str):
   drawing = svg2rlg(file)
   renderPM.drawToFile(drawing, output_name+'.png', fmt="PNG")

for root, dirs, files in os.walk("./cburnettsvg", topdown=False):
   for name in files:
      svg2png(os.path.join(root, name), name[:-4])
   for name in dirs:
      svg2png(os.path.join(root, name), name[:-4])

