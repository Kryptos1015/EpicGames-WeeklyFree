from requests import get
from webbrowser import open_new

free_games = {}
info_link = 'https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions'

# finds the 2 weekly free games, collects game info for bot
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


get_games_info()
