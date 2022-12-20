import discord
from random import *
from discord.ext import commands,tasks
from dotenv import load_dotenv
import requests
import re
import pandas as pd
import numpy as np

intents = discord.Intents.all()
intents.message_content=True
bot=discord.Client(intents=intents)
client = commands.Bot(command_prefix='daa.', intents=intents)
token = ''

@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    #Ruang turu 978448938430509067
    #Test serv 952848717952741386
    hai = ['hello','hai','hi','halo','ngikngok']
    sedih = ['sedih','sad','mengsad','mengsedih']
    print(f'{username}: {user_message} ({channel})')

    if message.author == client.user:
        pass

    if user_message.lower() == 'ping':
        await message.channel.send('pong! {0}ms'.format(round(client.latency,1)))
        return

    if user_message.lower() in hai:
        await message.channel.send(f'Halo {username}!')
        return

    if user_message.lower() == 'kamu siapa?':
        await message.channel.send('Aku bot untuk Final Project DAA!')
        return

    await client.process_commands(message)

@client.command()
async def jadwal(ctx):
    #Data jadwal
    df = pd.read_excel('E:\\Folder_apps\\NGODING\\Discord_bot\\Jadual Ganjil 2022-2023.xlsx',sheet_name='REGULER')
    df.rename(columns={'Jadual Kuliah Mata Kuliah Reguler Program Studi Informatika':'Jadual','Unnamed: 1' : 'KODE','Unnamed: 2' : 'MATA KULIAH','Unnamed: 3':'SKS','Unnamed: 11' : 'JADWAL B','Unnamed: 10' : 'JADWAL A','Unnamed: 12':'JADWAL C','Unnamed: 13':'JADWAL D','Unnamed: 14':'JADWAL E','Unnamed: 4' : 'Dosen A','Unnamed: 5':'Dosen B','Unnamed: 6':'Dosen C','Unnamed: 7' :'Dosen D','Unnamed: 8':'Dosen E'},inplace=True)
    df = df.loc[:,~df.columns.str.contains('^Unnamed')]
    dropindex = [int(x) for x in range(0,12)] + [int(x) for x in range(19,len(df))]
    df.drop(index=dropindex,inplace=True)
    df.drop(columns=['Jadual','KODE','SKS'],inplace=True)
    #Data jadwal fix

    #Data dosen
    datadosen = pd.read_excel('E:\\Folder_apps\\NGODING\\Discord_bot\\Jadual Ganjil 2022-2023.xlsx',sheet_name='DOSEN IF')
    datadosen.columns=datadosen.loc[2]
    datadosen=datadosen[3:28]
    datadosen.reset_index(drop=True,inplace=True)
    #Data dosen tersorting
    embed = discord.Embed(
        title='Jadwal Pelajaran IF\'2021',
        colour=discord.Colour.blue()
    )
    df.reset_index(inplace=True,drop=True)

    #Memisahkan jadwal2
    kelas = ['A','B','C','D','E']
    for x in kelas:
        for a,b in enumerate(df[f'Dosen {x}']):
            #memisahkan jadwal
            df.loc[a,f'JADWAL {x}'] = re.sub('/','|',df.loc[a,f'JADWAL {x}'])
            # print(b)
            #Mengganti kode dengan nama dosen
            for c,d in enumerate(datadosen['KODE']):
                # print(d,b)
                if(d==b): #kode ketemu yang sama
                    # print('found')
                    df.loc[a,f'Dosen {x}']=datadosen.loc[c,'NAMA'] #ganti ke nama

    #Priorities untuk sorting
    priorities = ['minggu','sabtu','jumat','kamis','rabu','selasa','senin']

    #Add field to discord embed
    for new in kelas:
        for x in range(1,len(df)):
            key = df[f'JADWAL {new}'].iloc[x].split()[0]
            check = x-1
            while(check>=0 and priorities.index(key.lower())>priorities.index(df[f'JADWAL {new}'].iloc[check].split()[0].lower())):
                b,c = df.iloc[check+1].copy(),df.iloc[check].copy()
                df.iloc[check+1],df.iloc[check]=c,b
                check-=1
        texter = ''
        date = ''
        for x,y,z in zip(df['MATA KULIAH'],df[f'Dosen {new}'],df[f'JADWAL {new}']):
            texter = texter + x + '\n'+ y.split(',')[0] + '\n' + '.'*50 + '\n'
            date = date + z + '\n.\n.\n'
        embed.add_field(name=f'KELAS {new}',value=texter,inline=True)
        # embed.add_field(name=f'KELAS {new}',value=df['MATA KULIAH'].to_string(index=False),inline=True)
        embed.add_field(name='JAM PELAJARAN',value=date,inline=True)
        # embed.add_field(name='JAM PELAJARAN',value=df[f'JADWAL {new}'].to_string(index=False),inline=True)
        embed.add_field(name='\u200b', value='\u200b')

    embed.set_author(name='by Kelompok 2',icon_url='https://cdn.discordapp.com/attachments/952898818767196202/1014169174320369704/Screenshot_2022-08-07_132626.png')
    await ctx.send(embed=embed)
    return
client.run(token)