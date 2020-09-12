# Innuendo Copyright 2020 By Zan4eg#5557 and Kostya#3533
# Импорты библиотек

import discord
import random
from discord.ext import commands
import asyncio
import socket
import smtplib
import datetime
from datetime import timedelta
import os
from Cybernator import Paginator as pag
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json, socket, threading, time, concurrent.futures
from six.moves import urllib


PREFIX = 'i.' # Переменная префикса

Bot = commands.Bot( command_prefix = PREFIX ) # Установка префикса бота
@Bot.remove_command('help') #Удаление стандартной комманды help

# При загрузке бота
@Bot.event
async def on_ready():
    activity = discord.Game(name = "Innuendo | i.help", url='https://twitch.com/zan4egpayne')
    await Bot.change_presence( status = discord.Status.online, activity = activity )
    await asyncio.sleep(8)
    await Bot.change_presence( status = discord.Status.online, activity = discord.Game(name = "i.help") )
    await asyncio.sleep(8)
    await Bot.change_presence( status = discord.Status.online, activity = discord.Activity(type = discord.ActivityType.watching, name = f"{len(Bot.guilds)} серверов!") )
    await asyncio.sleep(8)
    await Bot.change_presence( status = discord.Status.online, activity = discord.Streaming(name = "http://innuendo.ml/", url='https://twitch.com/zan4egpayne') )
    print("Logged in as Innuendo!")
    print("Innuendo Copyright 2020 By Zan4eg#5557 and N3Kostya_#1337")
    print("Бот запущен и готов к работе!")                              
# Информация о пользователе
@Bot.command( pass_context=True )
async def info(ctx, user: discord.Member = None):
    if user is None:
        await ctx.send(f"**{ctx.author}**, укажите участника сервера \n Пример команды: ***i.info ``@Пользователь``***")
    else:
        emb = discord.Embed( title="Информация об {}".format(user.name), colour=0x31f5f5 ) # Создаем ембед
        emb.add_field( name='Имя', value=user.name ) # Получаем имя пользователя
        emb.add_field( name='Присоединился', value=user.joined_at ) # Получаем присоедение пользователя
        emb.add_field( name='Айди', value=user.id ) # Получаем айди пользователя
        emb.set_thumbnail( url=user.avatar_url ) # Получаем аватар пользователя
        emb.set_author( name=Bot.user.name, url="https://discord.com/api/oauth2/authorize?Bot_id=725379044845027329&permissions=8&scope=bot" ) # Приглашение бота себе на сервер
        emb.set_footer(text= "Упомянули: {}".format(user.name), icon_url= user.avatar_url) # Получаем имя пользователя и его аву (опять же)
        await ctx.send( embed = emb )

# Пригласить бота на свой сервер
@Bot.command()
async def invite ( ctx ):
    emb = discord.Embed( title='Пригласить бота на свой сервер.', colour=0x31f5f5)
    emb.set_footer( text="Ссылка была отправлена в лс." )
    emb.set_author( name=Bot.user.name, url="https://discord.com/api/oauth2/authorize?Bot_id=725379044845027329&permissions=8&scope=bot" )
    await ctx.send( embed = emb )
    await ctx.author.send ('https://discord.bots.gg/bots/724699992199004281')

# Очистка сообщений
@Bot.command( pass_context = True )
@commands.has_permissions( administrator = True ) # Установка нужных прав для комманды
async def clear ( ctx, amount : int = None):  # Создание комманды/функции
    if amount is None:
        await ctx.send(f"**{ctx.author}**, укажите количество сообщений для удаления \n Пример команды: ***i.clear ``кол-во сообщений``***")
    else:
        await ctx.message.delete() # Удаление сообщения с коммандой
        await ctx.channel.purge( limit = amount ) # Сама очистка
        emb = discord.Embed( description=f'✅  Очищено {amount} сообщений!', colour=0x31f5f5 ) # Создание отчета об очистке
        await ctx.send( embed = emb )

# Информация о сервере
@Bot.command()
async def serverinfo(ctx):
    # Задаем переменные
    channels = len(ctx.guild.channels)
    text_channels = len(ctx.guild.text_channels)
    voice_channels = len(ctx.guild.voice_channels)
    categories = len(ctx.guild.categories)
    members = len(ctx.guild.members)
    embed = discord.Embed(title = 'Информация о сервере:', description = f'Назва сервера: ``{ctx.guild.name}``\nАйди сервера: ``{ctx.guild.id}``\nВсего участников: ``{members}``\nВсего каналов и категорий: ``{channels}``\nТекстовые каналы: ``{text_channels}``\nГолосовые каналы: ``{voice_channels}``\nКатегорий: ``{categories}``', colour= 0x31f5f5)
    await ctx.send( embed=embed )

