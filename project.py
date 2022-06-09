import requests
import pymongo
from tqdm import tqdm

# configure database access
db = pymongo.MongoClient()["starwars"]
starships, characters = db["starship"], db["characters"]
link_2_id = {}


def get_api_data(url, key):
    data = requests.get(url).json()
    return data[key]


def change_starship_pilot_link_to_id(data):
    new_starships = []
    for starship in tqdm(data):
        new_starships.append(pilot_link_to_id(starship))
    return new_starships


def pilot_link_to_id(starship):
    link_to_id = update_dictionary(starship)
    for index, pilot_link in enumerate(starship["pilots"]):
        starship["pilots"][index] = link_to_id[pilot_link]
    return starship


def update_dictionary(starship):
    global link_2_id
    for pilot_link in starship["pilots"]:
        if pilot_link not in link_2_id:
            name = get_api_data(pilot_link, "name")
            link_2_id[pilot_link] = get_id_of_name(name)
    return link_2_id


def get_id_of_name(n):
    return characters.find_one({"name": n}, {"_id": 1})["_id"]


def view_data(data, options):
    for i, v in enumerate(data):
        for opt in options:
            print(f"{opt:<7}= {v[opt]}")
        print("\n", end="")


# MAIN

api_data = get_api_data("https://swapi.dev/api/starships", "results")
starship_list = change_starship_pilot_link_to_id(api_data)

# Clean the starship database first, then insert
starships.drop()
starships.insert_many(starship_list)

view_data(starship_list, options=["name", "pilots"])
