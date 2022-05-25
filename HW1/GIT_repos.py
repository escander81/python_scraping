import requests
import json


# user = 'escander81'
user = input("Enter the github username: ")
url = f'https://api.github.com/users/{user}/repos'

response = requests.get(url)
data_json = response.json()

for rep in data_json:
    if not rep['private']:
        print(f'{data_json.index(rep)}{")"} {rep["name"]}')
try:
    with open('GIT_repos.json', 'w') as f:
      json.dump(data_json, f, ensure_ascii=False, indent=4)
    print("Completed")
except:
    print("Failed")