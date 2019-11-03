import json
from pprint import pprint

def getData(path):
    f = open(path, "r")
    lines = []
    imageData = {}

    for i, line in enumerate(f):
        formatted = json.loads(line)

        waterImages = formatted['water']
        peopleImages = formatted['people']
        buildingImages = formatted['buildings']
        

        
    return waterImages, peopleImages, buildingImages

    
t, y, u = getData('data.txt')
print(t)