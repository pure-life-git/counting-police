import discord
import os
import random
from discord.ext import commands
import asyncio
import psycopg2

client = discord.Client()
bot = commands.Bot(command_prefix = '.')

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

forbiddenList = [
    "https://img.webmd.com/dtmcms/live/webmd/consumer_assets/site_images/articles/health_tools/ways_to_make_your_feet_feel_better_slideshow/493ss_thinkstock_rf_woman_stretching_feet.jpg",
    "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/gh-why-do-my-feet-hurt-toes-1594663599.png?crop=0.914xw:0.687xh;0.0864xw,0.110xh&resize=480:*",
    "https://post.greatist.com/wp-content/uploads/2019/07/Feet_1200x628-facebook.jpg",
    "https://www.saga.co.uk/contentlibrary/saga/publishing/verticals/health-and-wellbeing/conditions/happyfeetshutterstock_297390392768x576.jpg",
    "https://media.phillyvoice.com/media/images/09102019_feet_Pixabay.2e16d0ba.fill-735x490.jpg"
]

attackerList = [
    "Zero", "Ace", "Iana", "Kali", "Amaru", "Nøkk", "Gridlock", "Nomad",
    "Maverick", "Lion", "Finka", "Dokkaebi", "Zofia", "Ying", "Jackal",
    "Hibana", "Capitão", "Blackbeard", "Buck", "Sledge", "Thatcher", "Ash",
    "Thermite", "Montagne", "Twitch", "Blitz", "IQ", "Fuze", "Glaz"
]

defenderList = [
    "Aruni", "Melusi", "Oryx", "Wamai", "Goyo", "Warden", "Mozzie", "Kaid",
    "Clash", "Maestro", "Alibi", "Vigil", "Ela", "Lesion", "Mira", "Echo",
    "Caveira", "Valkyrie", "Frost", "Mute", "Smoke", "Castle", "Pulse", "Doc",
    "Rook", "Jäger", "Bandit", "Tachanka", "Kapkan"
]
#count = []
#games = []

def countEntry(num):
    SQL = "INSERT INTO countingtable (count) VALUES (%s);"
    data = (num,)
    cur.execute(SQL, data)
    conn.commit()
    #print(cur.execute("SELECT * FROM countingtable"))
    #cur.execute("SELECT countingtable FROM information_schema.tables WHERE table_schema = 'puclib'")
    #for table in cur.fetchall():
    #    print(table)

def gameEntry(game):
    SQL = """INSERT INTO gametable (games) VALUES (%s)"""
    data = (game,)
    cur.execute(SQL,data)
    conn.commit()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    cur.execute("SELECT COUNT(name) FROM striketable;")
    numCriminalsTable = cur.fetchall()
    numCriminals = numCriminalsTable[0][0]
    print(numCriminals)
    presence = str(numCriminals) + " criminals"
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=presence))

@bot.command()
async def operator(ctx,arg1):
    if arg1.lower() == "attacker":
        op = random.randint(0, len(attackerList)-1)
        await ctx.send(attackerList[op])
        await ctx.message.add_reaction("⚔️")
        return
    if arg1.lower() == "defender":
        op = random.randint(0, len(defenderList)-1)
        await ctx.send(defenderList[op])
        await ctx.message.add_reaction("🛡️")
        return
    else:
        await ctx.send("Please enter either 'Attacker' or 'Defender'")

@bot.command()
async def gamehelp(ctx):
    helpEmbed = discord.Embed(title='Help', description = 'Help with the bot', color=discord.Color.blurple())
    helpEmbed.add_field(name=".decide", value='Decide takes two arguments and generates a random number in the range of the two arguments', inline=False)
    helpEmbed.add_field(name=".strikes", value='Lets you know how many strikes you have in the counting channel', inline=False)
    helpEmbed.add_field(name=".finn", value="Sends a picture of feet to Finn",inline=False)
    helpEmbed.add_field(name=".operator", value="Chooses a random operator from Rainbow Six Siege. Enter either 'Attacker' or 'Defender'")
    helpEmbed.add_field(name=".game", value='Game will add a game to the Game List. Simply type the command and then\nthe game you would like to add', inline=False)
    helpEmbed.add_field(name=".gameremove", value='Gameremove removes a game from the Game List. Simply type the command then\nthe game you would like to remove', inline=False)
    helpEmbed.add_field(name=".choosegame", value='Choosegame will randomly choose a game from the Game List', inline=False)
    helpEmbed.add_field(name=".gameclear", value='Gameclear will clear the game list of all games')
    helpEmbed.add_field(name=".gamelist", value='Gamelist will print out a list of all the games you have added to the gamelist', inline=False)
    await ctx.send(embed=helpEmbed)

