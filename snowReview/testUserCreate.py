# RUN LOCAlLY
# Creates a user and logs in after creation

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker

def createUser(driver, badTest=False):
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

    # If this is a bad test, send a different password to the confirm password field
    if badTest:
        confirm_password.send_keys("badPassword")
    else:
        confirm_password.send_keys(password_str)

    try:
        submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
        submit_button.click()

        # Check if the error message is present
        error_message = driver.find_elements(By.XPATH, '//div[@class="alert alert-danger"]')

        if error_message:
            return False
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

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

    success_alert = driver.find_elements(By.XPATH, '//div[@class="alert alert-success alert-dismissible fade show"]')
    if not success_alert:
        result = False
    else:
        result = True

    return result

    
def test_user_create(badTest=False):
    # create a new Chrome session
    driver = webdriver.Chrome()

    # create a new user
    if badTest:
        result = createUser(driver, True)
    else:
        result = createUser(driver)
    
    if isinstance(result, bool) and not result:
        print("User creation failed.")
        # Perform any necessary cleanup here
    else:
        username, password = result

    print(f'\nusername: {username}')

    # Log in with the new user
    is_logged_in = loginUser(driver, username, password)

    # Close the browser window
    driver.quit()

    return is_logged_in


if __name__ == "__main__":
    test_user_create()
