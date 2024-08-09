import requests
print(requests.get('http://localhost:8000/hotels/12', params={'date_from':'12/12/2012', 'date_to':'11/11/2011'}).text)
