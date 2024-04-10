# RUN LOCALLY
# iterates through a list of credentials and makes reviews on different snowboards.

import random
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

def login(driver, username, password):
    # navigate to the application home page
    driver.get("http://172.16.0.106:8000/login/")

    # get the username textbox
    username_field = driver.find_element("id", "username")
    username_field.clear()

    # enter username
    username_field.send_keys(username)

    # get the password textbox
    password_field = driver.find_element("id", "password")
    password_field.clear()

    # enter password
    password_field.send_keys(password)

    # get the submit button
    submit_button = driver.find_element("xpath", '//button[text()="Login"]')

    # click on the submit button
    submit_button.click()


def makeReview(driver, reviews):
    # navigate to snowboards page
    driver.get("http://172.16.0.106:8000/snowboard-list/")

    # iterate over the first 'reviews' number of snowboards
    for i in range(3, reviews + 1):
        print(f"i is now: {i}")
        try:
            # Navigate to review page
            review_url = f"http://172.16.0.106:8000/snowboard/{i}/review/"
            driver.get(review_url)

            # code to make a review 

            # Board Size
            board_size = driver.find_element(By.ID, "id_boardSize")
            size = randint(131, 169)
            board_size.send_keys(size)

            # Date
            date = driver.find_element(By.ID, "id_date")
            randMonth = randint(1, 12)
            randDay = randint(1, 28)
            date.send_keys(f"{randMonth:02d}-{randDay:02d}-2024")

            # Conditions
            conditions_list = ["Bluebird", "Sunny", "Cloudy", "Powder", "Groomed", "Windy", "Snowing"]
            random_condition = random.choice(conditions_list)
        
            conditions = driver.find_element(By.ID, "id_conditions")
            conditions.send_keys(random_condition)
            
            # Snowfall
            snow24_value = random.randint(0, 10)
            snow24 = driver.find_element(By.ID, "id_snow24")
            snow24.send_keys(str(snow24_value))
        
            snow7_value = random.randrange(int(snow24_value), 20)
            snow7 = driver.find_element(By.ID, "id_snow7")
            snow7.send_keys(str(snow7_value))

            # Height
            rider_height = driver.find_element(By.ID, "id_riderHeight")
            rider_height.send_keys("70")

            # Weight
            rider_weight = driver.find_element(By.ID, "id_riderWeight")
            rider_weight.send_keys("180")

            wait = WebDriverWait(driver, 10)
            submit_button = wait.until(EC.element_to_be_clickable((By.ID, "submit-button")))

            driver.execute_script("arguments[0].click();", submit_button)


        except NoSuchElementException:
            # the user is not authorized to review, break the loop
            break

            # navigate back to the snowboards page
        driver.get("http://172.16.0.106:8000/snowboard-list/")  

def test_user_login_and_review():
    driver = webdriver.Chrome()

    # create a new Chrome session
    default = "TestPassword123"
    users = [("marley", "spacexspacex"), ("kathy_lopez", default), ("mary_hamilton", default), ("william_webb", default)]


    # iterate over the users
    for user in users:
        # log in the user
        login(driver, user[0], user[1])

        # make a review
        try:
            makeReview(driver, 1)
        except NoSuchElementException:
            print(f"User {user[0]} is not authorized to make a review.")
            continue

    # close the browser window
    driver.quit()

options = Options()
options.add_argument("--headless")


if __name__ == "__main__":
    #test_user_login_and_review()

    user = "kathy_lopez"
    password = "TestPassword123"
    driver = webdriver.Chrome(options=options)
    login(driver, user, password)
    makeReview(driver, 60)