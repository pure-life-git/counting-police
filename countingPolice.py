import discord
import os
import string
import random
from discord.ext import commands

client = discord.Client()
count = []
games = []

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name="Joe Mama"))

@client.event
async def on_message(message):
    if message.author == client.user:
            return
    if str(message.channel) != 'counting':
        print(count)
        print('Message recieved: ', message.content, 'by', message.author)
        messageChannel = message.channel
        print(messageChannel)
        print(type(messageChannel))

        if message.content.lower().startswith('im') or str(message.content).lower().startswith("i'm"):
            await message.channel.send('Hi ' + message.content.split(' ',1)[1] + ", I'm dad!")
        
        if message.content.lower().startswith('i am'):
            await message.channel.send('Hi ' + message.content.lower().split('i am ',1)[1] + ", I'm dad!")

        if message.content.startswith('$decide'):
            number = random.randint(int(message.content.split(' ')[1]),int(message.content.split(' ')[2]))
            await message.channel.send(number)

        if message.content.startswith('$game'):
            game = message.content.split(' ',1)[1]
            games.append(game)
            await message.channel.send(game + ' has been added to the games list.')
            await message.channel.send('\n'.join('{}: *{}*'.format(*k) for k in enumerate(games)))
        
        if message.content.startswith('$choicegame'):
            num = random.randint(0,len(games)-1)
            await message.channel.send(games[num] + ' has been chosen by machine engineering randomness!')

        return
    else:
        if len(count) == 0:
            count.append(int(message.content))
            return

        correctNumber = count[len(count)-1]+1
        print('Correct Number: ',str(correctNumber))

        
        if str(message.content).isnumeric() == False or int(message.content) != correctNumber:
            #await message.author.edit(roles='Counting Clown', reason='Ya done goofed the count')
            server = client.get_guild(599808865093287956)
            role = discord.utils.get(server.roles,name='Counting Clown')
            await message.author.add_roles(role)
            #message.author.edit(discord.utils.get(message.guild.role, name = 'Counting Clown'))
            await message.delete()
            count.clear()
            await message.channel.send(message.author.mention + ' entered ' + str(message.content) + ' and screwed up the count. Shame them!')
        else:
            count.append(int(message.content))


client.run(os.environ['token'])