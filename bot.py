import discord
import os
from dotenv import load_dotenv

import sql_database as sqldb


load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
GUILD = os.getenv('GUILD_NAME')
OWNER = os.getenv('OWNER_ID')


client = discord.Client()

# Laver embed af beskeden.
def makeEmbed(titel, navn, frist, elevtid):
    embed = discord.Embed(title=titel, color=discord.Color.red())
    embed.add_field(name="Navn:", value=navn, inline=True)
    embed.add_field(name="Frist:", value=frist, inline=True)
    embed.add_field(name="Elevtid:", value=elevtid, inline=True)
    embed.set_thumbnail(url="https://lectio.plus/images/OG_logo.png")
    embed.set_footer(text="Bot lavet af: Oliver D.", icon_url="https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/avatars/75/7577f213defbf688b945e6f3a93486e78a23d0c3_full.jpg")
    embed.set_author(name="TheFlowDK", url="https://steamcommunity.com/id/TheFlowDKK/", icon_url="https://cdn.discordapp.com/avatars/245792114745540610/88447856c0f0e1505d00bab466fc5467.png?size=128")
    return embed



@client.event
async def on_ready():
    for guild in client.guilds:
        #print(guild.name, guild.id)
        if guild.name == GUILD:
            break
        else:
            print("Noget gik galt...")
            print("Din .env fil er muligvis ikke opsat korrekt.")
            input()
            exit()
    
    print(
        f"{client.user} aktiv! (User-ID: {client.user.id}) \n"
        f"Guild: {guild.name} (Guild-ID: {guild.id})"
        )


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!lektier'):
        try:
            count = message.content.split("!lektier ",1)[1]
        except:
            lektier = sqldb.showNext(1)
            embed = makeEmbed("Næste lektie", f'{lektier[0][0]}', f'{lektier[0][1].strftime("%H:%M %d/%m/%Y")}', f'{lektier[0][2]}')
            await message.channel.send(embed=embed)
            return

        lektier = sqldb.showNext(int(count))
        navn = ""
        frist = ""
        elevtid = ""
        #besked = ""
        for x in range(len(lektier)):
            if len(lektier[x][0]) > 35:
                navn += f'{lektier[x][0][:32]}...\n'
            else:
                navn += f'{lektier[x][0]}\n'
            frist += f'{lektier[x][1].strftime("%H:%M %d/%m/%Y")}\n'
            elevtid += f'{lektier[x][2]}\n'
            #besked += (f'{lektier[x][0]} {lektier[x][1].strftime("%H:%M %d/%m/%Y")} {lektier[x][2]}\n')
        embed = makeEmbed(f"Næste {len(lektier)} lektier", navn, frist, elevtid)
        await message.channel.send(embed=embed)
    

    if message.content.startswith('!updatedb') and message.author.id == int(OWNER):
        sqldb.uploadToTable()
        sqldb.deleteOld()
        await message.channel.send(f'Database opdateret...')
    elif message.content.startswith('!updatedb') and message.author.id != int(OWNER):
        await message.channel.send(f'Mangler tilladelse...')


client.run(TOKEN)