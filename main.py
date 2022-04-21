from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import smtplib

path = 'C:\Program Files (x86)\chromedriver.exe'
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(path, options=options)

driver.get(
    'https://www.binance.com/en/futures-activity/leaderboard?type=myProfile&encryptedUid=8D27A8FA0C0A726CF01A7D11E0095577')

previousPrice = ""
previousRoe = ""


def send_email():
    gmailaddress = "test@example.com \n "
    gmailpassword = "test123* \n  "
    mailto = "test1@example.com \n"
    msg = "Bonjour Mr test1, \n \n  Il y a un changement de prix . \n Le dernier prix est : " + previousPrice + " \n Le nouveau prix est : " + price + " \n \n Le dernier taux est :" + previousRoe + " \n Le nouveau taux est : " + roe + " \n"
    try:
        mailServer = smtplib.SMTP('smtp.gmail.com', 587)
        mailServer.starttls()
        mailServer.login(gmailaddress, gmailpassword)
        mailServer.sendmail(gmailaddress, mailto, msg)
        print("Mail envoyé avec succès")
        mailServer.quit()
    except Exception as ex:
        print("Erreur lors de l'enboie du mail….", ex)


while True:
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'tab-MYPOSITIONS'))
        )
        element.click()
        link = []
        while True:
            try:
                link = driver.find_elements_by_xpath('//*[@id="__APP"]/div/div[2]/div[2]/div[7]/div/div[1]/div/div')
            except NoSuchElementException:
                continue
            if len(link[0].text.split('\n')) > 9:
                break
        price = link[0].text.split('\n')[9]
        roe = link[0].text.split('\n')[10].split(' ')[0]
        if (price != previousPrice) or (roe != previousRoe):
            print("Changement")
            send_email()
            previousPrice = price
            previousRoe = roe
    finally:
        driver.find_element_by_id('tab-MYPERFORMANCE').click()
        driver.find_element_by_id('tab-MYPOSITIONS').click()
        time.sleep(0.5)
