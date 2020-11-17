import discord
from discord.ext import commands

client = discord.Client()
count = []

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(count)
    print('Message recieved: ', message.content, 'by', message.author)
    messageChannel = message.channel
    print(messageChannel)
    print(type(messageChannel))

    if str(message.channel) != 'counting':
        return

    if len(count) == 0:
        count.append(int(message.content))
        return

    correctNumber = count[len(count)-1]+1
    print('Correct Number: ',str(correctNumber))
    
    if int(message.content) != correctNumber:
        #await message.author.edit(roles='Counting Clown', reason='Ya done goofed the count')
        server = client.get_guild(599808865093287956)
        role = discord.utils.get(server.roles,name='Counting Criminal')
        await message.author.add_roles(role)
        #message.author.edit(discord.utils.get(message.guild.role, name = 'Counting Clown'))
        await message.delete()
        count.clear()
        await message.channel.send('The count has been reset by ' + message.author.mention + '. Shame them.')
    else:
        count.append(int(message.content))


client.run('Nzc3NzAxNTQ4MjYzNjA0MjI0.X7HRAg.ayFBwNrlslG6xUL9qVMtVzkESBM')