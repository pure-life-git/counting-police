#--------------------------------------------------------------------------------------------------------------------------------------#
#  _____  __  __  _____    ____   _____  _______  _____ 
# |_   _||  \/  ||  __ \  / __ \ |  __ \|__   __|/ ____|
#   | |  | \  / || |__) || |  | || |__) |  | |  | (___  
#   | |  | |\/| ||  ___/ | |  | ||  _  /   | |   \___ \ 
#  _| |_ | |  | || |     | |__| || | \ \   | |   ____) |
# |_____||_|  |_||_|      \____/ |_|  \_\  |_|  |_____/ 


from logging import exception
import discord
import os
import re
import random
from discord.ext import commands
import asyncio
from discord.ext.commands.errors import CommandOnCooldown
import psycopg2
import wolframalpha
import datetime


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

#initializes connections to postgresql database
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()
conn.autocommit = True

#sets up wolfram api
wolframID = 'PAX2TQ-2V94QU68XE'
wolframClient = wolframalpha.Client(wolframID)


#--------------------------------------------------------------------------------------------------------------------------------------#
#   _____  _       ____   ____            _      
#  / ____|| |     / __ \ |  _ \    /\    | |     
# | |  __ | |    | |  | || |_) |  /  \   | |     
# | | |_ || |    | |  | ||  _ <  / /\ \  | |     
# | |__| || |____| |__| || |_) |/ ____ \ | |____ 
#  \_____||______|\____/ |____//_/    \_\|______|


channelList = [
    "bot", "admins-only"
]

#list of mod ids
modID = [
    203282979265576960,
    288710564367171595
]

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

#attacker list for .operator
attackerList = [
    "Zero", "Ace", "Iana", "Kali", "Amaru", "Nøkk", "Gridlock", "Nomad",
    "Maverick", "Lion", "Finka", "Dokkaebi", "Zofia", "Ying", "Jackal",
    "Hibana", "Capitão", "Blackbeard", "Buck", "Sledge", "Thatcher", "Ash",
    "Thermite", "Montagne", "Twitch", "Blitz", "IQ", "Fuze", "Glaz"
]

#defender list for .operator
defenderList = [
    "Aruni", "Melusi", "Oryx", "Wamai", "Goyo", "Warden", "Mozzie", "Kaid",
    "Clash", "Maestro", "Alibi", "Vigil", "Ela", "Lesion", "Mira", "Echo",
    "Caveira", "Valkyrie", "Frost", "Mute", "Smoke", "Castle", "Pulse", "Doc",
    "Rook", "Jäger", "Bandit", "Tachanka", "Kapkan"
]


#--------------------------------------------------------------------------------------------------------------------------------------#
#  ______  _    _  _   _   _____  _______  _____  ____   _   _   _____ 
# |  ____|| |  | || \ | | / ____||__   __||_   _|/ __ \ | \ | | / ____|
# | |__   | |  | ||  \| || |        | |     | | | |  | ||  \| || (___  
# |  __|  | |  | || . ` || |        | |     | | | |  | || . ` | \___ \ 
# | |     | |__| || |\  || |____    | |    _| |_| |__| || |\  | ____) |
# |_|      \____/ |_| \_| \_____|   |_|   |_____|\____/ |_| \_||_____/                                                                       
                                                                      

def reestablish():
    cur = conn.cursor()


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


#enters a game from any channel into the postgresql DB
def gameEntry(game):
    SQL = """INSERT INTO gametable (games) VALUES (%s)"""
    data = (game,)
    while True:
        try:
            cur.execute(SQL,data)
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
#   _____            __  __  ______ 
#  / ____|    /\    |  \/  ||  ____|
# | |  __    /  \   | \  / || |__   
# | | |_ |  / /\ \  | |\/| ||  __|  
# | |__| | / ____ \ | |  | || |____ 
#  \_____|/_/    \_\|_|  |_||______|                                                                      


