import re

def fetchLichessBoard(html):
    width = int(str(set(re.findall(r'<cg-container style="width: (.*?)px; height', html)))[2:-2])
    height = int(str(set(re.findall(r'px; height: (.*?)px;"><cg', html)))[2:-2])
    html = html[:html.find('class="mini-game__player">')]
    piece_locations_helper = re.findall(r'class="white pawn" style="transform: translate(.*?);"><\/piece>', html)
    piece_locations_helper.append(re.findall(r'class="black pawn" style="transform: translate(.*?);"><\/piece>', html))
    piece_locations_helper.append(re.findall(r'class="white knight" style="transform: translate(.*?);"><\/piece>', html))
    piece_locations_helper.append(re.findall(r'class="black knight" style="transform: translate(.*?);"><\/piece>', html))
    piece_locations_helper.append(re.findall(r'class="white bishop" style="transform: translate(.*?);"><\/piece>', html))
    piece_locations_helper.append(re.findall(r'class="black bishop" style="transform: translate(.*?);"><\/piece>', html))
    piece_locations_helper.append(re.findall(r'class="white rook" style="transform: translate(.*?);"><\/piece>', html))
    piece_locations_helper.append(re.findall(r'class="black rook" style="transform: translate(.*?);"><\/piece>', html))
    piece_locations_helper.append(re.findall(r'class="white queen" style="transform: translate(.*?);"><\/piece>', html))
    piece_locations_helper.append(re.findall(r'class="black queen" style="transform: translate(.*?);"><\/piece>', html))
    piece_locations_helper.append(re.findall(r'class="white king" style="transform: translate(.*?);"><\/piece>', html))
    piece_locations_helper.append(re.findall(r'class="black king" style="transform: translate(.*?);"><\/piece>', html))

    piece_locations = []
    for i in piece_locations_helper:
        if type(i) == list:
            for j in i:
                piece_locations.append(j)
        else: piece_locations.append(i)
    for i in piece_locations:
        if type(i) != str:
            break
        helper = []
        helper.append((float(str(re.findall(r'\((.*?)px', i))[2:-2]))/width)
        helper.append((float(str(re.findall(r'px, (.*?)px', i))[2:-2]))/height)
        piece_locations.append(helper)
    for i in range(0, int(len(piece_locations)/2)):
        piece_locations.pop(0)
    
    return piece_locations