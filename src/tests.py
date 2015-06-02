import run
import unittest

def equivalent(o1, o2):
	if not type(o1) is type(o2):
		return False
	if type(o1) == run.objects.Nil:
		return True
	if type(o1) in [run.objects.Bool, run.objects.Int, run.objects.String, run.objects.Symbol]:
		return o1.value == o2.value
	elif type(o1) == run.objects.Pair:
		return equivalent(o1.car(), o2.car()) and equivalent(o1.cdr(), o2.cdr())
	else:
		return o1 is o2

def evString(text):
	run.tokEval(run.ltoken.tokenize(text), run.mainEnv, True)



class Tokenizer(unittest.TestCase):
	def test_empty(self):
		self.assertEqual(run.ltoken.tokenize(""), [])
	
	def test_comment(self):
		self.assertEqual(run.ltoken.tokenize("some stuff\nother stuff ;comment\n" +
                                                "and; another comment\n;full line"),
		            ['some', 'stuff', 'other', 'stuff', 'and'])

	def test_quote(self):
		self.assertEqual(run.ltoken.tokenize("'(abc) '5 '6 (quote sym)"),
			   ["'", '(', 'abc', ')', "'", '5', "'", '6', '(', 'quote', 'sym', ')'])

	def test_string(self):
		self.assertEqual(run.ltoken.tokenize('hello "string" "longer string" '+
                                                '"string with ; comment" "string with \'quote"'),
		           ['hello', '"string"', '"longer string"', '"string with ; comment"',
                                     '"string with \'quote"'])


class BasicParse(unittest.TestCase):
	def basic_helper(self, text): # checks rest is [] and returns obj
		tok = run.ltoken.tokenize(text)
		(obj, rest) = run.lparse.parse(tok)
		self.assertEqual(rest, [])
		return obj

	def test_int(self):
		pos = self.basic_helper("42")
		neg = self.basic_helper("-25")
		self.assertTrue(type(pos) is run.objects.Int and type(pos) is run.objects.Int)
		self.assertTrue(pos.value == 42 and neg.value == -25)

	def test_string(self):
		obj = self.basic_helper('"string"')
		self.assertTrue(type(obj) is run.objects.String)
		self.assertTrue(obj.value == "string")
	
	def test_bool(self):
		true = self.basic_helper("#t")
		false = self.basic_helper("#f")
		self.assertTrue(type(true) is run.objects.Bool and type(false) is run.objects.Bool)
		self.assertTrue(true.value == True and false.value == False)

	def test_nil(self):
		obj = self.basic_helper("()")
		self.assertTrue(type(obj) is run.objects.Nil)

	def test_symbol(self):
		obj = self.basic_helper("025-sym")
		self.assertTrue(type(obj) is run.objects.Symbol)
		self.assertTrue(obj.value == "025-sym")
	

class PairParse(unittest.TestCase):
	def basic_helper(self, text): # checks rest is [] and returns obj
		tok = run.ltoken.tokenize(text)
		(obj, rest) = run.lparse.parse(tok)
		self.assertEqual(rest, [])
		return obj

	def test_pair(self):
		obj = self.basic_helper("(a . b)")
		self.assertTrue(equivalent(obj,
		      run.objects.Pair(run.objects.Symbol('a'), run.objects.Symbol('b'))))

	def test_pointedList(self):
		obj = self.basic_helper("(a b . c)")
		self.assertTrue(equivalent(obj,
                      run.objects.Pair(run.objects.Symbol('a'),
                             run.objects.Pair(run.objects.Symbol('b'), run.objects.Symbol('c')))))

	def test_list(self):
		obj = self.basic_helper("(a b c)")
		self.assertTrue(equivalent(obj,
                      run.objects.Pair(run.objects.Symbol('a'),
                             run.objects.Pair(run.objects.Symbol('b'),
		             run.objects.Pair(run.objects.Symbol('c'), run.objects.Nil())))))

	def test_nested1(self): pass

	def test_nested2(self): pass
		
	def test_garbage(self):
		with self.assertRaises(run.lparse.ParseError):
			self.basic_helper("(a b c . d e)")
		with self.assertRaises(run.lparse.ParseError):
			self.basic_helper("(a b c")
		with self.assertRaises(run.lparse.ParseError):
			self.basic_helper(")")
		with self.assertRaises(run.lparse.ParseError):
			self.basic_helper(".")


class Environment():
	def setUp(self):
		pass

class BasicEval(unittest.TestCase):
	def setUp(self):
		self.e = run.env.Env() # empty environment

	def test_int(self):
		i = run.objects.Int(5)
		self.assertEqual(i, i.evaluate(self.e))

	def test_string(self):
		s = run.objects.String("abc")
		self.assertEqual(s, s.evaluate(self.e))
	
	# test_bool, test_nil are skipped


class QuoteForm(unittest.TestCase):
	def setUp(self):
		self.e = run.env.Env()
	
	def test_quote_int(self):
		i = run.objects.Int(42)

class ComplexLambda(unittest.TestCase):
	def test_withdraw(self):
		evString('(define! mw (lambda (init) ((lambda (bal) (lambda (n) (set! bal (- bal n)))) init)))')
		evString('(define! W1 (mw 50)) (define! W2 (mw 70))')
		self.assertTrue(equivalent(evString('(W1 10)'), run.objects.Int(40)))
		self.assertTrue(equivalent(evString('(W2 0)'), run.objects.Int(70)))


if __name__ == '__main__':
	unittest.main()

