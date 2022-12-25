import time
import re

from selenium import webdriver
from selenium.webdriver.common.by import By

def numara_bulucu (ilanbilgisi, numwords={}):
    if not numwords:
        rakamlar = [
        "sıfır", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz",
        "dokuz", "on",]

        onluk = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]

        yüzlük = ["yüz", "bin", "milyon", "milyar", "trilyon"]


        for idx, word in enumerate(rakamlar):   numwords[word] = (1, idx)
        for idx, word in enumerate(onluk):      numwords[word] = (1, idx * 10)
        for idx, word in enumerate(yüzlük):     numwords[word] = (10 ** (idx * 3 or 2), 0)

    ilanbilgisi = ilanbilgisi.replace('-', ' ')

    current = result = 0
    curstring = ""
    onnumber = False
    for word in ilanbilgisi.split():
        if word not in numwords:
            if onnumber:
                curstring += repr(result + current) + " "
            curstring += word + " "
            result = current = 0
            onnumber = False
        else:
            scale, increment = numwords[word]
            current = current * scale + increment
            if scale > 100:
                result += current
                current = 0
            onnumber = True

    if onnumber:
        curstring += repr(result + current)

    curstring = curstring.replace(" ","")
    curstring = curstring.replace("(","")
    curstring = curstring.replace(")", "")

    return curstring


driver = webdriver.Chrome('/usr/local/chromedriver')

driver.get("https://www.sahibinden.com/")
driver.get("https://www.sahibinden.com/")
driver.maximize_window()
driver.get("https://www.sahibinden.com/bmw-z-serisi-z4")
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, ".desktop").click()
driver.find_element(By.CSS_SELECTOR, "#onetrust-accept-btn-handler").click()
for x in range(1,23):
    ilanlar = "#searchResultsTable > tbody > tr:nth-child(" + str(x) + ")"
    w = driver.find_element(By.CSS_SELECTOR, ilanlar)
    if "TL" not in w.text:
        continue
    driver.find_element(By.CSS_SELECTOR, ilanlar).click()
    driver.execute_script("window.scrollTo(0,700)")
    time.sleep(2)
    ilan_detaylari = driver.find_element(By.CSS_SELECTOR, "#classified-detail")
    bulunan_numaralar = numara_bulucu(ilan_detaylari.text)
    numaralar10 = re.findall(r'[\d]{10}', bulunan_numaralar)
    numaralar11 = re.findall(r'[\d]{11}', bulunan_numaralar)
    if numaralar11:
        print(str(x) + ".) bulunan numaralar " + str(numaralar11))
    elif numaralar10:
        print(str(x) + ".) bulunan numaralar " + str(numaralar10))
    else:
        print(str(x) +".) ilanda Telefon numarası bulunamadı")
    time.sleep(3)
    driver.back()
    if x % 3 == 0:
        time.sleep(1)
        driver.execute_script("window.scrollTo(0," + str(x*100) + ")")
    time.sleep(1)
time.sleep(2)
driver.close()

