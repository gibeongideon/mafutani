import requests

url = "https://odds.p.rapidapi.com/v4/sports"

querystring = {"all":"true"}

headers = {
	"X-RapidAPI-Key": "SIGN-UP-FOR-KEY",
	"X-RapidAPI-Host": "odds.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)



import requests

url = "https://odds.p.rapidapi.com/v4/sports/upcoming/odds"

querystring = {"regions":"us","oddsFormat":"decimal","markets":"h2h,spreads","dateFormat":"iso"}

headers = {
	"X-RapidAPI-Key": "SIGN-UP-FOR-KEY",
	"X-RapidAPI-Host": "odds.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)


import requests

url = "https://odds.p.rapidapi.com/v4/sports/americanfootball_nfl/scores"

querystring = {"daysFrom":"3"}

headers = {
	"X-RapidAPI-Key": "SIGN-UP-FOR-KEY",
	"X-RapidAPI-Host": "odds.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)