# Статистика каналов
@Bot.command() 
async def stat(ctx, channel: discord.TextChannel = None):
    if not channel: #проверяем ввели ли канал
        channel = ctx.channel
        text = 'в данном канале'
    else:
        text = f'в #{channel.name}'
    await ctx.send(f"{ctx.author.mention}, я начинаю вычисления, подождите немного...") #отправляем сообщение о начале отсчёта
    counter = 0
    yesterday = datetime.datetime.today() - timedelta(days = 1)
    #начинаем считать сообщения
    async for message in channel.history(limit=None, after=yesterday):
        counter += 1
    counter2 = 0
    weekago = datetime.datetime.today() - timedelta(weeks = 1)
    async for message in channel.history(limit=None, after=weekago):
        counter2 += 1
    counter3 = 0
    monthago = datetime.datetime.today() - timedelta(weeks = 4)
    async for message in channel.history(limit=None, after=monthago):
        counter3 += 1
    embed = discord.Embed(title = f'Статиститка сообщений {text}', colour= 0x31f5f5) #создаём embed-сообщение о подсчётах 
    embed.add_field(name = 'За сегодня', value = f'{counter}', inline = False) #добавляем поле "За сегодня"
    embed.add_field(name = 'За неделю', value = f'{counter2}', inline = False) #добавляем поле "За неделю" 
    embed.add_field(name = 'За месяц', value = f'{counter3}', inline = False) #добавляем поле "За месяц" 
    await ctx.send( f'{ctx.author.mention}', embed = embed ) #вывод сообщения с информацией о подсчётах

# Генератор паролей
lenght = int( '20' )
chars = '+-/*$#?=@<>abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
@Bot.command()
async def passgen( ctx ):
    await ctx.message.delete()
    password = ''
    for i in range( lenght ):
        password += random.choice( chars )
    emb = discord.Embed( description=f'✅ Ваш пароль был сгенерирован и отправлен вам в лс!', colour=0x31f5f5 )
    em = discord.Embed( description=f'✅ Ваш пароль: {password}\n⚠️ Никому не показывайте этот пароль!', colour=0x31f5f5 )
    await ctx.send( embed = emb )
    await ctx.author.send( embed = em )

# Получение айпи по домену
@Bot.command()
async def getip( ctx, host = None ):
    if host is None:
        await ctx.send(f"**{ctx.author}**, укажите домен \n Пример команды: ***i.getip ``домен```***")
    else:
        ip = socket.gethostbyname( host )
        await ctx.send( ip )

@Bot.command()
async def portscan( ctx, port = None, ip = None):
    if port is None:
        await ctx.send(f"**{ctx.author}**, укажите порт")
    else:
        if ip is None:
            await ctx.send(f"**{ctx.author}**, укажите айпи")
        else:
            portzhigovne = int( port )
            ip = socket.gethostbyname("unixgo.ru")
            for i in range(81):
                Bot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                if Bot.connect_ex((ip, port)):
                    await ctx.send( f'Порт {port} закрыт!' )
                else:
                    await ctx.send( f'Порт {port} открыт!' )   

@Bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member = None, *, reason = None):
    if member is None:
        await ctx.send(":x: | Укажите пользователя.")
    if member != ctx.author:
        await member.send(f'Ты был кикнут **{ctx.message.author}** на сервере ** {ctx.guild.name}** по причине: **{reason}**')
        await member.kick()
        await ctx.send(f':white_check_mark: | **{member}** кикнут.')

@Bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None, *, reason = None):
    if member is None:
        await ctx.send(":x: | Укажите пользователя.")
    if member != ctx.author and member != ctx.bot.user:
        await member.send(f'Ты был забанен **{ctx.message.author}** на сервере ** {ctx.guild.name}** по причине: **{reason}** ')
        await member.ban()
        await ctx.send(f':white_check_mark: | **{member}** забанен.')

@commands.cooldown(1, 5, commands.BucketType.user)
@Bot.command()
async def ping(ctx):
    em = discord.Embed(title="".format(ctx.guild.name), description="", color=0x31f5f5)
    em.set_author(name="")
    em.add_field(name="Ping", value='Понг! :ping_pong:', inline=True)
    em.add_field(name="MS", value=f'Пинг бота: **{ctx.bot.latency * 1000:,.2f}ms**', inline=True)
    await ctx.send(embed=em)

# Рандомное фото лисы
@Bot.command()
async def fox( ctx ):
    await ctx.message.delete()
    r = requests.get('https://randomfox.ca/floof/').json()
    em = discord.Embed( title="Рандомное фото лисы", color=0x31f5f5 )
    em.set_image( url=r["image"] )
    try:
        await ctx.send( embed=em )
    except:
        await ctx.send(r['image'])
        