@bot.command()
async def decide(ctx,arg1,arg2):
    number = random.randint(int(arg1),int(arg2))
    await ctx.send(number)

@bot.command()
async def finn(ctx):
    link = forbiddenList[random.randint(0,len(forbiddenList)-1)]
    finnEmbed = discord.Embed(title="Feet Pics", description="Here's some fuel, you weirdo.", type="rich", color=discord.color.dark_green())
    finnEmbed.set_image(url=link)
    id = int(203300155762540544)
    #user = client.get_user(id)#203300155762540544
    #print(user)
    finn = await ctx.message.guild.fetch_member(id)
    await finn.send(embed=finnEmbed)
    await ctx.message.add_reaction("🦶")


@bot.command()
async def game(ctx, *, arg):
    gameLower = str(arg).lower()
    cur.execute("SELECT * FROM gametable")
    rawList = list(cur.fetchall())
    games = []
    for i in rawList:
        games.append(i[0])
    if gameLower in games:
        await ctx.send('That game is already in the list')
        return
    gameEntry(gameLower)
    #games.append(gameLower)
    message = ctx.message
    await message.add_reaction('👍')
    #await ctx.send('**Successfully added **' + str(arg) + '** to the Game List.**')

@bot.command()
async def choosegame(ctx):
    cur.execute("SELECT * FROM gametable")
    rawList = list(cur.fetchall())
    numSQL = []
    for i in rawList:
        numSQL.append(i[0])
    num = random.randint(0, len(numSQL)-1)
    await ctx.send(numSQL[num] + ' has been chosen by machine engineered randomness!**')

@bot.command()
async def gameclear(ctx):
    #for i in range(len(games)):
    #    games.pop()
    cur.execute("DELETE FROM gametable")
    conn.commit()
    message = ctx.message
    await message.add_reaction('👍')
    #await ctx.send('The list of games has been successfully cleared')

@bot.command()
async def gamelist(ctx):
    cur.execute("SELECT * FROM gametable")
    rawList = list(cur.fetchall())
    games = []
    for i in rawList:
            games.append(i[0])
    if len(games) != 0:
        gamelistEmbed = discord.Embed(title="Game List", description="List of games entered", color=discord.Color.greyple())
        gamelistEmbed.add_field(name="Games",value='\n'.join('**{}**: {}'.format(*k) for k in enumerate(games,1)))
        await ctx.send(embed = gamelistEmbed)
    else:
        emptygamelistEmbed = discord.Embed(title="Game List", description="List of games entered", color=discord.Color.red())
        emptygamelistEmbed.add_field(name="No Games!", value="The game list is empty.", inline=False)
        await ctx.send(embed = emptygamelistEmbed)

@bot.command()
async def gameremove(ctx,*,arg):
    gameLower = str(arg).lower()
    cur.execute("SELECT * FROM gametable")

    #games.remove(str(arg).lower())
    SQL = "DELETE FROM gametable WHERE games=%s;"
    cur.execute(SQL,(gameLower,))
    conn.commit()
    message = ctx.message
    await message.add_reaction('👍')
    #await ctx.send(str(arg).lower()+'** was successfully removed from the list**')

@bot.command()
async def poll(ctx,*args):
    timer = 120

    argsList = list(args)
    if len(argsList) != 0:
        if argsList[len(argsList)-1].isnumeric() == True:
            timer = int(argsList[len(argsList)-1])
            argsList.pop(len(argsList)-1)

    embedVar = discord.Embed(title='Poll', description = ' '.join(argsList), color=discord.Color.blue())
    embedVar.add_field(name="Yes", value='<:white_check_mark:785597865081962528>', inline=False)
    embedVar.add_field(name="No", value='<:x:785598446983839784>', inline=False)
    m = await ctx.send(embed=embedVar)
    await m.add_reaction('✅')
    await m.add_reaction('❌')
    await asyncio.sleep(timer)
    m = await ctx.channel.fetch_message(m.id)
    print(m.reactions)
    counts = {react.emoji: react.count for react in m.reactions}
    print(counts)
    yesResult = counts['✅']-1
    print('yesresult='+str(yesResult))
    noResult = counts['❌']-1
    print('noresult='+str(noResult))
    yesPercent = yesResult/(yesResult+noResult)
    noPercent = noResult/(yesResult+noResult)
    resultsEmbed = discord.Embed(title='Results', description = ' '.join(argsList), color=discord.Color.gold())
    resultsEmbed.add_field(name='✅', value="{yes} votes - {yespercent:.0%}".format(yes=yesResult,yespercent=yesPercent), inline=False)
    resultsEmbed.add_field(name='❌', value='{no} votes - {nopercent:.0%}'.format(no=noResult,nopercent=noPercent), inline=False)
    await m.delete()
    await ctx.send(embed=resultsEmbed)

