from json import load
from urllib.request import urlopen
#https://sheets.googleapis.com/v4/spreadsheets/1KqyDRZRCgy8YgMFnY0tHSw_3jC99Z0zFvJrPbfm66vA/values:batchGet?ranges=combos!A2:Q&key=AIzaSyBD_rcme5Ff37Evxa4eW5BFQZkmTbgpHew
def getlistofcombos():
    try:
        f = open("combos.json", "r", encoding="cp1252")
    except:
        raise Exception("getlistofcombos(): file does not exist, call scrapesheet")
    data = load(f)
    f.close()

    data = data["valueRanges"][0]["values"]
    return data

def scrapesheet():
    try:
        url = "https://sheets.googleapis.com/v4/spreadsheets/1KqyDRZRCgy8YgMFnY0tHSw_3jC99Z0zFvJrPbfm66vA/values:batchGet?ranges=combos!A2:Q&key=AIzaSyBD_rcme5Ff37Evxa4eW5BFQZkmTbgpHew"
        data = urlopen(url).read().decode("cp1252")
        data = data.split("\n")
        f = open("combos.json", "w")
        for line in data:
            f.write(str(line) + "\n")
        f.close()
        return True
    except:
        return False

def getnumcombos():
    s = 0
    d = getlistofcombos()
    for combo in d:
        if len(combo) > 1:
            s += 1
    return s


uselesscards = [
    "plains",
    "island",
    "swamp",
    "mountain",
    "forest",
    "snow-covered plains",
    "snow-covered island",
    "snow-covered swamp",
    "snow-covered mountain",
    "snow-covered forest",
    "creature",
    "artifact",
    "planeswalker",
    "sorcery",
    "instant",
    "enchantment",
    "land",
    ""
]

def shortencard(c):
    c = c.lower()
    c = c.replace("/","").replace("'","").replace("-","").replace("+","").replace(",","")
    return c

def curatelist(lst):
    outputlst = []
    for card in lst:
        if card not in uselesscards:
            outputlst.append(shortencard(card))
    return outputlst

def getcomboscards(combo):
    if len(combo) <= 10:
        return []
    output = []
    for i in range(1,10):
        if len(combo[i]) != 0:
            output.append(shortencard(combo[i]))    
    return output

def getcomboidsfromlist(cardslst):
    if len(cardslst) == 0:
        return []
    cardslst = curatelist(cardslst)
    data = getlistofcombos()
    output = []
    for combo in data:
        if len(combo) <= 1:
            break
        combocards = getcomboscards(combo)
        cardfound = True
        for card in combocards:
            if shortencard(card) not in cardslst:
                cardfound = False
                break
        if cardfound:
            output.append(combo[0])
    return output

def convertrawdecklist(rawdeck):
    cardslst = []
    for line in rawdeck.split("\n"):
        while line[0].isdigit():
            line = line[1:]
        if line[:2] == "x ":
            line = line[2:]
        line = line.strip()
        cardslst.append(line)
    return cardslst




        
