import json

with open('stop.json', 'r', encoding='UTF-8') as file:
    data = json.load(file)

data["stop"] = True

with open('stop.json', 'w', encoding='UTF-8') as file:
    json.dump(data, file, indent=4)

