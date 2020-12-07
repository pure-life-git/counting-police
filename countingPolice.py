import discord
import os
import random
from discord.ext import commands

#bot = discord.bot()
bot = commands.Bot(command_prefix = '.')

count = []
games = []

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name="Joe Mama"))

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def decide(ctx,arg1,arg2):
    number = random.randint(int(arg1),int(arg2))
    await ctx.send(number)

@bot.command()
async def game(ctx, *, arg):
    games.append(str(arg))
    await ctx.send('**Successfully added **' + str(arg) + '** to the Game List.**')

@bot.command()
async def choosegame(ctx):
    num = random.randint(0, len(games)-1)
    await ctx.send(games[num] + '** has been chosen by machine engineered randomness!**')

@bot.command()
async def gameclear(ctx):
    for i in range(len(games)):
        games.pop()
    await ctx.send('The list of games has been successfully cleared')

@bot.command()
async def gameslist(ctx):
    await ctx.send('\n'.join('{}: *{}*'.format(*k) for k in enumerate(games)))


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
            server = bot.get_guild(599808865093287956)
            role = discord.utils.get(server.roles,name='Counting Clown')
            await message.author.add_roles(role)
            #message.author.edit(discord.utils.get(message.guild.role, name = 'Counting Clown'))
            await message.delete()
            count.clear()
            await message.channel.send(message.author.mention + ' entered ' + str(message.content) + ' and screwed up the count. Shame them!')
        else:
            count.append(int(message.content))


bot.run(os.environ['token'])