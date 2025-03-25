#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import re

url = "https://www.theblueground.com/sp?placeId=ct-eyJ0eXBlIjoiY2l0eSIsImxhdCI6MzkuNzY5MDksImxuZyI6LTg2LjE1ODAxOH0"

# Proxy configuration with login and password
proxy_host = 'gw.dataimpulse.com'
proxy_port = 823
proxy_login = 'bcbe2708f411937425ee'
proxy_password = '2aa0320b266a3c90'
proxy = f'http://{proxy_login}:{proxy_password}@{proxy_host}:{proxy_port}'

proxies = {
    'http': proxy,
    'https': proxy
}

response = requests.get(url, proxies=proxies)

soup = BeautifulSoup(response.text, 'html.parser')

apt_list = soup.find_all('a', class_='property')
prop_name_list = soup.find_all('span', class_='property__name')
address_list = soup.find_all('span', class_='property__address')
prop_id_list = soup.find_all('span', class_='property__id')

#print("Property Name List:", prop_name_list)
#print("*" *50)
#print("address list", address_list)
#print("*" * 50)
#print("Property ID list", prop_id_list)


def find_apt_by_criteria(apt_list, beds, baths, size):
    filtered_di = {}
    for i in range(len(apt_list)):
        url = "https://www.theblueground.com" + apt_list[i].get('href')
        details = apt_list[i].find_all('div', class_='listing-amenities__amenity')
        details_red = re.findall(">[0-9]<", str(details))
        apt_size = re.findall(">[0-9]*,*[0-9]+ ft", str(details))
        det_formatted = [det.strip("<>") for det in details_red]
        if len(det_formatted) == 1:
            det_formatted.insert(0, 0)
        det_formatted.append((str(apt_size).strip(">ft[]' ")).replace(",", ""))
        bedrooms, bathrooms, sqft = det_formatted
        if int(bedrooms) == beds and int(bathrooms) == baths and int(sqft) >= size:
            property_name = prop_name_list[i].get('title')
            property_address = address_list[i].text
            prop_id = prop_id_list[i].text.strip("ID:").replace(" ", "")
            filtered_di[prop_id] = property_name, property_address
    print("The following apartments meet your criteria!")    
    for i in range(len(filtered_di)):
        print("Apartment ID: " + list(filtered_di.keys())[i])
        print("Apartment Address: " + str(list(filtered_di.values())[i]))
        print("Link to Apartment: " + "https://www.theblueground.com/p/furnished-apartments/usa-" + str(list(filtered_di.keys())[i]))



find_apt_by_criteria(apt_list, 2, 2, 400)
