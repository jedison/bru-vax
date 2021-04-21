#!/usr/bin/env python

import selenium
import re
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

REQUEST_URL = "https://bruvax.brussels.doctena.be/"
NISS = "67112602401" # "66120251324"
ZIP = "1040"
WAITLIST = "ajouter sur la liste d"
CENTERS = ["Pacheco", "Heysel", "Woluwe-Saint-Pierre", "Schaerbeek", "Molenbeek", "Forest", "Anderlecht  RSCA", "Woluwe-Saint-Lambert", "Uccle", "Hôpital Militaire"]
FIRSTNAME = "Isabelle" #"Jeffrey"
LASTNAME = "Willot" # "Edison"
EMAIL = "isabelle.willot@levif.be" # "jeffrey.edison@gmail.com"
MOBILE = "0495537423" # "0476409605"

def startBrowser( ):
    print("starting webdriver")
    # Using Chrome to access web
    global driver
    options = webdriver.ChromeOptions()
    options.add_argument("disable-infobars");
    options.add_argument("--start-maximized");
    options.add_argument("--no-sandbox");
    options.add_argument("--disable-dev-shm-usage");
    # keep "head" until this works
    # options.add_argument("--headless");

    driver = webdriver.Chrome( options=options )

def gotoWebsite(url):
    # Open the website
    print("going to url")
    driver.get(url)
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(20)
    assert "BRUVAX" in driver.title

def login(niss, zip):
    # Select the niss box
    niss_box = driver.find_element_by_name("niss")
    # Send niss information
    niss_box.send_keys(niss)
    # Select the zip box
    zip_box = driver.find_element_by_name("zip")
    # Send zip information
    zip_box.send_keys(zip)

    # Find element by Xpath
    # checkbox = driver.find_element_by_xpath("//input[@type='checkbox']")
    # .click() fails with selenium.common.exceptions.ElementNotInteractableException: Message: element not interactable
    # checkbox.click()

    # wait = WebDriverWait(driver, 10)
    # checkbox = wait.until(EC.element_to_be_clickable( ( By.XPATH, "//input[@type='checkbox']" ) ) )
    # checkbox.click()

    # for i in range(10):
    #     try:
    #        driver.find_element_by_xpath(
    #            "//input[@type='checkbox']"
    #        ).click()
    #        break
    #    except NoSuchElementException as e:
    #        print('Retry in 1 second')
    #        time.sleep(1)
    #    else:
    #        raise e

    checkbox = driver.find_element_by_xpath("//input[@type='checkbox']")
    driver.implicitly_wait(10)
    ActionChains(driver).move_to_element(checkbox).click(checkbox).perform()

    # Find login button
    login_button = driver.find_element_by_tag_name("button")
    # Click login
    login_button.click()

def chooseCenter(which):
    print("Choosing: " + which)

    xpath = "//button[text()='" + which + "']"
    center_button = driver.find_element(By.XPATH, xpath)
    center_button.click()

    xpath = ".//*[contains(text(), '" + WAITLIST + "')]"
    waitlist_button = driver.find_element_by_xpath(xpath)
    waitlist_button.click()

def signup(center, firstName, lastName, email, mobile):
    print("Signup for " + center + " " + firstName + " " + lastName + " " + email + " " + mobile)
    firstName_box = driver.find_element_by_name("firstName")
    firstName_box.send_keys(firstName)
    lastName_box = driver.find_element_by_name("lastName")
    lastName_box.send_keys(lastName)
    email_box = driver.find_element_by_name("email")
    email_box.send_keys(email)
    mobile_box = driver.find_element_by_name("mobile")
    mobile_box.send_keys(mobile)
    # Uncomment the next two lines to ACTUALLY sign up on waitlist
##    send_button = driver.find_element_by_tag_name("button")
##    send_button.click()

    # This short loop will fail if you do not uncomment the send_button.click() above
    signedup = False
    for i in range(10):
        try:
            h2_text = driver.find_element_by_tag_name("h2")
            if "inscrit(e) sur la liste" in h2_text:
                # print("Found signedup")
                signedup = True
                break
            else:
                # print("Did not find signedup")
                # added in case print is commented out
                continue
        except:
            driver.implicitly_wait(10)
            # print("Waiting for response")

    if signedup:
        print("Signed up for " + center)
    else:
        print("Sign up FAILED " + center)

def changeCenter(which):
    select = Select(driver.find_element_by_name("centerEid"))
    select.select_by_visible_text(which)

class Waitlist:
    def __init__(self):
        # self.niss = int(input("What is your NISS? "))
        # self.zip = int(input("What is your postcode? "))
        self.niss = NISS
        self.zip = ZIP
        self.centers = list()
        for center in CENTERS:
            if "Y" in (input("Register for Vaccination Center: " + center + " (Y/N) ? ")).upper():
                self.centers.append(center)

    def main(self):
        startBrowser()
        i = 0
        while i < len(self.centers):
            gotoWebsite(REQUEST_URL)
            login(self.niss, self.zip)
            chooseCenter(self.centers[i])
            signup(self.centers[i], FIRSTNAME, LASTNAME, EMAIL, MOBILE)
            i = i + 1

            # BACK just will not work!
            # driver.back()
            # driver.execute_script("window.history.go(-1)")
            # this should work, but as back does not work, then go to start page of the process
            # changeCenter(self.centers[i])


if __name__ == "__main__":
    waitlist = Waitlist()
    Waitlist.main(waitlist)
