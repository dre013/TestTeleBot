import requests
import os

def getMediagroup():
    os.makedirs('media', exist_ok=True)
    with open('PhotoLinks.txt', 'r') as file:
        counter = 0
        for link in file:
            req = requests.get(link)
            out = open(f'media/img{counter}.jpg', 'wb')
            out.write(req.content)
            out.close()
            counter += 1