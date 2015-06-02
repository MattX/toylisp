import misc

class EmptyError(Exception): pass

class ReturnStack():
    def __init__(self):
        self.stack = []

    def push(self, fun, args, env):
        self.stack.append((fun, args, env))

    def pop(self):
        if len(self.stack) > 0:
            return self.stack.pop(self)
        else:
            raise EmptyError

    def isEmpty(self):
        return len(self.stack) > 0
