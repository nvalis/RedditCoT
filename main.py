import os
import requests
import getpass

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'}
username = 'XXX'
password = getpass.getpass('Reddit password: ')

url = 'https://www.reddit.com/api/guess_voting_key.json'

def login(session, username, password):
	r = session.get('https://www.reddit.com/api/requires_captcha/login.json', proxies=proxies)
	print(r.text)
	r = session.post('https://www.reddit.com/api/login/{}'.format(username), data=dict(api_type='json', op='login-main', passwd=password, user=username), proxies=proxies)
	print(r.text)

def try_password(session, circle_id, circle_password)
	data = dict(id=circle_id, raw_json=1, vote_key=circle_password)
	r = s.post(url, data=data, headers=headers, proxies=proxies, timeout=3)
	if r.status_code == requests.codes.ok:
		print(r.text)
	else:
		print('Error: {} ({})'.format(r.status_code, requests.status_codes._codes[r.status_code]))

s = requests.Session()
login(s, username, password)

circle_id = 't3_XXX'
circle_password = 'XXX'
try_password(s, circle_id, circle_password)
