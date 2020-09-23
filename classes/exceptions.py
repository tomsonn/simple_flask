class PageNumberNotFoundError(Exception):
	"""
		Exception raised when page number couldn't be parsed from string
	"""

	def __init__(self, message):
		self.message = message
		super().__init__(self.message)
