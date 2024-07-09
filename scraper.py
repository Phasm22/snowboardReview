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
import requests
from django.core.files.base import ContentFile
import json
from faker import Faker

def setup_django_environment(path, settings):
    """
    Sets up the Django environment for a script.

    This function adds the given path to the system path, and sets the
    DJANGO_SETTINGS_MODULE environment variable to the given settings module.
    It then sets up the Django environment.

    Args:
        path (str): The path to add to the system path.
        settings (str): The settings module to use for Django.

    """
    sys.path.insert(0, path)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings)
    os.environ['DJANGO_SETTINGS_MODULE'] = settings
    django.setup()

# Call the function at the start of your script
setup_django_environment('/home/code/software/snowboardReview/', 'django_project.settings')

from django.conf import settings
from snowReview.models import Snowboard, Terrain, Size

class Scraper:


    def __init__(self, config):
        self.config = config

    def scrape_website(self, website):
        raise NotImplementedError

    def get_links_from_user(self, num_links, url):
        raise NotImplementedError


class EvoScraper(Scraper):
    """
    A scraper for the Evo website.

    This class inherits from the Scraper base class and implements the scrape_website method
    specifically for the Evo website.

    """
    def scrape_website(self, website, debug=False):
        """
        Scrapes the given website.

        This method overrides the scrape_website method in the Scraper base class. It scrapes the
        given website and optionally prints debug information.

        Args:
            website (str): The URL of the website to scrape.
            debug (bool, optional): Whether to print debug information. Defaults to False.

        """
        # Define a list of two-word brand names
        two_word_brands = ['Never Summer', 'Lib Tech']  # Add more brand names as needed

        web = website
        # Get the fields for evo
        self.config = self.get_website_config(web)
        # Extract the flex mappings
        mappings = self.config['mappings']
        response = requests.get(web)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Initialize an empty dictionary to store the scraped data
        data = {}

        # Loop over the selectors
        for field, selector in self.config['selectors'].items():
            # Use select_one() to find the first element that matches the selector
            element = soup.select_one(selector)
            # If an element was found, get its text and store it in the data dictionary
            if element:
                text = element.get_text(strip=True)

                # Specific transformations
                if text == "CamRock":
                    text = "Hybrid Camber"
                if text == "Directional Twin Shape":
                    text = "Directional Twin"
                if text == "True Twin":
                    text = "True Twin"
                if field == 'rider':
                    text = text.split('-')[0].strip()


            text = text.replace('\n', '').replace('Shape:', '')

            # Apply mappings if necessary
            if field == 'flex':
                text = self.config['mappings'].get(text.lower(), 0)  # Default to 0 if the flex rating is not recognized

            # Store the text in the data dictionary
            data[field] = text

        # Extract the season from the name
        name = data.get('name', 'Unknown')
        match = re.search(r'\b\d{4}\b', name)
        season = match.group() if match else 'Unknown'

        # Extract the first two words from the name
        first_two_words = " ".join(name.split()[:2])

        # Check if the first two words match any of the brand names
        brand = first_two_words if first_two_words in two_word_brands else name.split()[0]

        # If 'rider' is 'Advanced', set it to 'Expert'
        if data.get('rider') == 'Advanced':
            data['rider'] = 'Expert'


        sizes = []
        # Loop over the elements that match the 'sizes' selector
        for size_element in soup.select(self.config['selectors']['sizes']):
            # Get the 'title' attribute of the element
            size = size_element.get('title')
            # If the 'title' attribute was found, extract the size with a regular expression
            if size:
                match = re.search(r'Select "(.*)"', size)
                if match:
                    size = match.group(1)  # The first group is the part of the string that matches the pattern
                    try:
                        size, created = Size.objects.get_or_create(size=size)  # Get or create a Size object
                        # print length of size
                        print(len(size.size))
                        sizes.append(size)
                    except Exception as e:
                        print(f"Error processing size: {e}")

        # Sort sizes
        sizes.sort(key=lambda size: size.size)

        image_element = soup.select_one(self.config['selectors']['image'])
        image_url = image_element['src'] if image_element else None

        def truncate_field(value, max_length):
            if value:
                print(f"Length of desc before truncation: {len(value)}")
            truncated_value = value[:max_length - 1] if value and len(value) >= max_length else value
            print(f"Length of desc after truncation: {len(truncated_value)}")
            return truncated_value
        
        ## terrains
        terrain_elements = soup.select(self.config['selectors']['terrain'])
        terrains = [terrain for element in terrain_elements if element for terrain in element.get_text(strip=True).split(', ')]
        print(terrains)

        # to avoid duplicates
        try:
            snowboard, created = Snowboard.objects.get_or_create(
                name=name,
                defaults={
                    'season': season,
                    'profile': truncate_field(data.get('profile', 'Unknown'), 40),
                    'shape': truncate_field(data.get('shape', 'Unknown'), 40),
                    'rider': data.get('rider', 'Unknown'),
                    'flex': data.get('flex', '0'),
                    'desc': truncate_field(data.get('desc', 'No description available'), 500),
                    'brand': brand,
                }
            )
            if created:
                print(f"Created new Snowboard: {snowboard.name}")
            else:
                print(f"Snowboard already exists: {snowboard.name}")

            # Only add sizes if snowboard creation was successful
            for size_element in soup.select(self.config['selectors']['sizes']):
                size = size_element.get('title')
                if size:
                    match = re.search(r'Select "(.*)"', size)
                    if match:
                        size = match.group(1)
                        size_obj, created = Size.objects.get_or_create(size=size)
                        snowboard.sizes.add(size_obj)

            # Associate the terrains with the snowboard
            for terrain_name in terrains:
                if terrain_name is not None:
                    terrain, created = Terrain.objects.get_or_create(name=terrain_name)
                    snowboard.terrain.add(terrain)

        except Exception as e:
            print(f"Error creating Snowboard: {e}")


        # Download the image and save it to the specified directory
        if image_url:
            try:
                response = requests.get(image_url)
                response.raise_for_status()  # Raise an exception if the GET request was not successful
            except Exception as e:
                print(f"Error downloading image: {e}")
            else:
                # Create a Django File object from the downloaded image
                image_file = ContentFile(response.content)
                image_name = os.path.basename(image_url)  # Use the last part of the URL as the image name

                # Check if the image name has a file extension
                if not os.path.splitext(image_name)[1]:
                    image_name += '.jpg'  # Add a default file extension if none was found

                try:
                    snowboard.image.save(image_name, image_file, save=False)  # Save the image file to the Snowboard instance
                except Exception as e:
                    print(f"Error saving image: {e}")
    
        # brand image
        brand_image_element = soup.select_one('.pdp-details-group .pdp-description-brand-logo')
        brand_image_url = brand_image_element['src'] if brand_image_element else None
        
        # Add the protocol to the URL
        if brand_image_url and brand_image_url.startswith('//'):
            brand_image_url = 'https:' + brand_image_url

        # Download the brand image and save it to the specified directory
        if brand_image_url:
            try:
                response = requests.get(brand_image_url)
                response.raise_for_status()  # Raise an exception if the GET request was not successful
            except Exception as e:
                print(f"Error downloading brand image: {e}")
            else:
                # Create a Django File object from the downloaded image
                brand_image_file = ContentFile(response.content)
                brand_image_name = os.path.basename(brand_image_url)  # Use the last part of the URL as the image name

                # Check if the image name has a file extension
                if not os.path.splitext(brand_image_name)[1]:
                    brand_image_name += '.jpg'  # Add a default file extension if none was found

                try:
                    snowboard.brand_image.save(brand_image_name, brand_image_file, save=False)  # Save the brand image file to the Snowboard instance
                except Exception as e:
                    print(f"Error saving brand image: {e}")
        

        # Delete the snowboard if it's part of a bundle or used
        for identifier in ['bundle_identifier', 'used_identifier', 'splitboard_identifier']:
            if self.config[identifier] in snowboard.name.lower():
                snowboard.delete()
                print(f"{identifier.capitalize().replace('_', ' ')} Snowboard Deleted")
                return

        snowboard.save()
        print("Snowboard Added!")
            # Print the name and season if debug is True
        if debug:
            print(f"Name: {name}")
            print(f"Brand: {brand}")
            print(f"Season: {season}")
            print(f"Profile: {data.get('profile', 'Unknown')}")
            print(f"Shape: {data.get('shape', 'Unknown')}")
            print(f"Sizes: {sizes}")
            print(f"Rider: {data.get('rider', 'Unknown')}")
            print(f"Flex: {data.get('flex', 'Unknown')}")
            print(f"Description: {data.get('desc', 'No description available')}")
            print(f"Terrains: {terrains}")

    def get_links_from_user(self, num_links, url):
        """
        Retrieves a specified number of unique product links from a given URL.

        This method sends a GET request to the provided URL, parses the HTML content, and finds all divs with a 
        specific class. It then iterates over these divs to extract product IDs and corresponding links. If a 
        product ID is not already in the set of known IDs, it is added and its link is stored. The process stops 
        once the desired number of links is reached. The updated set of product IDs is then saved to a JSON file.

        Args:
            num_links (int): The number of unique product links to retrieve.
            url (str): The URL from which to retrieve product links.

        Returns:
            list: A list of unique product links.

        Raises:
            FileNotFoundError: If the 'product_ids.json' file does not exist, a new set for product_ids is created.
        """

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


    def get_website_config(self, url):
        """
        Returns the appropriate configuration for scraping a given website.

        This method checks if the given URL contains 'evo.com', and if so, returns a dictionary containing
        the selectors for various elements on the page, mappings for flex ratings, and identifiers for 
        bundle, used, and splitboard products. If the URL does not contain 'evo.com', it raises a ValueError.

        Args:
            url (str): The URL of the website to scrape.

        Returns:
            dict: A dictionary containing the configuration for scraping the website.

        Raises:
            ValueError: If the URL does not contain 'evo.com'.
        """
        
        # Return the appropriate configuration based on the URL
        if 'evo.com' in url:
            return {
                'selectors': {
                    'name': 'h1.pdp-header-title',
                    'profile': '.pdp-feature-description em',
                    'shape': '.pdp-spec-list-item.spec-shape', 
                    'rider': '.pdp-spec-list-item.spec-ability-level .pdp-spec-list-description',
                    'flex': '.pdp-spec-list-item.spec-flex-rating .pdp-spec-list-description',
                    'desc': '.pdp-details-content p',
                    'sizes': 'label.pdp-selection-label span.pdp-selection-text.pdp-selector',
                    'image': '.js-pdp-hero-image-container .js-pdp-image-asset.active',
                    'terrain': '.pdp-spec-list-item.spec-terrain .pdp-spec-list-description'
                },
                'mappings': {
                    'soft': 3,  # 1-3
                    'medium': 6,  # 4-6
                    'stiff': 8,  # 7-8
                    'very stiff': 10  # 9-10
                },
                'bundle_identifier': ' + ',
                'used_identifier': 'used',
                'splitboard_identifier' : 'splitboard'
            }
        else:
            raise ValueError(f'No configuration found for website: {url}')


