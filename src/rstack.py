import misc

class EmptyError(Exception): pass

class Return():
    def __init_(self):
        pass

    def __str__(self):
        return "Default RI (this is a bug)"


class EvalReturn(Return):
    def __init__(self, env, obj):
        self.env = env
        self.obj = obj

    def __str__(self):
        return "Eval: " + str(self.obj) + ' in ' + str(self.env)

class FuncallReturn(Return):
    def __init__(self, env, fun, args, param = None):
        self.env = env
        self.fun = fun
        self.args = args
        if not param is None:
            self.param = param
        else:
            self.param = {}

    def __str__(self):
        return "Funcall: " + str(self.fun) + "{ " + str(self.args) + " }, params " + str(self.param)


class ReturnStack():
    def __init__(self, initial = None):
        if initial is None:
            self.stack = []
        else:
            self.stack = [initial]

    def push(self, retItem):
        self.stack.append(retItem)

    def pop(self):
        if len(self.stack) > 0:
            return self.stack.pop()
        else:
            raise EmptyError

    def isEmpty(self):
        return len(self.stack) == 0

    def __str__(self):
        return "RS: " + str(list(map(str, self.stack)))
