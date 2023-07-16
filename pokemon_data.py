# TO CREATE A DATABASE, SO NEED TO FETCH DATA ONINE ALL THE TIME AND SPEED UP !

# getting requests
import requests
import pandas as pd

url='https://pokeapi.co/api/v2/pokemon/'

pokemon = []
for ctr in range(1,1001):
    pokemon_info = requests.get(url+str(ctr)+'/').json()
    names = pokemon_info['forms'][0]['name']
    image_url = pokemon_info['sprites']['other']['official-artwork']['front_default']
    moves = [m['move']['name'] for m in pokemon_info['moves'][:5]]
    types = [t['type']['name'] for t in pokemon_info['types'][:5]]
    pokemon.append({'name':names, 'img':image_url, 'type':types, 'moves':moves})

pokedf = pd.DataFrame(pokemon)
pokedb = pokedf.to_csv('poke_db.csv')