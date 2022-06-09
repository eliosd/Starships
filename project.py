import requests
import pymongo
from tqdm import tqdm

# configure database access
db = pymongo.MongoClient()["starwars"]
starships, characters = db["starship"], db["characters"]


def get_api_data(url, key):
    data = requests.get(url).json()
    return data[key]


def change_pilot_links_to_names(data):
    new_starships = []
    link_2_id = {}

    # update pilot/id translations, hence modify starship to use name
    for i, starship in enumerate(tqdm(data)):
        link_2_id = update_dictionary(starship, link_2_id)
        starship = map_pilot_link_2_id(starship, link_2_id)
        new_starships.append(starship)
    return new_starships


def update_dictionary(starship, link_2_id):
    for pilot_link in starship["pilots"]:
        if pilot_link not in link_2_id:
            name = get_api_data(pilot_link, "name")
            link_2_id[pilot_link] = get_id_of_name(name)
    return link_2_id


def get_id_of_name(n):
    return characters.find_one({"name": n}, {"_id": 1})["_id"]


def map_pilot_link_2_id(star_list, link_to_name):
    for index_pilot, pilot_link in enumerate(star_list["pilots"]):
        pilot_id = link_to_name[pilot_link]
        star_list["pilots"][index_pilot] = pilot_id
    return star_list


def view_data(data, options):
    for i, v in enumerate(data):
        for opt in options:
            print(f"{opt:<7}= {v[opt]}")
        print("\n", end="")


# MAIN

api_date = get_api_data("https://swapi.dev/api/starships", "results")
starship_list = change_pilot_links_to_names(api_date)

# Clean the starship database first, then insert
starships.drop()
starships.insert_many(starship_list)

view_data(starship_list, options=["name", "pilots"])
