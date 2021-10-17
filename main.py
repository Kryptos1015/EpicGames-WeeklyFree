from requests import get
from webbrowser import open_new

free_games = []

def get_games():
    request = get('https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions').json()
    request = request['data']['Catalog']['searchStore']['elements']

    for game in request:
        if game['price']['totalPrice']['discount'] != 0:
            free_games.append('https://www.epicgames.com/store/p/' + game['urlSlug'])

print(free_games)