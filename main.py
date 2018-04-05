# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import json
import requests
import getpass

from secret import username, password, proxies


class CircleOfTrust():
	def __init__(self, username, password, proxies={}):
		self.session = requests.Session()
		self.session.proxies.update(proxies)
		self.session.trust_env = False  # https://stackoverflow.com/questions/30837839/how-can-i-set-a-single-proxy-for-a-requests-session-object#comment86036962_30839005
		self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'})
		self.login(username, password)

	@staticmethod
	def get_user_circle_url(username):
		return f'https://reddit.com/user/{username}/circle/embed'

	@staticmethod
	def get_vote_id(soup):
		return soup.find('input', {'class': 'link_fullname'})['value']

	@staticmethod
	def get_vote_hash(soup):
		return json.loads(soup.find(id='config').text[8:-1])['vote_hash']

	def login(self, username, password):
		print('Logging in...')
		self.session.get('https://www.reddit.com/api/requires_captcha/login.json')
		data = {'api_type': 'json', 'op': 'login-main', 'user': username, 'passwd': password}
		modhash = self.session.post(f'https://www.reddit.com/api/login/{username}', data=data).json()['json']['data']['modhash']
		self.session.headers.update({'x-modhash': modhash})
		print('Logged in.')

	def get_soup(self, url):
		r = self.session.get(url)
		return BeautifulSoup(r.text, 'html.parser')

	def get_password(self, username):
		soup = self.get_soup(self.get_user_circle_url(username))
		return soup.find(id='circle-passphrase')['value']

	def try_key(self, username, key):
		soup = self.get_soup(self.get_user_circle_url(username))
		data = {'id': self.get_vote_id(soup), 'raw_json': '1', 'vote_key': key}
		return self.session.post('https://www.reddit.com/api/guess_voting_key.json', data=data).json()

	def join(self, username):
		soup = self.get_soup(self.get_user_circle_url(username))
		data = {'id': self.get_vote_id(soup), 'dir': 1, 'vh': self.get_vote_hash(soup), 'isTrusted': False}
		return self.session.post(f'https://www.reddit.com/api/circle_vote.json?dir=1&id={vote_id}', data=data)

	def betray(self, username):
		soup = self.get_soup(self.get_user_circle_url(username))
		data = {'id': self.get_vote_id(soup), 'dir': -1, 'vh': self.get_vote_hash(soup), 'isTrusted': False}
		return self.session.post(f'https://www.reddit.com/api/circle_vote.json?dir=-1&id={vote_id}', data=data)


if __name__ == '__main__':
	cot = CircleOfTrust(username, password, proxies=proxies)
	print(cot.try_key('XXX', 'XXX'))
