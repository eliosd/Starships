import requests
import pymongo

client = pymongo.MongoClient()
db = client["starwars"]
stars = db["starship"]
characters = db["characters"]

x = requests.get("https://swapi.dev/api/starships")

# x = requests.post(
#     url="https://api/starships"
#     headers=headers,
#     data=json.dumps(body)
#     )

pcs = x.json()

# print(len(pcs["results"][0]))
print(pcs["results"][0])

pilot_list = []
starship_list = []
comb = []
raw = []
translate = {}

for i in range(len(pcs["results"]) - 1):
    print(i, pcs["results"][i]["pilots"])
    for j in pcs["results"][i]["pilots"]:
        pilot_list.append(j)
        starship_list.append(pcs["results"][i]["name"])
    raw.append(pcs["results"][i])

# print(len(pilot_list), pilot_list, sep="\n")

for i, v in enumerate(pilot_list):
    x = requests.get(v)
    pcs = x.json()
    print(starship_list[i], pcs["name"], sep="\n", end="\n\n")
    translate[v] = pcs["name"]

a = db.starship.find()

# for i in raw:
#     print(i, sep="\n\n")

translate2 = {}
for c in characters.find():
    # print(c["name"], c["_id"])
    translate2[c["name"]] = c["_id"]
print(translate2)

for i, v in enumerate(raw):
    for j, v2 in enumerate(raw[i]["pilots"]):
        try:
            raw[i]["pilots"][j] = translate[raw[i]["pilots"][j]]
        except:
            print("f")
            pass
        # print(raw[i]["pilots"])
        # print(raw[i]["pilots"][j], translate[raw[i]["pilots"][j]])
    # print(i, v, translate[raw[0]["pilots"][0]], sep="\n", end="\n\n")
# print(translate[raw[0]["pilots"][0]])

# print(raw[0]["pilots"])
# print(translate)
# for i in raw:
#     print(i["pilots"])

# for i in raw:
#     print(i, end="\n\n")

# print(translate)

# for i in x.text:
#     print(i, end="")

# for i, v in enumerate(raw):
#     raw[i]["_id"] = i
# for i in raw:
#     print(i, end="\n\n")

# for j in raw:
stars.drop()
stars.insert_many(raw)

# print(type(raw), type(raw[0]))
# for i in raw:
#     print(i, sep="\n\n")


