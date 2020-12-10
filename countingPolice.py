import discord
import os
import random
from discord.ext import commands
from time import sleep
import psycopg2

#bot = discord.bot()
bot = commands.Bot(command_prefix = '.')

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

count = []
games = []

def countEntry(num):
    SQL = "UPDATE countingtable SET count = %s;"
    data = (num,)
    cur.execute(SQL, data)
    conn.commit()

def gameEntry(game):
    SQL = "INSERT INTO gametable (games) VALUES (%s);"
    data = (game,)
    cur.execute(SQL,data)
    conn.commit()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name=".gamehelp"))

@bot.command()
async def gamehelp(ctx):
    helpEmbed = discord.Embed(title='Help', description = 'Help with the bot')
    helpEmbed.add_field(name=".decide", value='Decide takes two arguments and generates a random number in the range of the two arguments', inline=False)
    helpEmbed.add_field(name=".game", value='Game will add a game to the Game List. Simply type the command and then\nthe game you would like to add', inline=False)
    helpEmbed.add_field(name=".gameremove", value='Gameremove removes a game from the Game List. Simply type the command then\nthe game you would like to add', inline=False)
    helpEmbed.add_field(name=".choosegame", value='Choosegame will randomly choose a game from the Game List', inline=False)
    helpEmbed.add_field(name=".gameclear", value='Gameclear will clear the game list of all games')
    helpEmbed.add_field(name=".gamelist", value='Gamelist will print out a list of all the games you have added to the gamelist', inline=False)
    await ctx.send(embed=helpEmbed)

@bot.command()
async def decide(ctx,arg1,arg2):
    number = random.randint(int(arg1),int(arg2))
    await ctx.send(number)

@bot.command()
async def game(ctx, *, arg):
    if str(arg).lower() in games:
        await ctx.send('That game is already in the list')
        return
    gameLower = str(arg).lower()
    gameEntry(gameLower)
    games.append(gameLower)
    message = ctx.message
    await message.add_reaction('👍')
    #await ctx.send('**Successfully added **' + str(arg) + '** to the Game List.**')

@bot.command()
async def choosegame(ctx):
    num = random.randint(0, len(games)-1)
    #await ctx.send(games[num] + '** has been chosen by machine engineered randomness!**')

@bot.command()
async def gameclear(ctx):
    for i in range(len(games)):
        games.pop()
    message = ctx.message
    await message.add_reaction('👍')
    #await ctx.send('The list of games has been successfully cleared')

@bot.command()
async def gamelist(ctx):
    await ctx.send('\n'.join('**{}**: {}'.format(*k) for k in enumerate(games,1)))

@bot.command()
async def gameremove(ctx,*,arg):
    if str(arg).lower() in games:
        games.remove(str(arg).lower())
        message = ctx.message
        await message.add_reaction('👍')
        #await ctx.send(str(arg).lower()+'** was successfully removed from the list**')

@bot.command()
async def poll(ctx,*args):
    if len(args) == 0:
        embedVar = discord.Embed(title='Poll', description = 'Vote')
        embedVar.add_field(name="Yes", value='<:white_check_mark:785597865081962528>', inline=False)
        embedVar.add_field(name="No", value='<:x:785598446983839784>', inline=False)
        m = await ctx.send(embed=embedVar)
        await m.add_reaction('✅')
        await m.add_reaction('❌')
    else:
        embedVar = discord.Embed(title='Poll', description = ' '.join(args))
        embedVar.add_field(name="Yes", value='<:white_check_mark:785597865081962528>', inline=False)
        embedVar.add_field(name="No", value='<:x:785598446983839784>', inline=False)
        m = await ctx.send(embed=embedVar)
        await m.add_reaction('✅')
        await m.add_reaction('❌')

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    
    if message.author == bot.user:
            return
    
    print('Message recieved: ', message.content, 'by', message.author, 'in '+ str(message.channel))

    if str(message.channel) != 'counting':
        if message.content.lower().startswith('im') or str(message.content).lower().startswith("i'm"):
            await message.channel.send('Hi ' + message.content.split(' ',1)[1] + ", I'm dad!")
        
        if message.content.lower().startswith('i am'):
            await message.channel.send('Hi ' + message.content.lower().split('i am ',1)[1] + ", I'm dad!")
        return
    else:
        print(count)
        if len(count) == 0:
            count.append(int(message.content))
            return

        correctNumber = count[len(count)-1]+1
        print('Correct Number: ',str(correctNumber))

        
        if str(message.content).isnumeric() == False or int(message.content) != correctNumber:
            #await message.author.edit(roles='Counting Clown', reason='Ya done goofed the count')
            #server = bot.get_guild(599808865093287956)
            role = discord.utils.get(message.guild.roles,name='Counting Clown')
            await message.author.add_roles(role)
            #message.author.edit(discord.utils.get(message.guild.role, name = 'Counting Clown'))
            await message.delete()
            await message.channel.send(message.author.mention + ' entered ' + str(message.content) + ' and screwed up the count. Shame them!')
        else:
            count.append(int(message.content))
            countEntry(int(message.content))


bot.run(os.environ['token'])