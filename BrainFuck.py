#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Python3

class BrainFuck:
	"""BrainFuck class to generate BrainFuck Variants
	"""
	OP=['nxt','prv','inc','dec','put','get','opn','cls']
	TOKEN=['>','<','+','-','.',',','[',']']
	BF_TOKEN=TOKEN[:]
	HELLO_WORLD='>+++++++++[<++++++++>-]<.>+++++++[<++++>-]<+.+++++++..+++.[-]>++++++++[<++++>-]<.>+++++++++++[<+++++>-]<.>++++++++[<+++>-]<.+++.------.--------.[-]>++++++++[<++++>-]<+.[-]++++++++++.'
	ARRAY_SIZE=30000
	SEP=''

	def __init__(self, token=TOKEN, asize=ARRAY_SIZE, debug=False):
		"""parameter description:
		asize   = array size
		map     = dictionary of OP and TOKEN
		stoken   = sorted TOKEN to be used in lexer()
		maxtlen = maximum length in tokens to be used in lexer()
		"""
		self.asize=asize
		self.TOKEN=token
		self.map=dict(zip(self.TOKEN, self.OP))
		self.stoken=sorted(self.TOKEN, key=lambda x: len(x), reverse=True)
		self.maxtlen=len(self.stoken[0])
		if debug: self.printparams()

	def printparams(self):
		"""print spec for debugging
		"""
		print ('***** Spec of "'+self.__class__.__name__+'" *****')
		print ('Array size = '+str(self.asize))
		print ('Token map = ')
		for t in self.TOKEN: 
			print ('  '+self.map[t]+' => '+t)
		print ('Sorted token map=')
		for t in self.stoken: 
			print ('  '+t+' ('+str(len(t))+')')
		print ('*' * (23+len(self.__class__.__name__)))

	def lexer(self, src, tokenlist, maxtlen=1):
		"""lexical analysis of src code
		"""
		tokens=[]
		cur=0
		clen=1
		while cur <= len(src):
			end=cur+clen
			t=src[cur:end]
			if clen > maxtlen:
				cur+=1
				clen-=1
				continue
			elif end == len(src)+1:
				cur+=1
				continue
			else:
				flag=False
				for tt in tokenlist:
					if t == tt:
						flag=True
						break
				if flag:
					tokens.append(t)
					cur+=len(t)
					clen=1
				else:
					clen+=1
					continue
		return tokens

	def translator(self, tokens, transmap):
		"""translate token to opcode
		"""
		return [transmap[t] for t in tokens]

	def executer(self, code):
		"""execute BrainFuck opcode
		"""
		import sys
		cur=0 # index of codes
		cell = [0 for i in range(self.asize)] # cell
		ptr=0 # pointer of cell
		while cur < len(code):
			c = code[cur]
			if c == 'nxt':
				ptr +=1
			if c == 'prv':
				ptr -=1
			if c == 'inc':
				cell[ptr] += 1
			if c == 'dec':
				cell[ptr] -= 1
			if c == 'put':
				sys.stdout.write(chr(cell[ptr]))
			if c == 'get':
				cell[ptr] = ord(raw_input("Enter>")[0])
			if c == 'opn' and cell[ptr] == 0:
				level=1
				while code[cur]!='cls' or level!=0:
					if cur <= len(code): cur+=1
					if code[cur]=='opn': level+=1
					if code[cur]=='cls': level-=1
			if c == 'cls' and cell[ptr] != 0:
				level=1
				while code[cur]!='opn' or level!=0:
					if cur >= 0: cur-=1
					if code[cur]=='opn': level-=1
					if code[cur]=='cls': level+=1
			cur+=1
		return True

	def run(self, src):
		"""run
		"""
		return self.executer(self.opcode(src))

	def opcode(self, src):
		"""output opcode
		"""
		lex=self.lexer(src, self.stoken, self.maxtlen)
		return self.translator(lex, self.map)

	def converter(self, src):
		"""convert original BrainFuck code to variant code
		"""
		lex=self.lexer(src, self.BF_TOKEN)
		uc=self.translator(lex, dict(zip(self.BF_TOKEN, self.TOKEN)))
		code=uc[:]
		return self.SEP.join(code)

	def hello_world(self):
		"""print "Hello World!" code and the result
		"""
		src=self.converter(self.HELLO_WORLD)
		print ("src =", src)
		print ("opcode =", self.opcode(src))
		return self.run(src)

class BrainCrash (BrainFuck):
	OP=['nxt','prv','inc','dec','put','get','opn','cls','or','and','not','xor']
	TOKEN=['>','<','+','-','.',',','[',']','|','&','~','^']
	BF_TOKEN=TOKEN[:]
	def init(self, cell):
		cell[0:12]=[72,101,108,108,111,44,32,119,111,114,108,100,33]
		return cell
	def end(self, cell):
		import sys
		for ptr in xrange(len(cell)):
			if cell[ptr] == 0: break
			sys.stdout.write(chr(cell[ptr]))
		return ptr
	def executer(self, code):
		"""execute BrainCrash opcode
		"""
		import sys
		cur=0 # index of codes
		cell = [0 for i in xrange(self.asize)] # cell
		ptr=0 # pointer of cell
		cell=self.init(cell)
		while cur < len(code):
			c = code[cur]
			if c == 'nxt':
				ptr +=1
			if c == 'prv':
				ptr -=1
			if c == 'inc':
				cell[ptr] += 1
			if c == 'dec':
				cell[ptr] -= 1
			if c == 'put':
				sys.stdout.write(chr(cell[ptr]))
			if c == 'get':
				cell[ptr] = ord(raw_input("Enter>")[0])
			if c == 'opn' and cell[ptr] == 0:
				level=1
				while code[cur]!='cls' or level!=0:
					if cur <= len(code): cur+=1
					if code[cur]=='opn': level+=1
					if code[cur]=='cls': level-=1
			if c == 'cls' and cell[ptr] != 0:
				level=1
				while code[cur]!='opn' or level!=0:
					if cur >= 0: cur-=1
					if code[cur]=='opn': level-=1
					if code[cur]=='cls': level+=1
			if c == 'or':
				cell[ptr+1]=cell[ptr] | cell[ptr+1]
				ptr+=1
			if c == 'and':
				cell[ptr+1]=cell[ptr] & cell[ptr+1]
				ptr+=1
			if c == 'xor':
				cell[ptr+1]=cell[ptr] ^ cell[ptr+1]
				ptr+=1
			if c == 'not':
				cell[ptr]= ~ cell[ptr]
			cur+=1
		ptr=self.end(cell)
		return True

if __name__ == "__main__":
	# base BrainFuck class
	b=BrainFuck()
	b.hello_world()

	# sample of variant class
	# kapibara class
	k=BrainFuck(token=['のすのす','もでーん','キュルッ！','もふっ！',	'むぎゅっと','グッ！！','ぬっくし','うっとり'])
	k.hello_world()