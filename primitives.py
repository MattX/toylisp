import objects
import misc

class PrimitiveError(Exception): pass

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

def atom(a):
	return type(a) != objects.Pair


# Primitives

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

def evalP(l):
	if len(l) != 1:
		raise PrimitiveError("eval: wrong number of arguments")
	return evaluate(l[0])

def atomP(l):
	if len(l) != 1:
		raise PrimitiveError("atom: wrong number of arguments")
	return objects.Bool(atom(l[0]))

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
	
