import discord
from discord import app_commands
from defcombos import convertrawdecklist, shortencard, scrapesheet, getnumcombos, getlistofcombos, getcomboidsfromlist
from createembed import createembed
from getdecklistfromurl import decipherurl
from salt import getsaltlist, gettaglist, addsaltmsg, addtagmsg
from random import randint
from urllib.request import urlopen
from discord.ext import tasks
from assist import convertstrtoint

client = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(client)
f = open("TOKEN.txt")
TOKEN = f.read()
f.close()
scrapesheet()
combos = getlistofcombos()

col = 0xfc0fc0

global saltlist, taglist, oldsaltindex, oldtagindex
taglist = gettaglist()
oldtagindex = len(taglist)
saltlist = getsaltlist()
oldsaltindex = len(saltlist)
def getnext(old, issalt):
    old += 1
    if issalt:
        if old >= len(saltlist):
            oldsaltindex = 0
            saltlist = getsaltlist()
            return saltlist[0]
        oldsaltindex = old
        return saltlist[old]
    else:
        if old >= len(taglist):
            oldtagindex = 0
            taglist = gettaglist()
            return taglist[0]
        oldtagindex = old
        return taglist[old]



@client.event
async def on_ready():
    the_name = str(getnumcombos()) + ' combos at once'
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name=the_name))
    update_info.start()

@tree.command(name="sbhelp", description="Returns the help message")
async def first_command(interaction):
    helpm = """
**!sbhelp** Shows this help message.
**!sbid <id>** Shows the combo with the given id.
~~**!sbname <cardnames>** Shows a list of combos with the given cards included.~~
~~**!sbcolor <wubrgc>** Shows a list of combos which match the color identity.~~
~~**!sbresult <result>** Shows a list of combos which match the results.~~
**!sbrandom** Displays a random combo.
**!combocheck** or **!cc** Upload a text file with your decklist or a link to your deck and the bot will let you know what combos are in your deck!
~~**!combo** This command is a way to search the site without ever leaving Discord! Handy!~~
**!salt** Have you ever been salty? Well this bot has too, and it will certainly tell you so."""
    embed = discord.Embed(title="**List of Available Commands:**", description=helpm, color=col)
    await interaction.response.send(embed=embed)

@tree.command(name="cchelp", description="Returns the help message for how the bot checks combos in a decklist")
async def first_command(interaction):
    helpm = """
Most deck builder websites have an *export* or a *download* feature. You can drag the file ending with *.txt* onto discord and type **!cc** and press enter, and the bot will give you a list of combos.
If you don't want to download the deck, you can instead provide a link to the decklist.
For example you can type **!cc <decklist url>** and the bot will let you know what exciting combos are in the deck.
Supported websites currently include Aetherhub, Archidekt, Deckbox, Deckstats, ManaStack, Moxfield, MtgGoldfish, MTGVault, Scryfall, and TappedOut.
If you have any other websites you would like to see added to this list, please feel free to message <@579345356450693120>.
"""
    embed = discord.Embed(title="**Combo Check Help:**", description=helpm, color=col)
    await interaction.response.send(embed=embed)

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
    elif message.startswith("!salt"): #send a random salt message
        outstring = getnext(oldsaltindex, True)
        await msg.channel.send(outstring)
    
    elif message.startswith("!sbid "): #return embed containing the combo with the id passed by the user
        m = msg.content.replace("!sbid ","")
        try:
            m = convertstrtoint(m)
            await msg.channel.send(embed=createembed(m,combos))
        except:
            await msg.channel.send("Invalid identity!")
            raise
    elif message.startswith("!sbrand"): # returns an embed containing a random combo
        ran = randint(1, getnumcombos())
        await msg.channel.send(embed=createembed(ran,combos))
    elif message.startswith("!cc") or message.startswith("!combocheck"):
        rawdata = ""
        cardslst = []
        if len(msg.attachments) == 0:
            if "```" in msg.content:
                rawdata = msg.content.split("```")[1]
            elif "http" in message:
                url = msg.content.split(' ')[1] #should ignore the !cc prefix
                cardslst = decipherurl(url)
            else:
                return await msg.channel.send('No decklist was attached!')
        else:
            attachment_url = message.attachments[0].url
            rawdata = urlopen(attachment_url).read()
        if rawdata == "" and len(cardslst) == 0:
            return await msg.channel.send('No decklist was attached!')
        if len(cardslst) == 0:
            cardslst = convertrawdecklist(rawdata)
        comboids = getcomboidsfromlist(cardslst)
        if len(comboids) == 0:
            return await msg.channel.send('No combos found')
        e = createembed(comboids[0],combos)
        if len(comboids) > 1 and len(comboids) < 7:
            s = str(len(comboids)) + ' more combos, please view combos '
            for c in comboids:
                s+= '[**' + str(c) + '**](https://commanderspellbook.com/combo/'+str(c)+'/), '
            s = s[:-2] + "."
            e.add_field(name='\u200b', value=s, inline=False)
        elif len(comboids) != 1:
            s = str(len(comboids) - 1) + ' more combos not listed here, please view combos '
            for c in comboids:
                s += str(c) + ", "
            s = s[:-2] + "."
            e.add_field(name='\u200b', value=s, inline=False)
        return await msg.channel.send(embed=e)
        
        
@tasks.loop(hours=1) # this function updates the startup info every hour, including all sheets num combos and status
async def update_info():
    scrapesheet()
    combos = getlistofcombos()
    the_name = str(getnumcombos()) + ' combos at once'
    await client.change_presence(activity=discord.Game(name=the_name))

client.run(TOKEN)
