import requests
from pprint import pprint
import json
import shutil

import os
import json
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import TextRecognitionMode
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import sys
import time
import cv2


def analyzeImage(image_path):
    os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY'] = "ceb12c15a400458eb6884a6dc119986b"
    os.environ['COMPUTER_VISION_ENDPOINT'] = "https://deanhaleem.cognitiveservices.azure.com/"

    # Add your Computer Vision subscription key and endpoint to your environment variables.
    if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
        subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
    else:
        print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
        sys.exit()

    if 'COMPUTER_VISION_ENDPOINT' in os.environ:
        endpoint = os.environ['COMPUTER_VISION_ENDPOINT']

    analyze_url = endpoint + "vision/v2.1/analyze"

    
    # Set image_path to the local path of an image that you want to analyze.
    # image_path = url

    # Read the image into a byte array
    image_data = open(image_path, "rb").read()
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
            'Content-Type': 'application/octet-stream'}
    params = {'visualFeatures': 'Categories,Description,Color'}
    response = requests.post(
        analyze_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()

    # The 'analysis' object contains various fields that describe the image. The most
    # relevant caption for the image is obtained from the 'description' property.
    analysis = response.json()
    # return analysis['description']['captions'][0]['text']
    return analysis







subReddits = ['Photography', 'ITookAPictures']
headers = {'Content-Type': 'application/json', 'Accept':'application/json', 'User-agent': 'bleepbleep'}

params = {
    'count': '1',
    't':'all'
}

subredditNames = []
response = requests.get('https://www.reddit.com/r/travelphotos/top/.json', headers = headers, params=params)



rawdata = response.json()

data = rawdata['data']['children']

dataPath = 'data.txt'
organizedData = {}
waterImages = []
natureImages = []
buildingImages = []
for i, obj in enumerate(data):
    image_url = obj['data']['url']
    res = requests.get(image_url, stream=True)
    
    #
    path = os.path.join('./redditImages/',str(i)+'.jpg')

    
    with open (path, 'wb') as f:
        res.raw.decode_content = True
        imgdata = res.raw
        shutil.copyfileobj(res.raw, f)
        
        analysis = analyzeImage(path)
        # print(analysis)
        tags = analysis['description']['tags']
        for tag in tags:
            print(tag)
            if tag == 'water':
                waterImages.append(path)
            if tag in ['nature', 'mountain', 'rocky', 'hill', 'green', 'tree', 'nature']:
                natureImages.append(path)
            if tag == 'building':
                buildingImages.append(path)
        print("success")
            

# print(waterImages)  
organizedData['water'] = waterImages
organizedData['nature'] = natureImages
organizedData['buildings'] = buildingImages
print(organizedData)

with open('data.txt', 'w') as f:

    json.dump(organizedData, f)
    f.write('\n')
