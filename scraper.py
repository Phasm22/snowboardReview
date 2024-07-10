# Tandon Jenkins
# This program scrapes snowboard data from the evo.com website and saves it to the database.
# It uses the requests and BeautifulSoup libraries to scrape the data and save the images.
# The data is saved to the Snowboard model in the snowReview app.
# The program prompts the user for the number of links to scrape and then scrapes the data from those links.
# The scraped data includes the snowboard name, season, profile, shape, rider, flex rating, description, image, brand, and brand image.
# The media files are saved to the 'media/snowboards' and 'media/brands' directories.
import os
import django
import aiohttp
import asyncio
import re
from bs4 import BeautifulSoup
import sys
from django.core.files.base import ContentFile
import json
from django.conf import settings

# Setup Django environment
def setup_django_environment(path, settings_module):
    sys.path.insert(0, path)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
    django.setup()


setup_django_environment('/home/code/software/snowboardReview', 'django_project.settings')

from snowReview.models import Snowboard, Terrain, Size
import time
class Scraper:
    def __init__(self, config):
        self.config = config

    async def scrape_website(self, session, website):
        raise NotImplementedError

    async def get_links_from_user(self, session, num_links, url):
        raise NotImplementedError

class EvoScraper(Scraper):
    async def scrape_website(self, session, website, debug=False):
        two_word_brands = ['Never Summer', 'Lib Tech']

        web = website
        self.config = self.get_website_config(web)
        mappings = self.config['mappings']

        async with session.get(web) as response:
            content = await response.text()
            soup = BeautifulSoup(content, 'html.parser')

        data = {}

        for field, selector in self.config['selectors'].items():
            element = soup.select_one(selector)
            if element:
                text = element.get_text(strip=True)
                if text == "CamRock":
                    text = "Hybrid Camber"
                if text == "Directional Twin Shape":
                    text = "Directional Twin"
                if text == "True Twin":
                    text = "True Twin"
                if field == 'rider':
                    text = text.split('-')[0].strip()
                text = text.replace('\n', '').replace('Shape:', '')
                if field == 'flex':
                    text = self.config['mappings'].get(text.lower(), 0)
                data[field] = text

        name = data.get('name', 'Unknown')
        match = re.search(r'\b\d{4}\b', name)
        season = match.group() if match else 'Unknown'
        first_two_words = " ".join(name.split()[:2])
        brand = first_two_words if first_two_words in two_word_brands else name.split()[0]

        if data.get('rider') == 'Advanced':
            data['rider'] = 'Expert'

        sizes = []
        for size_element in soup.select(self.config['selectors']['sizes']):
            size = size_element.get('title')
            if size:
                match = re.search(r'Select "(.*)"', size)
                if match:
                    size = match.group(1)
                    try:
                        size, created = await Size.objects.aget_or_create(size=size)
                        sizes.append(size)
                    except Exception as e:
                        print(f"Error processing size: {e}")

        sizes.sort(key=lambda size: size.size)

        image_element = soup.select_one(self.config['selectors']['image'])
        image_url = image_element['src'] if image_element else None

        def truncate_field(value, max_length):
            truncated_value = value[:max_length - 1] if value and len(value) >= max_length else value
            return truncated_value

        terrain_elements = soup.select(self.config['selectors']['terrain'])
        terrains = [terrain for element in terrain_elements if element for terrain in element.get_text(strip=True).split(', ')]

        try:
            snowboard, created = await Snowboard.objects.aget_or_create(
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

            for size_element in soup.select(self.config['selectors']['sizes']):
                size = size_element.get('title')
                if size:
                    match = re.search(r'Select "(.*)"', size)
                    if match:
                        size = match.group(1)
                        size_obj, created = await Size.objects.aget_or_create(size=size)
                        await snowboard.sizes.aadd(size_obj)

            for terrain_name in terrains:
                if terrain_name is not None:
                    terrain, created = await Terrain.objects.aget_or_create(name=terrain_name)
                    await snowboard.terrain.aadd(terrain)

        except Exception as e:
            print(f"Error creating Snowboard: {e}")

        if image_url:
            try:
                async with session.get(image_url) as response:
                    response.raise_for_status()
                    image_file = ContentFile(await response.read())
                    image_name = os.path.basename(image_url)
                    
                    if not os.path.splitext(image_name)[1]:
                        image_name += '.jpg'
                    try:
                        await snowboard.image.save(image_name, image_file, save=False)
                    except Exception as e:
                        print(f"Error saving image: {e}")
            except Exception as e:
                print(f"Error downloading image: {e}")

        brand_image_element = soup.select_one('.pdp-details-group .pdp-description-brand-logo')
        brand_image_url = brand_image_element['src'] if brand_image_element else None
        if brand_image_url and brand_image_url.startswith('//'):
            brand_image_url = 'https:' + brand_image_url

        if brand_image_url:
            try:
                async with session.get(brand_image_url) as response:
                    response.raise_for_status()
                    brand_image_file = ContentFile(await response.read())
                    brand_image_name = os.path.basename(brand_image_url)
                    
                    if not os.path.splitext(brand_image_name)[1]:
                        brand_image_name += '.jpg'
                    try:
                        await snowboard.brand_image.save(brand_image_name, brand_image_file, save=False)
                    except Exception as e:
                        print(f"Error saving brand image: {e}")
            except Exception as e:
                print(f"Error downloading brand image: {e}")

        for identifier in ['bundle_identifier', 'used_identifier', 'splitboard_identifier']:
            if self.config[identifier] in snowboard.name.lower():
                await snowboard.adelete()
                print(f"{identifier.capitalize().replace('_', ' ')} Snowboard Deleted")
                return

        await snowboard.asave()
        print("Snowboard Added!")
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

    async def get_links_from_user(self, session, num_links, url):
        try:
            with open('product_ids.json', 'r') as f:
                product_ids = set(json.load(f))
        except FileNotFoundError:
            product_ids = set()

        async with session.get(url) as response:
            content = await response.text()
            soup = BeautifulSoup(content, 'html.parser')

        divs = soup.find_all('div', {'class': 'product-thumb js-product-thumb'})
        links = []

        for div in divs:
            product_id = div.get('data-productid')
            if product_id not in product_ids:
                product_ids.add(product_id)
                a_tag = div.find('a', {'class': 'product-thumb-link js-product-thumb-details-link'})
                if a_tag:
                    link = 'https://www.evo.com' + a_tag.get('href')
                    links.append(link)
            if len(links) >= num_links:
                break

        with open('product_ids.json', 'w') as f:
            json.dump(list(product_ids), f)

        return links

    def get_website_config(self, url):
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
                    'terrain': '.pdp-spec-list-item.spec-terrain .pdp-spec-list-description',
                },
                'mappings': {
                    'very stiff': 5,
                    'stiff': 4,
                    'medium': 3,
                    'medium-soft': 2,
                    'soft': 1,
                    'very soft': 0,
                },
                'bundle_identifier': 'package',
                'used_identifier': 'used',
                'splitboard_identifier': 'splitboard'
            }
async def main():
    async with aiohttp.ClientSession() as session:
        evo_scraper = EvoScraper(config=None)
        num_links = int(input("Enter the number of links to scrape: "))
        urls = await evo_scraper.get_links_from_user(session, num_links, "https://www.evo.com/shop/snowboard/snowboards")
        
        start_time = time.time()
        
        for url in urls:
            await evo_scraper.scrape_website(session, url, debug=True)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Scraping completed in {elapsed_time:.2f} seconds")

if __name__ == '__main__':
    asyncio.run(main())