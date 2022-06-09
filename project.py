import requests
import pymongo

# configure database access
client = pymongo.MongoClient()
db = client["starwars"]
stars = db["starship"]
characters = db["characters"]


def get_api_data(url):
    get_request = requests.get(url)
    data = get_request.json()
    return data


def extract_from_api_data(data):
    return_list = []
    translation = {}
    for index, starship_item in enumerate(data["results"]):
        for pilot_link in starship_item["pilots"]:
            translation[pilot_link] = pilot_url_to_name(pilot_link)
        return_list.append(starship_item)
    return return_list, translation


def pilot_url_to_name(link):
    data = get_api_data(link)
    return data["name"]


def generate_name_id():
    translation = {}
    for c in characters.find():
        translation[c["name"]] = c["_id"]
    return translation


def starship_pilot_to_id(star_list, link_to_name, name_to_id):
    for index_star, starship in enumerate(star_list):
        for index_pilot, pilot_link in enumerate(starship["pilots"]):
            pilot_name = link_to_name[pilot_link]
            pilot_id = name_to_id[pilot_name]
            star_list[index_star]["pilots"][index_pilot] = pilot_id
    return star_list


def view_data(data):
    for i in data:
        print(i, end="\n\n")


# MAIN

starship_api_data = get_api_data("https://swapi.dev/api/starships")
starship_list, link_2_name = extract_from_api_data(starship_api_data)
name_2_id = generate_name_id()
starship_list = starship_pilot_to_id(starship_list, link_2_name, name_2_id)


# Clean the starship database first, then insert
stars.drop()
stars.insert_many(starship_list)


view_data(starship_list)

