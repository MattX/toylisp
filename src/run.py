import objects
import env
import primitives as prim
import evaluate
import ltoken
import lparse

mainEnv = env.Env()

def associate(sym, fun):
	mainEnv.addValue(sym, objects.Primitive(mainEnv, fun))

def tokEval(tok, env, silent=False):
	while(tok != []):
		(obj, tok) = lparse.parse(tok)
		res = evaluate.eval(obj, env)
		if not silent:
			print(res)

def exprOk(text):
	toks = ltoken.tokenize(text)
	bal = 0
	for i in range(0, len(toks)):
		if toks[i] == '(':
			bal = bal + 1
		elif toks[i] == ')':
			bal = bal - 1
	return bal <= 0

def load(fname):
	with open (fname, "r") as infile:
		code = infile.read()
	if not exprOk(code):
		raise RuntimeError("load: " + fname + " is not balanced")
	tokEval(ltoken.tokenize(code), mainEnv, True)

def loadP(l):
	if len(l) != 1:
		raise prim.PrimitiveError("load: wrong number of arguments")
	load(l[0].value)

associate("+", prim.plusP)
associate("*", prim.mulP)
associate("-", prim.subP)
associate(">", prim.gtP)
associate("cons", prim.consP)
associate("car", prim.carP)
associate("cdr", prim.cdrP)
associate("atom", prim.atomP)
associate("eq", prim.eqP)
associate("=", prim.equalP)
#associate("eval", prim.evalP)
associate("apply", prim.applyP)
associate("load", loadP)
associate("print", prim.printP)
associate("input", prim.inputP)
associate("macro", prim.macroP)
associate("gensym", prim.gensymP)
associate("isnil", prim.nilP)
mainEnv.addValue("nil", objects.Nil())

def repl():
	mainEnv.addValue("__cont", objects.Bool(True))
	while mainEnv.getValue("__cont").value == True:
		command = input(">>> ")
		while not exprOk(command):
			command = command + '\n' + input("... ")
		tokEval(ltoken.tokenize(command), mainEnv, False)

if __name__ == '__main__':
	repl()

