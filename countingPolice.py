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


#--------------------------------------------------------------------------------------------------------------------------------------#
#  _____  _   _  _____  _______  _____            _       _____  ______        _______  _____  ____   _   _   _____ 
# |_   _|| \ | ||_   _||__   __||_   _|    /\    | |     |_   _||___  /    /\ |__   __||_   _|/ __ \ | \ | | / ____|
#   | |  |  \| |  | |     | |     | |     /  \   | |       | |     / /    /  \   | |     | | | |  | ||  \| || (___  
#   | |  | . ` |  | |     | |     | |    / /\ \  | |       | |    / /    / /\ \  | |     | | | |  | || . ` | \___ \ 
#  _| |_ | |\  | _| |_    | |    _| |_  / ____ \ | |____  _| |_  / /__  / ____ \ | |    _| |_| |__| || |\  | ____) |
# |_____||_| \_||_____|   |_|   |_____|/_/    \_\|______||_____|/_____|/_/    \_\|_|   |_____|\____/ |_| \_||_____/ 


#initialize client and bot
client = discord.Client()
bot = commands.Bot(command_prefix = '.', description = 'Help for the H Welding Machine Bot')

#initializes connections to postgresql database
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

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
                                                                      

#enters a message from the #counting channel into the postgresql DB
def countEntry(num):
    SQL = "INSERT INTO countingtable (count) VALUES (%s);"
    data = (num,)
    cur.execute(SQL, data)
    conn.commit()
    if num % 25 == 0:
        SQLtwo = "DELETE FROM countingtable WHERE count < (%s);"
        dataTwo = (num-1,)
        cur.execute(SQLtwo, dataTwo)
        conn.commit()

#enters a game from any channel into the postgresql DB
def gameEntry(game):
    SQL = """INSERT INTO gametable (games) VALUES (%s)"""
    data = (game,)
    cur.execute(SQL,data)
    conn.commit()


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
    cur.execute("SELECT COUNT(name) FROM striketable;")
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
    await ctx.send("Valid subcommands: add, remove, clear, list, choose")


#adds a game provided by the user to the gameList
@game.command(name = 'add', description = 'Adds a game to the game list')
async def add(ctx, *, arg):
    gameLower = str(arg).lower()
    cur.execute("SELECT * FROM gametable") #select every entry in the gametable from the DB 
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
    gameLower = str(arg).lower()
    cur.execute("SELECT * FROM gametable") #selects all the entries from the gamelist
    SQL = "DELETE FROM gametable WHERE games=%s;" #deletes the row in the game table with the game name
    cur.execute(SQL,(gameLower,))
    conn.commit()
    message = ctx.message
    await message.add_reaction('👍')


#clears game list
@game.command(name = 'clear', description = 'Clears the game list')
async def clear(ctx):
    cur.execute("DELETE FROM gametable") #deletes all entries from the game list
    conn.commit()
    message = ctx.message
    await message.add_reaction('👍')


#randomly chooses a game from the game list
@game.command(name = 'choose', description='Randomly chooses a game from the game list')
async def choose(ctx):
    cur.execute("SELECT * FROM gametable") #selects all of the entries from the table
    rawList = list(cur.fetchall()) # makes a list out of the selection
    numSQL = []
    for i in rawList:
        numSQL.append(i[0]) #takes the list of tuples and appends the first index to a new list
    num = random.choice(numSQL) #chooses a 
    await ctx.send(num + ' has been chosen by machine engineered randomness!') #sends a message with the result


#lists all of the games in the gamelist
@game.command(name = 'list', description = 'Displays the game list')
async def gamelist(ctx):
    cur.execute("SELECT * FROM gametable") #selects all entries from the game list
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
    argsJoin = ' '.join(args)
    answer = eval(argsJoin)
    await ctx.send(answer)


#sends user input to the wolframalpha api and prints out the answer
@commands.cooldown(1, 20, commands.BucketType.user)
@bot.command(name = 'wolfram', description='Returns the simple answer to a query from Wolfram|Alpha')
async def wolfram(ctx,*args):
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


