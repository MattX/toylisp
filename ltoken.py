def partOfSym(char):
	return (not char.isspace() and char != "(" and char != ")" and
                    char != "'")

def tokenize(text):
	parsed = []
	acc = ""
	in_str = False
	for i in range(0, len(text)):
		if text[i] == '"':
			if not in_str:
				in_str = True
				if acc != "":
					parsed.append(acc)
					acc = ""
			else:
				in_str = False
				parsed.append('"' + acc + '"')
				acc = ""
		elif in_str:
			acc = acc + text[i]
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
