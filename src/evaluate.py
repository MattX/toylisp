import objects
import env
import misc

def quote(expr, env, depth = 1):
	if misc.atom(expr):
		return expr
	elif type(expr.car()) is objects.Symbol and expr.car().value == "unquote" and depth == 1:
		return expr.cdr().car().evaluate(env)
	elif type(expr.car()) is objects.Symbol and expr.car().value == "quote":
		return objects.Pair(quote(expr.car(), env, depth+1), quote(expr.cdr(), env, depth+1))
	else:
		return objects.Pair(quote(expr.car(), env, depth), quote(expr.cdr(), env, depth))

def funcall(fun, args, env):
#	print("------------")
#	print(fun, args, env)
#	env.showEnv()
	if type(fun) is objects.Symbol:
		# formes speciales
		if fun.value == "quote":
			return quote(args.car(), env)
		elif fun.value == "if":
			res = args.car().evaluate(env)
			if not type(res) is objects.Bool:
				raise misc.ExecutionError("Type of " + str(args.car()) + " is not Bool")
			else:
				if res.value == True:
					return args.cdr().car().evaluate(env)
				elif type(args.cdr().cdr()) is objects.Nil:
					return objects.Nil()
				else:
					return args.cdr().cdr().car().evaluate(env)
		elif fun.value == "begin":
			ops = misc.pairsToList(args)
			for i in range(0, len(ops) - 1):
				ops[i].evaluate(env)
			if len(ops) == 0:
				return objects.Nil()
			else:
				return ops[-1].evaluate(env)
		elif fun.value == "set!" or fun.value == "define!":
			if type(args.cdr()) is objects.Nil():
				raise misc.ExecutionError(fun.value + " expects two arguments")
			newVal = args.cdr().car().evaluate(env)
			if not type(args.car()) is objects.Symbol:
				raise misc.ExecutionError(fun.value + " expects a symbol as its first argument")
			if fun.value == "set!":
				env.setValue(args.car().value, newVal)
			else:
				env.addValue(args.car().value, newVal)
			return newVal
		elif fun.value == "lambda":
			return objects.Lambda(env, args.car(), objects.Pair(objects.Symbol("begin"), args.cdr()))
		
		#macro
		elif env.getValue(fun.value).macro:
			r = fun.evaluate(env).apply(args)
			#print(r)
			return r.evaluate(env)


	#fonction normale
	largs = misc.pairsToList(args)
	evaluated = misc.listToPairs(list(map(lambda x: x.evaluate(env), largs)))
	return fun.evaluate(env).apply(evaluated)


def eval(obj, env):
	return obj.evaluate(env)

def tests():
	e = env.Env()
	print(objects.Pair(objects.Symbol("if"), objects.Pair(objects.Bool(True), objects.Pair(objects.Int(4), objects.Pair(objects.Int(5), objects.Nil())))).evaluate(e))
	print(objects.Pair(objects.Symbol("set!"), objects.Pair(objects.Symbol("x"), objects.Pair(objects.Int(42), objects.Nil()))).evaluate(e))
	print(objects.Symbol("x").evaluate(e))

if __name__ == '__main__':
	tests()
