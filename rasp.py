from pdf2jpg import pdf2jpg
import requests
import hashlib
import urllib.request
import time

url = 'http://rasp.kolledgsvyazi.ru/npo.pdf'

def downloads():
    urllib.request.urlretrieve(url, "npo.pdf")
    pdf2jpg.convert_pdf2jpg("npo.pdf", "", pages="ALL")

old_hash = 1
while True:
    path = requests.get(url).text
    hash_object = hashlib.md5(path.encode('utf-8')).hexdigest()
    print(hash_object)
    if hash_object != old_hash:
        print("Расписание обновлено!")
        old_hash = hash_object
        downloads()
    else:
        pass
    time.sleep(300)