@bot.command(name = "tictactoe", description = "*WIP* Challenge another player to a game of tic-tac-toe")
async def tictactoe(ctx):
    game = True
    moves = 0
    board = {
        '1': ' ', '2': ' ', '3': ' ',
        '4': ' ', '5': ' ', '6': ' ',
        '7': ' ', '8': ' ', '9': ' '
    }
    keys = board.keys()
    def printBoard(board):
        return(f"{board['1']}|{board['2']}|{board['3']}\n-+-+-\n{board['4']}|{board['5']}|{board['6']}\n-+-+-\n{board['7']}|{board['8']}|{board['9']}")
    playerOne = ctx.message.author
    playerTwo = ctx.message.mentions[0]

    plays = [(playerOne,'x'), (playerTwo, 'o')]
    def checkTwo(user):
        return user == playerTwo
    def checkOne(user):
        return user == playerOne
    await ctx.send(f"{playerOne} has challenged {playerTwo} to a game of Tic Tac Toe! Do you accept? Y/N")
    msg = await bot.wait_for('message', check=checkTwo, timeout=30)
    if msg.content.lower() == 'n':
        await ctx.send('Challenge denied')
        return

    while game == True:
        if moves % 2 == 0:
            mover = plays[0][0]
            move = plays[0][1]
            mess = await bot.wait_for('message', check=checkOne)
            if mess.content.lower() == 'end':
                game = False
                break
            elif mess.content.lower() not in keys:
                await ctx.send("That is not a valid input. Please enter a number 1-9")
                continue
            elif board[mess.content] != ' ':
                await ctx.send("That space if full. Please pick a free space")
            else:
                board[mess.content] = move
                moves += 1
        else:
            mover = plays[1][0]
            move = plays[1][1]
            mess = await bot.wait_for('message', check=checkTwo)
            if mess.content.lower() == 'end':
                game = False
                break
            elif mess.content.lower() not in keys:
                await ctx.send("That is not a valid input. Please enter a number 1-9")
                continue
            elif board[mess.content] != ' ':
                await ctx.send("That space if full. Please pick a free space")
            else:
                board[mess.content] = move
                moves += 1
        
        await ctx.send(printBoard(board))
        
        if moves >=5:
            if board['1'] == board['2'] == board['3'] != ' ':
                await ctx.send(f"{mover} has won the gamein {moves} moves!")
                game = False
                return
            elif board['4'] == board['5'] == board['6'] != ' ':
                await ctx.send(f"{mover} has won the game in {moves} moves!")
                game = False
                return
            elif board['7'] == board['8'] == board['9'] != ' ':
                await ctx.send(f"{mover} has won the game in {moves} moves!")
                game = False
                return
            elif board['1'] == board['4'] == board['7'] != ' ':
                await ctx.send(f"{mover} has won the game in {moves} moves!")
                game = False
                return
            elif board['2'] == board['5'] == board['8'] != ' ':
                await ctx.send(f"{mover} has won the game in {moves} moves!")
                game = False
                return
            elif board['3'] == board['6'] == board['9'] != ' ':
                await ctx.send(f"{mover} has won the game in {moves} moves!")
                game = False
                return
            elif board['1'] == board['5'] == board['9'] != ' ':
                await ctx.send(f"{mover} has won the game in {moves} moves!")
                game = False
                return
            elif board['3'] == board['5'] == board['7'] != ' ':
                await ctx.send(f"{mover} has won the game in {moves} moves!")
                game = False
                return
                
            

    



#sends a random picture from the forbiddenList directly to Finn
@commands.cooldown(1, 15, commands.BucketType.user)
@bot.command(name = 'finn', description = 'Sends a feet pic to Finn')
async def finn(ctx):
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


#mutes a member of the server for a specified amount of time
@bot.command(name = 'mute',help_command = None)
async def mute(ctx, mention, time='5s'):
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
    if ctx.message.author.id == 203282979265576960: #checks to see if the userID matches Kyle's
        await ctx.message.add_reaction('💯')
        return
    cur.execute("SELECT * FROM striketable") #selects all values in the striketable
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
        await asyncio.sleep(5)
        await errMess.delete()