def get_user_input(website_urls):
    """
    Interacts with the user to get the website they want to scrape and the number of links to scrape.

    This function presents the user with a list of websites and their URLs, and asks the user to choose
    one. It then asks the user to input the number of links they want to scrape from the chosen site.

    Args:
        website_urls (dict): A dictionary where the keys are website names and the values are dictionaries
                             containing details about the websites, including the URL.

    Returns:
        tuple: A tuple containing the user's chosen site (str) and the number of links they want to scrape (int).

    """
    # Present the options to the user
    for key, value in website_urls.items():
        print(f"{key}: {value['url']}")

    # Keep asking for the site until a valid choice is given
    while True:
        choice = input("\n\nWhich site do you want to scrape? ")
        if choice in website_urls:
            break
        else:
            print("Invalid choice. Please enter a valid site.")

    # Keep asking for the number of links until a valid number is given
    while True:
        num_links = input("How many links do you want to scrape from this site? ")
        if num_links.isdigit() and int(num_links) > 0:
            num_links = int(num_links)
            break
        else:
            print("Invalid number. Please enter a positive number.")

    return choice, num_links


if __name__ == "__main__":

    print("\n\n----------------Active Links-----------------\n\n")
    # Define the website URLs
    website_urls = {
        "1": {"url": "https://www.evo.com/shop/snowboard/snowboards/mens/womens/s_price-asc/rpp_400", "class": EvoScraper},
    }

    # Get user input
    choice, num_links = get_user_input(website_urls)

    # Get the corresponding URL and class
    website_url = website_urls[choice]["url"]
    ScraperClass = website_urls[choice]["class"]
    # Create an instance of the chosen scraper class
    scraper = ScraperClass(config={})

    # Get the links from the website
    links = scraper.get_links_from_user(num_links, website_url)

    # Scrape the links
    for index, link in enumerate(links):
        scraper.scrape_website(link)
        # index
        print(f"Processing link number: {index}")
