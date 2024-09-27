import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

# 봇 인스턴스 생성
intents = discord.Intents.default()
intents.message_content = True  # 메시지 내용을 읽을 수 있도록 설정
bot = commands.Bot(command_prefix='!', intents=intents)

# 봇이 준비되면 호출되는 이벤트
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# 간단한 명령어 정의
@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')
    
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def repeat(ctx, *, message: str):
    await ctx.send(message)
    
# on_message 이벤트로 메시지 감지
@bot.event
async def on_message(message):
    # 봇의 메시지는 무시
    if message.author == bot.user:
        return

    # '!ㅎㅇ' 메시지를 감지하여 hello 명령어 실행
    if message.content == '!ㅎㅇ':
        # 해당 메시지의 컨텍스트 가져오기
        ctx = await bot.get_context(message)
        await hello(ctx)  # hello 명령어 실행

    # 명령어 처리를 위해 on_message 안에서도 명령어가 작동하게 함
    await bot.process_commands(message)    


# 봇 실행
bot.run(os.getenv('DISCORD_KEY'))