@bot.command()
async def strikes(ctx):
    if ctx.message.author.id == 203282979265576960:
        await ctx.message.add_reaction('💯')
        return
    cur.execute("SELECT * FROM striketable")
    fetch = cur.fetchall()
    for i in fetch:
        if int(i[0]) == ctx.message.author.id:
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
    
    if message.author == bot.user:
            return
    
    print('Message recieved: ', message.content, 'by', message.author, 'in '+ str(message.channel))

    if str(message.channel) != 'counting':
        if message.content.lower().startswith('im') or str(message.content).lower().startswith("i'm"):
            dad = await message.channel.send('Hi ' + message.content.split(' ',1)[1] + ", I'm dad!")
            await dad.add_reaction('💯')
        if message.content.lower().startswith('i am'):
            dad = await message.channel.send('Hi ' + message.content.lower().split('i am ',1)[1] + ", I'm dad!")
            await dad.add_reaction('💯')
        return
    else:
        #print(count)
        #if len(count) == 0:
        #    count.append(int(message.content))
        #    countEntry(int(message.content))
        #    return

        #correctNumber = count[len(count)-1]+1
        cur.execute("SELECT MAX(count) FROM countingtable;")
        correctNumberDB = list(cur.fetchone())
        correctNumberSQL = int(correctNumberDB[0])+1
        #print('Correct Number: ',str(correctNumber))
        print('Correct Number in DB: ',str(correctNumberSQL))

        
        if str(message.content).isnumeric() == False or int(message.content) != correctNumberSQL:
            #await message.author.edit(roles='Counting Clown', reason='Ya done goofed the count')
            #server = bot.get_guild(599808865093287956)
            cur.execute("SELECT * FROM striketable")
            strikeList = cur.fetchall()
            userID = message.author.id
            for i in strikeList:
                if i[0] == userID:
                    if i[1] == 1:
                        await message.delete()
                        await message.channel.send(message.author.mention + ' entered ' + str(message.content) + ' and screwed up the count. This is their 2nd infraction.')
                        SQL = "UPDATE striketable SET strikes = 2 WHERE name = %s;"
                        cur.execute(SQL, (userID,))
                        conn.commit()
                        return
                    else:
                        SQLtwo = "UPDATE striketable SET strikes = 3 WHERE name = %s;"
                        cur.execute(SQLtwo, (userID,))
                        conn.commit()
                        role = discord.utils.get(message.guild.roles,name='Counting Clown')
                        await message.author.add_roles(role)
                        await message.delete()
                        await message.channel.send(message.author.mention + ' entered ' + str(message.content) + ' and screwed up the count. This was their 3rd and final infraction.')
                        return

            SQL = "INSERT INTO striketable (name, strikes) VALUES (%s, 1)"
            cur.execute(SQL, (userID,))
            conn.commit()
            await message.delete()
            await message.channel.send(message.author.mention + ' entered ' + str(message.content) + ' and screwed up the count. This is their 1st infraction.')
            cur.execute("SELECT COUNT(name) FROM striketable;")
            numCriminalsTable = cur.fetchall()
            numCriminals = numCriminalsTable[0][0]
            print(numCriminals)
            presence = str(numCriminals) + " criminals"
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=presence))


            #if userID not in strikeList:
            #    cur.execute("INSERT INTO striketable (name, strikes) VALUES (%s, 1)")

            #SQL = "INSERT IGNORE INTO striketable (name, strikes) VALUES (%s, %s)"
            #cur.execute()
            #role = discord.utils.get(message.guild.roles,name='Counting Clown')
            #await message.author.add_roles(role)
            #message.author.edit(discord.utils.get(message.guild.role, name = 'Counting Clown'))
            #await message.delete()
            #await message.channel.send(message.author.mention + ' entered ' + str(message.content) + ' and screwed up the count. Shame them!')
        else:
            #count.append(int(message.content))
            countEntry(int(message.content))


bot.run(os.environ['token'])