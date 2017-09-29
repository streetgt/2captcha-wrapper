#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, time, json

class TwoCaptcha:

	def __init__(self, key, soft_id=None, log=None):
		self.settings = {
			'request_url': 'http://2captcha.com/res.php',
			'insert_url': 'http://2captcha.com/in.php',
			'key': key,
			'json': 1,
			'soft_id': '' if soft_id is None else soft_id
		}

		if log:
			self.log = log
			self.logenabled = True
		else:
			self.logenabled = False
			

	def get_balance(self):
		"""
		Returns your current acccount balance
		:return: <YOURBALANCE> OK | EXCEPTION!
		"""
		payload = {
			'key': self.settings['key'],
			'action': 'getbalance',
			'json': self.settings['json']
		}
		
		r = requests.post(self.settings['request_url'], data=payload)
		response = json.loads(r.text)
		if response['status'] == 1:
			if self.logenabled:
				self.log.info("[TwoCaptcha] Balance: %s" % response['request'])
			return response['request']

		TwoCaptcha.raise_exception(response['request'])

	def upload(self, googlekey, pageurl, pingbackurl=None):
		"""
		Providing the googlekey and pageurl requests the token
		:param str googlekey: the google key
		:param str pageurl: the page url
		:param pingbackurl: pingback url
		:type pingbackurl: str or None
		:return: <request_id> OK | 1 ERROR!
		"""
		payload = {
			'key' : self.settings['key'],
			'method' : 'userrecaptcha',
			'json' : self.settings['json'],
			'soft_id' : self.settings['soft_id'],
			'googlekey' : googlekey,
			'pageurl': pageurl
		}

		if pingbackurl is not None:
			payload['pingback'] = pingbackurl

		r = requests.post(self.settings['insert_url'], data=payload)
		response = json.loads(r.text)
		if response['status'] == 1:
			if self.logenabled:
				self.log.info("[TwoCaptcha] Resolve reCaptcha request ID: %s" % response['request'])
			return response['request']

		TwoCaptcha.raise_exception(response['request'])

	def resolve_captcha(self, googlekey, pageurl, waittime = 15):
		"""
		Resolves the captcha and returns the token when its ready
		:param googlekey: the google key
		:param pageurl: the page url
		:return: <token> OK | 1 ERROR!
		"""
		if waittime < 15:
			raise CaptchaException("You can't set less that 15 seconds to resolve a captcha!")

		captcha_id = self.upload(googlekey, pageurl)
		time.sleep(waittime)
		token = self.get_response(captcha_id)

		while token is None:
			time.sleep(5)
			token = self.get_response(captcha_id)
			if token is not None:
				break

		return token

	def get_response(self, id, excep=False):
		"""
		Gets the token from the required captcha
		:param int id: the id from the required captha
		:return: <token> OK | EXCEPTION!
		"""
		payload = {
			'key' : self.settings['key'],
			'action' : 'get',
			'id': id,
			'json': self.settings['json']
		}

		r = requests.post('http://2captcha.com/res.php', data=payload)
		response = json.loads(r.text)

		if response['status'] == 0 and response['request'] == "CAPCHA_NOT_READY":
			return None
		elif response['status'] == 1:
			if self.logenabled:
				self.log.info("[TwoCaptcha] Response from get token: %s" % response['request'])
			return response['request']
		
		if excep is True:
			TwoCaptcha.raise_exception(response['request'])

	def complain(self, request_id):
		"""
		Providing the googlekey and pageurl requests the token
		:param int id: id from the resolved captcha
		:return: <request> OK | EXCEPTION!
		"""
		payload = {
			'key' : self.settings['key'],
			'action' : 'reportbad',
			'json' : self.settings['json'],
			'id' : request_id
		}

		r = requests.post(self.settings['request_url'], data=payload)
		response = json.loads(r.text)
		if response['status'] == 1:
			if self.logenabled:
				self.log.info("[TwoCaptcha] Your complaint about ID %s has been sent" % response['request'])
			return response['request']
		
		TwoCaptcha.raise_exception(response['request'])

	def add_pingback(self, url):
		"""
		Register new pingback URL
		:param str url: pingback url
		:return: <request> OK | EXCEPTION!
		"""
		payload = {
			'key' : self.settings['key'],
			'action' : 'add_pingback',
			'json' : self.settings['json'],
			'addr' : url
		}

		r = requests.post(self.settings['request_url'], data=payload)

		response = json.loads(r.text)
		if response['status'] == 1:
			if self.logenabled:
				self.log.info("[TwoCaptcha] Added URL (%s) to pingback " % response['request'])
			return response['request']
		
		TwoCaptcha.raise_exception(response['request'])

	def get_pingback(self):
		"""
		Get the list of your pingback URLs
		:return: <pingback list> OK | EXCEPTION!
		"""
		payload = {
			'key' : self.settings['key'],
			'action' : 'get_pingback',
			'json' : self.settings['json']
		}

		r = requests.post(self.settings['request_url'], data=payload)
		response = json.loads(r.text)
		if response['status'] == 1:
			if self.logenabled:
				self.log.info("[TwoCaptcha] Your pingback url list: %s" % response['request'])
			return response['request'].split("|")
		
		TwoCaptcha.raise_exception(response['request'])

	def delete_pingback(self,addr=None,all=False):
		"""
		Delete a pingback url or all
		:param addr: pingback url
		:type addr: str or None
		:param all: all pingbacks url
		:type all: bool or False
		:return: <request> OK | EXCEPTION!
		"""
		payload = {
			'key' : self.settings['key'],
			'action' : 'del_pingback',
			'json' : self.settings['json']
		}

		if addr is None and all is False:
			raise PingbackException("You need to specify or a URL or set all true.")
		elif addr is not None and all is not False:
			raise PingbackException("You can't have both request, choose a single URL providing url or set all to true.")

		payload['addr'] = addr if addr is not None else 'all'

		r = requests.post(self.settings['request_url'], data=payload)
		response = json.loads(r.text)
		if response['status'] == 1:
			if self.logenabled:
				self.log.info("[TwoCaptcha] Deleted ping back %s" % response['request'])
			return response['request']
		
		TwoCaptcha.raise_exception(response['request'])

	@staticmethod
	def raise_exception(string):
		if string == "ERROR_KEY_DOES_NOT_EXIST":
			raise KeyException("The key you've provided does not exists.")
		elif string == "ERROR_WRONG_ID_FORMAT":
			raise CaptchaException("Wrong format ID CAPTCHA. ID must contain only numbers")
		elif string == "ERROR_PAGEURL":
			raise AccessDeniedException("Page URL is missing in the request.")
		elif string == "ERROR_ZERO_BALANCE":
			raise BalanceException("You don't have money on your account.")
		elif string == "IP_BANNED":
			raise AccessDeniedException("Your IP address is banned due to many frequent attempts to access the server using wrong authorization keys.")
		elif string == "ERROR_NO_SLOT_AVAILABLE":
			raise AccessDeniedException("Error related to queue or maximum rate.")
		elif string == "ERROR_IP_NOT_ALLOWED":
			raise AccessDeniedException("The request is sent from the IP that is not on the list of your allowed IPs")
		elif string == "MAX_USER_TURN":
			raise AccessDeniedException("You made more than 60 requests within 3 seconds")
		if string == "CAPCHA_NOT_READY":
			raise CaptchaException("Your captcha is not resolved yet.")
		elif string == "ERROR_CAPTCHA_UNSOLVABLE":
			raise CaptchaException("We are unable to solve your captcha - three of our workers were unable solve it or we didn't get an answer within 90 seconds.")
		elif string == "ERROR_WRONG_USER_KEY":
			raise KeyException(" You've provided key parameter value in incorrect format, it should contain 32 symbols!")
		elif string == "ERROR_WRONG_CAPTCHA_ID":
			raise CaptchaException("You've provided incorrect captcha ID.")
		elif string == "ERROR_BAD_DUPLICATES":
			raise AccessDeniedException("The error means that max numbers of tries is reached but min number of matches not found.")
		elif string == "REPORT_NOT_RECORDED":
			raise AccessDeniedException("You already complained lots of correctly solved captchas.")
		
		
class AccessDeniedException(Exception):
	pass

class CaptchaException(Exception):
	pass

class BalanceException(Exception):
	pass

class PingbackException(Exception):
	pass

class KeyException(Exception):
	pass