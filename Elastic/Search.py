
import json
import requests
import elastic_requests


def make_request(request):
	'''
	@param request:  Request object. Generates and calls request.
	@return:         JSON response

	'''
	response = request.generate()()
	response = json.loads(response.text)
	if response.get('statusCode') >= 300:
		print response.get('error')
		if response.get('message') == "Browser client is out of date, please refresh the page":
			print "Update kbn-version in the script to match the Kibana server version."
	return json.loads(response.text)

class ElasticSearch:


	def __init__(self):
		pass

	def validate_mac(self, mac):
		'''
		@param mac: A mac address, separated by hyphens or colons or no separators.
  					Has 12 characters (0-9, A-F)

		'''

		mac = mac.lower().replace('-','').replace(':','')
		if set(mac).intersection(set(['1','2','3','4','5',
									  '6','7','8','9','0',
									  'a','b','c','d','e',
									  'f'])) != set(mac):
			raise ElasticMacError("Did not pass a valid MAC address. Make sure it only includes characters 0-9 and A-F.")

		return mac


	#
	# @make_request(elastic_requests.MSEARCH)
	def search_mac(self, mac, request=None):
		mac = self.validate_mac(mac)
		elastic_requests.MSEARCH.generate(["logstash-2017.08.31"])

		import pdb; pdb.set_trace()





class ElasticMacError(Exception):
	'''
	Did not pass a valid MAC
	'''
