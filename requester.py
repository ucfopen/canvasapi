class Requester(object):
	"""
	Responsible for handling HTTP requests.
	"""

	def __init__(self, base_url, access_token):
		"""
		:param base_url: string
		:param access_token: string
		"""
		self.base_url = base_url
		self.access_token = access_token


	def request(method, endpoint, **kwargs):
		"""Makes a request to the Canvas API.

		:param method: string
		:param endpoint: string
		"""
		
		if method == 'GET':
			response = _get_request(self.base_url + endpoint, kwargs)

		if method == 'POST':
			response = _post_request(self.base_url + endpoint, kwargs)


	def _get_request(url, data):
		"""Issue a GET request to the specified endpoint with the data provided.
		
		:param url: string
		:param data: dict
		"""
		pass

	def _post_request(url, data):
		"""Issue a POST request to the specified endpoint with the data provided.
		
		:param url: string
		:param data: dict
		"""
		pass