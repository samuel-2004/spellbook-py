from discord import Embed
from defcombos import getlistofcombos
expandemoji_dict = {
':mana0:' : '<:mana0:673716794959069196>',
':mana1:' : '<:mana1:673716795353595944>',
':mana2:' : '<:mana2:673716795034566709>',
':mana3:' : '<:mana3:673716795378499604>',
':mana4:' : '<:mana4:673716795466579978>',
':mana5:' : '<:mana5:673716795407859762>',
':mana6:' : '<:mana6:673716795039023127>',
':mana7:' : '<:mana7:673716795152007169>',
':mana8:' : '<:mana8:673716795076640779>',
':mana9:' : '<:mana9:673716795445608449>',
':mana10:' : '<:mana10:673716795483357185>',
':mana11:' : '<:mana11:673716795495940127>',
':mana12:' : '<:mana12:673716795525300304>',
':mana13:' : '<:mana13:673716795584151564>',
':mana14:' : '<:mana14:673716795554922496>',
':mana15:' : '<:mana15:673716795529494558>',
':mana16:' : '<:mana16:673716795508785152>',
':mana20:' : '<:mana20:673716795542077442>',
':mana2u:' : '<:mana2u:673716795114258436>',
':mana2r:' : '<:mana2r:673716795257126913>',
':mana2b:' : '<:mana2b:673716795303264276>',
':mana2g:' : '<:mana2g:673716795349401621>',
':mana2w:' : '<:mana2w:673716795366178827>',
':manabp:' : '<:manabp:673716795303264288>',
':manaq:' : '<:manaq:673716795466842148>',
':manag:' : '<:manag:673716795491876895>',
':manarp:' : '<:manarp:673716795504459781>',
':manaup:' : '<:manaup:673716795584282625>',
':manat:' : '<:manat:673716795601059872>',
':manabg:' : '<:manabg:673716795609186314>',
':manab:' : '<:manab:673716795651391519>',
':manac:' : '<:manac:673716795667906570>',
':manae:' : '<:manae:673716795668168744>',
':managu:' : '<:managu:673716795672231953>',
':manaur:' : '<:manaur:673716795730952223>',
':manaub:' : '<:manaub:673716795731083266>',
':manax:' : '<:manax:673716795755986955>',
':manabr:' : '<:manabr:673716795777089623>',
':managw:' : '<:managw:673716795781283848>',
':managp:' : '<:managp:673716795877621800>',
':manarg:' : '<:manarg:673716795886272523>',
':manau:' : '<:manau:673716795890335747>',
':manarw:' : '<:manarw:673716795919564810>',
':manawp:' : '<:manawp:673716795932409856>',
':manar:' : '<:manar:673716795978285097>',
':manaw:' : '<:manaw:673716795991130151>',
':manawu:' : '<:manawu:673716796003582012>',
':manas:' : '<:manas:673716796007645204>',
':manawb:' : '<:manawb:673716796213428224>'
}

def convertemojis(field):
    insidebrackets = False
    fieldsplit = list(field)
    for i in range(len(fieldsplit)):
        if insidebrackets:
            fieldsplit[i] = fieldsplit[i].lower()
        if fieldsplit[i] == "{":
            insidebrackets = True
        elif fieldsplit[i] == "}":
            insidebrackets = False
    field = "".join(fieldsplit)
    
    field = field.replace("{",":mana").replace("}",":")
    for elem, translation in expandemoji_dict.items():
        field = field.replace(elem, translation)
    return field

def truncfield(field, issteps = False):
    maxlen = 1024
    out = ""
    cutoff = False
    if field[-1] == ".":
        field = field[:-1]
    field = convertemojis(field)
    sentences = field.replace(". ",".").split(".")
    if not issteps:
        for s in sentences:
            if len(out) + len(s) + 1 < 1016:
                out += s + "\n"
            else:
                cutoff = True
                out = out[:-1] + " (cont.)"
                break
    else:
        offset = 0
        for s in sentences:
            offset += 3
            if len(out) + len(s) + 1 + offset <= 1016:
                out += s + "\n"
            else:
                cutoff = True
                break
    return field, cutoff



def getnames(idnum, combos):
    idnum = str(idnum)
    names = []
    for combo in combos:
        if combo[0] == idnum:
            for i in range(1,10):
                if combo[i] == "":
                    break
                else:
                    names.append(combo[i])
            break
    if len(names) == 0:
        raise Exception("No combo found with that id")

    output = ""
    for name in names:
        output += name + " | "
    return output[:-3]

def getcolid(idnum, combos):
    idnum = str(idnum)
    col = ""
    for combo in combos:
        if combo[0] == idnum:
            col = combo[11]
            break
    if len(col) == 0:
        raise Exception("No combo found with that id")
    return col

def getprereqs(idnum, combos):
    idnum = str(idnum)
    pre = ""
    for combo in combos:
        if combo[0] == idnum:
            pre = combo[12]
            break
    if len(pre) == 0:
        raise Exception("No combo found with that id")
    pre.rstrip()
    if pre[-1] != ".":
        pre = pre + "."
    output = truncfield(pre)
    return output[0].replace(". ","\n"), output[1]

def getsteps(idnum, combos):
    idnum = str(idnum)
    steps = ""
    for combo in combos:
        if combo[0] == idnum:
            steps = combo[13]
            break
    if len(steps) == 0:
        raise Exception("No combo found with that id")
    steps = steps.strip()
    if steps[-1] != ".":
        steps = steps + "."
    stepsfull = truncfield(steps, True)
    out = stepsfull[0]
    outsplit = out.split(". ")
    output = ""
    for i in range(len(outsplit)):
        oldoutput = output
        output += str(i + 1) + ") " + outsplit[i] + "\n"
        if len(output) > 1016:
            return oldoutput[:-1] + " (cont.)", True
    return output[:-1], False

def getresults(idnum, combos):
    idnum = str(idnum)
    res = ""
    for combo in combos:
        if combo[0] == idnum:
            res = combo[14]
            break
    if len(res) == 0:
        raise Exception("No combo found with that id")
    res.rstrip()
    if res[-1] != ".":
        res = res + "."
    output = truncfield(res)
    return output[0].replace(". ","\n"), output[1]

def createembed(idnum, combos):
    col = 0xfc0fc0
    idnum = str(idnum)
    urlbase = "https://commanderspellbook.com/combo/"
    embed = Embed(title = getnames(idnum, combos), url=urlbase+idnum, description="**Identity: **"+getcolid(idnum, combos), color=col)
    
    pre = getprereqs(idnum, combos)
    embed.add_field(name="**Prerequisites:**", value=pre[0], inline=False)
    
    ste = getsteps(idnum, combos)
    embed.add_field(name="**Steps:**",         value=ste[0], inline=False)
    
    res = getresults(idnum, combos)
    embed.add_field(name="**Results:**",       value=res[0], inline=False)
    
    if pre[1] or ste[1] or res[1]:
        embed.add_field(name='\u200b', value='There was too much information to display, please go [**here**](https://commanderspellbook.com/?id='+idnum+') for more information.', inline=False)

    embed.set_footer(text="Use !sbhelp to get a list of available commands.")
    return embed
