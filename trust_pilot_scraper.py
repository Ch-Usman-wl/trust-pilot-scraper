from bs4 import BeautifulSoup
import requests
import pandas as pd
import math
from datetime import datetime

data = []
# Set Trustpilot page numbers to scrape here
from_page = 1
to_page = 20
review_counter = 1

#Getting input dates
# Input the date and filtering option
input_date_str = input("Enter the date (MMM DD, YYYY) to filter reviews (leave blank for all):  ")
filter_option = input("Do you want reviews before or after this date? (Type 'before' or 'after' or leave blank for all): ").strip().lower()
input_date = None
# Try to parse the input date
if input_date_str.strip():  # Check if input date is not blank
    try:
        input_date = datetime.strptime(input_date_str, '%b %d, %Y')
        print("Input Date:", input_date)
    except ValueError:
        print("Invalid date format. Please use 'MMM DD, YYYY' (e.g., 'Aug 26, 2024').")
        exit()



#Dynamically getting total number of pages of reviews
url = "https://www.trustpilot.com/review/staytick.com?languages=all&page="
response = requests.get(f"{url}1")
web_page = response.text
soup = BeautifulSoup(web_page, "html.parser")
total_reviews_tag = soup.select_one('[data-reviews-count-typography]')


#if the tag for total reviews is found
if total_reviews_tag:
    #getting total review number
    total_reviews_text = total_reviews_tag.text.strip()
    total_reviews = total_reviews_text.split(' ')[0]  # Get the first part which is the number
    print(f"Total Reviews: {total_reviews}")

    #Getting final page number
    reviews_per_page = 20
    total_reviews = int(total_reviews)
    total_pages = math.ceil(total_reviews / reviews_per_page)
    to_page = total_pages
    #print(from_page)
else:
    print("Total reviews count not found. Setting page count to 20.")

#Scraping the website to get reviews
for i in range(from_page, to_page + 1):
    response = requests.get(f"{url}{i}")
    web_page = response.text
    soup = BeautifulSoup(web_page, "html.parser")
    print(len(soup.select('article[data-service-review-card-paper]')))
    for e in soup.select('article[data-service-review-card-paper]'):


        review_date_str = e.select_one('[data-service-review-date-time-ago]').text
        review_date = datetime.strptime(review_date_str, '%b %d, %Y')

        if not input_date_str.strip():  # If no date was provided
            data.append({
                'review_title': e.h2.text,
                'review_date_original': review_date,
                'review_rating': e.select_one('[data-service-review-rating]').get('data-service-review-rating'),
                'username': e.select_one('[data-consumer-name-typography]').text,
                'review_text': e.select_one('[data-service-review-text-typography]').text if e.select_one('[data-service-review-text-typography]') else None,
                'page_number': i,
                'review_number': len(data) + 1
            })
            review_counter += 1

        elif (filter_option == 'before' and review_date < input_date) or (filter_option == 'after' and review_date > input_date):
            data.append({
                'review_title':e.h2.text,
                'review_date_original': e.select_one('[data-service-review-date-time-ago]').text,
                'review_rating':e.select_one('[data-service-review-rating]').get('data-service-review-rating'),
                'username': e.select_one('[data-consumer-name-typography]').text,
                'review_text': e.select_one('[data-service-review-text-typography]').text if e.select_one('[data-service-review-text-typography]') else None,
                'page_number':i, 
                'review_number': review_counter
            })
            review_counter += 1


# Create DataFrame only if data is not empty
if data:
    df = pd.DataFrame(data)
    df = df[['review_number', 'page_number', 'username', 'review_rating', 'review_title', 'review_date_original', 'review_text']]
    # Saving to CSV
    df.to_csv('reviews.csv', index=False)
    print("Reviews saved to 'reviews.csv'.")
else:
    print("No reviews collected that match the specified date criteria.")

#'review_date_original': e.select_one('[data-service-review-date-of-experience-typography]').text.split(': ')[-1],