import objects as o

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
		return o.Pairs(l[0], listToPairs(l[1:]))

def tests():
	import ltoken as t
	import lparse as p
	
	print(pairsToList(p.parse(t.tokenize("(1 2 3 4)"))[0]))


if __name__ == '__main__':
	tests()

