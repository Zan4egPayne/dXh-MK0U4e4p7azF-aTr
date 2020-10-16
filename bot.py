# Innuendo Copyright 2020 By Zan4eg#5557 and Kostya#3533
# Импорты библиотек

import discord
import random
from discord.ext import commands
import asyncio
import socket
import smtplib
import datetime
import pyowm
import json
from datetime import timedelta
import os
from Cybernator import Paginator as pag
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json, socket, threading, time, concurrent.futures
from six.moves import urllib
from random import choice
import string
import requests
import pyshorteners

PREFIX = 'i.' # Переменная префикса

Bot = commands.Bot( command_prefix = PREFIX ) # Установка префикса бота
@Bot.remove_command('help') #Удаление стандартной комманды help

def get_random_string(length):
	letters = string.ascii_letters + string.digits
	result_str = ''.join(random.choice(letters) for i in range(length))
	return result_str

# При загрузке бота
@Bot.event
async def on_ready():
    activity = discord.Game(name = "Innuendo | i.help", url='https://twitch.com/zan4egpayne')
    await Bot.change_presence( status = discord.Status.online, activity = activity )
    print("Logged in as Innuendo!")
    print("Innuendo Copyright 2020 By Zan4eg#5557 and Kostya#3533")
    print("Бот запущен и готов к работе!")
    while True:
        await asyncio.sleep(8)
        await Bot.change_presence( status = discord.Status.online, activity = discord.Game(name = "i.help") )
        await asyncio.sleep(8)
        await Bot.change_presence( status = discord.Status.online, activity = discord.Activity(type = discord.ActivityType.watching, name = f"{len(Bot.guilds)} серверов!") )
        await asyncio.sleep(8)
        await Bot.change_presence( status = discord.Status.online, activity = discord.Streaming(name = "http://innuendo.ml/", url='https://twitch.com/zan4egpayne') )
	


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
    password = ''
    for i in range( lenght ):
        password += random.choice( chars )
    emb = discord.Embed( description=f'✅ Ваш пароль был сгенерирован и отправлен вам в лс!', colour=0x31f5f5 )
    em = discord.Embed( description=f'✅ Ваш пароль: {password}\n⚠️ Никому не показывайте этот пароль!', colour=0x31f5f5 )
    await ctx.send( embed = emb )
    await ctx.author.send( embed = em )
	
	
@Bot.command()
async def randcolor(ctx):
	await ctx.message.delete()
	random_number = random.randint(0,16777215)
	hex_number = str(hex(random_number))
	hex_number ='#'+ hex_number[2:]
	em = discord.Embed(title="Random Color Hex", description = f'Hex color: {hex_number}', color=random_number)
	await ctx.send(embed = em)
	log("Command randcolor executed.")
	
	
@Bot.command()
async def weather(ctx, city):
	await ctx.message.delete()
	owm = pyowm.OWM('a99967bc9ee70d5b4bd387902982f400', language = "RU")
	observation = owm.weather_at_place( city )
	w = observation.get_weather()
	temperature = w.get_temperature('celsius')['temp']
	await ctx.send( "В городе " + city + " сейчас " + str(temperature) + " градусов по Цельсию.\n" + "Погода: " + w.get_detailed_status() )
	
	

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
async def achievement( ctx, *, addition ):
    await ctx.message.delete()
    addition = addition.replace(" ", "+")
    url = f"https://minecraftskinstealer.com/achievement/2/New+advancement%21/{addition}"
    await ctx.send(url)
	

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

        
@Bot.command()
async def slot(ctx):
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
    АБВ = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
    message = await ctx.send(АБВ[0])
    await asyncio.sleep(2)
    for _next in АБВ[1:]:
        await message.edit(content=_next)
        await asyncio.sleep(2)

# Заварить ролтон
@Bot.command()
async def rolton( ctx ):
    emb = discord.Embed( title="Вы заварили Ролтон? Отличный выбор!", description="\n \n У вас получилось:", color=0x31f5f5 )
    emb.set_author( name='Ролтон', icon_url='https://cdn140.picsart.com/261815732025212.png?type=webp&to=min&r=640' )
    emb.set_image( url = 'https://pngimg.com/uploads/noodle/noodle_PNG59.png' )
    embed = discord.Embed( title="Инструкция", description="1. Откройте пачку ароматного Ролтона\n \n 2. Высыпите содержимое в тарелку \n \n 3. Залейте Ролтон кипятком \n \n 4. Накройте крышкой и подождите 4-5 минут \n \n 5. Наслаждайтесь вкусом вашего Ролтона", color=0x63009c )
    embed.set_author(name='Ролтон', icon_url='https://cdn140.picsart.com/261815732025212.png?type=webp&to=min&r=640')
    await ctx.send(embed = embed)
    await ctx.author.send(embed = emb)

