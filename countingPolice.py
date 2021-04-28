#--------------------------------------------------------------------------------------------------------------------------------------#
#  _____  __  __  _____    ____   _____  _______  _____ 
# |_   _||  \/  ||  __ \  / __ \ |  __ \|__   __|/ ____|
#   | |  | \  / || |__) || |  | || |__) |  | |  | (___  
#   | |  | |\/| ||  ___/ | |  | ||  _  /   | |   \___ \ 
#  _| |_ | |  | || |     | |__| || | \ \   | |   ____) |
# |_____||_|  |_||_|      \____/ |_|  \_\  |_|  |_____/ 


import discord
import os
import random
from discord import colour
from discord import embeds
from discord.errors import ClientException
from discord.ext import commands
import asyncio
from discord.ext.commands.errors import CommandOnCooldown
from discord.player import FFmpegPCMAudio
import psycopg2
import datetime
import requests
from youtube_search import YoutubeSearch
import youtube_dl
import ctypes
import ctypes.util
import spotipy
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials


#--------------------------------------------------------------------------------------------------------------------------------------#
#  _____  _   _  _____  _______  _____            _       _____  ______        _______  _____  ____   _   _   _____ 
# |_   _|| \ | ||_   _||__   __||_   _|    /\    | |     |_   _||___  /    /\ |__   __||_   _|/ __ \ | \ | | / ____|
#   | |  |  \| |  | |     | |     | |     /  \   | |       | |     / /    /  \   | |     | | | |  | ||  \| || (___  
#   | |  | . ` |  | |     | |     | |    / /\ \  | |       | |    / /    / /\ \  | |     | | | |  | || . ` | \___ \ 
#  _| |_ | |\  | _| |_    | |    _| |_  / ____ \ | |____  _| |_  / /__  / ____ \ | |    _| |_| |__| || |\  | ____) |
# |_____||_| \_||_____|   |_|   |_____|/_/    \_\|______||_____|/_____|/_/    \_\|_|   |_____|\____/ |_| \_||_____/ 


#initialize client and bot
#client = discord.Client()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix = '.', description = 'Help for the H Welding Machine Bot', intents = intents)
bot.remove_command('help')
bot_color = discord.Color.from_rgb(231, 76, 60)

#initializes connections to postgresql database
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()
conn.autocommit = True

find = ctypes.util.find_library('opus')
discord.opus.load_opus(find)

auth_manager = SpotifyClientCredentials(client_id=os.environ['spot_id'], client_secret=os.environ['spot_secret'])
sp = spotipy.Spotify(auth_manager=auth_manager)

#--------------------------------------------------------------------------------------------------------------------------------------#
#   _____  _       ____   ____            _      
#  / ____|| |     / __ \ |  _ \    /\    | |     
# | |  __ | |    | |  | || |_) |  /  \   | |     
# | | |_ || |    | |  | ||  _ <  / /\ \  | |     
# | |__| || |____| |__| || |_) |/ ____ \ | |____ 
#  \_____||______|\____/ |____//_/    \_\|______|



CLIENT_ID = os.environ['TWITCH_ID']
CLIENT_SECRET = os.environ['TWITCH_SECRET']
URL = "https://api.twitch.tv/helix/streams?user_login={}"
authURL = 'https://id.twitch.tv/oauth2/token'
AutParams = {'client_id': CLIENT_ID,
             'client_secret': CLIENT_SECRET,
             'grant_type': 'client_credentials'
             }


channelList = [
    "bot", "admins-only", "testing"
]

#list of mod ids
modID = [
    203282979265576960,
    288710564367171595
]

streamerList = {
    173202512977854466: "AGallonofRaccoons",
    221115052038684683: "smartinmoose",
    288710564367171595: "purelife_tv"
}

#foot picture list for .finn
forbiddenList = [
    "https://img.webmd.com/dtmcms/live/webmd/consumer_assets/site_images/articles/health_tools/ways_to_make_your_feet_feel_better_slideshow/493ss_thinkstock_rf_woman_stretching_feet.jpg",
    "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/gh-why-do-my-feet-hurt-toes-1594663599.png?crop=0.914xw:0.687xh;0.0864xw,0.110xh&resize=480:*",
    "https://post.greatist.com/wp-content/uploads/2019/07/Feet_1200x628-facebook.jpg",
    "https://www.saga.co.uk/contentlibrary/saga/publishing/verticals/health-and-wellbeing/conditions/happyfeetshutterstock_297390392768x576.jpg",
    "https://media.phillyvoice.com/media/images/09102019_feet_Pixabay.2e16d0ba.fill-735x490.jpg",
    "https://www.jeancoutu.com/globalassets/revamp/sante/conseils-sante/20160516-02-soin-pieds/soins_pieds_450.jpg",
    "https://www.wuwm.com/sites/wuwm/files/styles/x_large/public/201911/AdobeStock_245471467.jpeg",
    "https://cdn.aarp.net/content/dam/aarp/health/conditions_treatments/2019/05/1140-woman-rubbing-feet.jpg",
    "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/1076/feet600-1502734322.jpg",
    "https://st1.thehealthsite.com/wp-content/uploads/2015/09/foot-care-routine.jpg",
    "https://cdn2.hubspot.net/hubfs/3355520/a-cold-feet-in-bed.jpg",
    "https://www.unilad.co.uk/wp-content/uploads/2020/08/feet-2.jpg",
    "https://www.treehugger.com/thmb/k1t1mI-e1Y_bPt53uWLIJn81coA=/1000x678/filters:no_upscale():max_bytes(150000):strip_icc()/__opt__aboutcom__coeus__resources__content_migration__mnn__images__2016__04__feet-in-sand-65c3ef0552924bedbe1e0837d8e964d7.jpg",
    "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/skin-care-for-feet-royalty-free-image-639631390-1553460308.jpg",
    "https://www.yourfootpalace.com/wp-content/uploads/morning-foot-stiffness.jpg"
]

music_queue = []

ydl_opts = {
    'quiet': True,
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': './song.mp3'
}

now_playing = ""

repeating = False

#--------------------------------------------------------------------------------------------------------------------------------------#
#  ______  _    _  _   _   _____  _______  _____  ____   _   _   _____ 
# |  ____|| |  | || \ | | / ____||__   __||_   _|/ __ \ | \ | | / ____|
# | |__   | |  | ||  \| || |        | |     | | | |  | ||  \| || (___  
# |  __|  | |  | || . ` || |        | |     | | | |  | || . ` | \___ \ 
# | |     | |__| || |\  || |____    | |    _| |_| |__| || |\  | ____) |
# |_|      \____/ |_| \_| \_____|   |_|   |_____|\____/ |_| \_||_____/                                                                       
                                                                      

def reestablish():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    global cur 
    cur = conn.cursor()
    conn.autocommit = True


#enters a message from the #counting channel into the postgresql DB
def countEntry(num, user):
    SQL = "INSERT INTO countingtable (count) VALUES (%s);"
    data = (num,)
    while True:
        try:
            cur.execute(SQL, data)
            break
        except psycopg2.InterfaceError:
            reestablish()
    conn.commit()
    if num % 25 == 0:
        SQLtwo = "DELETE FROM countingtable WHERE count < (%s);"
        dataTwo = (num-1,)
        while True:
            try:
                cur.execute(SQLtwo, dataTwo)
                break
            except psycopg2.InterfaceError:
                reestablish()
        conn.commit()
    SQL = f"SELECT pointnumber FROM points WHERE id = {user.id};"
    while True:
        try:
            cur.execute(SQL)
            break
        except psycopg2.InterfaceError:
            reestablish()
    conn.commit()
    points = cur.fetchone()

    SQL = f"UPDATE points SET pointnumber = {points[0]+10} WHERE id = {user.id};"
    while True:
        try:
            cur.execute(SQL)
            break
        except psycopg2.InterfaceError:
            reestablish()
    conn.commit()

#deals a hand for blackjack
def deal(deck):
    hand = []
    for i in range(2):
        random.shuffle(deck)
        card = deck.pop()
        if card == 11: card = "J"
        if card == 12: card = "Q"
        if card == 13: card = "K"
        if card == 14: card = "A"
        hand.append(card)
    return hand

#calculates the total of a players hand
def total(hand):
    total = 0
    aces = 0
    for card in hand:
        if card == "J" or card == "Q" or card == "K":
            total += 10
        elif card == "A":
            aces += 1
        else:
            total += card
    for i in range(aces):
        if aces > 1:
            if total >= 10:
                total += 1
            else:
                total += 11
        else:
            if total >= 11: 
                total += 1
            else: 
                total += 11
    return total

#lets the player "hit" in blackjack
def hit(hand, deck):
    random.shuffle(deck)
    card = deck.pop()
    if card == 11: card = "J"
    if card == 12: card = "Q"
    if card == 13: card = "K"
    if card == 14: card = "A"
    hand.append(card)
    return hand


def bjwin(player):
    SQL = f"SELECT id, name FROM points ORDER BY totalPoints DESC;"
    cur.execute(SQL)
    highestPlayer = cur.fetchone()
    highestPlayerID = highestPlayer[0]
    if highestPlayerID == player.id:
        return True
    else: 
        return False


def Check(user):
    AutCall = requests.post(url=authURL, params=AutParams)
    access_token = AutCall.json()['access_token']

    head = {
        'Client-ID': CLIENT_ID,
        'Authorization': "Bearer " + access_token
    }

    r = requests.get(URL.format(user), headers = head).json()['data']

    #print(r)
    if r:
        r = r[0]
        if r['type'] == 'live':
            newTup = (1, r['game_name'])
            return(newTup)
        else:
            return 0, None
    else:
        return 0, None



#--------------------------------------------------------------------------------------------------------------------------------------#
#   ____   _   _        _____   ______            _____ __     __
#  / __ \ | \ | |      |  __ \ |  ____|    /\    |  __ \\ \   / /
# | |  | ||  \| |      | |__) || |__      /  \   | |  | |\ \_/ / 
# | |  | || . ` |      |  _  / |  __|    / /\ \  | |  | | \   /  
# | |__| || |\  |      | | \ \ | |____  / ____ \ | |__| |  | |   
#  \____/ |_| \_|      |_|  \_\|______|/_/    \_\|_____/   |_|                                                                                                                                   


#sets bot status based on number of people with strikes
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    while True:
        try:
            cur.execute("SELECT COUNT(name) FROM striketable;")
            break
        except psycopg2.InterfaceError:
            reestablish()
    conn.commit()
    numCriminalsTable = cur.fetchall()
    numCriminals = numCriminalsTable[0][0]
    print(numCriminals)
    presence = str(numCriminals) + " criminals"
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=presence))


#--------------------------------------------------------------------------------------------------------------------------------------#
#   _    _  ______  _       _____  
#  | |  | ||  ____|| |     |  __ \ 
#  | |__| || |__   | |     | |__) |
#  |  __  ||  __|  | |     |  ___/ 
#  | |  | || |____ | |____ | |     
#  |_|  |_||______||______||_|


