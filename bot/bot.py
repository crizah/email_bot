from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
import random
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from selenium.webdriver.chrome.service import Service
import smtplib
from webdriver_manager.chrome import ChromeDriverManager
import os
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options
import subprocess
from pathlib import Path



def driver():


    
    options = Options()
    options.add_argument("--headless=new") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    drv = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    # drv = webdriver.Chrome(options=options)

    drv.get("https://tenor.com/en-GB/search/silly-cat-gifs?format=memes")

    time.sleep(1)

    figs = drv.find_elements(By.CSS_SELECTOR, ".UniversalGifListItem.clickable")

    i = random.randint(0, len(figs)-1)
    chosen = figs[i]

    img = chosen.find_element(By.CSS_SELECTOR, "img")

    img_src = img.get_attribute("src")


    drv.quit()
    return img_src


def login(img_src, IMG_PATH):
    # filename = "img.png"   
    response = requests.get(img_src)

    print("downloaded")

    

    with open(IMG_PATH, "wb") as f:
        f.write(response.content)

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(os.getenv("EMAIL_ADDR"),os.getenv("APP_PASSWORD") )

    print("logged in")

    return smtp




def Message(subject = "Daily reminder", message= "", img=None):


    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg.attach(MIMEText(message))
   

    if img is not None:
        
        # Check whether we have the lists of images or not!
        if type(img) is not list:  
          
              # if it isn't a list, make it one
            img = [img] 

        # Now iterate through our list
        for one_img in img:
          
              # read the image binary data
            img_data = open(one_img, 'rb').read()  
            # Attach the image data to MIMEMultipart
            # using MIMEImage, we add the given filename use os.basename
            msg.attach(MIMEImage(img_data, name=os.path.basename(one_img)))
    return msg


def get_email():
    result = subprocess.run(
        ["git", "config", "--global", "user.email"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )

    email = result.stdout.strip()
    if not email:
        raise RuntimeError("Git email not set")
    return email


# def get_email():
#     result = subprocess.run(['git', 'config', '--global', 'user.email'], stdout=subprocess.PIPE)
#     result.stdout

#     ans = result.stdout.decode('utf-8')

#     return ans


def __main__():

    load_dotenv()
    BASE_DIR = Path(__file__).resolve().parent
    IMG_PATH = BASE_DIR/"img.png"

    img_src = driver()
    smtp = login(img_src=img_src, IMG_PATH=IMG_PATH)


    text = "You suck! but are also kinda awesome sauce. Dont cut your hair today, eat an appropriate amount of food, learn from ur mistakes, try. Kitty pix4u"
    
    msg = Message( message= text, img=str(IMG_PATH))
    
    send_to = get_email()

    to = [send_to]

    smtp.sendmail(from_addr=os.getenv("EMAIL_ADDR"),
              to_addrs=to, msg=msg.as_string())

    print("done")
    smtp.quit()





__main__()






