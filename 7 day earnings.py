import requests
import insightly
import time

url = "https://api.na1.insightly.com/v3.1/Contacts?brief=false&top=600&count_total=false"

payload={}
headers = {
		'Authorization': 'Basic ZWFiOTY2NTYtNDU5NS00NDNjLWIzOTktMzgzNTVjM2E3MGQxOg==',
		'Cookie': 'snaptid=sac1prdc01wut01'
        }

response = requests.request("GET", url, headers=headers, data=payload)

response = response.json()

for item in response:
    for field in item['CUSTOMFIELDS']:
        if field['FIELD_NAME'] ==
