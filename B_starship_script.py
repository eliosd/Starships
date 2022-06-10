import pymongo
import requests

client = pymongo.MongoClient()
db = client['starwars']

starships_data = requests.get('https://swapi.dev/api/starships').json()['results']


def drop_keys(starship_dict):
    for data in starship_dict:
        data.pop('edited')
        data.pop('url')
        data.pop('created')


def get_pilot_names(starship_dict):
    for starship in range(len(starship_dict)):
        if len(starship_dict[starship]['pilots']) > 0:
            for pilot in range(len(starship_dict[starship]['pilots'])):
                pilot_data = requests.get(starship_dict[starship]['pilots'][pilot]).json()
                starship_dict[starship]['pilots'][pilot] = pilot_data['name']


def get_object_id_pilots(starship_dict):
    pilot_ids = []
    for starship in starship_dict:
        current_ship = []
        for pilots in starship['pilots']:
            object_id = db.characters.find_one({'name': pilots}, {'id': 1})['_id']
            current_ship.append(object_id)
        pilot_ids.append(current_ship)
    return pilot_ids


def link_id_pilots(starship_dict, id_list):
    for index in range(len(starship_dict)):
        starship_dict[index]['pilots'] = id_list[index]


def push_starship_collection(starships_dict):
    db.starships.drop()
    db.starships.insert_many(starships_dict)


def lookup_starships_db():
    star = db.starships.aggregate(
        [{'$lookup': {'from': "characters", 'localField': "pilots", 'foreignField': "_id", 'as': "matched_pilot"}}])

    for i in star:
        if len(i['matched_pilot']) > 0:
            for k in i['matched_pilot']:
                print('Pilot:', k['name'], ' Starship:', i['name'])


drop_keys(starships_data)
get_pilot_names(starships_data)
link_id_pilots(starships_data, get_object_id_pilots(starships_data))
push_starship_collection(starships_data)
lookup_starships_db()

# def get_film_names(starship_dict):
#     for starship in range(len(starship_dict)):
#         if len(starship_dict[starship]['films']) > 0:
#             for film in range(len(starship_dict[starship]['films'])):
#                 film_data = requests.get(starship_dict[starship]['films'][film]).json()
#                 starship_dict[starship]['films'][film] = film_data['title']

# def get_object_id_films(starship_dict):
#     film_ids = []
#     for starship in starship_dict:
#         current_ship = []
#         for films in starship['films']:
#             print(films)
#             # object_id = db.characters.find_one({'name': films}, {'id': 1})['_id']
#             # current_ship.append(object_id)
#         # film_ids.append(current_ship)
#     print(film_ids)
#     return film_ids

# def link_id_films(starship_dict, id_list):
#     for index in range(len(starship_dict)):
#         starship_dict[index]['films'] = id_list[index]