@bot.group(name='help', invoke_without_command = True)
async def help(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    helpEmbed = discord.Embed(title = "H Welding Machine Help", description = "The prefix of the bot is `.`", color = bot_color)
    helpEmbed.add_field(name = ":slot_machine: **Gambling - 9**", value = "`blackjack`, `roulette`, `slots`, `points`, `claim`, `pay`, `leaderboard`, `totalpointslb`, `store`", inline = False)
    helpEmbed.add_field(name = ":musical_note: **Music - 8**", value = "`play`, `skip`, `clear`, `queue`, `leave`, `shuffle`, `repeat`, `ignore`")
    helpEmbed.add_field(name = ":game_die: **Miscellaneous - 8**", value = "`tictactoe`, `connect4`, `finn`, `suggestion`, `purge`, `asa`, `strikes`", inline = False)
    helpEmbed.set_footer(text = "For more information try .help (command) or .help (category), ex: .help play or .help gambling")
    await ctx.send(embed=helpEmbed)

# MUSIC HELP COMMANDS

@help.command(name = "music")
async def music_help(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    helpEmbed = discord.Embed(title = "H Welding Machine Help", description = "Help with the Music category", color = bot_color)
    helpEmbed.add_field(name = ":musical_note: Music Commands :musical_note:", value = "**.play**\nPlays a song\n**.skip**\nSkips the song\n**.clear**\nClears the queue\n**.queue**\nShows the queue\n**.leave**\nForces the bot to leave\n**.shuffle**\nShuffles the queue\n**.repeat**\nRepeats the song\n**.ignore**\nIgnores a user's commands", inline=False)
    helpEmbed.set_footer(text="For more help, type .help `command` (ex. .help play)")
    await ctx.send(embeds=helpEmbed)
@help.command(name = "play")
async def play_help(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    helpEmbed = discord.Embed(title = "H Welding Machine Help", description = "Help with the .play command", color = bot_color)
    helpEmbed.add_field(name = ".play `<youtube url, search term, or spotify playlist link>`", value = ".play lets you queue a song from youtube or a playlist from spotify")
    await ctx.send(embed=helpEmbed)
@help.command(name = "skip")
async def skip_help(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    helpEmbed = discord.Embed(title = "H Welding Machine Help", description = "Help with the .skip command", color = bot_color)
    helpEmbed.add_field(name = ".skip", value = ".skip lets you skip the currently playing song")
    await ctx.send(embed=helpEmbed)
@help.command(name = "clear")
async def blackjack_help(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    helpEmbed = discord.Embed(title = "H Welding Machine Help", description = "Help with the .clear command", color = bot_color)
    helpEmbed.add_field(name = ".clear", value = ".clear lets you clear the song queue")
    await ctx.send(embed=helpEmbed)
@help.command(name = "leave")
async def blackjack_help(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    helpEmbed = discord.Embed(title = "H Welding Machine Help", description = "Help with the .leave command", color = bot_color)
    helpEmbed.add_field(name = ".leave", value = ".leave forces the bot to leave the voice channel")
    await ctx.send(embed=helpEmbed)
@help.command(name = "shuffle")
async def blackjack_help(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    helpEmbed = discord.Embed(title = "H Welding Machine Help", description = "Help with the .shuffle command", color = bot_color)
    helpEmbed.add_field(name = ".shuffle", value = ".shuffle lets you shuffle the music queue")
    await ctx.send(embed=helpEmbed)
@help.command(name = "repeat")
async def blackjack_help(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    helpEmbed = discord.Embed(title = "H Welding Machine Help", description = "Help with the .repeat command", color = bot_color)
    helpEmbed.add_field(name = ".repeat", value = ".repeat lets you repeat a song indefinitely")
    await ctx.send(embed=helpEmbed)
@help.command(name = "ignore")
async def blackjack_help(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    helpEmbed = discord.Embed(title = "H Welding Machine Help", description = "Help with the .ignore command", color = bot_color)
    helpEmbed.add_field(name = ".ignore `<mention member>`", value = ".ignore lets a moderator take away someone's music bot privileges")
    await ctx.send(embed=helpEmbed)
@help.command(name = "queue")
async def blackjack_help(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    helpEmbed = discord.Embed(title = "H Welding Machine Help", description = "Help with the .queue command", color = bot_color)
    helpEmbed.add_field(name = ".queue", value = ".queue lets you view the song queue")
    await ctx.send(embed=helpEmbed)

# GAMBLING HELP COMMANDS
@help.command(name = "gambling")
async def gambling_help(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    helpEmbed = discord.Embed(title = "H Welding Machine Help", description = "Help with the Gambling category", color = bot_color)
    helpEmbed.add_field(name = ":slot_machine: Gambling Commands :slot_machine:", value = "**.blackjack**\nPlay a game of blackjack\n**.roulette**\nPlay a game of roulette\n**.slots**\nPlay a game of slots\n**.points**\nShows your number of points\n**.claim**\nLets you claim daily points\n**.pay**\nPay another user points\n**.leaderboard**\nShows a leaderboard\n**.totalpointslb**\nShows another leaderboard\n**.store**\nShows the storefront", inline=False)
    helpEmbed.set_footer(text="For more help, type .help `command` (ex. .help blackjack)")
    await ctx.send(embeds=helpEmbed)
@help.command(name = "blackjack")
async def blackjack_help(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    helpEmbed = discord.Embed(title = "H Welding Machine Help", description = "Help with the .blackjack command", color = bot_color)
    helpEmbed.add_field(name = ".blackjack `<bet>`", value = ".blackjack lets you bet your hard earned points on a game of blackjack")
    helpEmbed.set_footer(text = "All allegations of stacked decks or unfair odds will be ignored")
    await ctx.send(embed=helpEmbed)
@help.command(name = "roulette")
async def roulette_help(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    helpEmbed = discord.Embed(title = "H Welding Machine Help", description = "Help with the .roulette command", color = bot_color)
    helpEmbed.add_field(name = ".roulette `<type of bet>` `<bet>`", value = ".roulette lets you bet your hard earned points on a game of roulette", inline = False)
    helpEmbed.add_field(name = "Types of Bets", value = "- Red: Whether the ball will land on a red space\n- Black: Whether the ball will land on a black space\n- Even: Whether the ball will land on an even space\n- Odd: Whether the ball will land on an odd space\n- Lower: Whether the ball will land on a space whose value is less than 19\n- Greater: Whether the ball will land on a space whose value is greater than 18", inline = False)
    await ctx.send(embed=helpEmbed)
@help.command(name = "slots")
async def slots_help(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    helpEmbed = discord.Embed(title = "H Welding Machine Help", description = "Help with the .slots command", color = bot_color)
    helpEmbed.add_field(name = ".slots", value = ".slots lets you spend 10 of your hard earned points for a chance at big winnings", inline = False)
    helpEmbed.add_field(name = "Payouts", value = "- 🍒🍒🍒: 20 points\n- 🍊🍊🍊: 35 points\n- 🍋🍋🍋: 50 points\n- 🍑🍑🍑: 75 points\n- 🔔🔔🔔: 150 points\n- :seven::seven::seven:: JACKPOT 250 points", inline = False)
    await ctx.send(embed=helpEmbed)
@help.command(name = "points")
async def points_help(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    helpEmbed = discord.Embed(title = "H Welding Machine Help", description = "Help with the .points command", color = bot_color)
    helpEmbed.add_field(name = ".points", value = ".points allows you to see how many points you have")
    await ctx.send(embed=helpEmbed)
@help.command(name = "claim")
async def claim_help(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    helpEmbed = discord.Embed(title = "H Welding Machine Help", description = "Help with the .claim command", color = bot_color)
    helpEmbed.add_field(name = ".claim", value = "Lets you claim 25 points every 24 hours")
    await ctx.send(embed=helpEmbed)
@help.command(name = "pay")
async def pay_help(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    helpEmbed = discord.Embed(title = "H Welding Machine Help", description = "Help with the .pay command", color = bot_color)
    helpEmbed.add_field(name = ".pay `<player>` `<points>`", value = "Lets you give some of your hard earned points to another player")
    await ctx.send(embed=helpEmbed)
@help.command(name = "leaderboard")
async def leaderboard_help(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    helpEmbed = discord.Embed(title = "H Welding Machine Help", description = "Help with the .leaderboard command", color = bot_color)
    helpEmbed.add_field(name = ".leaderboard", value = "Lets you see the leaderboard of people with the most points")
    await ctx.send(embed=helpEmbed)
@help.command(name = "totalpointslb")
async def totalpointslb_help(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    helpEmbed = discord.Embed(title = "H Welding Machine Help", description = "Help with the .totalpointslb command", color = bot_color)
    helpEmbed.add_field(name = ".totalpointslb", value = "Lets you see the leaderboard of total gained points")
    await ctx.send(embed=helpEmbed)
@help.command(name = "store")
async def store_help(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    helpEmbed = discord.Embed(title = "H Welding Machine Help", description = "Help with the .store command", color = bot_color)
    helpEmbed.add_field(name = ".store `<item>`", value = "Lets you see what items are available to buy at the store\nYou can also see a specific item by doing `.store <item>` where item is one, two, etc. as displayed on the main store page")
    await ctx.send(embed=helpEmbed)

# MISCELLANEOUS HELP COMMANDS

@help.command(name = "miscellaneous")
async def miscellaneous_help(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    helpEmbed = discord.Embed(title = "H Welding Machine Help", description = "Help with the Miscellaneous category", color = bot_color)
    helpEmbed.add_field(name = ":game_die: Miscellaneous Commands :game_die:", value = "**.tictactoe**\nPlay a game of tic-tac-toe\n**.connect4**\nPlay a game of connect4\n**.source**\nSends a link to the source repo\n**.strikes**\nShows number of strikes\n**.suggestion**\nSends a suggestion for the bot\n**.purge**\nDeletes past bot messages\n**.asa**\nShows Asa's idle time\n**.finn**\nSends a picture to Finn", inline=False)
    helpEmbed.set_footer(text="For more help, type .help `command` (ex. .help tictactoe)")
    await ctx.send(embeds=helpEmbed)
@help.command(name = "tictactoe")
async def tictactoe_help(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    helpEmbed = discord.Embed(title = "H Welding Machine Help", description = "Help with .tictactoe command", color = bot_color)
    helpEmbed.add_field(name = ".tictactoe `<player>`", value = "Challenge another player to tic-tac-toe. Use 1-9 to indicate the space you would like to place your piece")
    await ctx.send(embed=helpEmbed)
@help.command(name = "finn")
async def finn_help(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    helpEmbed = discord.Embed(title = "H Welding Machine Help", description = "Help with .finn command", color = bot_color)
    helpEmbed.add_field(name = ".finn", value = "Sends a picture of feet to Finn")
    await ctx.send(embed=helpEmbed)
@help.command(name = "suggestion")
async def suggestion_help(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    helpEmbed = discord.Embed(title = "H Welding Machine Help", description = "Help with .suggestion command", color = bot_color)
    helpEmbed.add_field(name = ".suggestion `<suggestion>`", value = "Lets you suggest a feature for the bot")
    await ctx.send(embed=helpEmbed)
@help.command(name = "purge")
async def purge_help(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    helpEmbed = discord.Embed(title = "H Welding Machine Help", description = "Help with .purge command", color = bot_color)
    helpEmbed.add_field(name = ".purge `<# of messages>`", value = "Deletes all bot messages within the given number of messages")
    await ctx.send(embed=helpEmbed)
@help.command(name = "asa")
async def asa_help(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    helpEmbed = discord.Embed(title = "H Welding Machine Help", description = "Help with .asa command")
    helpEmbed.add_field(name = ".asa", value = "Displays the amount of time Asa has spent deafened in a VC")
    await ctx.send(embed=helpEmbed)
@help.command(name = "connect4")
async def connect4_help(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    helpEmbed = discord.Embed(title = "H Welding Machine Help", description = "Help with .connect4 command", color = bot_color)
    helpEmbed.add_field(name = ".connect4 `<player>`", value = "Challenge another player to connect four. Use 1-7 to indicate the column you would like to place your piece")
    await ctx.send(embed=helpEmbed)
@help.command(name = "strikes")
async def strikes_help(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    helpEmbed = discord.Embed(title = "H Welding Machine Help", description = "Help with .strikes command", color = bot_color)
    helpEmbed.add_field(name = ".strikes", value = "Indicates how many strikes you have in the counting channel")
    await ctx.send(embed=helpEmbed)
@help.command(name = "source")
async def source_help(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    helpEmbed = discord.Embed(title = "H Welding Machine Help", description = "Help with .source command", color = bot_color)
    helpEmbed.add_field(name = ".source", value = "Provides a link to the Git repo for the bot")
    await ctx.send(embed=helpEmbed)
#--------------------------------------------------------------------------------------------------------------------------------------#
#   _____  _____  _       _   __     __
#  / ____||_   _|| |     | |  \ \   / /
# | (___    | |  | |     | |   \ \_/ / 
#  \___ \   | |  | |     | |    \   /  
#  ____) | _| |_ | |____ | |____ | |   
# |_____/ |_____||______||______||_|                                                                              


@bot.command(name = "source")
async def source(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return 
    await ctx.send(f"Here's the link to the source repo.\nhttps://github.com/pure-life-git/counting-police")
@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command(name = "parker")
async def parker(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return 
    elif ctx.author.id not in modID:
        return

    SQL = "INSERT INTO parker VALUES (1)"
    cur.execute(SQL)

    await ctx.message.add_reaction('👍')


@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command(name = "parkercount")
async def parkercount(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    SQL = "SELECT * FROM parker;"
    cur.execute(SQL)
    res = cur.fetchall()
    await ctx.send(f"Parker has said some derivative of PogChamp {len(res)} times.")
    
#facilitates a tic-tac-toe game between two users
@commands.cooldown(1, 30, commands.BucketType.user)
@bot.command(name = "tictactoe", brief = "Challenge another player to a game of tic-tac-toe", description = "Simply type the command and then mention someone to start a game with them. To choose your space, treat the board as a numbered grid 1-9 starting at the top left.")
async def tictactoe(ctx):
    def checkWinner(board):
        return board['1'] == board['2'] == board['3'] != ' ' or board['4'] == board['5'] == board['6'] != ' ' or board['7'] == board['8'] == board['9'] != ' ' or board['1'] == board['4'] == board['7'] != ' ' or board['2'] == board['5'] == board['8'] != ' ' or board['3'] == board['6'] == board['9'] != ' ' or board['1'] == board['5'] == board['9'] != ' ' or board['3'] == board['5'] == board['7'] != ' '

    def getCompMove(board):
        corners = ['1', '3', '7', '9']
        for i in range (1,10):
            space = ''.join(i)
            copy = board.copy()
            if copy[space] == ' ':
                copy[space] = move
                if checkWinner(copy):
                    return space
        
        for i in range(1, 10):
            space = ''.join(i)
            copy = board.copy()
            if copy[space] == ' ':
                copy[space] = plays[0][1]
                if checkWinner(copy):
                    return space
        
        for i in corners:
            if board[i] == ' ':
                return i

        if board['5'] == ' ':
            return('5')
        


    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    game = True #this var keeps track of if the game is still being played
    bot = False
    moves = 0 #move counter
    
    board = { #establishes a dictionary containing the values at each space of the board 1-9
        '1': ' ', '2': ' ', '3': ' ', #first row
        '4': ' ', '5': ' ', '6': ' ', #second row
        '7': ' ', '8': ' ', '9': ' '  #third row
    }

    keys = board.keys() #this is our list of valid inputs for the users

    def printBoard(board): #this function prints the board in its current state
        return(f"` {board['1']} | {board['2']} | {board['3']} `\n`---+---+---`\n` {board['4']} | {board['5']} | {board['6']} `\n`---+---+---`\n` {board['7']} | {board['8']} | {board['9']} `")
    
    playerOne = ctx.message.author #sets player one as the person who initiated the challenge
    playerTwo = ctx.message.mentions[0] #sets player two as the person player one mentioned in their challenge
    if bot.user.mentioned_in(ctx.message):
        print('true')
        bot = True

    plays = [(playerOne,'x'), (playerTwo, 'o')] #gives each player a move set

    if not bot:

        challMsg = await ctx.send(f"{playerOne.name} has challenged {playerTwo.name} to a game of Tic Tac Toe! Do you accept? Y/N") #sends the challenge message
        try:
            msg = await bot.wait_for('message', check = lambda m: m.author == playerTwo, timeout = 30.0) #waits for a message from player two
            if msg.content.lower() == 'y':
                await ctx.send(f"Challenge accepted! {playerOne.name} goes first.") #if player two messaged "y" then the challenge is accepted
                await challMsg.delete() #deletes the challenge message that the bot sent
            else:
                await ctx.send('Challenge declined.') #if player two messaged anything other than "y", the challenge is declined and the command is returned
                await challMsg.delete() #deletes the challenge message that the bot sent
                return

        except asyncio.TimeoutError: #if the program raises a TimeoutError from asyncio, then the challenge times out
            await challMsg.delete() #deletes the challenge message that the bot sent
            await ctx.send("Challenge timed out.") #lets the user know that the challenge timed out
            return #returns the function

    while game == True: #checks if the game has ended
        
        if moves % 2 == 0: #check if its player one's turn
            mover = plays[0][0] #sets who is moving
            move = plays[0][1] #sets what piece they use
            mess = await bot.wait_for('message', check = lambda m: m.author == mover) #waits for the player's move

            if mess.content.lower() == 'end': #checks if the user wants to end the game
                game = False
                break

            elif mess.content.lower() not in keys: #checks if the space is a valid space on the board
                await ctx.send("That is not a valid input. Please enter a number 1-9")
                continue

            elif board[mess.content] != ' ': #checks if the space is full on the board
                await ctx.send("That space if full. Please pick a free space")
                continue
            else: #if none of the checks have triggered, then we set the board space to the player's piece and add one to the move count
                board[mess.content] = move
                moves += 1
        else: #else it's player two's turn
            mover = plays[1][0] #sets who is moving
            move = plays[1][1] #sets what piece they use
            if not bot:
                mess = await bot.wait_for('message', check = lambda m: m.author == mover) #waits for the player's move

                if mess.content.lower() == 'end': #checks if the user wants to end the game
                    game = False
                    break

                elif mess.content.lower() not in keys: #checks if the space is a valid space on the baord
                    await ctx.send("That is not a valid input. Please enter a number 1-9")
                    continue

                elif board[mess.content] != ' ': #checks if the space is full on the board
                    await ctx.send("That space if full. Please pick a free space") 
                    continue

                else: #if none of the checks have triggered, then we set the board space to the player's piece and add one to the move count
                    board[mess.content] = move
                    moves += 1
            else:
                board[getCompMove(board)] = move
                moves += 1
                               
        #Win Conditions
        if moves >=5:
            if board['1'] == board['2'] == board['3'] != ' ': #3 across the top
                await ctx.send(f"{mover.name} has won the gamein {moves} moves!") #formats the string with the player name and number of moves
                game = False
                await ctx.send(f"~~` {board['1']} | {board['2']} | {board['3']} `~~\n`---+---+---`\n` {board['4']} | {board['5']} | {board['6']} `\n`---+---+---`\n` {board['7']} | {board['8']} | {board['9']} `")
                 #prints out the winning board with strikethrough
                return

            elif board['4'] == board['5'] == board['6'] != ' ': #3 across the middle
                await ctx.send(f"{mover.name} has won the game in {moves} moves!") #formats the string with the player name and number of moves
                game = False
                await ctx.send(f"` {board['1']} | {board['2']} | {board['3']} `\n`---+---+---`\n~~` {board['4']} | {board['5']} | {board['6']} `~~\n`---+---+---`\n` {board['7']} | {board['8']} | {board['9']} `")
                 #prints out the winning board with strikethrough
                return

            elif board['7'] == board['8'] == board['9'] != ' ': #3 across the bottom
                await ctx.send(f"{mover.name} has won the game in {moves} moves!") #formats the string with the player name and number of moves
                game = False
                await ctx.send(f"` {board['1']} | {board['2']} | {board['3']} `\n`---+---+---`\n` {board['4']} | {board['5']} | {board['6']} `\n`---+---+---`\n~~` {board['7']} | {board['8']} | {board['9']} `~~")
                 #prints out the winning board with strikethrough
                return

            elif board['1'] == board['4'] == board['7'] != ' ': #3 down the right
                await ctx.send(f"{mover.name} has won the game in {moves} moves!") #formats the string with the player name and number of moves
                game = False
                await ctx.send(printBoard(board)) #prints out the winning board
                return

            elif board['2'] == board['5'] == board['8'] != ' ': #3 down the middle
                await ctx.send(f"{mover.name} has won the game in {moves} moves!") #formats the string with the player name and number of moves
                game = False
                await ctx.send(printBoard(board)) #prints out the winning board
                return

            elif board['3'] == board['6'] == board['9'] != ' ': #3 down the right
                await ctx.send(f"{mover.name} has won the game in {moves} moves!") #formats the string with the player name and number of moves
                game = False
                await ctx.send(printBoard(board)) #prints out the winning board
                return

            elif board['1'] == board['5'] == board['9'] != ' ': #3 from top left to bottom right
                await ctx.send(f"{mover.name} has won the game in {moves} moves!") #formats the string with the player name and number of moves
                game = False
                await ctx.send(printBoard(board)) #prints out the winning board
                return

            elif board['3'] == board['5'] == board['7'] != ' ': #3 from top right to bottom left
                await ctx.send(f"{mover.name} has won the game in {moves} moves!") #formats the string with the player name and number of moves
                game = False
                await ctx.send(printBoard(board)) #prints out the winning board
                return
        
        await ctx.send(printBoard(board))
        if moves == 9: #checks to see if the game is a draw
            await ctx.send("The game is a draw.") #sends a message to the channel letting the players know it's a draw
            game = False #sets the game to false
            return #returns the function

@commands.cooldown(1, 15, commands.BucketType.user)
@bot.command(name="connect4")
async def connectfour(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    keys = ["1","2","3","4","5","6","7"]
    def printBoard(board):
        return(f"""```
|{board[0][0]}|{board[1][0]}|{board[2][0]}|{board[3][0]}|{board[4][0]}|{board[5][0]}|{board[6][0]}|
|---+---+---+---+---+---+---|
|{board[0][1]}|{board[1][1]}|{board[2][1]}|{board[3][1]}|{board[4][1]}|{board[5][1]}|{board[6][1]}|
|---+---+---+---+---+---+---|
|{board[0][2]}|{board[1][2]}|{board[2][2]}|{board[3][2]}|{board[4][2]}|{board[5][2]}|{board[6][2]}|
|---+---+---+---+---+---+---|
|{board[0][3]}|{board[1][3]}|{board[2][3]}|{board[3][3]}|{board[4][3]}|{board[5][3]}|{board[6][3]}|
|---+---+---+---+---+---+---|
|{board[0][4]}|{board[1][4]}|{board[2][4]}|{board[3][4]}|{board[4][4]}|{board[5][4]}|{board[6][4]}|
|---+---+---+---+---+---+---|
|{board[0][5]}|{board[1][5]}|{board[2][5]}|{board[3][5]}|{board[4][5]}|{board[5][5]}|{board[6][5]}|
|---+---+---+---+---+---+---|
| 1 | 2 | 3 | 4 | 5 | 6 | 7 |
        ```""")

    def winconds(board, move: tuple, piece: str):
        col, row = move

        # check for 4 in up/down
        vertWin = False
        count = 0
        for i in range(4):
            try:
                if board[col][row+i] == piece:
                    count+= 1
                    if count == 4:
                        vertWin = True
                        return vertWin
                
                else:
                    break
            except IndexError:
                break
        

        #check for left/right win
        horWin = False
        count = 0
        for i in range(6):
            try:
                if board[i][row] == piece:
                    count += 1
                    if count == 4:
                        horWin = True
                        return horWin
                else:
                    count = 0
            except IndexError:
                break


        #check for bot. left -> top right
        topleft = row < 3 and col < 3
        bottomright = row > 2 and col  > 3
        if topleft or bottomright:
            bltrWin = False
        else:
            for x in range(3):
                for y in reversed(range(3,6)):
                    try:
                        # print("Spaces: \n", x,y,": ",board[x][y], "\n", x+1, y-1,": ", board[x+1][y-1],"\n",x+2,y-2,": ",board[x+2][y-2],"\n",x+3,y-3,": ",board[x+3][y-3])
                        if board[x][y] == piece and board[x+1][y-1] == piece and board[x+2][y-2] == piece and board[x+3][y-3] == piece:
                            bltrWin = True
                            return bltrWin
                    except IndexError:
                        continue

        #check for top left -> bot. right
        bottomleft = row > 2 and col < 3
        topright = row < 3 and col > 3
        if bottomleft or topright:
            tlbrWin = False
        else:
            for x in range(4):
                for y in range(3):
                    try:
                        # print("Spaces: \n", x,y,": ",board[x][y], "\n", x+1, y+1,": ", board[x+1][y+1],"\n",x+2,y+2,": ",board[x+2][y+2],"\n",x+3,y+3,": ",board[x+3][y+3])
                        if board[x][y] == piece and board[x+1][y+1] == piece and board[x+2][y+2] == piece and board[x+3][y+3] == piece:
                            tlbrWin = True
                            return tlbrWin
                    except IndexError:
                        continue
        print("done with winconds")
        return False

    board = [["   " for i in range(6)] for i in range(7)]

    playerone = ctx.author
    playertwo = ctx.message.mentions[0]
    challMsg = await ctx.send(f"{playerone.name} has challenged {playertwo.name} to a game of Connect 4! Do you accept? Y/N")
    try:
        msg = await bot.wait_for('message', check = lambda m: m.author == playertwo, timeout = 30.0)
        if msg.content.lower() in ['y', 'yes']:
            await ctx.send(f"Challenge accepted! {playerone.name} goes first.")
            await challMsg.delete()
        else:
            await ctx.send('Challenge declined.')
            await challMsg.delete()
            return
    except asyncio.TimeoutError:
        await challMsg.delete()
        await ctx.send("Challenge timed out.")
        return
    plays = [(playerone, " X "), (playertwo, " O ")]
    boardEmbed = discord.Embed(title = "Connect 4", color = discord.Color.red())
    boardEmbed.add_field(name="Board", value=printBoard(board), inline=False)
    boardEmbed.add_field(name="Turn:", value=f"{playerone.name}", inline=False)
    ogmessage = await ctx.send(embed=boardEmbed)
    allimportantid = ogmessage.id
    game = True
    movecount = 0
    while game:
        boardmessage = await ctx.fetch_message(allimportantid)
        if movecount % 2 == 0:
            player = playerone
            piece = plays[0][1]
            embedColor = discord.Color.red()
        else: 
            player = playertwo
            piece = plays[1][1]
            embedColor = discord.Color.gold()
        if movecount > 0:
            boardEmbed = discord.Embed(title = "Connect 4", color = embedColor)
            boardEmbed.add_field(name="Board", value=printBoard(board), inline=False)
            boardEmbed.add_field(name="Turn:", value=f"{player.name}", inline=False)
            await boardmessage.edit(embed=boardEmbed)

        move = await bot.wait_for('message', check = lambda m: m.author == player)
        if move.content.lower() == 'end':
            game = False
            await ctx.send(f"Game ended by {player}.")
            return
        elif move.content.lower() not in keys:
            await ctx.send("That is not a valid column. Please enter a number 1-7.")
            continue
        elif all(x != "   " for x in board[int(move.content)-1][1:]) == False:
            await ctx.send("That column is full. Please choose another.")
            continue

        column = board[int(move.content)-1]
        for count, row in enumerate(column): 
            if row != "   ":
                column[count-1] = piece
                if winconds(board, (int(move.content)-1, count-1), piece):
                    await move.delete()
                    game = False
                    boardEmbed = discord.Embed(title = "Connect 4", color = embedColor)
                    boardEmbed.add_field(name="Board", value=printBoard(board), inline=False)
                    boardEmbed.add_field(name="Turn:", value=f"{player.name}", inline=False)
                    await boardmessage.edit(embed=boardEmbed)
                    await ctx.send("You win!")
                    return
                break
            elif count == 5:
                board[int(move.content)-1][5] = piece
                win = winconds(board, (int(move.content)-1, 5), piece)
                if win:
                    await move.delete()
                    game = False
                    boardEmbed = discord.Embed(title = "Connect 4", color = embedColor)
                    boardEmbed.add_field(name="Board", value=printBoard(board), inline=False)
                    boardEmbed.add_field(name="Turn:", value=f"{player.name}", inline=False)
                    await boardmessage.edit(embed=boardEmbed)
                    await ctx.send("You win!")
                    return
                break
        stalecount = 0
        for cols in range(6):
            if all(elem != "   " for elem in board[cols]):
                stalecount += 1
                if stalecount == 7:
                    await move.delete()
                    game = False
                    boardEmbed = discord.Embed(title = "Connect 4", color = embedColor)
                    boardEmbed.add_field(name="Board", value=printBoard(board), inline=False)
                    boardEmbed.add_field(name="Turn:", value=f"{player.name}", inline=False)
                    await boardmessage.edit(embed=boardEmbed)
                    await ctx.send("The game is a stalemate!")
                    return
            else: break
        await move.delete()
        movecount += 1

#sends a random picture from the forbiddenList directly to Finn
@commands.cooldown(1, 15, commands.BucketType.user)
@bot.command(name = 'finn', description = 'Sends a feet pic to Finn')
async def finn(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    link = random.choice(forbiddenList)
    finnEmbed = discord.Embed(title="Feet Pics", description="Kinda cringe.", type="rich", color=discord.Color.dark_green())
    finnEmbed.set_image(url=link)
    id = int(203300155762540544) #sets id as Finn's userId
    finn = await ctx.message.guild.fetch_member(id) #fetches Finn's user from his id
    await finn.send(embed=finnEmbed)
    await ctx.message.add_reaction("🦶")

@bot.command(name="suggestion", brief="Submit a suggestion for the bot", description = "Submit a suggestion for the bot")
async def suggestion(ctx, *args):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    await ctx.message.add_reaction("🖕")
    await ctx.channel.send(f"This --> ({' '.join(args)}) fucking sucks. You should be ashamed.")

@commands.cooldown(1, 15, commands.BucketType.user)
@bot.command(name="asa")
async def asa(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    asa = bot.get_guild(270384027330936835).get_member(227250029788790785)

    if asa.voice != None and asa.voice.self_deaf:
        SQL = f"SELECT deafenstart FROM asa;"
        cur.execute(SQL)
        deafen_start = int(cur.fetchone()[0])

        cur_deaf = int(datetime.datetime.now().timestamp() - deafen_start)
        cur_deaf_orig = cur_deaf

        hours = cur_deaf // 3600 #gets number of hours asa has been deafened for this session

        cur_deaf %= 3600
        minutes = cur_deaf // 60 #gets number of minutes asa has been deafened for this session

        cur_deaf %= 60
        seconds = cur_deaf #gets number of seconds asa has been deafened for this session

        
        await ctx.send(f"Asa is on a {hours}h {minutes}m {seconds}s streak.")

        SQL = f"SELECT idletime FROM asa;"
        cur.execute(SQL)
        cur_time = cur.fetchone()[0]
        cur_time += cur_deaf_orig

        hours = cur_time // 3600 #gets number of hours until next claim time

        cur_time %= 3600
        minutes = cur_time // 60 #gets number of minutes until next claim time minus hours

        cur_time %= 60
        seconds = cur_time #gets number of seconds until next claim time minus hours and minutes
        
        await ctx.send(f"Asa has been deafened in a VC for {hours}h {minutes}m {seconds}s.")

        return

    SQL = f"SELECT idleTime from asa;"
    cur.execute(SQL)
    time = int(cur.fetchone()[0])

    hours = time // 3600 #gets number of hours until next claim time

    time %= 3600
    minutes = time // 60 #gets number of minutes until next claim time minus hours

    time %= 60
    seconds = time #gets number of seconds until next claim time minus hours and minutes

    await ctx.send(f"Asa has been deafened in a VC for {hours}h {minutes}m {seconds}s.")

    return

#--------------------------------------------------------------------------------------------------------------------------------------#
#   __  __   _    _    _____   _____    _____ 
#  |  \/  | | |  | |  / ____| |_   _|  / ____|
#  | \  / | | |  | | | (___     | |   | |     
#  | |\/| | | |  | |  \___ \    | |   | |     
#  | |  | | | |__| |  ____) |  _| |_  | |____ 
#  |_|  |_|  \____/  |_____/  |_____|  \_____|
# 


def col_to_sec(time:str):
    if len(time.split(":")) == 2:
        h=0
        m,s = time.split(':')
    elif len(time.split(":")) == 1:
        h,m = 0,0
        s=time
    else:
        h, m, s = time.split(':')

    return(int(h) * 3600 + int(m) * 60 + int(s))

def get_track_names(user, playlist_id):
    track_names = []
    playlist = sp.user_playlist(user, playlist_id)
    for item in playlist['tracks']['items']:
        track = item['track']
        track_names.append(sp.track(track['id'])['name'])
    return track_names

async def play_spotify(ctx, song):
    ytresults = YoutubeSearch(song, max_results=1).to_dict()

    if len(ytresults) == 0:
        await ctx.send("No results.")
        return
    else:
        song = "".join(("https://www.youtube.com", ytresults[0]["url_suffix"]))
        title = ytresults[0]["title"]
        channel = ytresults[0]["channel"]
        runtime = ytresults[0]["duration"]

    if len(runtime.split(":")) == 2:
        h=0
        m,s = runtime.split(':')
    elif len(runtime.split(":")) == 1:
        h,m = 0,0
        s=runtime
    else:
        h, m, s = runtime.split(':')

    runtime_sec = int(h) * 3600 + int(m) * 60 + int(s)

    if runtime_sec > 7200:
        await ctx.send("Cannot queue a song longer than 2 hours.")
        return

    voice = ctx.guild.voice_client

    if voice:
        if voice.is_playing():
            music_queue.append((song, title, channel, runtime, ctx.author))
            return
        else:
            await play_music(ctx, (song,title,channel, runtime, ctx.author))
    else:
        await ctx.author.voice.channel.connect()
        await play_music(ctx,(song,title,channel, runtime, ctx.author))


async def check_play_next(ctx):
    voice = ctx.guild.voice_client

    if len(music_queue) > 0:
        if repeating:
            if voice.is_playing():
                voice.stop()
                await play_music(ctx, now_playing)
                return
            else:
                await play_music(ctx, now_playing)
                return
        else:
            if voice.is_playing():
                print("check: voice is playing")
                voice.stop()
                await play_music(ctx, music_queue.pop(0))
                return
            else:
                print("check: voice isn't playing")
                await play_music(ctx, music_queue.pop(0))
                return
    else:
        if repeating:
            if voice.is_playing():
                voice.stop()
                await play_music(ctx,now_playing)
                return
            else:
                await play_music(ctx, now_playing)
                return
        else:
            voice.stop()
            await asyncio.sleep(120)
            print("idling...")
            if not voice.is_playing():
                asyncio.run_coroutine_threadsafe(voice.disconnect(), bot.loop)                                 

async def play_music(ctx,song):
    print(f"playing {song[1]}")
    if isinstance(ctx, discord.VoiceChannel):
        song_there = os.path.isfile("song.mp3")

        if song_there:
            os.remove("song.mp3")

        voice = ctx.guild.voice_client

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([song])

        if voice:
            if voice.is_connected():
                if voice.is_playing():
                    voice.stop()
                    voice.play(FFmpegPCMAudio(source="song.mp3"))
                else:
                    voice.play(FFmpegPCMAudio(source="song.mp3"))
            else:
                await ctx.connect()
                voice.play(FFmpegPCMAudio(source="song.mp3"))
        else:
            voice = await ctx.connect()
            voice.play(FFmpegPCMAudio(source="song.mp3"))
        await asyncio.sleep(120)
        if not voice.is_playing():
            asyncio.run_coroutine_threadsafe(voice.disconnect(), bot.loop)    
        return
        
    global now_playing
    if song != now_playing:
        now_playing = (song[0], song[1], song[2], song[3], song[4], int(datetime.datetime.now().timestamp()))
    title = song[1]
    channel = song[2]
    runtime = song[3]
    author = song[4]
    song = song[0]

    song_there = os.path.isfile("song.mp3")

    if song_there:
        os.remove("song.mp3")

    voice = ctx.guild.voice_client

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([song])
    
    
    # await ctx.send(f"**Now Playing:** {title} - {channel} | {runtime}")
    voice.play(FFmpegPCMAudio(source="song.mp3"), after = lambda e: asyncio.run_coroutine_threadsafe(check_play_next(ctx),bot.loop()))
    np_embed = discord.Embed(title="Now Playing", description=f"`{title}` requested by {author.mention}", value=f"Duration: {runtime}", color=bot_color)
    await ctx.send(embed=np_embed)

@bot.command(name="play", description="Plays a song in a voice channel", aliases=["p"])
async def play(ctx, *args):
    cur.execute(f"SELECT ignore FROM musicbot WHERE id = {int(ctx.author.id)};")
    ignored = cur.fetchone()[0]
    if str(ctx.channel) not in ["jukebox", "admins-only"]:
        await ctx.message.delete()
        return
    elif ignored:
        return

    song = " ".join(args)
    
    uservoice = ctx.author.voice

    if uservoice is None or uservoice.channel.name == "Out to Lunch - AFK":
        await ctx.send("You must be in an active voice channel to play music.")
        return
    
    if song.startswith("https://open.spotify.com/playlist"):
        track_names = get_track_names('spotify', song.split('playlist/')[1].split('?')[0])
        for track in track_names:
            await play_spotify(ctx, track)
        
        await ctx.send(f"Added `{len(track_names)}` songs to the queue.")
        return

    ytresults = YoutubeSearch(song, max_results=1).to_dict()

    if len(ytresults) == 0:
        await ctx.send("No results.")
        return
    else:
        song = "".join(("https://www.youtube.com", ytresults[0]["url_suffix"]))
        title = ytresults[0]["title"]
        channel = ytresults[0]["channel"]
        runtime = ytresults[0]["duration"]

    runtime_sec = col_to_sec(runtime)

    if runtime_sec > 7200:
        await ctx.send("Cannot queue a song longer than 2 hours.")
        return

    voice = ctx.guild.voice_client

    if voice:
        if voice.is_playing():
            music_queue.append((song, title, channel, runtime, ctx.author))
            total_runtime = 0
            for song in music_queue[1:]:
                total_runtime += col_to_sec(song[3])
            
            total_runtime += col_to_sec(now_playing[3])-(int(datetime.datetime.now().timestamp())-now_playing[5])

            queueadd_embed = discord.Embed(title="**Added to Queue**", description=f"Added `{title}` to the queue.\nEstimated Time until Playing: `{str(datetime.timedelta(seconds=total_runtime))}`", color=bot_color)
            await ctx.send(embed=queueadd_embed)
            return
        else:
            await play_music(ctx, (song,title,channel, runtime, ctx.author))
    else:
        await uservoice.channel.connect()
        await play_music(ctx,(song,title,channel, runtime, ctx.author))

@bot.command(name="skip", description="Skips the currently playing song", aliases=["s"])
async def skip(ctx):
    cur.execute(f"SELECT ignore FROM musicbot WHERE id = {int(ctx.author.id)};")
    ignored = cur.fetchone()[0]
    if str(ctx.channel) not in ["jukebox", "admins-only"]:
        await ctx.message.delete()
        return
    elif ignored:
        return
    # elif "Coin Operator" not in [i.name for i in ctx.author.roles]:
    #     await ctx.send("You need a role called `Coin Operator` to do that.")

    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        if voice.is_playing():
            voice.stop()
            if len(music_queue)>0:
                await check_play_next(ctx)
        else:
            await ctx.send("The bot is not currently playing anything")
            return
    else:
        await ctx.send("The bot is not connected to an active voice channel.")

@bot.command(name="leave", description="Makes the bot leave an active voice channel", aliases=["l"])
async def leave(ctx):
    cur.execute(f"SELECT ignore FROM musicbot WHERE id = {int(ctx.author.id)};")
    ignored = cur.fetchone()[0]
    if str(ctx.channel) not in ["jukebox", "admins-only"]:
        await ctx.message.delete()
        return
    elif ignored:
        return
    # elif "Coin Operator" not in [i.name for i in ctx.author.roles]:
    #     await ctx.send("You need a role called `Coin Operator` to do that.")
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
        music_queue.clear()
    else:
        await ctx.send("The bot is not connected to an active voice channel.")
        return

@bot.command(name="clear", description="Clears the queue", aliases=["c"])
async def clear(ctx):
    cur.execute(f"SELECT ignore FROM musicbot WHERE id = {int(ctx.author.id)};")
    ignored = cur.fetchone()[0]
    if str(ctx.channel) not in ["jukebox", "admins-only"]:
        await ctx.message.delete()
        return
    elif ignored:
        return
    # elif "Coin Operator" not in [i.name for i in ctx.author.roles]:
    #     await ctx.send("You need a role called `Coin Operator` to do that.")
    num_songs = len(music_queue)
    music_queue.clear()
    await ctx.send(f"The queue has been cleared of {num_songs} songs.")

@bot.command(name="queue", description="Displays the queue of songs", aliases=["q"])
async def queue(ctx):
    if str(ctx.channel) not in ["jukebox", "admins-only"]:
        await ctx.message.delete()
        return
    
    total_runtime = 0
    queue_embed = discord.Embed(title="Music Queue", description="", color=bot_color)
    queue_embed.add_field(name=":musical_note: Now Playing :musical_note:", value=f"Title: {now_playing[1]}  |  Channel: {now_playing[2]}\nRuntime: {now_playing[3]}  |  Queued by: {now_playing[4].mention}")
    for num,song in enumerate(music_queue):
        if num < 6:
            queue_embed.add_field(name=f"{num+1} - {song[1]} | {song[2]}", value=f"Runtime: {song[3]}  |  Queued by: {song[4].mention}", inline=False)
        total_runtime += col_to_sec(song[3])
    
    total_runtime += col_to_sec(now_playing[3])-(int(datetime.datetime.now().timestamp())-now_playing[5])
    if len(music_queue) > 7:
        queue_embed.add_field(name="-=-=-=-=-=-=-=-=-=-=-==-=-=-=-", value=f"+ {len(music_queue)-5} more")
    
    hms_runtime = str(datetime.timedelta(seconds = total_runtime))

    queue_embed.add_field(name="Length", value=f"{len(music_queue)}", inline = False)
    queue_embed.add_field(name="Repeating", value=repeating, inline=True)
    queue_embed.add_field(name = "Total Playtime", value = hms_runtime, inline=True)

    await ctx.send(embed=queue_embed)

@bot.command(name="repeat", description="Toggles song repeating", aliases=["r"])
async def repeat(ctx):
    cur.execute(f"SELECT ignore FROM musicbot WHERE id = {int(ctx.author.id)};")
    ignored = cur.fetchone()[0]
    if str(ctx.channel) not in ["jukebox", "admins-only"]:
        await ctx.message.delete()
        return
    elif ignored:
        return
    # elif "Coin Operator" not in [i.name for i in ctx.author.roles]:
    #     await ctx.send("You need a role called `Coin Operator` to do that.")
    global repeating
    repeating = not repeating
    await ctx.send(f"**Repeating:** {repeating}")

@bot.command(name="shuffle", description="Shuffles the music queue")
async def shuffle(ctx):
    cur.execute(f"SELECT ignore FROM musicbot WHERE id = {int(ctx.author.id)};")
    ignored = cur.fetchone()[0]
    if str(ctx.channel) not in ["jukebox", "admins-only"]:
        await ctx.message.delete()
        return
    elif ignored:
        return
    # elif "Coin Operator" not in [i.name for i in ctx.author.roles]:
    #     await ctx.send("You need a role called `Coin Operator` to do that.")
    random.shuffle(music_queue)
    await ctx.send("Queue successfully shuffled.")

@bot.command(name="ignore", description="Lets a Coin Operator take away someone's music bot privileges", aliases=["i"])
async def ignore(ctx, user: discord.Member):
    cur.execute(f"SELECT ignore FROM musicbot WHERE id = {int(ctx.author.id)};")
    ignored = cur.fetchone()[0]
    print(ignored)
    if str(ctx.channel) not in ["jukebox", "admins-only"]:
        await ctx.message.delete()
        return
    elif ignored or ctx.author.id not in modID:
        return

    name = user.name
    id = int(user.id)
    print(id)
    SQL = f"UPDATE musicbot SET ignore = NOT ignore WHERE id = {id};"

    cur.execute(SQL)
    conn.commit()

    SQL = f"SELECT ignore FROM musicbot WHERE id = {id};"
    cur.execute(SQL)
    ignored = cur.fetchone()[0]
    if ignored:
        await ctx.send(f"{name} is now being ignored by the music bot.")
    else:
        await ctx.send(f"{name} is no longer being ignored by the music bot.")

@bot.command(name="remove", description="Lets a user remove a song from the queue")
async def remove(ctx, index: int):
    cur.execute(f"SELECT ignore FROM musicbot WHERE id = {int(ctx.author.id)};")
    ignored = cur.fetchone()[0]
    if str(ctx.channel) not in ["jukebox", "admins-only"]:
        await ctx.message.delete()
        return
    elif ignored:
        return
    # elif "Coin Operator" not in [i.name for i in ctx.author.roles]:
    #     await ctx.send("You need a role called `Coin Operator` to do that.")
    if index < 1 or index > len(music_queue):
        await ctx.send("That is not a valid queue position.")
        return

    song = music_queue.pop(index-1)
    await ctx.send(f"Removed `{song[1]} - {song[2]}` queued by `{song[4].mention}`")

@bot.command(name="nowplaying", description="Displays the song that is currently playing", aliases=["np"])
async def nowplaying(ctx):
    nowplaying_embed = discord.Embed(title = ":musical_note: Now Playing :musical_note:", description="", color=bot_color)
    nowplaying_embed.add_field(name=f"{now_playing[1]}", value=f"Artist: {now_playing[2]}\nRuntime: {now_playing[3]}\nQueued by: {now_playing[4].mention}")
    await ctx.send(embed=nowplaying_embed)



#--------------------------------------------------------------------------------------------------------------------------------------#
#   _____            __  __  ____   _       _____  _   _   _____ 
#  / ____|    /\    |  \/  ||  _ \ | |     |_   _|| \ | | / ____|
# | |  __    /  \   | \  / || |_) || |       | |  |  \| || |  __ 
# | | |_ |  / /\ \  | |\/| ||  _ < | |       | |  | . ` || | |_ |
# | |__| | / ____ \ | |  | || |_) || |____  _| |_ | |\  || |__| |
#  \_____|/_/    \_\|_|  |_||____/ |______||_____||_| \_| \_____|                                                                
                                                                

#lets the user see how many points they have to gamble
@commands.cooldown(1, 15, commands.BucketType.user)
@bot.command(name = 'points', description = "Tells the user how many points they have for gambling")
async def points(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    SQL = f"SELECT pointnumber FROM points WHERE id = {ctx.author.id};" #gets the point value from the DB
    while True:
        try:
            cur.execute(SQL)
            break
        except psycopg2.InterfaceError:
            reestablish()
    numPoints = cur.fetchone()
    conn.commit()

    #april fools
    # if int(numPoints[0]) == 0:
    #     await ctx.send("You're broke.")
    #     return  
    # lower_limit = random.randint(0,50)
    # upper_limit = random.randint(0,50)

    # while int(numPoints[0])-lower_limit < 0:
    #     lower_limit = random.randint(0,50)
    # await ctx.send(f'You have between {int(numPoints[0])-lower_limit} and {int(numPoints[0])+upper_limit} points.')

    await ctx.send(f'You have {numPoints[0]} points.') #sends a message with the point value


#lets the user play blackjack and gamble their points
@commands.cooldown(1, 15, commands.BucketType.user)
@bot.command(name = "blackjack", brief = "Allows the user to bet their points on a game of blackjack", description = "Type the command and then the amount of points you would like to bet")
async def blackjack(ctx, bet: int):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    game = True
    dealer = True
    player = ctx.author

    SQL = f"SELECT pointnumber FROM points WHERE id = {player.id};"
    while True:
        try:
            cur.execute(SQL)
            break
        except psycopg2.InterfaceError:
            reestablish()
    points = cur.fetchone()[0]

    if bet > points or bet <= 0: #checks if the user has enough points to place the bet
        await ctx.send("You do not have enough points to bet that much.")
        return
    
    SQL = f"UPDATE points SET pointnumber = {points-bet} WHERE id = {player.id};" #subtracts the points from their "account"
    while True:
        try:
            cur.execute(SQL)
            break
        except psycopg2.InterfaceError:
            reestablish()
    conn.commit()

    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] * 4 #initializes the deck as a list
    playerHand = deal(deck) #deals cards to the player
    dealerHand = deal(deck) #deals cards to the dealer
    await ctx.send(f"The dealer is showing a {dealerHand[0]}.") #tells the user what the dealer is showing
    await ctx.send(f"Your Hand: {', '.join(map(str,playerHand))}\nTotal: {total(playerHand)}") #tells the user what their hand is

    while game == True:
        if total(playerHand) == 21:
            await ctx.send("Congratulations! You got a blackjack.")
            game = False
            SQL = f"UPDATE points SET pointnumber = {points+bet} WHERE id = {player.id}" #adds the bet*2 to the users "account"
            while True:
                try:
                    cur.execute(SQL)
                    break
                except psycopg2.InterfaceError:
                    reestablish()
            conn.commit()
            
            SQL = f"UPDATE points SET bjwins = bjwins + 1 WHERE id = {player.id};"
            cur.execute(SQL)
            conn.commit()

            SQL = f"UPDATE points SET totalpoints = totalpoints + {bet} WHERE id = {player.id};"
            cur.execute(SQL)
            conn.commit()
            bjRole = ctx.guild.get_role(794512596740079616)
            if bjwin(player) == True:
                if bjRole not in player.roles:
                    await player.add_roles(bjRole)
                for member in bjRole.members:
                    if member != ctx.author:
                        await member.remove_roles(bjRole)
            return
        await ctx.send("Would you like to [H]it, [S]tand, [D]ouble or [Q]uit") #asks the user for their input
        try:
            move = await bot.wait_for('message', check = lambda m: m.author == ctx.author) #waits for the message from the user
            if move.content.lower() == "h"or move.content.lower() == "hit": #checks if they want to hit
                playerHand = hit(playerHand, deck) #calls the hit function
                await ctx.send(f"{ctx.author.mention} Your Hand: {', '.join(map(str,playerHand))}\nTotal: {total(playerHand)}") #sends the players hand
                if total(playerHand) == 21: #checks for blackjack
                    await ctx.send("Congratulations! You got a blackjack.")
                    game = False
                    SQL = f"UPDATE points SET pointnumber = {points+bet} WHERE id = {player.id}" #adds the bet*2 to the users "account"
                    while True:
                        try:
                            cur.execute(SQL)
                            break
                        except psycopg2.InterfaceError:
                            reestablish()
                    conn.commit()
                    SQL = f"UPDATE points SET bjwins = bjwins + 1 WHERE id = {player.id};"
                    cur.execute(SQL)
                    conn.commit()

                    SQL = f"UPDATE points SET totalpoints = totalpoints + {bet} WHERE id = {player.id};"
                    cur.execute(SQL)
                    conn.commit()
                    bjRole = ctx.guild.get_role(794512596740079616)
                    if bjwin(player) == True:
                        if bjRole not in player.roles:
                            await player.add_roles(bjRole)
                        for member in bjRole.members:
                            if member != ctx.author:
                                await member.remove_roles(bjRole)
                    return

                elif total(playerHand) > 21: #checks for user bust
                    await ctx.send("You busted! Good luck next time.")
                    game = False
                    return

                else:
                    continue

            elif move.content.lower() == "s" or move.content.lower() == "stand": #checks if they want to stand
                game = False
                break
                
            elif move.content.lower() == "d" or move.content.lower() == "double":
                if points-bet < bet:
                    await ctx.send("You don't have enough points to double down.")
                    continue
                SQL = f"UPDATE points SET pointnumber = {points-(bet*2)} WHERE id = {player.id};" #subtracts the points from their "account"
                while True:
                    try:
                        cur.execute(SQL)
                        break
                    except psycopg2.InterfaceError:
                        reestablish()
                conn.commit()
                bet *= 2
                playerHand = hit(playerHand, deck)
                await ctx.send(f"Your Hand: {', '.join(map(str,playerHand))}\nTotal: {total(playerHand)}") #sends the players hand
                if total(playerHand) == 21: #checks for blackjack
                    await ctx.send("Congratulations! You got a blackjack.")
                    game = False
                    SQL = f"UPDATE points SET pointnumber = {points+bet} WHERE id = {player.id}" #adds the bet*2 to the users "account"
                    while True:
                        try:
                            cur.execute(SQL)
                            break
                        except psycopg2.InterfaceError:
                            reestablish()
                    conn.commit()
                    SQL = f"UPDATE points SET bjwins = bjwins + 1 WHERE id = {player.id};"
                    cur.execute(SQL)
                    conn.commit()

                    SQL = f"UPDATE points SET totalpoints = totalpoints + {bet} WHERE id = {player.id};"
                    cur.execute(SQL)
                    conn.commit()
                    bjRole = ctx.guild.get_role(794512596740079616)
                    if bjwin(player) == True:
                        if bjRole not in player.roles:
                            await player.add_roles(bjRole)
                        for member in bjRole.members:
                            if member != ctx.author:
                                await member.remove_roles(bjRole)
                    return

                elif total(playerHand) > 21: #checks for user bust
                    await ctx.send("You busted! Good luck next time.")
                    game = False
                    return
                else:
                    break

            else: #else they quit the game
                game = False
                await ctx.send("You quit.")
                return

        except asyncio.TimeoutError: #check for TimeoutError
            await ctx.send("The game timed out")
            return
    
    while dealer == True: #loop for dealer moves
        await ctx.send(f'Dealer Hand: {", ".join(map(str,dealerHand))}\nTotal: {total(dealerHand)}') #tells the user the new dealer's hand
        if total(dealerHand) == 21: #checks for blackjack
            await ctx.send("The dealer got a blackjack! Good luck next time.")
            dealer = False
            return

        elif total(dealerHand) > 21: #checks for dealer bust
            await ctx.send("The dealer busted! Congratulations.")
            dealer = False
            SQL = f"UPDATE points SET pointnumber = {points+bet} WHERE id = {player.id}" #adds double the bet to the user's account
            while True:
                try:
                    cur.execute(SQL)
                    break
                except psycopg2.InterfaceError:
                    reestablish()
            conn.commit()
            SQL = f"UPDATE points SET bjwins = bjwins + 1 WHERE id = {player.id};"
            cur.execute(SQL)
            conn.commit()

            SQL = f"UPDATE points SET totalpoints = totalpoints + {bet} WHERE id = {player.id};"
            cur.execute(SQL)
            conn.commit()
            bjRole = ctx.guild.get_role(794512596740079616)
            if bjwin(player) == True:
                if bjRole not in player.roles:
                    await player.add_roles(bjRole)
                for member in bjRole.members:
                    if member != ctx.author:
                        await member.remove_roles(bjRole)
            return

        elif total(dealerHand) > total(playerHand): #checks for greater hand
            await ctx.send("The dealer had a greater hand. Good luck next time.")
            dealer = False
            return
        
        elif total(dealerHand) > 16:
            dealer = False
            if total(dealerHand) == total(playerHand):
                await ctx.send("Push. Your bet has been returned.")
                SQL = f"UPDATE points SET pointnumber = {points} WHERE id = {player.id};"
                cur.execute(SQL)
                conn.commit()
                return
            await ctx.send("Congratulations. You had a greater hand.")
            SQL = f"UPDATE points SET pointnumber = {points+bet} WHERE id = {player.id}" #adds double the bet to the user's account
            while True:
                try:
                    cur.execute(SQL)
                    break
                except psycopg2.InterfaceError:
                    reestablish()
            conn.commit()

            SQL = f"UPDATE points SET bjwins = bjwins + 1 WHERE id = {player.id};"
            cur.execute(SQL)
            conn.commit()

            SQL = f"UPDATE points SET totalpoints = totalpoints + {bet} WHERE id = {player.id};"
            cur.execute(SQL)
            conn.commit()
            bjRole = ctx.guild.get_role(794512596740079616)
            if bjwin(player) == True:
                if bjRole not in player.roles:
                    await player.add_roles(bjRole)
                for member in bjRole.members:
                    if member != ctx.author:
                        await member.remove_roles(bjRole)
            return
        else:
            dealerHand = hit(dealerHand, deck) #dealer hits


#lets the user place bets on a game of roulette
@bot.command(name = "roulette", brief = "Lets the user place bets on a game of roulette", description = "Type the command, what you're betting on (red, black, even, odd, low, high) and then the amount of points to bet.")
async def roulette(ctx, guess: str, bet: int):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    player = ctx.author
    SQL = f"SELECT pointnumber FROM points WHERE id = {player.id};"
    while True:
        try:
            cur.execute(SQL)
            break
        except psycopg2.InterfaceError:
            reestablish()
    points = cur.fetchone()[0]

    if bet > points or bet < 0: #checks if the user has enough points to place the bet
        await ctx.send("You do not have enough points to bet that much.")
        return
    
    SQL = f"UPDATE points SET pointnumber = {points-bet} WHERE id = {player.id};" #subtracts the points from their "account"
    while True:
        try:
            cur.execute(SQL)
            break
        except psycopg2.InterfaceError:
            reestablish()
    conn.commit()

    winConds = []
    red = [
        32, 19, 21, 25, 34, 27, 36, 30,
        23, 5, 16, 1, 14, 9, 18, 7, 12, 3
    ]
    black = [
        15, 4, 2, 17, 6, 13, 11, 8, 10, 
        24, 33, 20, 31, 22, 29, 28, 35, 26
    ]

    roll = random.randint(0,36)
    if roll in red:
        winConds.append('red')
        await ctx.send(f'Roll: {roll}🟥')
    if roll in black:
        winConds.append('black')
        await ctx.send(f'Roll: {roll}⬛')
    
    if roll in red:
        winConds.append('red')
    if roll in black:
        winConds.append('black')
    if roll % 2 == 0:
        winConds.append('even')
    if roll % 2 != 0:
        winConds.append('odd')
    if roll <= 18:
        winConds.append('low')
    if roll >= 19:
        winConds.append('high')
    
    if guess.lower() in winConds:
        await ctx.send('You win! Congratulations.')
        SQL = f"UPDATE points SET pointnumber = {points+bet} WHERE id = {player.id}" #adds the bet*2 to the users "account"
        while True:
            try:
                cur.execute(SQL)
                break
            except psycopg2.InterfaceError:
                reestablish()
        conn.commit()
        return
    else:
        await ctx.send('You lose! Better luck next time.')
        return

@commands.cooldown(1,15, commands.BucketType.user)
@bot.command(name = "slots", brief = "Lets the user spin a slot machine", description = "To play, all you need are 10 points. Then simply type the command and cross your fingers. Payouts are as follows:\n- 🍒🍒🍒: 20 points\n- 🍊🍊🍊: 35 points\n- 🍋🍋🍋: 50 points\n- 🍑🍑🍑: 75 points\n- 🔔🔔🔔: 150 points\n- 7️7️7️: JACKPOT 250 points")
async def slots(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    player = ctx.author
    SQL = f"SELECT pointnumber FROM points WHERE id = {player.id};"
    while True:
        try:
            cur.execute(SQL)
            break
        except psycopg2.InterfaceError:
            reestablish()
    points = cur.fetchone()[0]

    if 10 > points: #checks if the user has enough points to play
        await ctx.send("You do not have enough points to play.")
        return
    
    SQL = f"UPDATE points SET pointnumber = {points-10} WHERE id = {player.id};" #subtracts the points from their "account"
    while True:
        try:
            cur.execute(SQL)
            break
        except psycopg2.InterfaceError:
            reestablish()
    conn.commit()

    items = [
        '🍒','🍒', '🍒', '🍒', '🍒', '🍒', '🍒', '🍒', '🍒',
         '🍊', '🍊', '🍊', '🍊', '🍊', '🍊', '🍊',
          '🍋', '🍋', '🍋', '🍋', '🍋',
           '🍑', '🍑', '🍑',
            '🔔', '🔔',
             '7️'
    ]

    wheelOne = random.choice(items)
    wheelTwo = random.choice(items)
    wheelThree = random.choice(items)
    await ctx.send(f"`[🟥|🟥|🟥]`\n`-----------`\n`[{wheelOne}|{wheelTwo}|{wheelThree}]`\n`-----------`\n`[🟥|🟥|🟥]`")
    if wheelOne == wheelTwo == wheelThree:
        if wheelOne == '🍒':
            await ctx.send("Congratulations! You won 20 points.")
            SQL = f"UPDATE points SET pointnumber = {points+20} WHERE id = {player.id};"
            while True:
                try:
                    cur.execute(SQL)
                    break
                except psycopg2.InterfaceError:
                    reestablish()
            conn.commit()
            return
        elif wheelOne == '🍊':
            await ctx.send("Congratulations! You won 35 points.")
            SQL = f"UPDATE points SET pointnumber = {points+35} WHERE id = {player.id};"
            while True:
                try:
                    cur.execute(SQL)
                    break
                except psycopg2.InterfaceError:
                    reestablish()
            conn.commit()
            return
        elif wheelOne == '🍋':
            await ctx.send("Congratulations! You won 50 points.")
            SQL = f"UPDATE points SET pointnumber = {points+50} WHERE id = {player.id};"
            while True:
                try:
                    cur.execute(SQL)
                    break
                except psycopg2.InterfaceError:
                    reestablish()
            conn.commit()
            return
        elif wheelOne == '🍑':
            await ctx.send("Congratulations! You won 75 points.")
            SQL = f"UPDATE points SET pointnumber = {points+75} WHERE id = {player.id};"
            while True:
                try:
                    cur.execute(SQL)
                    break
                except psycopg2.InterfaceError:
                    reestablish()
            conn.commit()
            return
        elif wheelOne == '🔔':
            await ctx.send("Congratulations! You won 150 points.")
            SQL = f"UPDATE points SET pointnumber = {points+150} WHERE id = {player.id};"
            while True:
                try:
                    cur.execute(SQL)
                    break
                except psycopg2.InterfaceError:
                    reestablish()
            conn.commit()
            return
        elif wheelOne == '7️':
            await ctx.send("Congratulations! You won the jackpot of 250 points.")
            SQL = f"UPDATE points SET pointnumber = {points+250} WHERE id = {player.id};"
            while True:
                try:
                    cur.execute(SQL)
                    break
                except psycopg2.InterfaceError:
                    reestablish()
            conn.commit()
            return
    else:
        await ctx.send("You didn't win. Good luck next time.")
        return


@bot.group(name='store', brief = 'Displays the store page', invoke_without_command = True)
async def store(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    SQL = f"SELECT pointnumber FROM points WHERE id = {ctx.author.id};"
    while True:
        try:
            cur.execute(SQL)
            break
        except psycopg2.InterfaceError:
            reestablish()
    points = cur.fetchone()[0]
    storeEmbed = discord.Embed(title = "The Lounge Store", description = "Purchase things with your hard earned points\nNO REFUNDS")
    storeEmbed.add_field(name = "Your Points", value = f"{points}", inline = False)
    storeEmbed.add_field(name = "One - Remove a strike", value = "Removes a strike from your counting record\nCost: 250 points", inline = False)
    await ctx.send(embed=storeEmbed)


@store.command(name = "one", description = "Removes a strike from your counting record")
async def one(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    itemEmbed = discord.Embed(title = "Remove a Strike", description = "Removes a strike from your counting record")
    itemEmbed.add_field(name = "Cost", value = "250 points")
    itemEmbed.add_field(name = "Would you like to purchase this item?", value = "[Y]es or [N]o")
    await ctx.send(embed=itemEmbed)
    decision = await bot.wait_for('message', check = lambda n: n.author == ctx.author)
    if decision.content.lower() != 'y' and decision.content.lower() != 'yes':
        await ctx.send("Come again soon!")
        return
    
    SQL = f"SELECT * FROM striketable WHERE name = '{ctx.author.id}';"
    while True:
        try:
            cur.execute(SQL)
            break
        except psycopg2.InterfaceError:
            reestablish()
    strikeEntry = cur.fetchone()
    if strikeEntry is None:
        await ctx.send("You don't have strikes.")
        return

    
    SQL = "SELECT * FROM storetable WHERE number = 1;"
    while True:
        try:
            cur.execute(SQL)
            break
        except psycopg2.InterfaceError:
            reestablish()
    entry = cur.fetchone()
    item = entry[1]
    cost = entry[2]
    SQL = f"SELECT pointnumber FROM points WHERE id = {ctx.author.id};"
    while True:
        try:
            cur.execute(SQL)
            break
        except psycopg2.InterfaceError:
            reestablish()
    points = cur.fetchone()[0]
    if points < cost:
        await ctx.send("You do not have enought points to purchase that item")
        return
    
    if strikeEntry[1] == 1:
        SQL = f"DELETE FROM striketable WHERE name = '{ctx.author.id}';"
        while True:
            try:
                cur.execute(SQL)
                break
            except psycopg2.InterfaceError:
                reestablish()
    elif strikeEntry[1] == 3:
        SQL = f"UPDATE striketable SET strikes = 2 WHERE name = '{ctx.author.id}';"
        while True:
            try:
                cur.execute(SQL)
                break
            except psycopg2.InterfaceError:
                reestablish()
        role = discord.utils.get(ctx.guild.roles,name='Counting Clown')
        await ctx.author.remove_roles(role)
    else:
        SQL = f"UPDATE striketable SET strikes = 1 WHERE name = '{ctx.author.id}';"
        while True:
            try:
                cur.execute(SQL)
                break
            except psycopg2.InterfaceError:
                reestablish()
    
    SQL = f"UPDATE points SET pointnumber = {points-cost} WHERE id = {ctx.author.id};"
    while True:
        try:
            cur.execute(SQL)
            break
        except psycopg2.InterfaceError:
            reestablish()
    await ctx.send(f"Thank you for your purchase! You now have {points-cost} points.")

@bot.command(name = "leaderboard", brief = "Displays a leaderboard of points")
async def leaderboard(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    pointList = []
    winList = []
    memberList = []
    SQL = f"SELECT id, pointnumber, bjwins FROM points ORDER BY pointnumber DESC;"
    while True:
        try:
            cur.execute(SQL)
            break
        except psycopg2.InterfaceError:
            reestablish()
    conn.commit()
    fullList = cur.fetchall()
    for pair in fullList:
        print(pair[0])
        user = await ctx.message.guild.fetch_member(pair[0])
        point = pair[1]
        wins = pair[2]
        memberList.append(user)
        pointList.append(point)
        winList.append(wins)
    
    leaderboardEmbed = discord.Embed(title = "Points Leaderboard", description = "Leaderboard of points", color = discord.Color.blurple())
    leaderboardEmbed.add_field(name = "Top 5", value = f"1. {memberList[0].name} - {pointList[0]} points ({winList[0]} wins)\n2. {memberList[1].name} - {pointList[1]} points ({winList[1]} wins)\n3. {memberList[2].name} - {pointList[2]} points ({winList[2]} wins)\n4. {memberList[3].name} - {pointList[3]} points ({winList[3]} wins)\n5. {memberList[4].name} - {pointList[4]} points ({winList[4]} wins)", inline=False)
    userIndex = memberList.index(ctx.author)
    leaderboardEmbed.add_field(name = "Your place", value = f"{userIndex+1}. {memberList[userIndex].name} - {pointList[userIndex]} points ({winList[userIndex]} wins)")
    await ctx.send(embed=leaderboardEmbed)


@bot.command(name = "pay", brief = "Gives another user some of your points")
async def pay(ctx, recipient: discord.User, amount:int):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    
    if amount <= 0:
        await ctx.send("No. Fuck u")
        return

    if recipient == ctx.author:
        await ctx.send("You can't pay yourself.")
        return

    SQL = f"SELECT pointnumber FROM points WHERE id = {ctx.author.id};"
    while True:
        try:
            cur.execute(SQL)
            break
        except psycopg2.InterfaceError:
            reestablish()
    conn.commit()
    authorPoints = cur.fetchone()[0]

    if amount > authorPoints:
        await ctx.send("You don't have enough points for that.")
        return

    SQL = f"SELECT pointnumber FROM points WHERE id = {recipient.id};"
    while True:
        try:
            cur.execute(SQL)
            break
        except psycopg2.InterfaceError:
            reestablish()
    conn.commit()
    recipientPoints = cur.fetchone()[0]

    SQL = f"UPDATE points SET pointnumber = {authorPoints-amount} WHERE id = {ctx.author.id};"
    while True:
        try:
            cur.execute(SQL)
            break
        except psycopg2.InterfaceError:
            reestablish()
    conn.commit()

    SQL = f"UPDATE points SET pointnumber = {recipientPoints+amount} WHERE id = {recipient.id};"
    while True:
        try:
            cur.execute(SQL)
            break
        except psycopg2.InterfaceError:
            reestablish()
    conn.commit()

    await ctx.send(f"Transfer successful! {ctx.author.name} -{amount} --> {recipient.name} +{amount}")


@commands.cooldown(1, 10, commands.BucketType.user)
@bot.command(name = "totalpointslb", brief = "Displays a leaderboard of the total points gained by a user")
async def totalpointslb(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    pointList = []
    memberList = []
    SQL = f"SELECT id, totalpoints FROM points ORDER BY totalpoints DESC;"
    while True:
        try:
            cur.execute(SQL)
            break
        except psycopg2.InterfaceError:
            reestablish()
    conn.commit()
    fullList = cur.fetchall()
    for pair in fullList:
        user = await ctx.message.guild.fetch_member(pair[0])
        point = pair[1]
        memberList.append(user)
        pointList.append(point)
    
    leaderboardEmbed = discord.Embed(title = "Total Points Leaderboard", description = "Leaderboard of total points (as of 1/1/2021)", color = discord.Color.blurple())
    leaderboardEmbed.add_field(name = "Top 5", value = f"1. {memberList[0].name} - {pointList[0]} total points\n2. {memberList[1].name} - {pointList[1]} total points\n3. {memberList[2].name} - {pointList[2]} total points\n4. {memberList[3].name} - {pointList[3]} total points\n5. {memberList[4].name} - {pointList[4]} total points", inline=False)
    userIndex = memberList.index(ctx.author)
    leaderboardEmbed.add_field(name = "Your place", value = f"{userIndex+1}. {memberList[userIndex].name} - {pointList[userIndex]} total points")
    await ctx.send(embed=leaderboardEmbed)


#--------------------------------------------------------------------------------------------------------------------------------------#
#  __  __   ____   _____   ______  _____          _______  _____  ____   _   _ 
# |  \/  | / __ \ |  __ \ |  ____||  __ \     /\ |__   __||_   _|/ __ \ | \ | |
# | \  / || |  | || |  | || |__   | |__) |   /  \   | |     | | | |  | ||  \| |
# | |\/| || |  | || |  | ||  __|  |  _  /   / /\ \  | |     | | | |  | || . ` |
# | |  | || |__| || |__| || |____ | | \ \  / ____ \ | |    _| |_| |__| || |\  |
# |_|  |_| \____/ |_____/ |______||_|  \_\/_/    \_\|_|   |_____|\____/ |_| \_|                                                                                                                                                            


#deletes the bot messages in the last n number of messages
@bot.command(name = 'purge', description = 'Deletes the bot messages within the last number of message specified by the user (limit 50)')
async def purge(ctx,amount: int):
    if amount > 50: #checks to see if the request is stupid (i.e. made by parker)
        await ctx.send("Fuck off dickbag.")
    message = await ctx.history(limit=amount).flatten() #flattens a list of the recent messages
    counter = 0
    for m in message:
        if m.author == bot.user:
            await m.delete() #while iterating throught the list, if the message was sent by the bot it deletes it
            counter += 1 #keeps track of how many messages the bot deleted
    await ctx.send(f'Deleted {counter} bot messages') #prints out a message letting the user know how many message were deleted

#lets the user check how many strikes they have
@commands.cooldown(1, 10, commands.BucketType.user)
@bot.command(name = 'strikes', description = 'Reacts with the number of strikes the user has in the counting channel')
async def strikes(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    if ctx.message.author.id == 203282979265576960: #checks to see if the userID matches Kyle's
        await ctx.message.add_reaction('💯')
        return
    while True:
        try:
            cur.execute("SELECT * FROM striketable") #selects all values in the striketable
            break
        except psycopg2.InterfaceError:
            reestablish()
    fetch = cur.fetchall() #fetches all values in the striketable
    for i in fetch: #for each value in the fetch tuple, check if the 
        if int(i[0]) == ctx.message.author.id: #checks if the message authors userID is in the list of people with strikes
            #if it is, it checks how many strikes the user has and adds a reaction to denote that
            if i[1] == 1: 
                await ctx.message.add_reaction('1️⃣')
                return
            if i[1] == 2:
                await ctx.message.add_reaction('2️⃣')
                return
            if i[1] == 3:
                await ctx.message.add_reaction('3️⃣')
                return

    await ctx.message.add_reaction('0️⃣')

@commands.cooldown(1,15, commands.BucketType.user)
@bot.command(name = "claim", brief = "Claims daily points")
async def claim(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    SQL = f"SELECT claimtime FROM points WHERE id = {ctx.author.id};" #grab the last claimtime row from the DB
    while True:
        try:
            cur.execute(SQL)
            break
        except psycopg2.InterfaceError:
            reestablish()
    conn.commit()
    lastTime = cur.fetchone()[0] #gets the actual time from the returned tuple

    UTCtime = datetime.datetime.now(datetime.timezone.utc) #grabs the time now

    timeDifference = UTCtime - lastTime #gets the time differnce between the last claim time and the current time
    secondDifference = timeDifference.total_seconds() #obtains a difference in seconds from the difference
    hourDifference = secondDifference/3600 #converts the second difference to an hour difference

    secondDifference = 86400 - secondDifference

    hours = secondDifference // 3600 #gets number of hours until next claim time

    secondDifference %= 3600
    minutes = secondDifference // 60 #gets number of minutes until next claim time minus hours

    secondDifference %= 60
    seconds = secondDifference #gets number of seconds until next claim time minus hours and minutes

    if hourDifference > 24: #if the time difference is more than a day
        SQL = f"SELECT pointnumber FROM points WHERE id = {ctx.author.id};"
        cur.execute(SQL)
        conn.commit()
        points = cur.fetchone()[0] #selects the current point value of the user

        SQL = f"UPDATE points SET pointnumber = {points+25} WHERE id = {ctx.author.id};" #adds 25 points to the user's account
        cur.execute(SQL)
        conn.commit()

        SQL = f"UPDATE points SET claimtime = '{UTCtime}' WHERE id = {ctx.author.id};" #updates the claimtime to the current time
        cur.execute(SQL)
        conn.commit()
        await ctx.send("25 points have been added to your account. You can claim again in 24 hours.")
        
    else:
        await ctx.send(f"You can claim your points in {int(hours)}h {int(minutes)}m {int(seconds)}s.") #tells the user how long they have until they can claim their points
        return


#--------------------------------------------------------------------------------------------------------------------------------------#
#  ______  _____   _____    ____   _____  
# |  ____||  __ \ |  __ \  / __ \ |  __ \ 
# | |__   | |__) || |__) || |  | || |__) |
# |  __|  |  _  / |  _  / | |  | ||  _  / 
# | |____ | | \ \ | | \ \ | |__| || | \ \ 
# |______||_|  \_\|_|  \_\ \____/ |_|  \_\                                                                                  



@finn.error
async def finn_error(ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
        await ctx.message.delete()
        errMess = await ctx.send(f'You are on cooldown for this command. Try again in {error.retry_after:.2f}s')
        await asyncio.sleep(error.retry_after)
        await errMess.delete()


@strikes.error
async def strike_error(ctx,error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.message.delete()
        errMess = await ctx.send(f'You are on cooldown for this command. Try again in {error.retry_after:.2f}s')
        await asyncio.sleep(error.retry_after)
        await errMess.delete()

@tictactoe.error
async def tictactoe_error(ctx,error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.message.delete()
        errMess = await ctx.send(f'You are on cooldown for this command. Try again in {error.retry_after:.2f}s')
        await asyncio.sleep(error.retry_after)
        await errMess.delete()

@blackjack.error
async def blackjack_error(ctx,error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.message.delete()
        errMess = await ctx.send(f'You are on cooldown for this command. Try again in {error.retry_after:.2f}s')
        await asyncio.sleep(error.retry_after)
        await errMess.delete()

@roulette.error
async def roulette_error(ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
        await ctx.message.delet()
        errMess = await ctx.send(f'You are on cooldown for this command. Try again in {error.retry_after:.2f}s')
        await asyncio.sleep(error.retry_after)
        await errMess.delete()

@slots.error
async def slots_error(ctx,error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.message.delete()
        errMess = await ctx.send(f'You are on cooldown for this command. Try again in {error.retry_after:.2f}s')
        await asyncio.sleep(5)
        await errMess.delete()

@claim.error
async def claim_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.message.delete()
        errMess = await ctx.send(f'You are on cooldown for this command. Try again in {error.retry_after:.2f}s')
        await asyncio.sleep(error.retry_after)
        await errMess.delete()

@points.error
async def points_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.message.delete()
        errMess = await ctx.send(f"You are on cooldown for this command. Try again in {error.retry_after:.2f}s")
        await asyncio.sleep(error.retry_after)
        await errMess.delete()

@asa.error
async def asa_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.message.delete()
        errMess = await ctx.send(f"You are on cooldown for this command. Try again in {error.retry_after:.2f}s")
        await asyncio.sleep(error.retry_after)
        await errMess.delete()

@connectfour.error
async def connectfour_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.message.delete()
        errMess = await ctx.send(f"You are on cooldown for this command. Try again in {error.retry_after:.2f}s")
        await asyncio.sleep(error.retry_after)
        await errMess.delete()


#--------------------------------------------------------------------------------------------------------------------------------------#
#   ____   _   _            __  __  ______   _____  _____           _____  ______ 
#  / __ \ | \ | |          |  \/  ||  ____| / ____|/ ____|   /\    / ____||  ____|
# | |  | ||  \| |          | \  / || |__   | (___ | (___    /  \  | |  __ | |__   
# | |  | || . ` |          | |\/| ||  __|   \___ \ \___ \  / /\ \ | | |_ ||  __|  
# | |__| || |\  |          | |  | || |____  ____) |____) |/ ____ \| |__| || |____ 
#  \____/ |_| \_|          |_|  |_||______||_____/|_____//_/    \_\\_____||______|
#                  ______                                                         
#                 |______|                                                        


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    
    if message.author == bot.user and str(message.channel) != "admins-only": #checks to see if the message author is the bot and returns
        return
    
    print('Message recieved: ', message.content, 'by', message.author, 'in '+ str(message.channel))
    # april fools
    # await message.add_reaction("<:amongsus:826690527138938911>")

    #if the message is from a channel other than counting, it checks to see if it can make a dad joke
    if str(message.channel) != 'counting':
        if message.content.lower().startswith('im ') or str(message.content).lower().startswith("i'm"):
            dad = await message.channel.send('Hi ' + message.content.split(' ',1)[1] + ", I'm dad!")
            await dad.add_reaction('👌')
        if message.content.lower().startswith('i am'):
            dad = await message.channel.send('Hi ' + message.content.lower().split('i am ',1)[1] + ", I'm dad!")
            await dad.add_reaction('👌')  
        return
    else:
        while True:
            try:
                cur.execute("SELECT MAX(count) FROM countingtable;") #gets the max value from the countingtable
                break
            except psycopg2.InterfaceError:
                reestablish()
        correctNumberDB = list(cur.fetchone()) #fetches the value tuple and stores it in a variable
        correctNumberSQL = int(correctNumberDB[0])+1 #get the actual int value and increases it by one to reflect the correct value
        print('Correct Number in DB: ',str(correctNumberSQL))
        if str(message.content).isnumeric() == False or int(message.content) != correctNumberSQL: #checks to see if the message is not a number or is not the correct number
            while True:    
                try:
                    cur.execute("SELECT * FROM striketable") #selects all the values in the strikelist
                    break
                except psycopg2.InterfaceError:
                    reestablish()
            strikeList = cur.fetchall()
            userID = message.author.id
            for i in strikeList:
                if i[0] == str(userID): #checks to see if the user is already in the strikelist
                    if i[1] == 1: #checks if they have one strike
                        await message.delete()
                        #sends a message alerting everyone to the user's infraction
                        await message.channel.send(message.author.mention + ' entered ' + str(message.content) + ' and screwed up the count. This is their 2nd infraction.')
                        SQL = "UPDATE striketable SET strikes = 2 WHERE name = '%s';" #updates their strikes to reflect the new number
                        while True:
                            try:
                                cur.execute(SQL, (userID,))
                                break
                            except psycopg2.InterfaceError:
                                reestablish()
                        conn.commit()
                        return
                    else: #if they don't have one strike and theyre already in the table, then they have two strikes
                        SQLtwo = "UPDATE striketable SET strikes = 3 WHERE name = '%s';" #updates their strikes to reflect the new number
                        while True:
                            try:
                                cur.execute(SQLtwo, (userID,))
                                break
                            except psycopg2.InterfaceError:
                                reestablish()
                        conn.commit()
                        role = discord.utils.get(message.guild.roles,name='Counting Clown') #assigns the counting clown role to a variable
                        await message.author.add_roles(role) #give the author the counting clown role
                        await message.delete() #deletes the user's message
                        #sends a message alerting everyone to the user's infraction
                        await message.channel.send(message.author.mention + ' entered ' + str(message.content) + ' and screwed up the count. This was their 3rd and final infraction.')
                        return

            #if we haven't returned by now, it means they are not in the table
            SQL = "INSERT INTO striketable (name, strikes) VALUES (%s, 1)" #inserts their userid into the table
            while True:
                try:
                    cur.execute(SQL, (userID,))
                    break
                except psycopg2.InterfaceError:
                    reestablish()
            conn.commit()
            await message.delete() #deletes their message
            #sends a message alerting everyone to the user's infraction
            await message.channel.send(message.author.mention + ' entered ' + str(message.content) + ' and screwed up the count. This is their 1st infraction.')
            while True:
                try:
                    cur.execute("SELECT COUNT(name) FROM striketable;") #updates the status of the bot to match the new number of criminals
                    break
                except psycopg2.InterfaceError:
                    reestablish()

            numCriminalsTable = cur.fetchall()
            numCriminals = numCriminalsTable[0][0]
            print(numCriminals)
            presence = str(numCriminals) + " criminals"
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=presence))
        else:
            #if the message was in the counting channel but was the right number, 
            #then we just call the function that adds their number to the DB
            countEntry(int(message.content), message.author)
            if int(message.content) == 1000:
                await message.add_reaction("🎉")
                await message.add_reaction("🎊")
                guild = message.guild
                await guild.create_role(name="1000", color=discord.Color.from_rgb(21,244,238))
                oneThousandRole = discord.utils.get(message.guild.roles,name='1000')
                await message.author.add_roles(oneThousandRole)


@bot.event
async def on_voice_state_update(member, before, after):
    #checks for octave bot joining the vc
    if member == bot.get_user(201503408652419073):
        return
    asa = bot.get_user(227250029788790785)

    #if the member is asa
    if member == asa:
        if after.channel and not before.channel:
            await play_music(after.channel, "https://www.youtube.com/watch?v=PS_cV18z67Y")
        #if asa starts a deafen
        if after.self_deaf:
            deafen_start = datetime.datetime.now().timestamp()
            SQL = f"UPDATE asa SET deafenstart = {deafen_start};"
            cur.execute(SQL)
            conn.commit()
        
        #if asa ends a deafen
        if before.self_deaf and not after.self_deaf:
            SQL = f"SELECT deafenstart FROM asa;"
            cur.execute(SQL)
            deafen_start = int(cur.fetchone()[0])
            deafen_end = datetime.datetime.now().timestamp()
            deafen_time = (deafen_end - deafen_start)
            SQL = f"UPDATE asa SET idleTime = idleTime + {int(deafen_time)};"
            cur.execute(SQL)
            conn.commit()

        #if asa leaves all channels
        if after.channel == None:
            if before.self_deaf:
                SQL = f"SELECT deafenstart FROM asa;"
                cur.execute(SQL)
                deafen_start = int(cur.fetchone()[0])
                deafen_end = datetime.datetime.now().timestamp()
                deafen_time = (deafen_end - deafen_start)
                SQL = f"UPDATE asa SET idleTime = idleTime + {int(deafen_time)};"
                cur.execute(SQL)
                conn.commit()

    if before.channel != after.channel and after.channel is not None:
        vc = after.channel
        #print(vc.name)
        streamersInVC = []
        for person in vc.members:
            if person.id in streamerList:
                streamersInVC.append(streamerList[person.id])
        
        msgs = []
        for streamer in streamersInVC:
            streaming, name = Check(streamer)
            if streaming == 1 and streamer != member.id:
                botChannel = bot.get_channel(514562197217738769)
                streamer = bot.get_user(list(streamerList.keys())[list(streamerList.values()).index(streamer)])
                msg = await botChannel.send(f"{member.mention}, {streamer.name} is streaming {name}.")
                msgs.append(msg)
        await asyncio.sleep(30)
        for mess in msgs:
            await mess.delete()
    else:
        return

@bot.event
async def on_member_join(member):
    #insert into musicbot
    SQL = f"INSERT INTO musicbot(ignore, id) VALUES (False, '{member.id}';"
    cur.execute(SQL)
    conn.commit()

    #insert into points table
    SQL = f"INSERT INTO points(pointnumber, id, claimtime, bjwins, totalpoints) VALUES (0, {member.id}, {datetime.datetime.now(datetime.timezone.utc)}, 0, 0);"
    cur.execute(SQL)
    conn.commit()


@bot.event
async def on_member_leave(member):
    #check for striketable
    SQL = "SELECT * FROM striketable;"
    cur.execute(SQL)
    entries = cur.fetchall()
    for entry in [i[0] for i in entries]:
        if member.id == entry:
            #delete from striketable
            SQL = f"DELETE FROM striketable WHERE name='{member.id}';"
            cur.execute(SQL)
            conn.commit()
    
    #delete from music bot
    SQL = f"DELETE FROM musicbot WHERE id='{member.id}';"
    cur.execute(SQL)
    conn.commit()

    SQL = f"DELETE FROM points WHERE id={member.id};"
    cur.execute(SQL)
    conn.commit()


#--------------------------------------------------------------------------------------------------------------------------------------#
#runs the bot using the discord bot token provided within Heroku
bot.run(os.environ['token'])
