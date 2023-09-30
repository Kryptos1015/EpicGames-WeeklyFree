from requests import get
import asyncio, discord
from discord.ext import commands

client = commands.Bot(command_prefix='-')

@client.event
async def on_ready():
    print('bot online')

free_games = {}
info_link = 'https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions'

# Finds the two weekly free games on the epic games store, then collects game info for the bot
def get_games_info():
    request = get(info_link).json()
    request = request['data']['Catalog']['searchStore']['elements']

    for game in request:
        original_price = game['price']['totalPrice']['originalPrice']
        discount = game['price']['totalPrice']['discount']

        # len of lists change, loop needs to be used to find game image
        if discount != 0 and discount == original_price:
            for image in game['keyImages']:
                if 'OfferImageWide' in image.values():
                    embed_image = image['url']

            # organizing all info neatly into dicts :DDD
            free_games[game['title']] = {'link': 'https://www.epicgames.com/store/p/' + game['urlSlug'],
                                        'description': game['description'],
                                        'start_date': game['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['startDate'],
                                        'end_date': game['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['endDate'],
                                        'image': embed_image}

def display_embeds():
    get_games_info()
    for game in free_games:
        embed = discord.Embed(title=game, url=free_games[game]['link'], description=free_games[game]['description'])
        embed.set_image(url=free_games[game]['image'])
        embed.set_footer(text='Start Date: ' + free_games[game]['start_date'].split('T')[0] + '\nEnd Date: ' + free_games[game]['end_date'].split('T')[0])
        return embed

@client.command()
async def show_games(ctx):
    await ctx.send('React with ✅ if interested, otherwise press ❎')

    embed = display_embeds()
    msg = await ctx.send(embed=embed)
    await msg.add_reaction('✅')
    await msg.add_reaction('❎')

@client.event
async def on_reaction_add(reaction, user):
    #check if reaction is from bot, dm embed
    if user != client.user and reaction.emoji == '✅':
        await user.send('Please download the game from the link below:')
        await user.send(embed=display_embeds())

        #while user does not send "stop" remind them to download game every hour
        while True:
            await user.send('Please download the game from the link below:')
            await user.send(embed=display_embeds())
            await asyncio.sleep(3600)

client.run('<key>')
