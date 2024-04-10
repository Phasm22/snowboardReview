# RUN LOCAlLY
# Creates a user and logs in after creation

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker

def createUser(driver):
    # navigate to the application home page
    driver.get("http://172.16.0.106:8000/register/")
    fake = Faker()

    # get the username textbox ex. "john_doe"
    username_str = (f"{fake.first_name()}_{fake.last_name()}").lower()
    
    password_str = "TestPassword123"

    # fill in the registration form
    username = driver.find_element(By.ID, "id_username")
    username.send_keys(username_str)

    email = driver.find_element(By.ID, "id_email")
    email.send_keys(fake.ascii_email())

    password = driver.find_element(By.ID, "id_password1")
    password.send_keys(password_str)

    confirm_password = driver.find_element(By.ID, "id_password2")
    confirm_password.send_keys(password_str)

    submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
    submit_button.click()

    return username_str, password_str

def loginUser(driver, username, password):
    # navigate to the login page
    driver.get("http://172.16.0.106:8000/login/")

    # fill in the login form
    username_field = driver.find_element(By.ID, "username")
    username_field.send_keys(username)

    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)

    submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
    submit_button.click()
   
    # wait for the user to be logged in
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "alert-success")))

    
def test_user_create():
    # create a new Chrome session
    driver = webdriver.Chrome()

    # create a new user
    username, password = createUser(driver)

    # log in with the new user
    loginUser(driver, username, password)

    # close the browser window
    driver.quit()

if __name__ == "__main__":
    test_user_create()
