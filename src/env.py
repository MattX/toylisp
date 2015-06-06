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
	def setValue(self, name, value):
		if name in self.bindings:
			self.bindings[name] = value
		elif self.parent is None:
			raise UndefinedError(name)
		else:
			self.parent.setValue(name, value)
	def addValue(self, name, value):
		self.bindings[name] = value
	def addDict(self, d):
		for key in d:
			self.addValue(key, d[key])
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

