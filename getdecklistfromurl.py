from urllib.request import urlopen, Request

"""
------COMPLETED------
Aetherhub
Archidekt
Deckbox
Deckstats
ManaStack
Moxfield
MtgGoldfish
MTGVault
Scryfall
TappedOut

------NOT COMPLETED------
"""

def aetherhubExtract(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    f = urlopen(req).read().decode("utf-8")
    decklistinfo = ""
    for line in f.split("\n"):
        if "||" in line and '<a class="btn btn-light btn-sm btn-outline-dark" href="' in line:
            decklistinfo = line
            break
    decklistinfo = decklistinfo.split('aetherhub&c=')[1].split('"')[0].replace("&#x27;","'")
    decklistinfo = decklistinfo.split("||")
    decklist = []
    for card in decklistinfo:
        while card[0].isdigit():
            card = card[1:]
        card = card.strip()
        decklist.append(card)
    return decklist
    
def archidektExtract(url):
    deckid = url.split("#")[0].split("/")[-1]
    url = "https://archidekt.com/api/decks/" + deckid + "/"
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    f = urlopen(req).read().decode("utf-8")
    decklistinfo = f.split(',"categories":[{"id')[0].split('"name":"')
    decklist = []
    for card in decklistinfo:
        card = card.split('"')[0]
        decklist.append(card)
    return decklist[2:]

def deckboxExtract(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    f = urlopen(req).read().decode("utf-8")
    decklistinfo = ""
    for line in f.split("\n"):
        if 'Tcg.set = new Tcg.MtgDeck({"id":' in line:
            decklistinfo = line
            break
    decklistinfo = decklistinfo.split('"name":"')[1:]
    decklist = []
    for card in decklistinfo:
        card = card.split('"')[0]
        decklist.append(card)
    return decklist[1:]

def deckstatsExtract(url):
    f = urlopen(url).read().decode("utf-8")
    decklistinfo = ""
    for line in f.split("\n"):
        if '(function(){ init_deck_page();deck_page.key = "";init_deck_data({"sections":[' in line:
            decklistinfo = line
            break
    decklistinfo = decklistinfo.split('"cards":[{')[1].split(',"url_neutral"')[0]
    decklistinfo = decklistinfo.split('"name"')
    decklist = []
    for card in decklistinfo:
        card = card.split('"')
        if len(card) > 1:
            card = card[1].replace("\\/","/")
            decklist.append(card)

    return decklist

def manastackExtract(url):
    url = "https://manastack.com/api/deck?slug=" + url.split("/")[-1]
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    f = urlopen(req).read().decode("utf-8")
    decklistinfo = f.split('"name":"')
    decklist = []
    abool = True
    for card in decklistinfo:
        if abool:
            abool = False
            continue
        else:
            abool = True
        card = card.split('"')[0]
        card = card.replace("\u2019","'")
        if card not in decklist:
            decklist.append(card)
    return decklist[2:]

def moxfieldExtract(url):
    deckid = url.split("/")[-1]
    #      https://api2.moxfield.com/v2/decks/all/Lnuw6oBWlkS0dGi783lRZQ
    print(deckid)
    url = "https://api2.moxfield.com/v2/decks/all/" + deckid
    print(repr(url),"https://api2.moxfield.com/v2/decks/all/Lnuw6oBWlkS0dGi783lRZQ")
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    f = urlopen(req).read().decode("utf-8")
    decklistinfo = f.split('"name":"')
    decklist = []
    commandername = ""
    for i in range(2,len(decklistinfo)):
        cardname = decklistinfo[i].split('"')[0].replace("\\u0027","'")
        if cardname != commandername:
            decklist.append(cardname)
        else:
            break
        if len(decklist) > 0:
            commandername = decklist[0]
    print(len(decklist))
    return decklist

def mtggoldfishExtract(url):
    f = urlopen(url).read().decode("utf-8")
    decklist = []
    abool = False
    for line in f.split("\n"):
        if '<input type="hidden" name="deck_input[deck]" id="deck_input_deck" value="' in line:
            abool = True
            line = line.replace('<input type="hidden" name="deck_input[deck]" id="deck_input_deck" value="','')
        elif '" />' in line and abool:
            break
        if abool:
            decklist.append(line)
    for i in range(len(decklist)):
        while decklist[i][0].isdigit():
            decklist[i] = decklist[i][1:]
        decklist[i] = decklist[i].strip().replace("&#39;","'")
    return decklist

def mtgvaultExtract(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    f = urlopen(req).read().decode("utf-8")
    decklist = []
    for line in f.split("\n"):
        if '<div class="deck-card"><img class="card_image" src=' in line:
            line = line.split('" alt="')[1].split('"')[0]
            decklist.append(line)
    
    return decklist
    #https://www.mtgvault.com/boynate95/decks/codys-wort-deck/
    

def scryfallExtract(url):
    f = urlopen(url).read().decode("utf-8")
    decklistinfo = ""
    for line in f.split("\n"):
        if "||" in line:
            decklistinfo = line
            break
    decklistinfo = decklistinfo.replace('  <input type="hidden" name="c" value="',"")
    decklistinfo = decklistinfo.replace('" autocomplete="off" />',"")
    decklist = decklistinfo.split("||")
    for i in range(len(decklist)):
        while decklist[i][0].isdigit():
            decklist[i] = decklist[i][1:]
        decklist[i] = decklist[i].strip().replace("&#39;","'")
    return decklist

def tappedoutExtract(url):
    req1 = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    f1 = urlopen(req1).read().decode("utf-8")
    last_update_epoch = ""
    for line in f1.split("\n"):
        if 'var last_update_epoch = "' in line:
            last_update_epoch = line.split('"')[1]
            break
    if last_update_epoch == "":
        return

    if url[-1] == "/":
        url = url[:-1]
    deckname = url.split("/")[-1]
    
    newurl = "https://tappedout.net/api/collection:deck/" + deckname + "/data/?cb=" + last_update_epoch + "&cat=custom"
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    f = urlopen(req1).read().decode("utf-8")
    #decklistinfo = f.split('"typeData"')[1]
    decklistinfo = f.split('\n')
    deckstuff = ""
    for line in decklistinfo:
        if "||" in line and '<input type="hidden" name="c" value="' in line:
            deckstuff = line
    if deckstuff == "":
        return
    deckstuff = deckstuff.replace('&#x27;',"'")
    deckstuff = deckstuff.split('<input type="hidden" name="c" value="')[1]
    deckstuff = deckstuff.split('">')[0]
    decklist = deckstuff.split("||")
    for i in range(len(decklist)):
        while decklist[i][0].isdigit():
            decklist[i] = decklist[i][1:]
        decklist[i] = decklist[i].strip()
    
    return decklist





def decipherurl(url):#Takes in any url and calls the correct function
    if "aetherhub" in url:
        return aetherhubExtract(url)
    elif "archidekt" in url:
        return archidektExtract(url)
    elif "deckbox" in url:
        return deckboxExtract(url)
    elif "deckstats" in url:
        return deckstatsExtract(url)
    elif "manastack" in url:
        return manastackExtract(url)
    elif "moxfield" in url:
        return moxfieldExtract(url)
    elif "mtggoldfish" in url:
        return mtggoldfishExtract(url)
    elif "mtgvault" in url:
        return mtgvaultExtract(url)
    elif "scryfall" in url:
        return scryfallExtract(url)
    elif "tappedout" in url:
        return tappedoutExtract(url)
    else:
        return None


if __name__ == "__main__":
    url = "https://www.moxfield.com/decks/Lnuw6oBWlkS0dGi783lRZQ"
    print(decipherurl(url))




