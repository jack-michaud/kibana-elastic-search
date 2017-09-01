

class Request:

	def __init__(self, url, payload, headers, querystring):
		'''
		@param url:          URL
		@param payload:      Data payload (with {keyword} in the string that will be formatted in generate)
		@param headers:      HTTP headers  (with {keyword} in the string that will be formatted in generate)
		@param querystring:  GET parameters (with {keyword} in the string that will be formatted in generate)

		'''
		self.url = url
		self.payload = payload
		self.headers = headers
		self.querystring = querystring

	def generate(**kwargs):
		'''
		@param(s):  The necessary keywords that will fully populate the payload & headers & querystring
		@return 

		'''

		try:
			self.payload.format(**kwargs)
			self.headers.format(**kwargs)
			self.querystring.format(**kwargs)
		except KeyError as e:
			raise Exception("Did not include the necessary keywords: {}".format(str(e)))

		return lambda x: requests.request("POST", self.url, \
											data=self.payload.format(**kwargs), \
											headers=self.headers.format(**kwargs), \
											params=self.querystring.format(**kwargs))


