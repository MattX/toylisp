class UndefinedError(Exception): pass

class Env():
	def __init__(self, parent=None):
		self.parent=parent
		self.bindings = {}
	def getValue(self, name):
		try:
			return self.bindings[name]
		except KeyError:
			if self.parent != None:
				return self.parent.getValue(name)
			else:
				raise UndefinedError(name)
	def sv(self, name, value, bottom=True):
		if name in self.bindings:
			self.bindings[name] = value
			return True
		else:
			if self.parent and self.parent.sv(name, value, False):
				return True
			elif bottom:
				self.bindings[name] = value
				return True
			else:
				return False
	def setValue(self, name, value):
		self.sv(name, value, True)
	def showEnv(self, parent=True):
		print("Env listing" + (" (with parents)" if parent else ""))
		for i in self.bindings:
			print(i, "->", self.bindings[i])
		if parent and self.parent:
			self.parent.showEnv(True)


def tests():
	e = Env()
	e.setValue('x', 5)
	e.setValue('y', "Hello")
	f = Env(e)
	print("5 :", f.getValue('x'))
	f.setValue('x', 8)
	print("8 :", f.getValue('x'))
	g = Env(e)
	print("5 :", g.getValue('x'))
	try:
		e.getValue('undef')
	except UndefinedError:
		print("OK")

if __name__=='__main__':
	tests()

