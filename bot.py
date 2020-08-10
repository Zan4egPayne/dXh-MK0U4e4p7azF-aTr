# Innuendo Copyright 2020 By Zan4eg#5557 and Kostya#3533
# Импорты библиотек

import discord
import random
from discord.ext import commands
import asyncio
import socket
import datetime
from datetime import timedelta
import requests


PREFIX = 'i.' # Переменная префикса

Bot = commands.Bot( command_prefix = PREFIX ) # Установка префикса бота
@Bot.remove_command('help') #Удаление стандартной комманды help

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
		await Bot.change_presence( status = discord.Status.online, activity = discord.Game(name = "Kostya#3533 | Zan4eg#5557") )
		await asyncio.sleep(8)
		await Bot.change_presence( status = discord.Status.online, activity = discord.Activity(type = discord.ActivityType.watching, name = f"{len(Bot.guilds)} серверов!") )
		await asyncio.sleep(8)
		await Bot.change_presence( status = discord.Status.online, activity = discord.Streaming(name = "Innuendo | i.help", url='https://twitch.com/zan4egpayne') )


# Глушим ошибки 
# @Bot.event
# async def on_command_error( ctx, error ):
# 	pass


# Информация о пользователе
@Bot.command( pass_context=True )
async def info(ctx, user: discord.Member):
	emb = discord.Embed( title="Информация об {}".format(user.name), colour=0x31f5f5 ) # Создаем ембед
	emb.add_field( name='Имя', value=user.name ) # Получаем имя пользователя
	emb.add_field( name='Присоединился', value=user.joined_at ) # Получаем присоедение пользователя
	emb.add_field( name='Айди', value=user.id ) # Получаем айди пользователя
	emb.set_thumbnail( url=user.avatar_url ) # Получаем аватар пользователя
	emb.set_author( name=Bot.user.name, url="https://discord.com/api/oauth2/authorize?client_id=725379044845027329&permissions=8&scope=bot" ) # Приглашение бота себе на сервер
	emb.set_footer( text="Вызвано: {}".format(user.name) ) # Получаем имя пользователя и его аву (опять же)
	await ctx.send( embed = emb )

# Пригласить бота на свой сервер
@Bot.command()
async def invite ( ctx ):
	emb = discord.Embed( title='Пригласить бота на свой сервер.', colour=0x31f5f5)
	emb.set_footer( text="Ссылка была отправлена в лс." )
	emb.set_author( name=Bot.user.name, url="https://discord.com/api/oauth2/authorize?client_id=725379044845027329&permissions=8&scope=bot" )
	await ctx.send( embed = emb )
	await ctx.author.send ('https://discord.com/api/oauth2/authorize?client_id=725379044845027329&permissions=8&scope=bot')



# Очистка сообщений
@Bot.command( pass_context = True )
@commands.has_permissions( administrator = True ) # Установка нужных прав для комманды
async def clear ( ctx, amount : int ):  # Создание комманды/функции
	await ctx.message.delete() # Удаление сообщения с коммандой
	await ctx.channel.purge( limit = amount ) # Сама очистка
	emb = discord.Embed( description=f'✅  Очищено {amount} сообщений!', colour=0x31f5f5 ) # Создание отчета об очистке
	await ctx.send( embed = emb )

# Задаем параметры ошибки
@clear.error
async def clear_error( ctx, error ):
	if isinstance( error, commands.MissingRequiredArgument ):
		await ctx.send( f'⚠️ {ctx.author.mention} укажите аргумент!' )

	if isinstance( error, commands.MissingPermissions ):
		await ctx.send( f'🛑 {ctx.author.mention} у вас недостаточно прав!' ) 



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
async def getip( ctx, host ):
	ip = socket.gethostbyname( host )
	await ctx.send( ip )

# Порт сканнер

# async def scan_port( ip, port ):
# 	client = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
#	if client.connect_ex( ( ip, port ) ):
#		await ctx.send( f'Порт {port} закрыт!' )
#	else:
#	await ctx.send( f'Порт {port} открыт!' )

@Bot.command()
async def portscan( ctx, ip, port):
	portzhigovne = int( port )
	ip = socket.gethostbyname("unixgo.ru")
	for i in range(81):
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		if client.connect_ex((ip, port)):
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

@Bot.listen()
async def on_message(message : discord.Message):
    if Bot.user.mentioned_in(message):
        await message.channel.send(':sleeping: | Ты меня разбудил :( . Мой префикс `i.` , чтобы узнать список команд напиши `i.help`', delete_after=10)
  
