# Snowboard Review App
### The Snowboard Review App is a web application built with Django. It provides a platform for snowboarding enthusiasts to share their experiences and insights about different snowboards.

## Key features of the application include:

### User Authentication
- Users can register, log in, and log out. The app provides custom authentication forms for these operations.

### User Profiles
- Each user has a profile where they can view their personal information and activity on the app. This includes their comments and, if they are a reviewer, the reviews they've written.

### Snowboard Reviews
- Users who are designated as reviewers can write reviews about snowboards. Each review includes a rating and a detailed description.

### Comments
- All users can comment on the reviews, providing their thoughts and experiences about the snowboards.
<img src="https://github.com/Phasm22/snowboardReview/assets/92405484/cb951820-f970-4c3d-9753-1460c8b21dbf" width="1200">

# Python Scraper
- The scraper is designed to extract snowboard data from the evo.com website and save it to a Django database. It uses the requests and BeautifulSoup libraries to scrape and handle the HTML content of the web pages.

- The script begins by setting up the Django environment and importing the necessary Django models (Snowboard, Terrain, Size).
- From the scraped text, it is cleaned and processed (e.g., removing newline characters, splitting on hyphens, mapping flex ratings to numbers) and stored in a dictionary.

- The script also extracts the snowboard's available sizes and image URLs for the snowboard and the brand. It downloads these images and saves them to the Snowboard instance in the database.
<img src="https://github.com/Phasm22/snowboardReview/assets/92405484/8946e2af-1786-4c84-af6f-8ed9ad482daf" width="1200">

# Snowboard Details
- The snowboard detail  page displays specific information about a selected snowboard, such as its name, description, price, and images.
-  This page is designed to provide users with all the necessary details to make an informed decision about purchasing a snowboard.

![image](https://github.com/Phasm22/snowboardReview/assets/92405484/51a49bc9-d079-4fc2-bf19-24084a16dccb)

# Comments and Reviews
- I've implemented the functionality for adding, editing, and deleting comments and reviews.
![image](https://github.com/Phasm22/snowboardReview/assets/92405484/0f1040c4-5fe7-43a5-871d-6c611c0f4334)
