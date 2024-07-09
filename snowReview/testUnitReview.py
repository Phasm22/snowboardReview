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

START_INDEX = 259

''' Pass in the driver, the username, and the password to log in to the application.'''
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

''' Pass in the driver, the number of reviews to make, and whether or not to make a bad review.'''
def makeReview(driver, reviews, bad_review=False):
    # navigate to snowboards page
    driver.get("http://172.16.0.106:8000/snowboard-list/")
    end = reviews + START_INDEX

    # iterate over the first 'reviews' number of snowboards
    for i in range(START_INDEX, end):
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
            print(f"No review page found for index {i}")
            result = False



            # navigate back to the snowboards page
        driver.get("http://172.16.0.106:8000/snowboard-list/")  
    
        return result
    
''' Pass in the driver, the snowboard_id, and whether or not to make a bad comment.'''
def makeComment(driver, snowboard_id, bad_comment=False):
    # navigate to snowboards page
    driver.get(f"http://172.16.0.106:8000/snowboard/{snowboard_id}/add_comment/")


    # wait for the add comment button to be clickable
    add_comment_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'add-comment-button')))

    # use JavaScript to click the button
    driver.execute_script("arguments[0].click();", add_comment_button)

    # find the comment form
    comment = driver.find_element(By.ID, 'comment_text')

    # Add a comment to a snowboard review
    if bad_comment:
        # set comment to string longer than 500 characters
        comment_text = "a" * 501
    else:
        comment_text = "This is a test comment."
    comment.send_keys(comment_text)


    # find the submit button
    submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

    # use JavaScript to click the submit button
    driver.execute_script("arguments[0].click();", submit_button)

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
    # Users
    users = [
        {"username": "kathy_lopez", "password": "TestPassword123"}, # REVIEWER
        {"username": "michelle_dixon", "password": "TestPassword123"}, # NORMAL USER
    ]

    # Test making a review using authorized user, unauthorized user, and no user
    def test_makeReview(self):
        print("\n\nStarting review tests...\n")
        # loop through the users
        for user in self.users:
            # print the type of test
            if user["username"] == "kathy_lopez":
                print("\nTesting reviewer user...")
                reviewer = True
            else:
                print("\nTesting normal user...")
                reviewer = False

            driver = webdriver.Chrome()
            # log in the user
            login(driver, user["username"], user["password"])
            
            try:
                # make a review
                result = makeReview(driver, 1)
                expected_result = True if reviewer else False
                self.assertEqual(result, expected_result)
                print(f"Normal review passed for user {user['username']}. (1/2)")
            except AssertionError:
                print(f"Test failed for user {user['username']}. Normal review did not return {expected_result}. (1/2)")

            try:
                # make a bad review
                bad_result = makeReview(driver, 1, True)
                self.assertEqual(bad_result, False)
                print(f"Bad review passed for user {user['username']}. (2/2)")
            except AssertionError:
                print(f"Test failed for user {user['username']}. Bad review did not return False. (2/2)")
            finally:
                # Always quit the driver, even if the test fails
                driver.quit()
        
            print("All review tests passed!")

    # Test making a comment using authorized user, unauthorized user, and no user
    def test_makeComment(self):
        print("\n\nStarting comment tests...\n")
        for user in self.users:
            driver = webdriver.Chrome()
            login(driver, user["username"], user["password"])
            
            try:
                # make a comment
                result = makeComment(driver, START_INDEX)
                self.assertEqual(result, True)
                print(f"Normal comment passed for user {user['username']}. (1/2)")
            except AssertionError:
                print(f"Test failed for user {user['username']}. Normal comment did not return True. (1/2)")
    
            try:
                # make a bad comment
                bad_result = makeComment(driver, START_INDEX, True)
                self.assertEqual(bad_result, False)
                print(f"Bad comment passed for user {user['username']}. (2/2)")
            except AssertionError:
                print(f"Test failed for user {user['username']}. Bad comment did not return False. (2/2)")
            finally:
                # Always quit the driver, even if the test fails
                driver.quit()
    
        print("All comment tests passed!")

    # Test user creation and user creation with bad data
    def test_UserCreate(self):
        print("\n\nStarting user creation tests...\n")
        try:
            # create a user
            result = testUserCreate.test_user_create()
            self.assertEqual(result, True)
            print("Normal user creation passed. (1/2)")
        except AssertionError:
            print("Test failed. Normal user creation did not return True. (1/2)")
    
        try:
            # create a bad user
            bad_result = testUserCreate.test_user_create(True)
            self.assertEqual(bad_result, False)
            print("Bad user creation passed. (2/2)")
        except AssertionError:
            print("Test failed. Bad user creation did not return False. (2/2)")
    
        print("All user creation tests passed!")


if __name__ == "__main__":
    user = "marley"
    password = "spacexspacex"

    unittest.main()

    # options = Options()
    # options.add_argument("--headless")

    