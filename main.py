# import eel
from random import randint
from pprint import pprint

# PRODUCTION = True

# eel.init('wgui')
# eel.start('', block=False, size=(1280, 720))

# @eel.expose
# def WindowClose():
# 	exit()

# @eel.expose
def GenTest(n, actions): # генерируем тесты
	rs = []
	for _ in range(n):
		nums = 0
		stack = []
		for j in range(actions):
			if nums > 1 and bool(randint(0, 1)) or nums >= actions - j: # black magic
				print(nums, j, actions - j)
				nums -= 1
				stack.append('+-*/'[randint(0, 3)])
			else:
				print(nums, j, actions - j)
				stack.append(str(randint(1, 512)))
				nums += 1
		t = {}
		t['answer'] = ''
		try: # выкидываем лишнее, если есть
			t['question'] = ' '.join(stack)
			t['correctAnswer'] = Calc(t['question'])
		except:
			stack.pop()
			t['question'] = ' '.join(stack)
			t['correctAnswer'] = Calc(t['question'])
		rs.append(t)
	return rs

# while True:
# 	eel.sleep(10)

def Calc(expr):
	expr = expr.split()
	stack = []
	for token in expr:
		if token == '+':
			b, a = stack.pop(), stack.pop()
			stack.append(a + b)
		elif token == '-':
			b, a = stack.pop(), stack.pop()
			stack.append(a - b)
		elif token == '*':
			b, a = stack.pop(), stack.pop()
			stack.append(a * b)
		elif token == '/':
			b, a = stack.pop(), stack.pop()
			stack.append(a / b)
		else:
			stack.append(int(token))
	return int(stack.pop())

pprint(GenTest(10, 10))