@Bot.command()
@commands.has_permissions( administrator = True ) # Установка нужных прав для комманды
async def news(ctx, *, args):
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
	    port = int(port)
	    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	    sock.settimeout(1.0)
	    sock.connect((host, port))
	    getinfo = urllib.request.urlopen('https://api.mcsrvstat.us/2/' + host + ':' + str(port))
	    jsoninfo = json.loads(getinfo.read().decode('utf-8'))
	    await ctx.send(f'Айпи: ' + host + ':' + str(port) + '\nВерсия: {0} \nМотд: {1}'.format(jsoninfo['version'], jsoninfo['motd']['clean'][0]))
	    sock.close()

@Bot.command()
async def userpic(ctx, *, avamember: discord.Member):
    emb = discord.Embed(title = f"Аватар {avamember.name}", colour = 0x31f5f5)
    emb.set_image(url = avamember.avatar_url)
    await ctx.send(embed = emb)

@Bot.command()
async def botinfo(ctx):
    guilds = await Bot.fetch_guilds(limit = None).flatten()  
    emb = discord.Embed(title = "Статистика", colour = 0x31f5f5)
    emb.add_field(name = "Основная:", value = f"Серверов: **{len(guilds)}**\nУчастников: **{len(set(Bot.get_all_members()))}**")    # 1: Количество серверов, 2: количество уникальных участников на всех серверах
    emb.add_field(name = "Бот:", value = f"Задержка: **{int(Bot.latency * 1000)} мс**") # Скорость соединения бота с API дискорда
    await ctx.send(embed = emb)

@Bot.command()
async def emoji(ctx, emoji: discord.Emoji):
     emb = discord.Embed(title = f"{emoji.name}", colour = 0x31f5f5)
     emb.set_image(url = emoji.url)
     await ctx.send(embed = emb)

@Bot.command(pass_context=True,aliases=["кф","коин","коинфлип"])
async def coinflip(ctx,*,arg):
    if arg.lower() in ["орел","орёл","решка","р","о"]:
        ajkd=random.choice(["орел","решка"])
        if arg[0]=="о" and ajkd[0]=="о":
            await ctx.send(embed=discord.Embed(title="Победа!",description="Выпал орёл!",color=0x31f5f5))
        elif arg[0]=="р" and ajkd[0]=="р":
            await ctx.send(embed=discord.Embed(title="Победа!",description="Выпала решка!",color=0x31f5f5))
        elif arg[0]=="р" and ajkd[0]=="о":
            await ctx.send(embed=discord.Embed(title="Вы проиграли",description="Выпал орел",color=0x31f5f5))
        else:
            await ctx.send(embed=discord.Embed(title="Вы проиграли",description="Выпала решка",color=0x31f5f5))
    else:
        await ctx.send(embed=discord.Embed(title="Ошибка",description="Вы не указали на что ставите[орел,решка]",color=0x31f5f5))
	
@Bot.command(aliases=['geolocate', 'iptogeo', 'iptolocation', 'ip2geo', 'ip'])
async def geoip(ctx, *, ipaddr: str = '1.3.3.7'): # b'\xfc'
    await ctx.message.delete()
    r = requests.get(f'http://extreme-ip-lookup.com/json/{ipaddr}')
    geo = r.json()
    em = discord.Embed( colour= 0x31f5f5 )
    fields = [
        {'name': 'Айпи', 'value': geo['query']},
        {'name': 'Тип', 'value': geo['ipType']},
        {'name': 'Страна', 'value': geo['country']},
        {'name': 'Город', 'value': geo['city']},
        {'name': 'Континент', 'value': geo['continent']},
        {'name': 'Название', 'value': geo['ipName']},
        {'name': 'Интернет-провайдер', 'value': geo['isp']},
        {'name': 'Широта', 'value': geo['lat']},
        {'name': 'Долгота', 'value': geo['lon']},
        {'name': 'Org', 'value': geo['org']},
        {'name': 'Область', 'value': geo['region']},
        {'name': 'Статус', 'value': geo['status']},
    ]
    for field in fields:
        if field['value']:
            em.add_field(name=field['name'], value=field['value'], inline=True)
    return await ctx.send(embed=em)


