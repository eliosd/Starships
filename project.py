import requests
import pymongo
from tqdm import tqdm

# configure database access
client = pymongo.MongoClient()
db = client["starwars"]
stars = db["starship"]
characters = db["characters"]


def extract_api_data(url):
    get_request = requests.get(url)
    data = get_request.json()
    return data


def change_pilot_links_to_names(data):
    new_stars = []
    name_2_id = generate_name_id()
    link_2_id = {}

    for index, star_obj in enumerate(tqdm(data["results"])):
        for pilot_link in star_obj["pilots"]:
            if pilot_link not in link_2_id:
                name = pilot_link_to_name(pilot_link)
                link_2_id[pilot_link] = name_2_id[name]

        # change pilot links to id, hence add to list
        star_obj = map_pilot_link_2_id(star_obj, link_2_id)
        new_stars.append(star_obj)
    return new_stars


def pilot_link_to_name(link):
    data = extract_api_data(link)
    return data["name"]


def generate_name_id():
    translation = {}
    for c in characters.find():
        translation[c["name"]] = c["_id"]
    return translation


def map_pilot_link_2_id(star_list, link_to_name):
    for index_pilot, pilot_link in enumerate(star_list["pilots"]):
        pilot_id = link_to_name[pilot_link]
        star_list["pilots"][index_pilot] = pilot_id
    return star_list


def view_data(data, options=None):
    if options:
        for i, v in enumerate(data):
            for opt in options:
                print(f"{opt:<7}= {v[opt]}")
            print("\n", end="")
    else:
        for i in data:
            print(i, end="\n\n")


# MAIN

starship_api_data = extract_api_data("https://swapi.dev/api/starships")
starship_list = change_pilot_links_to_names(starship_api_data)

# Clean the starship database first, then insert
stars.drop()
stars.insert_many(starship_list)

view_data(starship_list, options=["name", "pilots"])
