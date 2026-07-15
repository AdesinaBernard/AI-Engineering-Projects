import json
from urllib.request import urlopen

with urlopen("https://api.github.com") as response:
	data = json.load(response)

print(data)