@Bot.command()
async def slot(ctx):
    await ctx.message.delete()
    emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
    a = random.choice(emojis)
    b = random.choice(emojis)
    c = random.choice(emojis)
    slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"
    if (a == b == c):
        await ctx.send(embed=discord.Embed.from_dict({"title":"Казино", "description":f"{slotmachine} Все совпадения, вы выиграли!"}))
    elif (a == b) or (a == c) or (b == c):
        await ctx.send(embed=discord.Embed.from_dict({"title":"Казино", "description":f"{slotmachine} 2 подряд вы выиграли!"}))
    else:
        await ctx.send(embed=discord.Embed.from_dict({"title":"Казино", "description":f"{slotmachine} Нет совпадения, вы проиграли"}))

@commands.cooldown(1, 30, commands.BucketType.user)
@Bot.command()
async def abc(ctx): # b'\xfc'
    await ctx.message.delete()
    АБВ = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
    message = await ctx.send(АБВ[0])
    await asyncio.sleep(2)
    for _next in АБВ[1:]:
        await message.edit(content=_next)
        await asyncio.sleep(2)

# Рандомное фото или гиф гуся
@Bot.command()
async def duck( ctx ):
    await ctx.message.delete()
    r = requests.get('https://random-d.uk/api/random').json()
    em = discord.Embed( title="Рандомное фото или гифка гуся", color=0x31f5f5 )
    em.set_image(url=r["url"])
    try:
        await ctx.send(embed=em)
    except:
        await ctx.send(r['url'])


# Заварить ролтон
@Bot.command()
async def rolton( ctx ):
    await ctx.message.delete()
    emb = discord.Embed( title="Вы заварили Ролтон? Отличный выбор!", description="\n \n У вас получилось:", color=0x31f5f5 )
    emb.set_author( name='Ролтон', icon_url='https://cdn140.picsart.com/261815732025212.png?type=webp&to=min&r=640' )
    emb.set_image( url = 'https://pngimg.com/uploads/noodle/noodle_PNG59.png' )
    embed = discord.Embed( title="Инструкция", description="1. Откройте пачку ароматного Ролтона\n \n 2. Высыпите содержимое в тарелку \n \n 3. Залейте Ролтон кипятком \n \n 4. Накройте крышкой и подождите 4-5 минут \n \n 5. Наслаждайтесь вкусом вашего Ролтона", color=0x63009c )
    embed.set_author(name='Ролтон', icon_url='https://cdn140.picsart.com/261815732025212.png?type=webp&to=min&r=640')
    await ctx.send(embed = embed)
    await ctx.author.send(embed = emb)

# Узнать курс биткоина
@Bot.command( aliases=['bitcoin'] )
async def btc( ctx ): 
    await ctx.message.delete()
    r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,EUR')
    r = r.json()
    usd = r['USD']
    eur = r['EUR']
    em = discord.Embed( description=f'USD: `{str(usd)}$`\nEUR: `{str(eur)}€`', colour= 0x31f5f5 )
    em.set_author( name='Bitcoin', icon_url='https://cdn.pixabay.com/photo/2013/12/08/12/12/bitcoin-225079_960_720.png' )
    await ctx.send( embed=em )

# Узнать курс эфириума
@Bot.command( aliases=['ethereum'] )
async def eth( ctx ): 
    await ctx.message.delete()
    r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD,EUR')
    r = r.json()
    usd = r['USD']
    eur = r['EUR']
    em = discord.Embed( description=f'USD: `{str(usd)}$`\nEUR: `{str(eur)}€`', colour= 0x31f5f5 )
    em.set_author( name='Ethereum', icon_url='https://cdn.discordapp.com/attachments/271256875205525504/374282740218200064/2000px-Ethereum_logo.png' )
    await ctx.send( embed=em )

@Bot.command()
@commands.has_permissions( administrator = True ) # Установка нужных прав для комманды
async def news(ctx, *, args):
    await ctx.message.delete()
    for member in ctx.guild.members:
        try:
            await member.send(args)
        except:
            continue


@Bot.command()
@commands.cooldown(3, 86400, commands.BucketType.user)
async def mail( ctx, to = None, message = None ):
    if to is None:
        await ctx.send(f"**{ctx.author}**, укажите почту \n Пример команды: ***i.mail ``почта`` ``сообщение``***")
    else:
        if message is None:
            await ctx.send(f"**{ctx.author}**, укажите сообщение \n Пример команды: ***i.mail ``почта`` ``сообщение``***")
        else:
            msg = MIMEMultipart()
            msg['Subject'] = 'By Innuendo'
            server = smtplib.SMTP('smtp.gmail.com: 587')
            server.starttls()
            server.login('sendermailbot2020@gmail.com', 'dontchangethispassplz:)')
            msg.attach(MIMEText(message, 'plain'))
            server.sendmail('sendermailbot2020@gmail.com', to, msg.as_string())
            emb=discord.Embed( title = f"Сообщение было отправлено на почту: {to}", colour= 0x31f5f5)
            emb.add_field( name = 'Следующая отправка будет доступна через', value = '24 часа' )
            await ctx.send( embed=emb )
            server.quit()

