import objects
import env
import primitives as prim
import evaluate
import ltoken
import lparse
import misc

mainEnv = env.Env()
macroEnv = env.Env()


def tokEval(tok, environment, menv, silent=False):
	while(tok != []):
		(obj, tok) = lparse.parse(tok)
		try:
			res = evaluate.eval(obj, environment)
		except env.UndefinedError as e:
			print('* Undefined variable: ' + e.args[0])
		except objects.NotAFunctionError as e:
			print('* Not a function: ' + e.args[0])
		except misc.ExecutionError as e:
			print('* Error: ' + e.args[0])
		else:
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
		raise misc.ExecutionError("load: " + fname + " is not balanced")
	tokEval(ltoken.tokenize(code), mainEnv, macroEnv, True)

def loadP(l):
	if len(l) != 1:
		raise prim.PrimitiveError("load: wrong number of arguments")
	load(l[0].value)


def prepareEnv(environment):
	primitives = { "+": prim.plusP, "*": prim.mulP,
		       "-": prim.mulP, "-": prim.subP,
		       ">": prim.gtP, "eq": prim.eqP, "=": prim.equalP, "nil?": prim.nilP, "atom?": prim.atomP,
		       "cons": prim.consP, "car": prim.carP, "cdr": prim.cdrP,
		       "apply": prim.applyP,
		       "load": loadP,
		       "print": prim.printP, "input": prim.inputP,
		       "macro": prim.macroP, "gensym": prim.gensymP }
	prim.associatePrimitives(primitives, environment)
	environment.addValue("nil", objects.Nil())

def repl():
	prepareEnv(mainEnv)
	mainEnv.addValue("__cont", objects.Bool(True))
	while mainEnv.getValue("__cont").value == True:
		command = input(">>> ")
		while not exprOk(command):
			command = command + '\n' + input("... ")
		tokEval(ltoken.tokenize(command), mainEnv, macroEnv, False)

if __name__ == '__main__':
	repl()

