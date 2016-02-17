class Canvas(object): 
	"""
	The main class to be instantiated to provide access to Canvas's API.
	""" 

	def __init__(self, base_url, access_token):
		"""
		:param base_url: string
		:param access_token: string
		"""
		self.__requester = Requester(base_url, access_token)
