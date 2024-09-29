import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import yt_dlp
from googleapiclient.discovery import build

load_dotenv()

# 봇 인스턴스 생성
intents = discord.Intents.default()
intents.message_content = True  # 메시지 내용을 읽을 수 있도록 설정
bot = commands.Bot(command_prefix='!', intents=intents)

# YouTube API 설정
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def search_youtube(query):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=query,
        type="video"
    )
    response = request.execute()
    video_id = response['items'][0]['id']['videoId']
    video_title = response['items'][0]['snippet']['title']
    return video_id, video_title

# 봇이 준비되면 호출되는 이벤트
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# !p 명령어로 노래 제목 검색 및 재생
@bot.command()
async def p(ctx, *, search_query: str):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice_client = await channel.connect()

        # 유튜브에서 노래 제목 검색
        video_id, video_title = search_youtube(search_query)
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        # yt-dlp를 사용하여 유튜브 오디오 추출
        ydl_opts = {
            'format': 'bestaudio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'noplaylist': True,
            'extract_flat': True,
            'skip_download': True,
        }



        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            audio_url = info_dict['formats'][0]['url']

        # 디스코드 음성 채널에서 오디오 재생 (경로를 명시하지 않음)
        voice_client.play(discord.FFmpegPCMAudio(
            source=audio_url,
            before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -nostdin",
            options="-vn"
        ))

        await ctx.send(f"Now playing: {video_title}")

    else:
        await ctx.send("먼저 음성 채널에 들어가주세요.")

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
    if message.author == bot.user:
        return

    if message.content == '!ㅎㅇ':
        ctx = await bot.get_context(message)
        await hello(ctx)

    await bot.process_commands(message)

# 봇 실행
bot.run(os.getenv('DISCORD_KEY'))