@Bot.command()
@commands.cooldown(3, 600, commands.BucketType.user)
async def srvinfo( ctx, host = None, port = None ):
    if host is None:
        await ctx.send(f"**{ctx.author}**, укажите айпи \n Пример команды: ***i.srvinfo ``айпи`` ``порт``***")
    else:
        if port is None:
            await ctx.send(f"**{ctx.author}**, укажите айпи \n Пример команды: ***i.srvinfo ``айпи`` ``порт``***")
        else:
	    port = int(port)
	    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	    sock.settimeout(1.0)
	    sock.connect((host, port))
	    getinfo = urllib.request.urlopen('https://api.mcsrvstat.us/2/' + host + ':' + str(port))
	    jsoninfo = json.loads(getinfo.read().decode('utf-8'))
	    await ctx.send(f'Айпи: ' + host + ':' + str(port) + '\nВерсия: {0} \nМотд: {1}'.format(jsoninfo['version'], jsoninfo['motd']['clean'][0]))
	    sock.close()

            
# Навигация по командам
@Bot.command( pass_context = True )
async def help( ctx, amount = 1 ):
    await ctx.channel.purge( limit = amount )
    
    emb1=discord.Embed( title = 'Навигация по командам :pushpin:', colour= 0x31f5f5 )
    emb1.add_field( name = '``{}info``'.format( PREFIX ), value = 'Информация об пользователе.' )
    emb1.add_field( name = '``{}clear``'.format( PREFIX ), value = 'Очистка чата.' )
    emb1.add_field( name = '``{}stat``'.format( PREFIX ), value = 'Стистика каналов.' )
    emb1.add_field( name = '``{}serverinfo``'.format( PREFIX ), value = 'Информация о сервере.' )
    emb1.add_field( name = '``{}btc``'.format( PREFIX ), value = 'Узнать курс биткойна.' )
    emb2=discord.Embed( title = 'Навигация по командам :pushpin:', colour= 0x31f5f5 )
    emb2.add_field( name = '``{}eth``'.format( PREFIX ), value = 'Узнать курс ефириума.' )
    emb2.add_field( name = '``{}fox``'.format( PREFIX ), value = 'Рандомное фото лисы.' )
    emb2.add_field( name = '``{}duck``'.format( PREFIX ), value = 'Рандомное фото гуся.' )
    emb2.add_field( name = '``{}rolton``'.format( PREFIX ), value = 'Заварить ролтон.' )
    emb2.add_field( name = '``{}news``'.format( PREFIX ), value = 'Отправить всем в лс сообщение.' )
    emb3=discord.Embed( title = 'Навигация по командам :pushpin:', colour= 0x31f5f5 )
    emb3.add_field( name = '``{}passgen``'.format( PREFIX ), value= 'Сгенерировать сложный пароль.' )
    emb3.add_field( name = '``{}getip``'.format( PREFIX ), value= 'Получить айпи по домену.' )
    emb3.add_field( name = '``{}invite``'.format( PREFIX ), value= 'Пригласить бота на свой сервер.' )
    emb3.add_field( name = '``{}ban``'.format( PREFIX ), value= 'Забанить пользователя.' )
    emb3.add_field( name = '``{}kick``'.format( PREFIX ), value= 'Кикнуть пользователя.' )
    emb4=discord.Embed( title = 'Навигация по командам :pushpin:', colour= 0x31f5f5 )
    emb4.add_field( name = '``{}ping``'.format( PREFIX ), value= 'Узнать задержку бота.' )
    emb4.add_field( name = '``{}slot``'.format( PREFIX ), value= 'Казино.' )
    emb4.add_field( name = '``{}abc``'.format( PREFIX ), value= 'Алфавит.' )
    emb4.add_field( name = '``{}mail``'.format( PREFIX ), value= 'Сообщение на почту' )
    emb4.add_field( name = '``{}srvinfo``'.format( PREFIX ), value= 'Инфа о сервере майна' )
    embeds = [emb1, emb2, emb3, emb4]

    message = await ctx.send(embed=emb1)
    page = pag(Bot, message, only=ctx.author, use_more=False, embeds=embeds)
    await page.start()



token = os.environ.get('BOT_TOKEN')
Bot.run( str(token) )