@wolfram.error
async def wolfram_error(ctx,error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.message.delete()
        errMess = await ctx.send(f'You are on cooldown for this command. Try again in {error.retry_after:.2f}s')
        await asyncio.sleep(5)
        await errMess.delete()


@wolframfull.error
async def wolframfull_error(ctx,error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.message.delete()
        errMess = await ctx.send(f'You are on cooldown for this command. Try again in {error.retry_after:.2f}s')
        await asyncio.sleep(5)
        await errMess.delete()


@operator.error
async def operator_error(ctx,error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.message.delete()
        errMess = await ctx.send(f'You are on cooldowwn for this command. Try again in {error.retry_after:.2f}s')
        await asyncio.sleep(5)
        await errMess.delete()


@rps.error
async def rps_error(ctx,error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.message.delete()
        errMess = await ctx.send(f'You are on cooldown for this command. Try again in {error.retry_after:.2f}s')
        await asyncio.sleep(5)
        await errMess.delete()


@decide.error
async def decide_error(ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
        await ctx.message.delete()
        errMess = await ctx.send(f'You are on cooldown for this command. Try again in {error.retry_after:.2f}s')
        await asyncio.sleep(5)
        await errMess.delete()


@finn.error
async def finn_error(ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
        await ctx.message.delete()
        errMess = await ctx.send(f'You are on cooldown for this command. Try again in {error.retry_after:.2f}s')
        await asyncio.sleep(5)
        await errMess.delete()


@strikes.error
async def strike_error(ctx,error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.message.delete()
        errMess = await ctx.send(f'You are on cooldown for this command. Try again in {error.retry_after:.2f}s')
        await asyncio.sleep(5)
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
        if message.content.lower().startswith('im') or str(message.content).lower().startswith("i'm"):
            dad = await message.channel.send('Hi ' + message.content.split(' ',1)[1] + ", I'm dad!")
            await dad.add_reaction('👌')
        if message.content.lower().startswith('i am'):
            dad = await message.channel.send('Hi ' + message.content.lower().split('i am ',1)[1] + ", I'm dad!")
            await dad.add_reaction('👌')
        return
    else:
        cur.execute("SELECT MAX(count) FROM countingtable;") #gets the max value from the countingtable
        correctNumberDB = list(cur.fetchone()) #fetches the value tuple and stores it in a variable
        correctNumberSQL = int(correctNumberDB[0])+1 #get the actual int value and increases it by one to reflect the correct value
        print('Correct Number in DB: ',str(correctNumberSQL))
        if str(message.content).isnumeric() == False or int(message.content) != correctNumberSQL: #checks to see if the message is not a number or is not the correct number
            cur.execute("SELECT * FROM striketable") #selects all the values in the strikelist
            strikeList = cur.fetchall()
            userID = message.author.id
            for i in strikeList:
                if i[0] == str(userID): #checks to see if the user is already in the strikelist
                    if i[1] == 1: #checks if they have one strike
                        await message.delete()
                        #sends a message alerting everyone to the user's infraction
                        await message.channel.send(message.author.mention + ' entered ' + str(message.content) + ' and screwed up the count. This is their 2nd infraction.')
                        SQL = "UPDATE striketable SET strikes = 2 WHERE name = '%s';" #updates their strikes to reflect the new number
                        cur.execute(SQL, (userID,))
                        conn.commit()
                        return
                    else: #if they don't have one strike and theyre already in the table, then they have two strikes
                        SQLtwo = "UPDATE striketable SET strikes = 3 WHERE name = '%s';" #updates their strikes to reflect the new number
                        cur.execute(SQLtwo, (userID,))
                        conn.commit()
                        role = discord.utils.get(message.guild.roles,name='Counting Clown') #assigns the counting clown role to a variable
                        await message.author.add_roles(role) #give the author the counting clown role
                        await message.delete() #deletes the user's message
                        #sends a message alerting everyone to the user's infraction
                        await message.channel.send(message.author.mention + ' entered ' + str(message.content) + ' and screwed up the count. This was their 3rd and final infraction.')
                        return

            #if we haven't returned by now, it means they are not in the table
            SQL = "INSERT INTO striketable (name, strikes) VALUES (%s, 1)" #inserts their userid into the table
            cur.execute(SQL, (userID,))
            conn.commit()
            await message.delete() #deletes their message
            #sends a message alerting everyone to the user's infraction
            await message.channel.send(message.author.mention + ' entered ' + str(message.content) + ' and screwed up the count. This is their 1st infraction.')
            cur.execute("SELECT COUNT(name) FROM striketable;") #updates the status of the bot to match the new number of criminals
            numCriminalsTable = cur.fetchall()
            numCriminals = numCriminalsTable[0][0]
            print(numCriminals)
            presence = str(numCriminals) + " criminals"
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=presence))
        else:
            #if the message was in the counting channel but was the right number, 
            #then we just call the function that adds their number to the DB
            countEntry(int(message.content))
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