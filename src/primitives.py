import objects
import misc
import env

class PrimitiveError(Exception): pass

def associate(sym, fun, environment):
	environment.addValue(sym, objects.Primitive(environment, fun))

def associatePrimitives(primitives, environment):
	for sym, fun in primitives.items():
		associate(sym, fun, environment)


def add(i, j):
	return objects.Int(i.value + j.value)

def mul(i, j):
	return objects.Int(i.value * j.value)

def sub(i, j):
	return objects.Int(i.value - j.value)

def div(i, j):
	return objects.Int(i.value // j.value)

def mod(i, j):
	return objects.Int(i.value % j.value)

def gt(i, j):
	return objects.Bool(i.value > j.value)

def bneg(b):
	return objects.Bool(not b.value)

def bor(b, c):
	return objects.Bool(b.value or c.value)

def band(b, c):
	return objects.Bool(b.value and c.value)

def catstr(s1, s2):
	return s1 + s2


# Primitives

def macroP(l):
	if len(l) != 1:
		raise PrimitiveError("macro: wrong number of args")
	f = l[0]
	if not isinstance(f, objects.Function):
		raise PrimitiveError("macro: expected " + f + " to be a function")
	f.macro = True
	return f

def nilP(l):
	if len(l) != 1:
		raise PrimitiveError("nil: wrong number of args")
	return objects.Bool(type(l[0]) is objects.Nil)

def consP(l):
	if len(l) != 2:
		raise PrimitiveError("cons: wrong number of args")
	return objects.Pair(l[0], l[1])

def carP(l):
	if len(l) != 1:
		raise PrimitiveError("car: wrong number of args")
	if not type(l[0]) is objects.Pair:
		raise PrimitiveError("car: not a pair")
	return l[0].car()

def cdrP(l):
	if len(l) != 1:
		raise PrimitiveError("cdr: wrong number of args")
	if not type(l[0]) is objects.Pair:
		raise PrimitiveError("cdr: not a pair")
	return l[0].cdr()

def plusP(l):
	if l == []:
		return objects.Int(0)
	else:
		return add(l[0], plusP(l[1:]))

def eqP(l):
	if len(l) != 2:
		raise PrimitiveError("eq: wrong number of args")
	else:
		return objects.Bool(l[0] is l[1])

def equalP(l):
	if len(l) != 2:
		raise PrimitiveError("=: wrong number of args")
	elif not type(l[0]) is type(l[1]):
		raise PrimitiveError("=: cannot compare objects of different types")
	elif not type(l[0]) in [objects.Bool, objects.Int, objects.String, objects.Symbol, objects.Nil]:
		raise PrimitiveError("=: cannot compare type " + str(type(l[0])))
	elif type(l[0]) is objects.Nil:
		return objects.Bool(True)
	else:
		return objects.Bool(l[0].value == l[1].value)

def applyP(l):
	if len(l) != 2:
		raise PrimitiveError("apply: wrong number of arguments")
	if not isinstance(l[0], objects.Functon) or not isinstance(l[1], objects.Pair):
		raise PrimitiveError("apply: wrong argument type")
	return l[0].apply(misc.pairsToList(l[1]))

#def evalP(l):
#	if len(l) != 1:
#		raise PrimitiveError("eval: wrong number of arguments")
#	return evaluate.eval(l[0], e)

def atomP(l):
	if len(l) != 1:
		raise PrimitiveError("atom: wrong number of arguments")
	return objects.Bool(misc.atom(l[0]))

def mulP(l):
	if len(l) != 2:
		raise PrimitiveError("*: wrong number of arguments")
	return mul(l[0], l[1])

def subP(l):
	if len(l) != 2:
		raise PrimitiveError("-: wrong number of arguments")
	return sub(l[0], l[1])

def gtP(l):
	if len(l) != 2:
		raise PrimitiveError(">: wrong number of arguments")
	return gt(l[0], l[1])
	
def printP(l):
	if len(l) != 1:
		raise PrimitiveError("print: wrong number of arguments")
	print(l[0])
	return objects.Nil()

def inputP(l):
	if len(l) > 1:
		raise PrimitiveError("input: wrong number of arguments")
	if len(l) == 1:
		res = input(l[0].value)
	else:
		res = input()
	return objects.String(res)
	
def gensymP(l):
	if len(l) != 0:
		raise PrimitiveError("gensym: wrong number of arguments")
	return objects.Symbol(misc.gensym())

