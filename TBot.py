import discord, asyncio, time, json, requests
from discord.ext.commands import bot
from discord.ext import commands

Client = discord.Client()
client = commands.Bot(command_prefix = "!")

channelToken = 'Insira seu token aqui'


@client.event
async def on_ready():
    print('Bot pronto!')


@client.event
async def on_message(message):
    if message.content.upper().startswith('!HELP'):
        resposta = ('<@%s> os comandos são:\n !char <nome do personagem> \n !highlevel <nome do mundo>' % message.author.id)
        await client.send_message(message.channel, resposta)

    if message.content.upper().startswith('!CHAR'):
        userID = message.author.id
        args = message.content.split(" ")
        nome = ' '.join(map(str, args[1:]))
        char = requests.get("https://api.tibiadata.com/v2/characters/%s.json" % nome)
        retorno = json.loads(char.content)
        if 'error' in retorno['characters']:
            await client.send_message(message.channel, '<@%s> Infelizmente não encontramos esse char :frowning2:' % userID)
        else:
            try:
                if retorno['characters']['data']['guild']:
                    await client.send_message(message.channel, '<@%s> \n Nome: %s \n Level: %s \n Vocação: %s \n Mundo: %s\n Guild: %s' % (userID, retorno['characters']['data']['name'], retorno['characters']['data']['level'], retorno['characters']['data']['vocation'], retorno['characters']['data']['world'], retorno['characters']['data']['guild']['name']))
            except:
                await client.send_message(message.channel, '<@%s> \n Nome: %s \n Level: %s \n Vocação: %s \n Mundo: %s' % (userID, retorno['characters']['data']['name'], retorno['characters']['data']['level'], retorno['characters']['data']['vocation'], retorno['characters']['data']['world']))

    if message.content.upper().startswith('!HIGHLEVEL'):
        args = message.content.split(" ")
        mundo = ''
        userID = message.author.id
        if len(args) == 1:
            await client.send_message(message.channel, 'Favor inserir um mundo.')
        elif len(args) >= 2:
            mundo = args[1]
        retorno = requests.get('https://api.tibiadata.com/v2/highscores/{world}.json'.format(world=mundo))
        highscore = json.loads(retorno.content)
        highlevels = ''
        if highscore['highscores']['type'] == 'experience':
            for index in range(0, 10):
                highlevels += 'Nome: %s \n rank: %s \n Level: %s \n Vocação: %s \n\n' % (highscore['highscores']['data'][index]['name'], highscore['highscores']['data'][index]['rank'], highscore['highscores']['data'][index]['level'], highscore['highscores']['data'][index]['voc'])
        await client.send_message(message.channel, '<@%s> o top 10 de %s são:\n %s' % (userID, mundo, highlevels))

client.run(channelToken)