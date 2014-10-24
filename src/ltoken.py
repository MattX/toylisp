def partOfSym(char):
	return (not char.isspace() and char != "(" and char != ")" and
                    char != "'" and char != ',')

def tokenize(text):
	parsed = []
	acc = ""
	in_str = False
	in_comment = False
	for i in range(0, len(text)):
		if in_str and text[i] != '"':
			acc = acc + text[i]
		elif text[i] == ';':
			in_comment = True
			if acc != "":
				parsed.append(acc)
				acc = ""
		elif text[i] == '\n' and in_comment:
			in_comment = False
		elif in_comment:
			pass
		elif text[i] == '"':
			if not in_str:
				in_str = True
				if acc != "":
					parsed.append(acc)
					acc = ""
			else:
				in_str = False
				parsed.append('"' + acc + '"')
				acc = ""
		elif partOfSym(text[i]):
			acc = acc + text[i]
		elif text[i].isspace():
			if acc != "":
				parsed.append(acc)
				acc = ""
		else:
			if acc != "":
				parsed.append(acc)
				acc = ""
			parsed.append(text[i])

	if acc != "":
		parsed.append(acc)

	return parsed

def tests():
	 print(tokenize('(abc "def ghi ::-()" 3)'))

if __name__ == '__main__':
	tests()
