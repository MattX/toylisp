import objects
import env
import misc
import rstack

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
		# special forms
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
			# TODO : check args.car() is a proper arg sequence
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


def oldEval(obj, env):
	return obj.evaluate(env)

def newQuote(stack, last, ans):
	expr = last.args.car()
	env = last.env
	param = last.param

	param['depth'] = param.get('depth', 1)

	if misc.atom(expr):
		ans.append(expr)
	elif type(expr.car()) is objects.Symbol and expr.car().value == "unquote" and param['depth'] == 1:
		stack.push(rstack.EvalReturn(env, expr.cdr().car()))
	else:
		if type(expr.car()) is objects.Symbol and expr.car().value == "quote":
			new_depth = param['depth'] + 1
		else:
			new_depth = param['depth']

		if not param.get('gotValues', False):
			param['gotValues'] = True
			stack.push(rstack.FuncallReturn(env, last.fun, last.args, param))
			stack.push(rstack.FuncallReturn(env, objects.Symbol("quote"), objects.Pair(expr.car(), objects.Nil()), {'depth': new_depth}))
			stack.push(rstack.FuncallReturn(env, objects.Symbol("quote"), objects.Pair(expr.cdr(), objects.Nil()), {'depth': new_depth}))
		else:
			car = ans.pop()
			cdr = ans.pop()

			ans.append(objects.Pair(car, cdr))

def newIf(stack, last, ans):
	fun = last.fun
	args = last.args
	env = last.env
	param = last.param

	if not param.get('checkedCond', False):
		param['checkedCond'] = True
		stack.push(rstack.FuncallReturn(env, fun, args, param))
		stack.push(rstack.EvalReturn(env, args.car()))
	else:
		res = ans.pop()
		if not type(res) is objects.Bool:
			raise misc.ExecutionError("Type of " + str(args.car()) + " is not Bool")
		else:
			if res.value:
				stack.push(rstack.EvalReturn(env, args.cdr().car()))
			elif type(args.cdr().cdr()) is objects.Nil:
				ans.append(objects.Nil())
			else:
				stack.push(rstack.EvalReturn(env, args.cdr().cdr().car()))

def newBegin(stack, last, ans):
	fun = last.fun
	args = last.args
	env = last.env
	param = last.param

	if not param.get('gotValues', False):
		param['gotValues'] = True
		ops = misc.pairsToList(args)
		param['beginLen'] = len(ops)

		if len(ops) == 0:
			ans.append(objects.Nil())
		else:
			stack.push(rstack.FuncallReturn(env, fun, args, param))
			for i in range(2, len(ops) + 1): # evaluate all but the last expression
				stack.push(rstack.EvalReturn(env, ops[len(ops) - i]))

	else:
		ops = misc.pairsToList(args)
		for _ in range(0, param['beginLen'] - 1):
			ans.pop()
		stack.push(rstack.EvalReturn(env, ops[len(ops) - 1]))

def newDefine(stack, last, ans): # define! AND set!
	fun = last.fun
	args = last.args
	env = last.env
	param = last.param

	if type(args.cdr()) is objects.Nil():
		raise misc.ExecutionError(fun.value + " expects two arguments")

	if not param.get('gotValues', False):
		param['gotValues'] = True
		stack.push(rstack.FuncallReturn(env, fun, args, param))
		stack.push(rstack.EvalReturn(env, args.cdr().car()))
	else:
		newVal = ans.pop()
		if not type(args.car()) is objects.Symbol:
			raise misc.ExecutionError(fun.value + " expects a symbol as its first argument")
		if fun.value == "set!":
			env.setValue(args.car().value, newVal)
		else:
			env.addValue(args.car().value, newVal)
		ans.append(newVal)

def newApply(stack, last, ans):
	fun = last.fun
	args = last.args
	env = last.env
	param = last.param

	largs = misc.pairsToList(last.args)
	if not param.get('gotFunction', False):
		param['gotFunction'] = True
		stack.push(rstack.FuncallReturn(env, fun, args, param))
		stack.push(rstack.EvalReturn(env, fun))

	elif not param.get('gotValues', False):
		param['gotValues'] = True
		param['funobj'] = ans.pop()
		param['macro'] = param['funobj'].macro
		if not param['macro']:
			stack.push(rstack.FuncallReturn(env, fun, args, param))
			for arg in largs:
				stack.push(rstack.EvalReturn(env, arg))
			return

	if param.get('gotFunction', False) and param.get('gotValues', False):
		fun = param['funobj']

		if not param['macro']:
			evaluated = []
			for _ in largs:
				evaluated.insert(0, ans.pop())
			evaluated = list(reversed(evaluated))
		else:
			evaluated = largs

		res = fun.apply(misc.listToPairs(evaluated))
		if isinstance(res, rstack.Return):
			stack.push(res)
		elif param['macro']:
			stack.push(rstack.EvalReturn(env, res))
		else:
			ans.append(res)

def eval(obj, env):
	ans = []
	stack = rstack.ReturnStack(rstack.EvalReturn(env, obj))

	while not stack.isEmpty():
		print("			ans is", ans, "stack is", stack)
		last = stack.pop()

		if type(last) is rstack.EvalReturn:
			res = last.obj.evaluate(last.env)
			if isinstance(res, rstack.Return):
				stack.push(res)
			else:
				ans.append(res)

		else: # we have to evaluate a pair
			fun = last.fun
			if type(fun) is objects.Symbol and fun.value in ['quote', 'if', 'begin', 'set!', 'define*', 'lambda']:
				# special forms
				if fun.value == "quote":
					newQuote(stack, last, ans)

				elif fun.value == "if":
					newIf(stack, last, ans)

				elif fun.value == "begin":
					newBegin(stack, last, ans)

				elif fun.value == "set!" or fun.value == "define*":
					newDefine(stack, last, ans)

				elif fun.value == "lambda":
					# TODO : check args.car() is a proper arg sequence
					ans.append(objects.Lambda(last.env, last.args.car(), objects.Pair(objects.Symbol("begin"), last.args.cdr())))

			else:
				newApply(stack, last, ans)

	print("			ans is", ans, "stack is", stack)


	if len(ans) > 1:
		print("**WARN : return stack not empty")

	return ans.pop()


def tests():
	e = env.Env()
	print(objects.Pair(objects.Symbol("if"), objects.Pair(objects.Bool(True), objects.Pair(objects.Int(4), objects.Pair(objects.Int(5), objects.Nil())))).evaluate(e))
	print(objects.Pair(objects.Symbol("set!"), objects.Pair(objects.Symbol("x"), objects.Pair(objects.Int(42), objects.Nil()))).evaluate(e))
	print(objects.Symbol("x").evaluate(e))

if __name__ == '__main__':
	tests()
