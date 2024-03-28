import os
from selenium import webdriver
import django
import requests
import re
from bs4 import BeautifulSoup
import sys
from django.core.files import File


sys.path.insert(0, '/home/code/software/snowboardReview/')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_project.settings'
django.setup()

from django.conf import settings
from snowReview.models import Snowboard

"""
what we want to scape into the database
    price = models.FloatField(default=0)
    season = models.CharField(max_length=20, default='Unknown')
    shape = models.CharField(max_length=20, choices=SHAPES, default=SHAPES[0][0])
    profile = models.CharField(max_length=20, choices=PROFILES, default=PROFILES[0][0])
    rider = models.CharField(max_length=20, choices=SKILL, default=SKILL[0][0])
    flex = models.FloatField(default=0)
    brand = models.CharField(max_length=20, default='Unknown')
    name = models.CharField(max_length=20, default='Unknown')
    desc = models.CharField(max_length=200, default='No description available')
    image = models.ImageField(upload_to='snowboards/', null=True)
    brand_image = models.ImageField(upload_to='brands/', null=True)
"""
def scrape_website(website):
    web = website
    # This is a simplified example. Replace with your actual scraping code.
    response = requests.get(web)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Define a dictionary of fields to scrape
    fields = {
        'name': 'h1.pdp-header-title',
        'profile': '.pdp-feature-description em',  # Add the shape field'
        'shape': '.pdp-spec-list-item.spec-shape',  # Corrected CSS selector
        'rider': '.pdp-spec-list-item.spec-ability-level .pdp-spec-list-description',
        'flex': '.pdp-feature-description em:contains("Flex Rating") + span',
        'desc': '.pdp-details-content p'


        # Add other fields here, in the format 'fieldexit
        # _name': 'css_selector'
    }

    # Initialize an empty dictionary to store the scraped data
    data = {}

        # Loop over the fields dictionary
    for field, selector in fields.items():
        # Use select_one() to find the first element that matches the selector
        element = soup.select_one(selector)
        # If an element was found, get its text and store it in the data dictionary
        if element:
            text = element.text
            # check shape definitions
            # CamRock = Hybrid Camber
            if text == "CamRock":
                text = "Hybrid Camber"
            if text == "Directional Twin Shape":
                text = "Directional Twin"

            
            # Remove newline characters
            text = text.replace('\n', '').replace('Shape:', '')

                        # If the field is 'rider', split on the hyphen and take the first word
            if field == 'rider':
                text = text.split('-')[0].strip()
            
                    # If the field is 'flex', find the first number in the string
            if field == 'flex':
                match = re.search(r'\d+', text)
                if match:
                    text = match.group()
                else:
                    text = '0'

            data[field] = text

        # Extract the season from the name
    name = data.get('name', 'Unknown')
    season = name.split()[-1] if name else 'Unknown'
    # brand is just first word of name up until first whitespace
    brand = name.split()[0] if name else 'Unknown'

    # Print the name and season
    print(f"Name: {name}")
    print(f"Brand: {brand}")
    print(f"Season: {season}")
    print(f"Profile: {data.get('profile', 'Unknown')}")
    print(f"Shape: {data.get('shape', 'Unknown')}")
    print(f"Rider: {data.get('rider', 'Unknown')}")
    print(f"Flex: {data.get('flex', 'Unknown')}")
    print(f"Description: {data.get('desc', 'No description available')}")

    # Extract the image URL
    image_element = soup.select_one('.js-pdp-hero-image-container .js-pdp-image-asset.active')
    image_url = image_element['src'] if image_element else None

    # Download the image and save it to the specified directory
    if image_url:
        response = requests.get(image_url)
        image_name = image_url.split("/")[-1]  # Use the last part of the URL as the image name
        image_path = os.path.join('media/snowboards', image_name)  # Use a path relative to your Django project's root

        with open(image_path, 'wb') as f:
            f.write(response.content)

        image_file = File(open(image_path, 'rb'))

    # Create a new Snowboard instance and save it
    snowboard = Snowboard(
        name=name,
        season=season,
        profile=data.get('profile', 'Unknown'),
        shape=data.get('shape', 'Unknown'),
        rider=data.get('rider', 'Unknown'),
        flex=data.get('flex', '0'),
        desc=data.get('desc', 'No description available'),
        brand=brand, price=0,
        image=image_file if image_url else None  # Add the image file to the Snowboard instance
    )
    snowboard.save()



def get_links_from_user(num_links, url):
    # Send a GET request to the URL
    response = requests.get(url)
    # Parse the HTML content of the page with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the divs with the specified class
    divs = soup.find_all('div', {'class': 'product-thumb js-product-thumb'})

    # Initialize an empty set to store the product IDs
    product_ids = set()

    # Initialize an empty list to store the links
    links = []

    # Iterate over the divs
    for div in divs:
        # Get the product ID
        product_id = div.get('data-productid')

        # If the product ID is not already in the set, add it and get the link
        if product_id not in product_ids:
            product_ids.add(product_id)
            a_tag = div.find('a', {'class': 'product-thumb-link js-product-thumb-details-link'})
            if a_tag:
                # Add the base URL to the link
                link = 'https://www.evo.com' + a_tag.get('href')
                links.append(link)

        # If we've already got the desired number of links, break the loop
        if len(links) >= num_links:
            break

    return links
if __name__ == "__main__":
    # URL of the page to scrape
    url = "https://www.evo.com/shop/snowboard/snowboards/all-mountain/mens"

    # Get the number of links from the user
    num_links = int(input("Enter the number of links you want to scrape: "))

    # Get the links from the webpage
    websites = get_links_from_user(num_links, url)

    # Pass each link to the scrape_website function
    for website in websites:
        scrape_website(website)