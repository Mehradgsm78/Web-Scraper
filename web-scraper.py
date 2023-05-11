import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

from datetime import datetime
companyName = []
datePublished = []
ratingValue = []
reviewBody = []
first_page = 1
last_page = 101
for i in range(first_page, last_page + 1):
    response = requests.get(
        f"https://www.trustpilot.com/review/listwithclever.com?page={i}").text
    soup = BeautifulSoup(response, "html.parser")
    reviews = soup.find_all(
        'section', class_='styles_reviewContentwrapper__zH_9M')

    for item in reviews:
        body = item.find(
            class_="typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn")
        if body == None:
            reviewBody.append("")
        else:
            reviewBody.append(body.getText())

        company = 'Clever Real Estate'
        companyName.append(company)

        date = item.find(
            class_="typography_body-m__xgxZ_ typography_appearance-default__AAY17 typography_color-black__5LYEn")
        if date == None:
            datePublished.append("")
        else:
            date_str = date.text.replace('Date of experience:', '')
            date_obj = datetime.strptime(date_str, ' %B %d, %Y')
            datePublished.append(date_obj.strftime('%Y-%m-%d'))

        rating = item.find(class_="styles_reviewHeader__iU9Px").find(
            'img').get('alt')
        if rating == None:
            ratingValue.append("")
        else:
            ratingValue.append(rating.split()[1])

df_reviews = pd.DataFrame(list(zip(companyName, reviewBody, datePublished, ratingValue)),
                          columns=['companyName', 'reviewBody', 'datePublished', 'ratingValue'])

df_reviews.to_csv('reviews.csv', index=False)