@Bot.command()
async def tinyurl(ctx, url : str = None):
    if url is None:
        await ctx.send(embed = discord.Embed(
                title = "Укоротитель ссылок",
                description = "Ошибка | Укажите ссылку которую хотите укоротить",
                colour = 0x31f5f5
            ))
    else:
        shortener = pyshorteners.Shortener()
        short_url = shortener.tinyurl.short(url)
        await ctx.send("Ваша ссылка готова : " + short_url)
	

# Навигация по командам
@Bot.command( pass_context = True )
async def help( ctx, amount = 1 ):
    
    emb1=discord.Embed( title = 'Навигация по командам :pushpin:', colour= 0x31f5f5 )
    emb1.set_thumbnail( url='https://cdn.discordapp.com/attachments/724886353065803778/766295278927216670/e52a182a29690cf9.png' )
    emb1.add_field( name = '``{}info``'.format( PREFIX ), value = 'Информация об пользователе.' )
    emb1.add_field( name = '``{}stat``'.format( PREFIX ), value = 'Стистика каналов.' )
    emb1.add_field( name = '``{}serverinfo``'.format( PREFIX ), value = 'Информация о сервере.' )
    emb1.add_field( name = '``{}getip``'.format( PREFIX ), value= 'Получить айпи по домену.' )
    emb1.add_field( name = '``{}invite``'.format( PREFIX ), value= 'Пригласить бота на свой сервер.' )
    emb1.add_field( name = '``{}ping``'.format( PREFIX ), value= 'Узнать задержку бота.' )
    emb1.add_field( name = '``{}srvinfo``'.format( PREFIX ), value= 'Инфа о сервере майна.' )
    emb1.add_field( name = '``{}userpic``'.format( PREFIX ), value= 'Узнать аватар пользователя.' )
    emb1.add_field( name = '``{}botinfo``'.format( PREFIX ), value= 'Узнать статистику бота.' )
    emb1.add_field( name = '``{}weather``'.format( PREFIX ), value= 'Получить погоду.' )
    emb1.add_field( name = '``{}geoip``'.format( PREFIX ), value= 'Получить данные по айпи.' )
    emb1.add_field( name = '``{}tinyurl``'.format( PREFIX ), value= 'Укоротить ссылку.' )
    emb2=discord.Embed( title = 'Навигация по командам :pushpin:', colour= 0x31f5f5 )
    emb2.set_thumbnail( url='https://cdn.discordapp.com/attachments/724886353065803778/766295281406181437/1abb1364301a30c7.png' )
    emb2.add_field( name = '``{}clear``'.format( PREFIX ), value = 'Очистка чата.' )
    emb2.add_field( name = '``{}news``'.format( PREFIX ), value = 'Отправить всем в лс сообщение.' )
    emb2.add_field( name = '``{}ban``'.format( PREFIX ), value= 'Забанить пользователя.' )
    emb2.add_field( name = '``{}kick``'.format( PREFIX ), value= 'Кикнуть пользователя.' )
    emb3=discord.Embed( title = 'Навигация по командам :pushpin:', colour= 0x31f5f5 )
    emb3.set_thumbnail( url='https://cdn.discordapp.com/attachments/724886353065803778/766295277001768990/e2104f40da530197.png' )
    emb3.add_field( name = '``{}rolton``'.format( PREFIX ), value = 'Заварить ролтон.' )
    emb3.add_field( name = '``{}passgen``'.format( PREFIX ), value= 'Сгенерировать сложный пароль.' )
    emb3.add_field( name = '``{}slot``'.format( PREFIX ), value= 'Казино.' )
    emb3.add_field( name = '``{}abc``'.format( PREFIX ), value= 'Алфавит.' )
    emb3.add_field( name = '``{}mail``'.format( PREFIX ), value= 'Сообщение на почту.' )
    emb3.add_field( name = '``{}emoji``'.format( PREFIX ), value= 'Конвертировать емоджы в изображение.' )
    emb3.add_field( name = '``{}coinflip``'.format( PREFIX ), value= 'Подбросить монетку.' )
    emb3.add_field( name = '``{}randcolor``'.format( PREFIX ), value= 'Рандомный цвет.' )
    emb3.add_field( name = '``{}achievement``'.format( PREFIX ), value= 'Сделать кастомную ачивку.' )


    embeds = [emb1, emb2, emb3]

    message = await ctx.send(embed=emb1)
    page = pag(Bot, message, only=ctx.author, use_more=False, embeds=embeds)
    await page.start()



token = os.environ.get('BOT_TOKEN')
Bot.run( str(token) )
