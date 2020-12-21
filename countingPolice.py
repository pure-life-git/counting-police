import discord
import os
import random
from discord.ext import commands
import asyncio
import psycopg2
import wolframalpha
import youtube_dl
import ctypes
import ctypes.util


#initialize client and bot
client = discord.Client()
bot = commands.Bot(command_prefix = '.')
bot.remove_command('help')

#initializes connections to postgresql database
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

#sets up wolfram api
wolframID = 'PAX2TQ-2V94QU68XE'
wolframClient = wolframalpha.Client(wolframID)

#suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

#sets up and loads the opus library
print("ctypes - Find opus:")
a = ctypes.util.find_library('opus')
print(a)
 
print("Discord - Load Opus:")
b = discord.opus.load_opus(a)
print(b)
 
print("Discord - Is loaded:")
c = discord.opus.is_loaded()
print(c)

#foot picture list for .finn
forbiddenList = [
    "https://img.webmd.com/dtmcms/live/webmd/consumer_assets/site_images/articles/health_tools/ways_to_make_your_feet_feel_better_slideshow/493ss_thinkstock_rf_woman_stretching_feet.jpg",
    "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/gh-why-do-my-feet-hurt-toes-1594663599.png?crop=0.914xw:0.687xh;0.0864xw,0.110xh&resize=480:*",
    "https://post.greatist.com/wp-content/uploads/2019/07/Feet_1200x628-facebook.jpg",
    "https://www.saga.co.uk/contentlibrary/saga/publishing/verticals/health-and-wellbeing/conditions/happyfeetshutterstock_297390392768x576.jpg",
    "https://media.phillyvoice.com/media/images/09102019_feet_Pixabay.2e16d0ba.fill-735x490.jpg"
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

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

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

#sends user input to the wolframalpha api and prints out the answer
@bot.command()
async def wolfram(ctx,*args):
    question = ' '.join(args) #joins the user args into a single string
    response = wolframClient.query(question) #gets a query from the wolfram api using the question
    wolframEmbed = discord.Embed(title="Wolfram|Alpha API", description=" ", color=discord.Color.from_rgb(255,125,0))
    for pod in response.results: #for each returned pod from the query, adds a new field to the answer embed
        wolframEmbed.add_field(name=pod.title,value=pod.text,inline=False)
    #wolframEmbed.add_field(name="Result", value=response.results.text,inline=False)
    await ctx.channel.send(embed=wolframEmbed)

#sends user input to the wolframalpha api and prints out a full answer
@bot.command()
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

@bot.command()
async def doot(ctx):
    user = ctx.message.author
    voice_channel = user.voice.channel
    channel=None
    if voice_channel != None:
        channel = voice_channel.name
        voice = await voice_channel.connect()
        player = await YTDLSource.from_url('https://www.youtube.com/watch?v=WTWyosdkx44')
        voice.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        await asyncio.sleep(5)
        await voice.disconnect()


#randomly chooses an attacker or defender from the respective lists
@bot.command()
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

#help command to explain each command for the bot
@bot.command()
async def help(ctx):
    helpEmbed = discord.Embed(title='Help', description = 'Help with the bot', color=discord.Color.blurple())
    helpEmbed.add_field(name=".decide", value='Decide takes two arguments and generates a random number in the range of the two arguments', inline=False)
    helpEmbed.add_field(name=".strikes", value='Lets you know how many strikes you have in the counting channel', inline=False)
    helpEmbed.add_field(name=".finn", value="Sends a picture of feet to Finn",inline=False)
    helpEmbed.add_field(name=".dice", value="Rolls dice in the format (# of dice)d(# of sides). You can even input multiple dice in one command.\nExample: '.dice 1d4 2d6' would roll 1 4 sided die and 2 6 sided die", inline=False)
    helpEmbed.add_field(name=".rps", value="Plays a game of rock paper scissors with you\nExample: .rps paper")
    helpEmbed.add_field(name=".operator", value="Chooses a random operator from Rainbow Six Siege. Enter either 'Attacker' or 'Defender'", inline=False)
    helpEmbed.add_field(name=".game", value='Game will add a game to the Game List. Simply type the command and then\nthe game you would like to add', inline=False)
    helpEmbed.add_field(name=".gameremove", value='Gameremove removes a game from the Game List. Simply type the command then\nthe game you would like to remove', inline=False)
    helpEmbed.add_field(name=".choosegame", value='Choosegame will randomly choose a game from the Game List', inline=False)
    helpEmbed.add_field(name=".gameclear", value='Gameclear will clear the game list of all games', inline=False)
    helpEmbed.add_field(name=".gamelist", value='Gamelist will print out a list of all the games you have added to the gamelist', inline=False)
    await ctx.send(embed=helpEmbed)

#plays a game of rock paper scissorcs with the user
@bot.command()
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

#chooses a random number whose bounds are the numbers the user passed
@bot.command()
async def decide(ctx,arg1,arg2):
    number = random.randint(int(arg1),int(arg2))
    await ctx.send(number)

#sends a random picture from the forbiddenList directly to Finn
@bot.command()
async def finn(ctx):
    link = random.choice(forbiddenList)
    finnEmbed = discord.Embed(title="Feet Pics", description="Here's some fuel, you weirdo.", type="rich", color=discord.Color.dark_green())
    finnEmbed.set_image(url=link)
    id = int(203300155762540544) #sets id as Finn's userId
    finn = await ctx.message.guild.fetch_member(id) #fetches Finn's user from his id
    await finn.send(embed=finnEmbed)
    await ctx.message.add_reaction("🦶")

#common dice roller with parsing
@bot.command()
async def dice(ctx, *args):
    #converts all the arguments the user passes into a list
    argsList = list(args)
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

#adds a game provided by the user to the gameList
@bot.command()
async def game(ctx, *, arg):
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

#randomly chooses a game from the game list
@bot.command()
async def choosegame(ctx):
    cur.execute("SELECT * FROM gametable") #selects all of the entries from the table
    rawList = list(cur.fetchall()) # makes a list out of the selection
    numSQL = []
    for i in rawList:
        numSQL.append(i[0]) #takes the list of tuples and appends the first index to a new list
    num = random.choice(numSQL) #chooses a 
    await ctx.send(num + ' has been chosen by machine engineered randomness!') #sends a message with the result

#clears game list
@bot.command()
async def gameclear(ctx):
    cur.execute("DELETE FROM gametable") #deletes all entries from the game list
    conn.commit()
    message = ctx.message
    await message.add_reaction('👍')

#lists all of the games in the gamelist
@bot.command()
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

#removes a particular game from the gamelist
@bot.command()
async def gameremove(ctx,*,arg):
    gameLower = str(arg).lower()
    cur.execute("SELECT * FROM gametable") #selects all the entries from the gamelist
    SQL = "DELETE FROM gametable WHERE games=%s;" #deletes the row in the game table with the game name
    cur.execute(SQL,(gameLower,))
    conn.commit()
    message = ctx.message
    await message.add_reaction('👍')


@bot.command()
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

@bot.command()
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

#runs the bot using the discord bot token provided within Heroku
bot.run(os.environ['token'])