@bot.group(name='game', invoke_without_command=True)
async def game(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    await ctx.send("Valid subcommands: add, remove, clear, list, choose")


#adds a game provided by the user to the gameList
@game.command(name = 'add', description = 'Adds a game to the game list')
async def add(ctx, *, arg):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    gameLower = str(arg).lower()
    while True:
        try:
            cur.execute("SELECT * FROM gametable") #select every entry in the gametable from the DB 
            break
        except psycopg2.InterfaceError:
            reestablish()
    conn.commit()
    rawList = list(cur.fetchall()) #makes a list with every entry
    games = []
    for i in rawList: 
        games.append(i[0]) #takes the list of tuples and appends the first index to a new list
    if gameLower in games: #checks to see if the game is already in the list
        await ctx.send('That game is already in the list')
        return
    gameEntry(gameLower) #calls a function that adds the game to the sql table
    message = ctx.message
    await message.add_reaction('👍')


#removes a particular game from the gamelist
@game.command(name = 'remove', description = 'Removes a game from the game list')
async def remove(ctx,*,arg):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    gameLower = str(arg).lower()
    while True:
        try:
            cur.execute("SELECT * FROM gametable") #selects all the entries from the gamelist
            break
        except psycopg2.InterfaceError:
            reestablish()
    conn.commit()
    SQL = "DELETE FROM gametable WHERE games=%s;" #deletes the row in the game table with the game name
    while True:
        try:
            cur.execute(SQL,(gameLower,))
            break
        except psycopg2.InterfaceError:
            reestablish()
    conn.commit()
    message = ctx.message
    await message.add_reaction('👍')


#clears game list
@game.command(name = 'clear', description = 'Clears the game list')
async def clear(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    while True:
        try:
            cur.execute("DELETE FROM gametable") #deletes all entries from the game list
            break
        except psycopg2.InterfaceError:
            reestablish()
    conn.commit()
    message = ctx.message
    await message.add_reaction('👍')


#randomly chooses a game from the game list
@game.command(name = 'choose', description='Randomly chooses a game from the game list')
async def choose(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    while True:
        try:
            cur.execute("SELECT * FROM gametable") #selects all of the entries from the table
            break
        except psycopg2.InterfaceError:
            reestablish()
    conn.commit()
    rawList = list(cur.fetchall()) # makes a list out of the selection
    numSQL = []
    for i in rawList:
        numSQL.append(i[0]) #takes the list of tuples and appends the first index to a new list
    num = random.choice(numSQL) #chooses a game from the list
    await ctx.send(num + ' has been chosen by machine engineered randomness!') #sends a message with the result


#lists all of the games in the gamelist
@game.command(name = 'list', description = 'Displays the game list')
async def gamelist(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    while True:
        try:
            cur.execute("SELECT * FROM gametable") #selects all entries from the game list
            break
        except psycopg2.InterfaceError:
            reestablish()
    rawList = list(cur.fetchall()) #makes a list out of all the entries
    games = []
    for i in rawList:
            games.append(i[0]) #takes each tuple in the list and appends the first index to a new list
    if len(games) != 0: #checks if the gamelist is empty
        #creates a new embed and adds the contents of the gamelist in an ordered list to an embed field
        gamelistEmbed = discord.Embed(title="Game List", description="List of games entered", color=discord.Color.greyple())
        gamelistEmbed.add_field(name="Games",value='\n'.join('{}: {}'.format(*k) for k in enumerate(games,1)))
        await ctx.send(embed = gamelistEmbed) #sends the embed
    else:
        #if the gamelist is empty, the embed is sent but with contents that let the user know the list is empty
        emptygamelistEmbed = discord.Embed(title="Game List", description="List of games entered", color=discord.Color.red())
        emptygamelistEmbed.add_field(name="No Games!", value="The game list is empty.", inline=False)
        await ctx.send(embed = emptygamelistEmbed)


#--------------------------------------------------------------------------------------------------------------------------------------#
#   _____  _____  _       _   __     __
#  / ____||_   _|| |     | |  \ \   / /
# | (___    | |  | |     | |   \ \_/ / 
#  \___ \   | |  | |     | |    \   /  
#  ____) | _| |_ | |____ | |____ | |   
# |_____/ |_____||______||______||_|                                                                               


#plays a game of rock paper scissorcs with the user
@commands.cooldown(2, 15, commands.BucketType.user)
@bot.command(name = 'rps', description = 'Plays a game of rock paper scissors with you')
async def rps(ctx, userPick):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    #initializes a list with the possible choices the bot can make
    choices = [
        "rock",
        "paper",
        "scissors"
    ]
    #checks if the users input is a valid choice
    if userPick.lower() not in choices:
        ctx.channel.send("Please enter either 'rock', 'paper' or 'scissors'")
        return
    #sets a 1 in 100 chance that the bot chooses gun and automatically wins. else the bot
    #picks a random choice
    gunChance = random.randint(1,100)
    if  gunChance == 69:
        botPick = "gun"
    else:
        botPick = random.choice(choices)

    #if the bot chose gun, then an embed is created and sent with the result
    if botPick == "gun":
        resultEmbed = discord.Embed(title="Rock Paper Scissors with {}".format(str(ctx.message.author)), description=" ", color=discord.Color.red())
        resultEmbed.add_field(name="Your Pick", value="{}".format(userPick), inline=False)
        resultEmbed.add_field(name="Bot's Pick", value="{}".format(botPick), inline=False)
        resultEmbed.add_field(name="You Lose!", value="Better luck next time", inline=False)
        await ctx.channel.send(embed=resultEmbed)
        return

    #checks for a draw
    if userPick.lower() == botPick:
        resultEmbed = discord.Embed(title="Rock Paper Scissors with {}".format(str(ctx.message.author)), description=" ", color=discord.Color.gold())
        resultEmbed.add_field(name="Your Pick", value="{}".format(userPick), inline=False)
        resultEmbed.add_field(name="Bot's Pick", value="{}".format(botPick), inline=False)
        resultEmbed.add_field(name="Draw", value="You both chose the same option", inline=False)
        await ctx.channel.send(embed=resultEmbed)
        return

    #handles interactions if the user chooses rock
    if userPick.lower() == "rock":
        if botPick == "scissors":
            resultEmbed = discord.Embed(title="Rock Paper Scissors with {}".format(str(ctx.message.author)), description=" ", color=discord.Color.green())
            resultEmbed.add_field(name="Your Pick", value="{}".format(userPick), inline=False)
            resultEmbed.add_field(name="Bot's Pick", value="{}".format(botPick), inline=False)
            resultEmbed.add_field(name="You Win!", value="Congratulations!", inline=False)
            await ctx.channel.send(embed=resultEmbed)
            return

        if botPick == "paper":
            resultEmbed = discord.Embed(title="Rock Paper Scissors with {}".format(str(ctx.message.author)), description=" ", color=discord.Color.red())
            resultEmbed.add_field(name="Your Pick", value="{}".format(userPick), inline=False)
            resultEmbed.add_field(name="Bot's Pick", value="{}".format(botPick), inline=False)
            resultEmbed.add_field(name="You Lose!", value="Better luck next time", inline=False)
            await ctx.channel.send(embed=resultEmbed)
            return

    #handles interactions if the user chooses scissors
    if userPick.lower() == "scissors":
        if botPick == "paper":
            resultEmbed = discord.Embed(title="Rock Paper Scissors with {}".format(str(ctx.message.author)), description=" ", color=discord.Color.green())
            resultEmbed.add_field(name="Your Pick", value="{}".format(userPick), inline=False)
            resultEmbed.add_field(name="Bot's Pick", value="{}".format(botPick), inline=False)
            resultEmbed.add_field(name="You Win!", value="Congratulations!", inline=False)
            await ctx.channel.send(embed=resultEmbed)
            return
            

        if botPick == "rock":
            resultEmbed = discord.Embed(title="Rock Paper Scissors with {}".format(str(ctx.message.author)), description=" ", color=discord.Color.red())
            resultEmbed.add_field(name="Your Pick", value="{}".format(userPick), inline=False)
            resultEmbed.add_field(name="Bot's Pick", value="{}".format(botPick), inline=False)
            resultEmbed.add_field(name="You Lose!", value="Better luck next time", inline=False)
            await ctx.channel.send(embed=resultEmbed)
            return

    #handles interactions if the user chooses paper
    if userPick.lower() == "paper":
        if botPick == "rock":
            resultEmbed = discord.Embed(title="Rock Paper Scissors with {}".format(str(ctx.message.author)), description=" ", color=discord.Color.green())
            resultEmbed.add_field(name="Your Pick", value="{}".format(userPick), inline=False)
            resultEmbed.add_field(name="Bot's Pick", value="{}".format(botPick), inline=False)
            resultEmbed.add_field(name="You Win!", value="Congratulations!", inline=False)
            await ctx.channel.send(embed=resultEmbed)
            return
            

        if botPick == "scissors":
            resultEmbed = discord.Embed(title="Rock Paper Scissors with {}".format(str(ctx.message.author)), description=" ", color=discord.Color.red())
            resultEmbed.add_field(name="Your Pick", value="{}".format(userPick), inline=False)
            resultEmbed.add_field(name="Bot's Pick", value="{}".format(botPick), inline=False)
            resultEmbed.add_field(name="You Lose!", value="Better luck next time", inline=False)
            await ctx.channel.send(embed=resultEmbed)
            return


@commands.cooldown(1, 10, commands.BucketType.user)
@bot.command(name = 'py', help_command = None)
async def py(ctx, *args):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    argsJoin = ' '.join(args)
    answer = eval(argsJoin)
    await ctx.send(answer)


#sends user input to the wolframalpha api and prints out the answer
@commands.cooldown(1, 20, commands.BucketType.user)
@bot.command(name = 'wolfram', description='Returns the simple answer to a query from Wolfram|Alpha')
async def wolfram(ctx,*args):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    question = ' '.join(args) #joins the user args into a single string
    response = wolframClient.query(question) #gets a query from the wolfram api using the question
    wolframEmbed = discord.Embed(title="Wolfram|Alpha API", description=" ", color=discord.Color.from_rgb(255,125,0))
    try:
        for pod in response.results: #for each returned pod from the query, adds a new field to the answer embed
            wolframEmbed.add_field(name=pod.title,value=pod.text,inline=False)
        #wolframEmbed.add_field(name="Result", value=response.results.text,inline=False)
        if len(wolframEmbed.fields) == 0:
            await ctx.send("Wolfram|Alpha could not find any simple results for that query.")
            return
        else:
            await ctx.channel.send(embed=wolframEmbed)
    except KeyError:
        await ctx.send("Something went wrong. Please try a different query.")


#sends user input to the wolframalpha api and prints out a full answer
@commands.cooldown(1, 120, commands.BucketType.user)
@bot.command(name = 'wolframfull', description = 'Returns the full answer to a query from Wolfram|Alpha')
async def wolframfull(ctx,*args):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    question = ' '.join(args) #joins all the user passed args into a single string
    res = wolframClient.query(question) #sends the question to be queried from the wolfram api
    wolframEmbed = discord.Embed(title="Wolfram|Alpha API", description=" ", color=discord.Color.from_rgb(255,125,0))
    for pod in res.pods:
        if pod.text:
            #printPod
            wolframEmbed.add_field(name=pod.title,value=pod.text,inline=False)
        for sub in pod.subpods: #checks to see if any of the returned queries subpods contain images
            if sub['img']['@src']: #if there is an image, creates a new embed and adds the image
                wolframImgEmbed = discord.Embed(title=pod.title,description=" ", color=discord.Color.from_rgb(255,125,0))
                wolframImgEmbed.set_image(url=sub['img']['@src'])
                await ctx.send(embed=wolframImgEmbed)
    await ctx.send(embed=wolframEmbed)


#facilitates a tic-tac-toe game between two users
@commands.cooldown(1, 30, commands.BucketType.user)
@bot.command(
    name = "tictactoe", 
    brief = "Challenge another player to a game of tic-tac-toe", 
    description = "Simply type the command and then mention someone to start a game with them. To choose your space, treat the board as a numbered grid 1-9 starting at the top left."
    )
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


#starts a poll with reaction-based voting
@bot.command(name = 'poll', description = 'Starts a poll. Default time is 120s')
async def poll(ctx,*args):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    timer = 120 #sets a default timer as 2 minutes

    argsList = list(args) #gets the list of args passed by the user
    if len(argsList) != 0:
        if argsList[len(argsList)-1].isnumeric() == True: #checks if the last argument in the list is a number
            timer = int(argsList[len(argsList)-1]) #sets the timer as the last argument in the list
            argsList.pop(len(argsList)-1) #removes the number from the args

    #creates a new embed for the poll
    embedVar = discord.Embed(title='Poll', description = ' '.join(argsList), color=discord.Color.blue())
    embedVar.add_field(name="Yes", value='<:white_check_mark:785597865081962528>', inline=False)
    embedVar.add_field(name="No", value='<:x:785598446983839784>', inline=False)
    m = await ctx.send(embed=embedVar)
    #adds reaction to the poll embed
    await m.add_reaction('✅')
    await m.add_reaction('❌')
    #sleeps for 2 minutes or whatever amount the user entered
    await asyncio.sleep(timer)
    m = await ctx.channel.fetch_message(m.id)
    print(m.reactions)
    counts = {react.emoji: react.count for react in m.reactions} #gets the amount of reactions as a dictionary
    print(counts)
    yesResult = counts['✅']-1 #gets the amount of reactions for "yes" minus the bot's vote
    print('yesresult='+str(yesResult))
    noResult = counts['❌']-1 #gets the amount of reactions for "no" minus the bot's vote
    print('noresult='+str(noResult))
    if noResult == 0 and yesResult == 0: #checks to see if no one voted
        resultsEmbed = discord.Embed(title="No Votes", description=' '.join(argsList), color=discord.Color.gold())
        resultsEmbed.add_field(name='No Votes Were Counted', value='No results to be shown', inline=False)
        await m.delete()
        await ctx.send(embed=resultsEmbed)
        return
    yesPercent = yesResult/(yesResult+noResult) #calculates a percent of yes votes
    noPercent = noResult/(yesResult+noResult) #calculates a percent of no votes
    resultsEmbed = discord.Embed(title='Results', description = ' '.join(argsList), color=discord.Color.gold())
    resultsEmbed.add_field(name='✅', value="{yes} votes - {yespercent:.0%}".format(yes=yesResult,yespercent=yesPercent), inline=False)
    resultsEmbed.add_field(name='❌', value='{no} votes - {nopercent:.0%}'.format(no=noResult,nopercent=noPercent), inline=False)
    await m.delete() #deletes the original embed
    await ctx.send(embed=resultsEmbed) #sends the results embed


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
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    if amount > 50: #checks to see if the request is stupid (i.e. made by parker)
        await ctx.send("Fuck off dickbag.")
    message = await ctx.history(limit=amount).flatten() #flattens a list of the recent messages
    counter = 0
    for m in message:
        if m.author == bot.user:
            await m.delete() #while iterating throught the list, if the message was sent by the bot it deletes it
            counter += 1 #keeps track of how many messages the bot deleted
    await ctx.send(f'Deleted {counter} bot messages') #prints out a message letting the user know how many message were deleted


#mutes a member of the server for a specified amount of time
@bot.command(name = 'mute',help_command = None)
async def mute(ctx, mention, time='5s'):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    if time[0] == '-' or time[0].isnumeric() == False:
        await ctx.send("Please enter a positive number") #sanitizes input
        return
    if int(ctx.message.author.id) not in modID:
        await ctx.send("You do not have permission to use this command.") #only mods can use this command
        return
    
    multiplier = 0
    
    if time[len(time)-1].lower() == 's': #
        multiplier = 1                   #   
    if time[len(time)-1].lower() == 'm': #   this set of ifs checks to see
        multiplier = 60                  #   what unit of time the user 
    if time[len(time)-1].lower() == 'h': #   would like to use: seconds,
        multiplier = 3600                #   minutes, hours, or days
    if time[len(time)-1].lower() == 'd': #
        multiplier = 86400               #
    
    member = ctx.message.mentions[0]
    await member.edit(mute=True)
    await ctx.send(f"{member} has been muted for {time}") #sends a confirmation message to the user
    time = int(time[:-1])
    time *= multiplier
    await asyncio.sleep(time) #sleeps for the duration of time
    await member.edit(mute=False) #unmutes after the duration of time


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


@bot.command(name = "lock")
async def lock(ctx, channel: discord.TextChannel):
    if ctx.author.id not in modID:
        await ctx.send("You do not have the permissions to use this command.")
        return
    channel = channel or ctx.channel
    role = discord.utils.get(ctx.message.guild.roles,name='Patrons') #assigns the counting clown role to a variable
    overwrite = channel.overwrites_for(role)
    overwrite.send_messages = False
    await channel.set_permissions(role, overwrite=overwrite)
    await channel.send("Channel locked.")


@bot.command(name = "unlock")
async def unlock(ctx, channel: discord.TextChannel):
    if ctx.author.id not in modID:
        await ctx.send("You do not have the permissions to use this command.")
        return
    channel = channel or ctx.channel
    role = discord.utils.get(ctx.message.guild.roles,name='Patrons') #assigns the counting clown role to a variable
    overwrite = channel.overwrites_for(role)
    overwrite.send_messages = True
    await channel.set_permissions(role, overwrite=overwrite)
    await channel.send("Channel unlocked.")


@commands.cooldown(1,15, commands.BucketType.user)
@bot.command(name = "claim", brief = "Claims daily points")
async def claim(ctx):
    if str(ctx.channel) not in channelList:
        await ctx.message.delete()
        return
    SQL = f"SELECT claimtime FROM points WHERE id = {ctx.author.id};"
    while True:
        try:
            cur.execute(SQL)
            break
        except psycopg2.InterfaceError:
            reestablish()
    conn.commit()
    lastTime = cur.fetchone()[0]

    UTCtime = datetime.datetime.now(datetime.timezone.utc)

    timeDifference = UTCtime - lastTime
    secondDifference = timeDifference.total_seconds()
    hourDifference = secondDifference/3600

    secondDifference = 86400 - secondDifference

    hours = secondDifference // 3600

    secondDifference %= 3600
    minutes = secondDifference // 60

    secondDifference %= 60
    seconds = secondDifference

    if hourDifference > 24:
        SQL = f"SELECT pointnumber FROM points WHERE id = {ctx.author.id};"
        cur.execute(SQL)
        conn.commit()
        points = cur.fetchone()[0]

        SQL = f"UPDATE points SET pointnumber = {points+25} WHERE id = {ctx.author.id};"
        cur.execute(SQL)
        conn.commit()

        SQL = f"UPDATE points SET claimtime = '{UTCtime}' WHERE id = {ctx.author.id};"
        cur.execute(SQL)
        conn.commit()
        await ctx.send("25 points have been added to your account. You can claim again in 24 hours.")
        
    else:
        await ctx.send(f"You can claim your points in {int(hours)}h {int(minutes)}m {int(seconds)}s.")
        return
    print(hourDifference)

@bot.command(name = "createrole")
async def createrole(ctx, name: str, r: int, g: int, b: int):
    if ctx.author.id not in modID:
        await ctx.send("You do not have the permissions to use this command.")
        return
    await ctx.guild.create_role(name=name, color=discord.Color.from_rgb(r, g, b))
    await ctx.send(f"Role created with name {name} and color from rgb({r}, {g}, {b})")


@bot.group(invoke_without_command = True)
async def dev(ctx):
    if ctx.author.id not in modID:
        return

@dev.command(name = 'pointtable')
async def pointtable(ctx):
    if ctx.author.id not in modID:
        return

    SQL = "SELECT pointnumber, name, id, bjwins,totalpoints FROM points;"
    cur.execute(SQL)
    rows = cur.fetchall()
    
    table = "```\n+------------+---------+------------------+-----------+--------+\n|pointnumber |name     |id                |bj wins    |totalpoints |\n+------------+---------+------------------+-----------+------------+\n"

    for row in rows:
        entry = f"|{row[0]:<12}|{row[1]:<9}|{row[2]:<18}|{row[3]:<11}|{row[4]:<12}|\n"
        table = "".join((table,entry))
        #await ctx.send(f"`|{row[0]:<7}|{row[1]:<9}|{row[2]:<18}|{row[3]:<11}|{row[4]:<8}|`")
    
    end = "+------------+---------+------------------+-----------+------------+```"
    table = "".join((table,end))
    print(len(table))
    await ctx.send(table)

@dev.command(name = 'striketable')
async def striketable(ctx):
    if ctx.author.id not in modID:
        return
    
    SQL = "SELECT name, strikes FROM striketable;"
    cur.execute(SQL)
    rows = cur.fetchall()
    
    table = "```\n+----------------------+--------------------+---------+\n|name                  |id                  |strikes  |\n+----------------------+--------------------+---------+\n"
    for row in rows:
        curUser = await ctx.message.guild.fetch_member(int(row[0]))
        entry = f"|{curUser.name:<22}|{int(row[0]):<20}|{row[1]:<9}|\n"
        table = "".join((table,entry))
    end = "+----------------------+--------------------+---------+```"
    table = "".join((table,end))
    await ctx.send(table)


@dev.command(name="sql")
async def devsql(ctx, statement: str):
    if ctx.author.id not in modID:
        return
    try:
        cur.execute(statement)
        await ctx.send("Process completed")
    except psycopg2.Error:
        await ctx.send("An error occurred")
        return
    


#--------------------------------------------------------------------------------------------------------------------------------------#
#  __  __  _____   _____   _____    
# |  \/  ||_   _| / ____| / ____|   
# | \  / |  | |  | (___  | |        
# | |\/| |  | |   \___ \ | |        
# | |  | | _| |_  ____) || |____   _ 
# |_|  |_||_____||_____/  \_____| (_)                                                                      


#randomly chooses an attacker or defender from the respective lists
@commands.cooldown(1, 15, commands.BucketType.user)
@bot.command(name = 'operator', description = 'Picks a random Rainbow Six Siege operator from either attack or defense')
async def operator(ctx,arg1):
    if str(ctx.channel) != "bot":
        await ctx.message.delete()
        return
    #checks if the user want an attacker or defender
    if arg1.lower() == "attacker":
        #sends a message with a random attacker
        await ctx.send(random.choice(attackerList))
        #adds an attacker reaction to the users message
        await ctx.message.add_reaction("⚔️")
        return
    if arg1.lower() == "defender":
        #sends a message with a random defender
        await ctx.send(random.choice(defenderList))
        #adds a defender reaction to the users message
        await ctx.message.add_reaction("🛡️")
        return
    else:
        #only happens if the user passed something other than attacker or defender
        await ctx.send("Please enter either 'Attacker' or 'Defender'")


#chooses a random number whose bounds are the numbers the user passed
@commands.cooldown(1, 10, commands.BucketType.user)
@bot.command(name = 'decide', description = 'Picks a random number between two numbers')
async def decide(ctx,arg1,arg2):
    if str(ctx.channel) != "bot":
        await ctx.message.delete()
        return
    try:
        if isinstance(arg1, int) == False or isinstance(arg2,int) == False:
            await ctx.send("Please enter whole numbers")
            return
        number = random.randint(int(arg1),int(arg2))
        await ctx.send(number)
    except CommandOnCooldown:
        pass


#common dice roller with parsing
@bot.command(name = 'dice', description = 'Rolls dice for the user\nFormat: [# of dice]d[# of sides] Separate different dice with spaces')
async def dice(ctx, *args):
    if str(ctx.channel) != "bot":
        await ctx.message.delete()
        return
    #converts all the arguments the user passes into a list
    argsList = list(args)
    if len(argsList) == 0:
        await ctx.send("Please enter dice to roll")
        return
    
    for i in argsList:
        matched = re.match("^[0-9]+d[0-9]+$", i)
        is_match = bool(matched)
        if is_match == False:
            await ctx.send("Please enter a valid die")
            return
    sum = 0
    rolls = []
    for i in range(len(argsList)):
        entry = argsList[i].split('d') #splits the index of argsList into two numbers, splicing at 'd'
        print(entry)
        for i in range(int(entry[0])): #repeats the dice roll for a number of times equal to the first index of the split
            roll = random.randint(1,int(entry[1])) #rolls a dice with the number of sides equal to the second index of the split
            rolls.append(roll)
            sum += roll
    await ctx.send("Rolls: "+', '.join(map(str,rolls))+"\nSum: "+str(sum)) #sends a message containing the rolls and the sum of all the rolls


@commands.cooldown(1, 15, commands.BucketType.user)
@bot.command(name = "source", brief = "Links the source github repo")
async def source(ctx):
    await ctx.send("https://hastebin.com/iseyugafik.py")


#--------------------------------------------------------------------------------------------------------------------------------------#
#  ______  _____   _____    ____   _____  
# |  ____||  __ \ |  __ \  / __ \ |  __ \ 
# | |__   | |__) || |__) || |  | || |__) |
# |  __|  |  _  / |  _  / | |  | ||  _  / 
# | |____ | | \ \ | | \ \ | |__| || | \ \ 
# |______||_|  \_\|_|  \_\ \____/ |_|  \_\                                                                                  


@py.error
async def py_error(ctx,error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.message.delete()
        errMess = await ctx.send(f'You are on cooldown for this command. Try again in {error.retry_after:.2f}s')
        await asyncio.sleep(error.retry_after)
        await errMess.delete()


@wolfram.error
async def wolfram_error(ctx,error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.message.delete()
        errMess = await ctx.send(f'You are on cooldown for this command. Try again in {error.retry_after:.2f}s')
        await asyncio.sleep(error.retry_after)
        await errMess.delete()


@wolframfull.error
async def wolframfull_error(ctx,error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.message.delete()
        errMess = await ctx.send(f'You are on cooldown for this command. Try again in {error.retry_after:.2f}s')
        await asyncio.sleep(error.retry_after)
        await errMess.delete()


@operator.error
async def operator_error(ctx,error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.message.delete()
        errMess = await ctx.send(f'You are on cooldowwn for this command. Try again in {error.retry_after:.2f}s')
        await asyncio.sleep(error.retry_after)
        await errMess.delete()


@rps.error
async def rps_error(ctx,error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.message.delete()
        errMess = await ctx.send(f'You are on cooldown for this command. Try again in {error.retry_after:.2f}s')
        await asyncio.sleep(error.retry_after)
        await errMess.delete()


@decide.error
async def decide_error(ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
        await ctx.message.delete()
        errMess = await ctx.send(f'You are on cooldown for this command. Try again in {error.retry_after:.2f}s')
        await asyncio.sleep(error.retry_after)
        await errMess.delete()


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
    
    if message.author == bot.user: #checks to see if the message author is the bot and returns
            return
    
    print('Message recieved: ', message.content, 'by', message.author, 'in '+ str(message.channel))

    #if the message is from a channel other than counting, it checks to see if it can make a dad joke
    if str(message.channel) != 'counting':
        if str(message.channel) == "one-word-sentence":
            if str(message.content) == ".":
                SQL = "SELECT * FROM sentence;"
                cur.execute(SQL)
                wordsListSQL = cur.fetchall()
                wordsList = []
                for word in wordsListSQL:
                    wordsList.append(word[0])
                await message.channel.send(" ".join(wordsList) + ".")
                SQL = "DELETE FROM sentence;"
                cur.execute(SQL)
                return
            else:
                SQL = f"INSERT INTO sentence VALUES ({str(message.content)});"
                cur.execute(SQL)
        if message.content.lower().startswith('im') or str(message.content).lower().startswith("i'm"):
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


#--------------------------------------------------------------------------------------------------------------------------------------#
#runs the bot using the discord bot token provided within Heroku
bot.run(os.environ['token'])