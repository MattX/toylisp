import evaluate
import env
import misc

class NotAFunctionError(Exception): pass

class Value():
	def __str__(self):
		return "**Generic value (this is a bug)**"
	def evaluate(self, env):
		raise NotImplementedError
	def apply(self, values):
		raise NotAFunctionError(str(self))

class Nil(Value):
	def __str__(self):
		return '()'
	def evaluate(self, env):
		return self
	

class Int(Value):
	def __init__(self, value=0):
		self.value = value
	def __str__(self):
		return str(self.value)
	def evaluate(self, env):
		return self

class Bool(Value):
	def __init__(self, value=False):
		self.value = value
	def __str__(self):
		if self.value:
			return "#t"
		else:
			return "#f"
	def evaluate(self, env):
		return self

class String(Value):
	def __init__(self, value=""):
		self.value = value
	def __str__(self):
		return '"' + self.value + '"'
	def evaluate(self, env):
		return self

class Symbol(Value):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return self.value.upper()
	def evaluate(self, env):
		return env.getValue(self.value)

class Pair(Value):
	def __init__(self, car, cdr):
		self.vcar = car
		self.vcdr = cdr
	def insidePrint(self):
		if type(self.cdr()) is Nil:
			return str(self.car()) + ")"
		elif type(self.cdr()) is Pair:
			return str(self.car()) + " " + self.cdr().insidePrint()
		else:
			return str(self.car()) + " . " + str(self.cdr()) + ")"

	def __str__(self):
		return "(" + self.insidePrint()

	def evaluate(self, env):
		return evaluate.funcall(self.car(), self.cdr(), env)
	def car(self):
		return self.vcar
	def cdr(self):
		return self.vcdr

class Function(Value):
	def __init__(self):
		raise NotImplementedError

class Lambda(Function):
	def __init__(self, env, args, body):
		self.env = env
		self.args = args
		self.body = body
		self.macro = False
	def __str__(self):
		return ("macro " if self.macro else "") + "lambda function : " + str(self.args) + " -> " + str(self.body) + " in " + str(self.env)
	def evaluate(self, env):
		return self
	def apply(self, values):
		e = env.Env(self.env)
		argMappings = misc.filterMap(self.args, values)
		e.addDict(argMappings)
		return self.body.evaluate(e)


class Primitive(Function):
	def __init__(self, env, prim):
		self.env = env
		self.primitive = prim
		self.macro = False
	def __str__(self):
		return ("macro " if self.macro else "") + "primitive function : " + str(self.primitive)
	def evaluate(self, env):
		return self
	def apply(self, values):
		values = misc.pairsToList(values)
		return self.primitive(values)


def tests():
	i = Int(42)
	j = String("hello")
	k = Bool(False)
	l = Nil()
	p1 = Pair(i, k)
	print(p1)
	print(Pair(k, p1))
	print(Pair(p1, p1))
	print(Pair(p1, Pair(p1, Nil)))


if __name__ == '__main__':
	tests()
