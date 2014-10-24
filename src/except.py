class RunError(Exception): pass

class TypeError(RunError): pass
class UndefinedError(RunError): pass
class PrimitiveError(RunError):
	def __init__(self, fun, message):
		self.fun = fun
		self.message = message
	def __str__(self):
		

