import objects

def parse_list(tokens): # assuming the initial '(' and possibly some elements have been parsed
                        # returns a pair : scanned object and rest of tokens
	if tokens == []:
		raise RuntimeError("Improper list")
	if tokens[0] == ')':
		return (objects.Nil(), tokens[1:])
	if tokens[0] == '.':
		(obj, rest) = parse(tokens[1:])
		if rest[0] != ')':
			raise RuntimeError("Random stuff after '.'")
		return (obj, rest[1:])		
	else:
		(obj, rest) = parse(tokens)
		(end, rest) = parse_list(rest)
		return (objects.Pair(obj, end), rest)

def parse(tokens): # returns (scanned object, rest of tokens)
	if tokens[0] == 'nil' or tokens[0] == '()':
		return (objects.Nil(), tokens[1:])

	if tokens[0] == '(':
		return parse_list(tokens[1:])
	if tokens[0] == ')' or tokens[0] == '.':
		raise RuntimeError("Parser : ??? at " + tokens)
	if tokens[0] == "'":
		(obj, rest) = parse(tokens[1:])
		return (objects.Pair(objects.Symbol("quote"), objects.Pair(obj, objects.Nil())), rest)
	
	if tokens[0] == "#t":
		return (objects.Bool(True), tokens[1:])
	if tokens[0] == "#f":
		return (objects.Bool(False), tokens[1:])
	if len(tokens[0]) >= 2 and tokens[0][0] == '"' and tokens[0][-1] == '"':
		return (objects.String(tokens[0][1:-1]), tokens[1:])
	try:
		i = int(tokens[0])
		return (objects.Int(i), tokens[1:])
	except ValueError:
		return (objects.Symbol(tokens[0]), tokens[1:])

def tests():
	print(parse(['1']))
	print(parse(['#t']))
	print(parse(['#t', 'nil']))
	print(str(parse(['(', '1', ')'])[0]))
	print(str(parse(['(', '1', '(', '2', '.', '3', ')', ')'])[0]))

if __name__ == '__main__':
	tests()
