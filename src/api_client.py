import requests

def get_location(ip):
    response = requests.get(f'http://freeipapi.com/api/json/{ip}')
    response.raise_for_status()
    data = response.json()
    return {
        "country": data['countryName'],
        "region": data['regionName'],
        "city": data['cityName'],
    }
