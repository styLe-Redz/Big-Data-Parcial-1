import requests
from bs4 import BeautifulSoup
import json

def lambda_handler(event, context):
    url = "https://www.fincaraiz.com.co/venta/casa/bogota/chapinero/?ad=30|1||||1||8,9,16||116|1080001||||||||||||||||1|||1||griddate%20desc||||-1||"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    properties = []
    for result in soup.find_all('div', {'class': 'posting-card'}):
        title = result.find('h2', {'class': 'posting-title'}).text.strip()
        link = result.find('a', {'class': 'posting-link'}).get('href')
        price = result.find('span', {'class': 'posting-price'}).text.strip()

        property = {
            'title': title,
            'link': link,
            'price': price,
        }
        properties.append(property)

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': json.dumps(properties),
    }