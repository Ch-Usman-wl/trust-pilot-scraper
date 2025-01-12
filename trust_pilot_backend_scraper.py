import requests
import pandas as pd
import math
from datetime import datetime
import time

review_data = []

def get_requests(filter_option, input_date):
    i=1
    end_bool = False

    cookies = {
        }

    headers = {
        }

    while True:
        if i == 1:
            params = {
                'languages': 'all',
                'businessUnit': '',
            }
        else:
            params = {
                'languages': 'all',
                'page': f'{i}',
                'businessUnit': '',
            }

        retries = 5
        response = None
        for attempt in range(retries):
            try:
                time.sleep(2)
                response = requests.get('INSERT URL HERE OF COOKIES AND HEADERS',
                    params=params, cookies=cookies,headers=headers)
                response.raise_for_status()
                break
            except requests.exceptions.HTTPError as http_err:
                if response.status_code == 404:
                    print(f'Request Failed. Status code: {response.status_code}')
                    print('Hence, End of reviews reached. Stopping...')
                    end_bool = True
                    break
                else:
                    print(f'Request Failed. HTTP error: {http_err}')
                print(f'Attempt {attempt + 1} failed: {http_err}')
                print('Waiting 8 seconds to retry...')
                time.sleep(8)
            
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                print(f"Attempt {attempt + 1} failed: {e}")
                print('Waiting 8 seconds to retry...')
                time.sleep(8)

        if response:
            resp = response.json()
            #print(resp)
            page_props = resp.get('pageProps', {})
            #print(page_props)
            reviews = page_props.get('reviews', [])
            #print(reviews)
            if reviews:
                for review in reviews:
                    title = review.get('title', None)
                    description = review.get('text', None)
                    rating = review.get('rating', None)
                    consumer = review.get('consumer', {})
                    display_name = consumer.get('displayName') if consumer else None
                    dates = review.get('dates', {})
                    pub_date = dates.get('publishedDate') if dates else None
                    parsed_date = datetime.strptime(pub_date, "%Y-%m-%dT%H:%M:%S.%fZ") if pub_date else None
                    published_date = parsed_date.strftime("%Y-%m-%d") if parsed_date else None
                    published_date_dt = datetime.strptime(published_date, "%Y-%m-%d") if published_date else None
                    if not input_date:
                        review_data.append({
                            'title': title, 
                            'rating': rating, 
                            'display_name': display_name, 
                            'published_date': published_date,
                            'description': description
                            })

                    elif ((filter_option == 'before' and published_date_dt < input_date) and published_date_dt ) or ((filter_option == 'after' and published_date_dt > input_date) and published_date_dt):
                        review_data.append({
                            'title': title, 
                            'rating': rating, 
                            'display_name': display_name, 
                            'published_date': published_date,
                            'description': description
                            })
                print('Data appended.')
            else:
                print('No reviews found.')
        i += 1
        if end_bool:
            break


def main():
    filter_option = None
    input_date_str = input("Enter the date (YYYY-MM-DD) to filter reviews (leave blank for all):  ")
    if input_date_str:
        filter_option = input("Do you want reviews before or after this date? (Type 'before' or 'after'): ").strip().lower()
    input_date = None
    if input_date_str.strip():  # Check if input date is not blank
        try:
            input_date = datetime.strptime(input_date_str, '%Y-%m-%d')
            print("Input Date:", input_date)
        except ValueError:
            print("Invalid date format. Please use 'YYYY-MM-DD' (e.g., '2024-08-26').")
            exit()
    

    get_requests(filter_option, input_date)

    df = pd.DataFrame(review_data)
    df = df[['title', 'rating', 'display_name', 'published_date', 'description']]
    df.to_csv('trust_pilot_reviews.csv', index=False)
    print('Reviews saved to trust_pilot_reviews.csv.')


if __name__ == '__main__':
    main()