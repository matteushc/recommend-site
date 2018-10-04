import requests
import mysql.connector
import simplejson as json
import argparse

class Client:

	def send_url(self, base_url, url, userId):
		url = base_url + str(url) + "/view"
		user = {'userId': userId}
		self.make_post_request(url, user)		

	def get_url(self, base_url, url):
		url = base_url + str(url) + "/similar"
		self.make_get_request(url)

	def process(self, base_url):
		url = base_url + "process"
		self.make_get_request(url)

	def make_post_request(self, url, user):
		headers = {'Content-type': 'application/json'}
		r = requests.post(url, data=json.dumps(user), headers=headers)
		print(r.text)

	def make_get_request(self, url):
		r = requests.get(url)
		print(r.json())

if __name__=="__main__":
	parser = argparse.ArgumentParser(description="Creation Client to send similar url")
	parser.add_argument('-u','--url', metavar='url', type=str, help='url name')
	parser.add_argument('-i','--userId', metavar='userId', type=int, help='User id')
	parser.add_argument('-o','--host', metavar='host', type=str, help='host name')
	parser.add_argument('-t','--typeRequest', metavar='typeRequest', type=int, help='Type requests - 1 - POST, 2 - GET or 3 - PROCESS')
	args = parser.parse_args()

	cli = Client()
	if args.typeRequest == 1:
		cli.send_url(args.host, args.url, args.userId)
	elif args.typeRequest == 2:
		cli.get_url(args.host, args.url)
	elif args.typeRequest == 3:
		cli.process(args.host)
	else:
		print("Opcao nao existente! Digite --help para ajuda nas opcoes")