import eel
from random import randint
from pprint import pprint

from pairs import pairs
import example as ex
from config import config as CONFIG

PRODUCTION = True

eel.init('wgui')
eel.start('', block=False, size=CONFIG['WIN_SIZE'])

@eel.expose
def WindowClose():
	exit()

lastSentTest = [None]
name, group = '', ''

@eel.expose
def GetTime():
	return CONFIG['TIME']

@eel.expose
def GenTest(_name, _group, train, trainNum=None): # генерируем тесты
	global name, group
	name, group = _name, _group
	n, actions = trainNum or CONFIG['TASKS'], CONFIG['TOKENS']
	rs = []
	for _ in range(n):
		nums = 0
		stack = []
		for j in range(actions):
			if nums > 1 and bool(randint(0, 1)) or nums >= actions - j: # black magick
				nums -= 1
				stack.append('+-*/'[randint(0, 3)])
			else:
				stack.append(str(randint(CONFIG['NUM_MIN'], CONFIG['NUM_MAX'])))
				nums += 1
		t = {}
		t['answer'] = None
		try: # выкидываем лишнее, если есть. AKA костыль
			t['question'] = ' '.join(stack)
			t['correctAnswer'] = str(Calc(t['question']))
		except:
			stack.pop()
			t['question'] = ' '.join(stack)
			t['correctAnswer'] = str(Calc(t['question']))
		rs.append(t)
	global lastSentTest
	lastSentTest = []
	for v in rs:
		lastSentTest.append(dict(v))
	if not train:
		for i in range(len(rs)):
			rs[i]['correctAnswer'] = None
	# print(lastSentTest)
	return rs


@eel.expose
def Judge(test, train):
	global lastSentTest
	total = len(lastSentTest)
	done = 0
	tasks = [] # выходная таблица, для GUI (!)
	for i in range(len(lastSentTest)):
		v = lastSentTest[i]
		ok = isinstance(test[i]['answer'], str) and test[i]['answer'].strip() == v['correctAnswer'] # верность ответа
		lastSentTest[i]['answer'] = test[i]['answer'] # пишем ответ в выход
		if ok:
			done += 1
		tasks.append({
			'answer': test[i]['answer'],
			'correctAnswer': v['correctAnswer'],
			'correct': ok
		})
	mark = done / total
	if not train:
		# print(tasks)
		ex.SendToServer(CONFIG['IP'], name, group, mark, lastSentTest)
	vmark = 0
	for i, threshold in pairs(CONFIG['VRATES']):
		if mark * 100 >= threshold:
			vmark = 5 - i
			break
	return { 'tasks': tasks, 'mark': mark, 'vmark': vmark }


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
	
while True:
	eel.sleep(10)