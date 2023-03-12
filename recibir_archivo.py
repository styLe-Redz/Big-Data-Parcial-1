import boto3
from datetime import datetime
from bs4 import BeautifulSoup


def f():
    nombre = str(datetime.today().strftime('%Y-%m-%d'))
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('landing-casas-1032498680')
    obj = bucket.Object(str(nombre + ".html"))
    body = obj.get()['Body'].read()
    html = BeautifulSoup(body, 'html.parser')
    data_casa = html.find_all('div', class_='listing listing-card')
    data_titulo = html.find_all('div', class_='listing-card__title')
    data_precio = html.find_all('div', class_='price')
    fecha_actual = datetime.today().strftime('%Y-%m-%d')
    linea_0 = "FechaDescarga, Info, Valor, NumHabitaciones, NumBanos, mts2\n"
    for i in range(len(data_casa)):
        ca = data_casa[i].find_all('div', class_='listing-card__properties')[0]
        linea_0 = linea_0 + fecha_actual + "," + \
            str(data_titulo[i].text) + "," + \
            str(data_precio[i].text) + "," + \
            str(data_casa[i]['data-rooms']) + "," + \
            str(ca.find_all('span')[1].text[:1]) + "," + \
            str(ca.find_all('span')[2].text) + \
            "\n"
    boto3.client('s3').put_object(Body=linea_0, Bucket='casas-fina-1032498680',
                                  Key=str(nombre+".csv"))