# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import json
import requests
import getpass

from secret import username, password, proxies


class CircleOfTrust():
	def __init__(self, username, password, proxies={}):
		self.session = requests.Session()
		self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'})
		self.proxies = proxies
		self.session.get('https://www.reddit.com/api/requires_captcha/login.json', proxies=self.proxies)
		data = {'op': 'login', 'user': username, 'passwd': password, 'rem': 'yes', 'api_type': 'json'}
		self.session.post(f'https://www.reddit.com/api/login/{username}', data=data, proxies=self.proxies)

	@staticmethod
	def get_user_circle_url(username):
		return f'https://reddit.com/user/{username}/circle/embed'

	@staticmethod
	def get_vote_id(soup):
		print(soup)
		return soup.find('input', {'class': 'link_fullname'})['value']

	@staticmethod
	def get_vote_hash(soup):
		return json.loads(soup.find(id='config').text[8:-1])['vote_hash']

	def get_soup(self, url):
		r = self.session.get(url, proxies=self.proxies)
		return BeautifulSoup(r.text, 'html.parser')

	def get_password(self, username):
		soup = self.get_soup(self.get_user_circle_url(username))
		return soup.find(id='circle-passphrase')['value']

	def try_key(self, username, key):
		soup = self.get_soup(self.get_user_circle_url(username))
		data = {'id': self.get_vote_id(soup), 'vote_key': key}
		return self.session.post(f'https://www.reddit.com/api/guess_voting_key.json', data=data, proxies=self.proxies)

	def join(self, username):
		soup = self.get_soup(self.get_user_circle_url(username))
		data = {'id': self.get_vote_id(soup), 'dir': 1, 'vh': self.get_vote_hash(soup), 'isTrusted': False}
		return self.session.post(f'https://www.reddit.com/api/circle_vote.json?dir=1&id={vote_id}', data=data, proxies=self.proxies)

	def betray(self, username):
		soup = self.get_soup(self.get_user_circle_url(username))
		data = {'id': self.get_vote_id(soup), 'dir': -1, 'vh': self.get_vote_hash(soup), 'isTrusted': False}
		return self.session.post(f'https://www.reddit.com/api/circle_vote.json?dir=-1&id={vote_id}', data=data, proxies=self.proxies)


if __name__ == '__main__':
	cot = CircleOfTrust(username, password, proxies=proxies)
	print(cot.try_key('BluApex', 'Testing').text)
