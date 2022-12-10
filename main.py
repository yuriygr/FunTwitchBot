from bot_settings import *
from some_data import *
from twitchio.ext import commands
from twitchio.user import User
from twitchio.channel import Channel

import time
import datetime
import random
import re
from bot_utilities import *

from gpiozero import CPUTemperature

class Bot(commands.Bot):

    #Инициализация бота
    def __init__(self):
        super().__init__(token=ACCESS_TOKEN, prefix=PREFIX, initial_channels=INITIAL_CHANNELS)

    #Событие готовности бота
    async def event_ready(self):
        print(f'Вошел как | {self.nick}')
        print(f'Id пользователя | {self.user_id}')

    #Обработка сообщений
    async def event_message(self, message):
        if message.echo:
            return
        print(f'{message.timestamp}({message.channel.name}){message.author.name}:{message.content}')
        
        if str(message.content).startswith(PREFIX):
            await self.handle_commands(message)
            return
        
        #Опускание мубота
        if message.author.name == 'moobot':
            await message.channel.send(f'@{message.author.name}, мубот соси')
            return

        #Приветствия и покатствия
        check_str = re.split(r',|!|;|\.|\?', message.content)[0]
        cust_com = custom_commands_with_tag.get(str(check_str.lower()))
        if(cust_com):
            await message.channel.send(f'@{message.author.name}, {random.choice(cust_com)}')
            return
        
        if(check_str in custom_copypast_cmd):
            await message.channel.send(check_str)
            return
            
        if(str(f'@{self.nick}') in str(message.content).lower()):
            await message.channel.send(f'@{message.author.name}, {random.choice(bot_messages)}')
            return
            
    #Информационные команды
    @commands.command(name='тг', aliases=['телеграм', 'телега', 'telegram', 'tg'])
    async def telegram(self, ctx: commands.Context):
        msg = telegrams.get(ctx.channel.name)
        if(not msg == None):
            await ctx.send(msg)
    
    @commands.command(name='вконтакте', aliases=['вк', 'vk', 'vkontakte'])
    async def vkontakte(self, ctx: commands.Context):
        msg = vks.get(ctx.channel.name)
        if(not msg == None):
            await ctx.send(msg)
            
    @commands.command(name='бусти', aliases=['boosty'])
    async def boosty(self, ctx: commands.Context):
        msg = boostys.get(ctx.channel.name)
        if(not msg == None):
            await ctx.send(msg)
            
    @commands.command(name='смайлы', aliases=['7tv', 'smiles', 'emoji', 'смайлики'])
    async def SpecialSmiles(self, ctx: commands.Context):
        if ctx.channel.name in ALLOW_URL:
            await ctx.send('Чтобы видеть и посылать крутые смайлы в чате устанавливайте расширение для браузера по ссылке: https://7tv.app/')
        
    @commands.command(name='help', aliases=['commands', 'команды', 'помощь'])
    async def help_bot(self, ctx: commands.Context):
        await ctx.send(f'@{ctx.author.name} Я бот и я ничего не умею 4Head')
        
    #Команды для белого списка 
    @commands.command(name='горячесть', aliases=['температура', 'темп', 'temp'])
    async def temperature(self, ctx: commands.Context):
        if ctx.author.name in white_list:
            cpuT = CPUTemperature()
            await ctx.send(f'Моя горячесть равна {cpuT.temperature} градусам')

    #Обработка исключений
    async def event_command_error(self, ctx, error: Exception) -> None:
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'Команда "{error.command.name}" заряжается, еще {int(error.retry_after)} сек.')
        else:
            print(error)
    
    #Событие подключения к чату
    async def event_join(self, channel: Channel, user: User):
        print(f'{datetime.datetime.now()}: Пользователь {user.name} вошел в чат {channel.name}')
        if channel.name == user.name:
            await channel.send(f'@{user.name}, привет стример! 😘')
            print(f'{datetime.datetime.now()}: Стример в чате {user.name}')

bot = Bot()
bot.run()
