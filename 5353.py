from PIL import Image
from urllib.request import urlopen

url = "https://www.kinopoisk.ru/./images/film/7109.jpg"

image = Image.open(urlopen(url))
print(image)
image.show()