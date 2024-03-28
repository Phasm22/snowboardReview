# Tandon Jenkins
# This program scrapes snowboard data from the evo.com website and saves it to the database.
# It uses the requests and BeautifulSoup libraries to scrape the data and save the images.
# The data is saved to the Snowboard model in the snowReview app.
# The program prompts the user for the number of links to scrape and then scrapes the data from those links.
# The scraped data includes the snowboard name, season, profile, shape, rider, flex rating, description, image, brand, and brand image.
# The media files are saved to the 'media/snowboards' and 'media/brands' directories.

import os
import django
import requests
import re
from bs4 import BeautifulSoup
import sys
from django.core.files import File
import json
from faker import Faker


sys.path.insert(0, '/home/code/software/snowboardReview/')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_project.settings'
django.setup()

from django.conf import settings
from snowReview.models import Snowboard, Terrain

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
        'flex': '.pdp-spec-list-item.spec-flex-rating .pdp-spec-list-description',
        'desc': '.pdp-details-content p',
    }

    flex_rating_map = {
    'soft': 3,  # 1-3
    'medium': 6,  # 4-6
    'stiff': 8,  # 7-8
    'very stiff': 10  # 9-10
    }

    # Initialize an empty dictionary to store the scraped data
    data = {}

        # Loop over the fields dictionary
    for field, selector in fields.items():
        # Use select_one() to find the first element that matches the selector
        element = soup.select_one(selector)
        # If an element was found, get its text and store it in the data dictionary
        if element:
            text = element.get_text(strip=True)
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
                text = flex_rating_map.get(text.lower(), 0)  # Default to 0 if the flex rating is not recognized

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
        image_dir = ('media/snowboards')
        print(image_dir)
        image_path = (image_dir + image_name)  # This is an absolute path
        print(image_path)

        # Create the directory if it doesn't exist
        os.makedirs(image_dir, exist_ok=True)

        with open(image_path, 'wb') as f:
            f.write(response.content)
        
        image_file = File(open(image_path, 'rb'))  # Use the absolute path to open the file


    # brand image
    brand_image_element = soup.select_one('.pdp-details-group .pdp-description-brand-logo')
    brand_image_url = brand_image_element['src'] if brand_image_element else None

    # Add the protocol to the URL
    if brand_image_url and brand_image_url.startswith('//'):
        brand_image_url = 'https:' + brand_image_url

    # Download the image and save it to the specified directory
    if brand_image_url:
        response = requests.get(brand_image_url)
        brand_image_name = brand_image_url.split("/")[-1]
        brand_dir = ('media/brands')
        brand_image_path = (brand_dir + brand_image_name)

        # Create the directory if it doesn't exist
        os.makedirs(brand_dir, exist_ok=True)

        with open(brand_image_path, 'wb') as f:
            f.write(response.content)
        
        brand_image_file = File(open(brand_image_path, 'rb'))

        # terrain
    terrain_elements = soup.select('.pdp-spec-list-item.spec-terrain .pdp-spec-list-description')
    terrains = [element.get_text(strip=True) for element in terrain_elements if element]


    snowboard = Snowboard(
        name=name,
        season=season,
        profile=data.get('profile', 'Unknown'),
        shape=data.get('shape', 'Unknown'),
        rider=data.get('rider', 'Unknown'),
        flex=data.get('flex', '0'),
        desc=data.get('desc', 'No description available'),
        brand=brand,
        image=image_file if image_url else None,  # Add the image file to the Snowboard instance
        brand_image=brand_image_file if brand_image_url else None
    )
    snowboard.save()

    # Associate the terrains with the snowboard
    for terrain_name in terrains:
        if terrain_name is not None:
            terrain, created = Terrain.objects.get_or_create(name=terrain_name)
            snowboard.terrain.add(terrain)
    snowboard.save()

def get_links_from_user(num_links, url):
    # Load the product IDs from the file
    try:
        with open('product_ids.json', 'r') as f:
            product_ids = set(json.load(f))
    except FileNotFoundError:
        product_ids = set()

    # Send a GET request to the URL
    response = requests.get(url)
    # Parse the HTML content of the page with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the divs with the specified class
    divs = soup.find_all('div', {'class': 'product-thumb js-product-thumb'})

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

    # Save the product IDs to the file
    with open('product_ids.json', 'w') as f:
        json.dump(list(product_ids), f)

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