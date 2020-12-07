import discord
import os
import string
from discord.ext import commands

client = discord.Client()
count = []

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name="Joe Mama"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(count)
    print('Message recieved: ', message.content, 'by', message.author)
    messageChannel = message.channel
    print(messageChannel)
    print(type(messageChannel))

    if str(message.content).lower().startswith('im') or str(message.content).lower().startswith("i'm"): 
        await message.channel.send('Hi ' + message.content.split(' ',1)[1] + ", I'm dad!")
    
    if str(message.content).lower().startswith('i am'):
        await message.channel.send('Hi ' + message.content.split(' ',1)[2] + ", I'm dad!")

    if str(message.channel) != 'counting':
        return

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