import objects as o

last_gensym = 0

class ExecutionError(Exception): pass

def gensym():
	global last_gensym 
	last_gensym = last_gensym + 1
	return "__sym_" + str(last_gensym)

def pairsToList(pairs):
        if type(pairs) is o.Nil:
                return []
        elif type(pairs) is o.Pair:
                return [pairs.car()] + pairsToList(pairs.cdr())
        else:
                raise RuntimeError("pairsToList : " + str(pairs) + " is not a pair")

def listToPairs(l):
	if l == []:
		return o.Nil()
	else:
		return o.Pair(l[0], listToPairs(l[1:]))

def atom(a):
        return type(a) != o.Pair

def merge(d1, d2):
	for key in d2:
		d1[key] = d2[key]
	return d1

def filterMap(p1, p2):
	if type(p1) is o.Symbol:
		return { p1.value: p2 }
	elif not type(p1) is type(p2):
		raise misc.ExecutionError("filterMap: cannot filter " + str(p2) + " against " + str(p1))
	elif type(p1) is o.Pair:
		cmap = filterMap(p1.cdr(), p2.cdr())
		amap = filterMap(p1.car(), p2.car())
		return merge(cmap, amap)
	elif type(p1) is o.Nil:
		return {}
	else:
		raise misc.ExecutionError("filterMap: cannot filter against " + str(p1))

def tests():
	import ltoken as t
	import lparse as p
	
	print(str(pairsToList(p.parse(t.tokenize("(1 2 3 4)"))[0])))
	print(str(filterMap(p.parse(t.tokenize("(a b c)"))[0], p.parse(t.tokenize("(0 1 2)"))[0])))
	print(str(filterMap(p.parse(t.tokenize("(a b . c)"))[0], p.parse(t.tokenize("(0 1 2 3 4)"))[0])))
	print(str(filterMap(p.parse(t.tokenize("a"))[0], p.parse(t.tokenize("(0 1 2)"))[0])))
	print(str(filterMap(p.parse(t.tokenize("((name . args) . body)"))[0], p.parse(t.tokenize("((test x y) b0 b1)"))[0])))
	print(str(filterMap(p.parse(t.tokenize("((name . args) . body)"))[0], p.parse(t.tokenize("((test x . y) b0 b1)"))[0])))
	print(str(filterMap(p.parse(t.tokenize("((name . args) . body)"))[0], p.parse(t.tokenize("((test . y) b0 b1)"))[0])))

if __name__ == '__main__':
	tests()

