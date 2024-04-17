import random
import unittest
from random import randint
import testUserCreate
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


def makeReview(driver, reviews, bad_review=False):
    # navigate to snowboards page
    driver.get("http://172.16.0.106:8000/snowboard-list/")

    # iterate over the first 'reviews' number of snowboards
    for i in range(255, reviews + 1):
        print(f"i is now: {i}")
        try:
            # Navigate to review page
            review_url = f"http://172.16.0.106:8000/snowboard/{i}/review/"
            driver.get(review_url)

            # code to make a review 
            if not bad_review:
                # Board Size
                board_size = driver.find_element(By.ID, "id_boardSize")
                board_size.clear()
                size = randint(131, 169)
                board_size.send_keys(size)

                # Date
                date = driver.find_element(By.ID, "id_date")
                date.clear()
                randMonth = randint(1, 12)
                randDay = randint(1, 28)
                date.send_keys(f"{randMonth:02d}-{randDay:02d}-2024")

                # Conditions
                conditions_list = ["Bluebird", "Sunny", "Cloudy", "Powder", "Groomed", "Windy", "Snowing"]
                random_condition = random.choice(conditions_list)
            
                conditions = driver.find_element(By.ID, "id_conditions")
                conditions.clear()
                conditions.send_keys(random_condition)
                
                # Snowfall
                snow24_value = round(random.uniform(0, 10), 2)
                snow24 = driver.find_element(By.ID, "id_snow24")
                snow24.clear()
                snow24.send_keys(str(snow24_value))
                
                snow7_value = round(random.uniform(snow24_value, 20), 2)
                snow7 = driver.find_element(By.ID, "id_snow7")
                snow7.clear()
                snow7.send_keys(str(snow7_value))
                # Height
                rider_height = driver.find_element(By.ID, "id_riderHeight")
                rider_height.clear()
                rider_height.send_keys("70")

                # Weight
                rider_weight = driver.find_element(By.ID, "id_riderWeight")
                rider_weight.clear()
                rider_weight.send_keys("180")

                wait = WebDriverWait(driver, 10)
                submit_button = wait.until(EC.element_to_be_clickable((By.ID, "submit-button")))

                driver.execute_script("arguments[0].click();", submit_button)
            
            else:
                # code to make a bad review
                # Board Size
                board_size = driver.find_element(By.ID, "id_boardSize")
                board_size.clear()
                board_size.send_keys(190)

                # Date
                date = driver.find_element(By.ID, "id_date")
                date.clear()
                randMonth = randint(1, 12)
                randDay = randint(1, 28)
                date.send_keys(f"{randMonth:02d}-{randDay:02d}-2024")

                # Conditions
                conditions_list = ["Bluebird", "Sunny", "Cloudy", "Powder", "Groomed", "Windy", "Snowing"]
                random_condition = random.choice(conditions_list)
            
                conditions = driver.find_element(By.ID, "id_conditions")
                conditions.clear()
                conditions.send_keys(random_condition)
                
                # Snowfall
                snow24 = driver.find_element(By.ID, "id_snow24")
                snow24.clear()
                snow24.send_keys(str(300))
                
                snow7 = driver.find_element(By.ID, "id_snow7")
                snow7.clear()
                snow7.send_keys(str(700))

                # Height
                rider_height = driver.find_element(By.ID, "id_riderHeight")
                rider_height.clear()
                rider_height.send_keys("2")

                # Weight
                rider_weight = driver.find_element(By.ID, "id_riderWeight")
                rider_weight.clear()
                rider_weight.send_keys("2")

                wait = WebDriverWait(driver, 10)
                submit_button = wait.until(EC.element_to_be_clickable((By.ID, "submit-button")))

                driver.execute_script("arguments[0].click();", submit_button)

            # Check if the error message is present
            error_message = driver.find_elements(By.XPATH, '//div[@class="alert alert-danger"]')

            # If the error message is present, return False. Otherwise, return True.
            if error_message:
                print("Error message found")
                result = False
            else:
                print("No error message found")
                result = True


        except NoSuchElementException:
            # the user is not authorized to review, break the loop
            break

            # navigate back to the snowboards page
        driver.get("http://172.16.0.106:8000/snowboard-list/")  
        return result
    
def makeComment(driver, snowboard_id, bad_comment=False):
    # navigate to snowboards page
    # url http://172.16.0.106:8000/snowboard/251/add_comment/#accordionComments
    # replace 251 with snowboard_id
    driver.get(f"http://172.16.0.106:8000/snowboard/{snowboard_id}/add_comment/")

    # User input to click on the comment button
    input("Click on the comment button and press enter to continue.")

    # find the comment form
    comment = driver.find_element(By.ID, 'comment-text')


    # Add a comment to a snowboard review
    if bad_comment:
        # set comment to string longer than 500 characters
        comment_text = "a" * 501
    else:
        comment_text = "This is a test comment."
    comment.send_keys(comment_text)


    # submit the comment
    submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
    submit_button.click()

    # Check if the error message is present
    error_message = driver.find_elements(By.XPATH, '//div[@class="alert alert-danger"]')

    # If the error message is present, return False. Otherwise, return True.
    if error_message:
        result = False
    else:
        result = True

    return result

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


class TestSnowReview(unittest.TestCase):
    def test_makeReview(self):
        user = "kathy_lopez"
        password = "TestPassword123"
        
        driver = webdriver.Chrome()
        login(driver, user, password)
        
        try:
            result = makeReview(driver, 255)
            bad_result = makeReview(driver, 255, True)
            self.assertEqual(result, True)
            print("Normal review passed.")
            self.assertEqual(bad_result, False)
            print("Bad review passed.")
            print("All review tests passed!")
        except AssertionError:
            print("Test failed. makeReview did not return True.")
            # Perform any necessary cleanup here
        finally:
            # Always quit the driver, even if the test fails
            driver.quit()

    def test_makeComment(self):
        user = "kathy_lopez"
        password = "TestPassword123"
        
        driver = webdriver.Chrome()
        login(driver, user, password)
        
        try:
            result = makeComment(driver, 255)
            bad_result = makeComment(driver, 255, True)
            self.assertEqual(bad_result, False)
            print("Bad comment passed.")
            self.assertEqual(result, True)
            print("Normal comment passed.")
            print("All comment tests passed!")
        except AssertionError:
            print("Test failed. makeComment did not return True.")
            # Perform any necessary cleanup here
        finally:
            # Always quit the driver, even if the test fails
            driver.quit()

    def test_UserCreate(self):
        result = testUserCreate.test_user_create()
        bad_result = testUserCreate.test_user_create(True)
        self.assertEqual(result, True)
        print("Normal user creation passed.")
        self.assertEqual(bad_result, False)
        print("Bad user creation passed.")
        print("All user creation tests passed!")


if __name__ == "__main__":
    unittest.main()