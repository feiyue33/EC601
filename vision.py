import io
import os
from PIL import Image, ImageDraw, ImageFont
import glob

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()

path = './'
filelist = os.listdir(path)
total_num = len(filelist)

for file in filelist:
    if file.endswith('.jpg'):

    # The name of the image file to annotate
    # file_name = os.path.join(os.path.dirname(__file__), './pic1.jpg')

        # Loads the image into memory
        with io.open(file, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)

        # Performs label detection on the image file
        response = client.label_detection(image=image)
        labels = response.label_annotations

        # Add label to image

        img = Image.open(file)
        draw = ImageDraw.Draw(img)
        ttfront = ImageFont.truetype("/Library/Fonts/Arial.ttf", 24)
        # print(file)
        # print('Labels:')
        description = ''
        for label in labels:
            # print(label.description)
            description += str(label.description)+'\n'
        # print(description)
        height = img.size
        color = "#ffffff"
        draw.text((100, 40), description, fill=color, font=ttfront)
        img.save(file)
