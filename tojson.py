import json

data = {}
data['Hotels'] = []
data['Hotels'].append({
    'name':'',
    'price':'',
    'rating':'',
    'review':'',
    'img':'',
    'adress':'',
    'map_X':'',
    'map_Y':'',
    'Description':'',
    'facilities':''    
    })


with open('Hotel.json', 'w') as outfile:
    json.dump(data, outfile)