@commands.cooldown(1, 5, commands.BucketType.user)
@Bot.command()
async def respect(ctx):
    em = discord.Embed(title="".format(ctx.guild.name), description="", color=0x31f5f5)
    em.set_author(name="")
    em.add_field(name=f"{ctx.author.name}", value='Press :regional_indicator_f: to pay respect', inline=True)
    msg = await ctx.send(embed=em)
    await msg.add_reaction('\N{regional indicator symbol letter f}')

@commands.cooldown(1, 5, commands.BucketType.user)
@Bot.command(name='8ball')
async def l8ball(ctx):
    await ctx.send(random.choice(['✨ Несомненно.', '✨ Определенно да.', '✨ Без сомнения.', '✨ Да - определенно.', '✨ Вы можете положиться на это', '✨ На мой взгляд, да . ',' ✨ Скорее всего. ',' ✨ Да. ',' ✨ Знаки указывают на то, что да. ',' ✨ Ответ туманный, повторите попытку ',' ✨ Спросить еще раз, позже. ',' ✨ Лучше не говорить тебе сейчас. ',' ✨ Не могу предсказать. ',' ✨ Сконцентрируйся и спроси еще раз. ',' ✨ Не рассчитывай на это. ',' ✨ Мой ответ - нет. ','✨ Перспективы не очень хорошие.','✨ Очень сомнительно.' ]))

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

# Рандомное фото или гиф гуся
@Bot.command()
async def duck( ctx ):
	await ctx.message.delete()
	r = requests.get('https://random-d.uk/api/random').json()
	em = discord.Embed( title="Рандомное фото или гифка гуся", color=0x63009c )
	em.set_image(url=r["url"])
	try:
		await ctx.send(embed=em)
	except:
		await ctx.send(r['url'])


# Заварить ролтон
@Bot.command()
async def rolton( ctx ):
	await ctx.message.delete()
	emb = discord.Embed( title="Вы заварили Ролтон? Отличный выбор!", description="\n \n У вас получилось:", color=0x63009c )
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
    em = discord.Embed( description=f'USD: `{str(usd)}$`\nEUR: `{str(eur)}€`', colour= 0x63009c )
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
    em = discord.Embed( description=f'USD: `{str(usd)}$`\nEUR: `{str(eur)}€`', colour= 0x63009c )
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

# Навигация по командам
@Bot.command( pass_context = True )
async def help( ctx, amount = 1 ):
	await ctx.channel.purge( limit = amount )

	emb=discord.Embed( title = 'Навигация по командам :pushpin:', colour= 0x31f5f5 )

	emb.add_field( name = '{}info'.format( PREFIX ), value = 'Информация об пользователе.' )
	emb.add_field( name = '{}clear'.format( PREFIX ), value = 'Очистка чата.' )
	emb.add_field( name = '{}stat'.format( PREFIX ), value = 'Стистика каналов.' )
	emb.add_field( name = '{}serverinfo'.format( PREFIX ), value = 'Информация о сервере.' )
	emb.add_field( name = '{}btc'.format( PREFIX ), value = 'Узнать курс биткойна.' )
	emb.add_field( name = '{}eth'.format( PREFIX ), value = 'Узнать курс ефириума.' )
	emb.add_field( name = '{}fox'.format( PREFIX ), value = 'Рандомное фото лисы.' )
	emb.add_field( name = '{}duck'.format( PREFIX ), value = 'Рандомное фото гуся.' )
	emb.add_field( name = '{}rolton'.format( PREFIX ), value = 'Заварить ролтон.' )
	emb.add_field( name = '{}news'.format( PREFIX ), value = 'Отправить всем в лс сообщение.' )
	emb.add_field( name = '{}passgen'.format( PREFIX ), value= 'Сгенерировать сложный пароль.' )
	emb.add_field( name = '{}getip'.format( PREFIX ), value= 'Получить айпи по домену.' )
	emb.add_field( name = '{}invite'.format( PREFIX ), value= 'Пригласить бота на свой сервер.' )
	emb.add_field( name = '{}ban'.format( PREFIX ), value= 'Забанить пользователя.' )
	emb.add_field( name = '{}kick'.format( PREFIX ), value= 'Кикнуть пользователя.' )
	emb.add_field( name = '{}respect'.format( PREFIX ), value= 'Получить респект.' )
	emb.add_field( name = '{}8ball'.format( PREFIX ), value= 'Шар предсказаний.' )
	emb.add_field( name = '{}ping'.format( PREFIX ), value= 'Узнать задержку бота.' )
	emb.set_footer( text = 'Всего команд: 18' )


	await ctx.send( embed = emb )

Bot.run("NzI1Mzc5MDQ0ODQ1MDI3MzI5.XvN34Q.m7rtItnXfGFer0k6f6-xVws2rxk")