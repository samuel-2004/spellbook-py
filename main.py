import discord
from discord import app_commands

from defcombos import convertrawdecklist, shortencard, scrapesheet, getnumcombos, getlistofcombos, getcomboidsfromlist
from createembed import createembed
from getdecklistfromurl import decipherurl
from salt import getsaltlist, gettaglist, addsaltmsg, addtagmsg
from random import randint
from urllib.request import Request, urlopen
from discord.ext import tasks
from assist import convertstrtoint

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

f = open("TOKEN.txt")
TOKEN = f.read()
f.close()

scrapesheet()
combos = getlistofcombos()

col = 0xfc0fc0

taglist = gettaglist()
oldtagindex = len(taglist)
saltlist = getsaltlist()
oldsaltindex = len(saltlist)

def getnext(old, issalt):
    global saltlist, taglist, oldsaltindex, oldtagindex
    old += 1
    if issalt:
        if old >= len(saltlist):
            oldsaltindex = 0
            saltlist = getsaltlist()
            return saltlist[0]
        oldsaltindex = old
        return saltlist[oldsaltindex]
    else:
        if old >= len(taglist):
            oldtagindex = 0
            taglist = gettaglist()
            return taglist[0]
        oldtagindex = old
        return taglist[old]



@client.event
async def on_ready():
    print("Syncing...")
    await tree.sync()
    the_name = str(getnumcombos()) + ' combos at once'
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name=the_name))
    update_info.start()

@tree.command(name="sbhelp", description="Returns the help message")
async def sbhelp(interaction):
    helpm = """
**!sbhelp** Shows this help message.
**!sbid <id>** Shows the combo with the given id.
~~**!sbname <cardnames>** Shows a list of combos with the given cards included.~~
~~**!sbcolor <wubrgc>** Shows a list of combos which match the color identity.~~
~~**!sbresult <result>** Shows a list of combos which match the results.~~
**!sbrandom** Displays a random combo.
**!combocheck** Upload a text file with your decklist or a link to your deck and the bot will let you know what combos are in your deck!
~~**!combo** This command is a way to search the site without ever leaving Discord! Handy!~~
**!salt** Have you ever been salty? Well this bot has too, and it will certainly tell you so."""
    embed = discord.Embed(title="**List of Available Commands:**", description=helpm, color=col)
    await interaction.response.send_message(embed=embed)

@tree.command(name="cchelp", description="Returns the help message for checking a decklist")
async def cchelp(interaction):
    helpm = """
Most deck builder websites have an *export* or a *download* feature. You can drag the file ending with *.txt* onto discord and type **!cc** and press enter, and the bot will give you a list of combos.
If you don't want to download the deck, you can instead provide a link to the decklist.
For example you can type **!cc <decklist url>** and the bot will let you know what exciting combos are in the deck.
Supported websites currently include Aetherhub, Archidekt, Deckbox, Deckstats, ManaStack, Moxfield, MtgGoldfish, MTGVault, Scryfall, and TappedOut.
If you have any other websites you would like to see added to this list, please feel free to message <@579345356450693120>.
"""
    embed = discord.Embed(title="**Combo Check Help:**", description=helpm, color=col)
    await interaction.response.send_message(embed=embed)

@tree.command(name="combocheck", description="Returns the help message for checking a decklist")
async def combocheck(interaction, decklist: discord.Attachment=None, decklist_url: str=None):
    #fixing variable names
    attachment = decklist
    url = decklist_url
    
    rawdata = ""
    cardslst = []
    if attachment != None:
        url = attachment.url

        req = Request(
            url=url, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        rawdata = urlopen(req).read().decode('utf-8')
    elif url != None:
        cardslst = decipherurl(url)
        
    if rawdata == "" and len(cardslst) == 0:
        await interaction.response.send_message('No decklist was attached!')
        return
    if len(cardslst) == 0:
        cardslst = convertrawdecklist(rawdata)
    comboids = getcomboidsfromlist(cardslst)
    if len(comboids) == 0:
        await interaction.response.send_message('No combos found')
        return
    e = createembed(comboids[0],combos)
    if len(comboids) > 1 and len(comboids) < 7:
        s = str(len(comboids)) + ' more combos, please view combos '
        for c in comboids:
            s+= '[**' + str(c) + '**](https://commanderspellbook.com/combo/'+str(c)+'/), '
        s = s[:-2] + "."
        e.add_field(name='\u200b', value=s, inline=False)
    elif len(comboids) != 1:
        s = str(len(comboids) - 1) + ' more combos not listed here, please view combos '
        for c in comboids[1:]:
            s += str(c) + ", "
        s = s[:-2] + "."
        e.add_field(name='\u200b', value=s, inline=False)
    await interaction.response.send_message(embed=e)

@tree.command(name="sbrandom", description="Displays a random combo")
async def sbrandom(interaction):
    m = randint(1, getnumcombos())
    embed=createembed(m,combos)
    await interaction.response.send_message(embed=embed)
    
@tree.command(name="sbid", description="Displays the combo with the given id")
async def sbid(interaction, identity: int):
    m = identity
    try:
        embed=createembed(m,combos)
        await interaction.response.send_message(embed=embed)
    except:
        interaction.response.send_message("Invalid identity!")

@tree.command(name="salt", description="Have you ever been salty? Well this bot has too, and it will certainly tell you so.")
async def salt(interaction):
    outstring = getnext(oldsaltindex, True)
    await interaction.response.send_message(outstring)

@client.event
async def on_message(msg):
    message = msg.content.lower()
    if msg.author.bot: # message was sent by any bot
        return

    if client.user.mentioned_in(msg):
        outstring = getnext(oldtagindex, False)
        await msg.channel.send(outstring)
        
    if message.startswith("!saltadd"): # add a temporary message to the salt shortlist
        addsaltmsg(msg.content.replace("!saltadd","").strip())
    elif message.startswith("!tagadd"): # add a temporary message to the tag shortlist
        addtagmsg(msg.content.replace("!tagadd","").strip())
        
        
@tasks.loop(hours=1) # this function updates the startup info every hour, including all sheets num combos and status
async def update_info():
    scrapesheet()
    combos = getlistofcombos()
    the_name = str(getnumcombos()) + ' combos at once'
    await client.change_presence(activity=discord.Game(name=the_name))

client.run(TOKEN)
