import discord
from discord.ext import commands
from pytube import YouTube
import os
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
@client.event
async def ready_on():

    #這裡是機器人上線後預計會執行的程式
    print('目前登入身分', client.user)
    
    #也可以利用指令, 更改機器人目前在玩的遊戲
    game = discord.Game('幹python好難 網路複製最好用')
    await client.change_presence(status=discord.Status.idle, activity=game)

@client.command()
async def join(ctx):
    
    #這裡的指令會讓機器人進入call他的人所在的語音頻道
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if ctx.author.voice == None:
        await ctx.send("幹沒人阿")
    elif voice == None:
        voiceChannel = ctx.author.voice.channel
        await voiceChannel.connect()
    else:
        await ctx.send("準備撥放")
        
@client.command()
async def leave(ctx):
    
    #離開call他那個伺服器的所在頻道
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice == None:
        await ctx.send("掰掰")
    else:
        await voice.disconnect()
        
def endSong(path):

    #播放完後的步驟, 進行前一首歌刪除, 抓取一首清單內的歌進行播放
    os.remove(path)
    if len(playing_list) != 0:
        voice = discord.utils.get(client.voice_clients)
        url = playing_list[0]
        del playing_list[0]
        
        YouTube(url).streams.first().download()
        for file in os.listdir("./"):
            if file.endswith(".mp4"):
                os.rename(file,"song.mp4")
        
        voice.play(discord.FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe", source="song.mp4"),after = lambda x: endSong("song.mp4"))
playing_list = []
async def play(ctx, url :str = ""):
    
    #取得目前機器人狀態
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    
    #如果機器人正在播放音樂, 將音樂放入播放清單
    if voice.is_playing():
        playing_list.append(url)
        print(playing_list)
        await ctx.send("加入清單")
    
    #如果機器人沒在播放, 開始準備要播放的音樂
    else:
    
        #如果還有找到之前已經被播放過的音樂檔, 進行刪除
        song_there = os.path.isfile("song.mp4")
        
        try:
            if song_there:
                os.remove("song.mp4")
        except PermissionError:
            await ctx.send("等待目前播放的音樂結束或使用“停止”命令")
        
        #找尋輸入的Youtube連結, 將目標影片下載下來備用
        YouTube(url).streams.first().download()
        
        #將目標影片改名, 方便找到它
        for file in os.listdir("./"):
            if file.endswith(".mp4"):
                os.rename(file,"song.mp4")
        #找尋要播放的音樂並播放, 結束後依照after部分的程式進行後續步驟
        voice.play(discord.FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe", source="song.mp4"),after = lambda x: endSong("song.mp4"))

@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing")

@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not pause")

@client.command()
async def skip(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()




bot.run("MTE1MDMzMDk0Mjk1NTczMzAxNA.Gfr8W1.5NP5xAmnIsE-IZ1unWUAEudtRi0KvAhNXLJOJ0")