#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

## Python3
class OpToken(dict):
	def __init__(self, optokendict={}):
		dict.__init__(self, optokendict)
	def tokens(self):
		return self.values()
	def opcodes(self):
		return self.keys()
	def sorted_tokens(self): # sorted tokens by length
		return sorted(self.tokens(), key=lambda x: len(x), reverse=True)
	def swap(self): # return new OpToken object to swap token and opcode
		return OpToken(dict(zip(self.tokens(), self.opcodes())))
	def replace_tokens(self, tokens): # replace tokens with given list
		index=0
		for k in iter(self):
			self[k]=tokens[index]
			index+=1

class BrainFuck:
	"""BrainFuck class to generate BrainFuck Variants
	"""
	BF_OPTOKEN_DICT = dict( # BrainFuck opcode and token
		nxt = '>',
		prv = '<',
		inc = '+',
		dec = '-',
		put = '.',
		get = ',',
		opn = '[',
		cls = ']'
	)
	BF_OPTOKEN = OpToken(BF_OPTOKEN_DICT)
	OPTOKEN_DICT = dict(BF_OPTOKEN_DICT.items())
	HELLO_WORLD_SRC = '>+++++++++[<++++++++>-]<.>+++++++[<++++>-]<+.+++++++..+++.[-]>++++++++[<++++>-]<.>+++++++++++[<+++++>-]<.>++++++++[<+++>-]<.+++.------.--------.[-]>++++++++[<++++>-]<+.[-]++++++++++.'
	ARRAY_SIZE = 30000 # default cell array size
	SEP = '' # default separator

	def __init__(self, optoken_dict=OPTOKEN_DICT, asize=ARRAY_SIZE, sep=SEP, tokens=None, debug=False):
		"""parameter description:
		optoken_dict = dict of op and token
		asize  = cell array size
		"""
		self.asize = asize
		self.sep = sep
		self.optoken = OpToken(optoken_dict)
		if tokens!=None:
			if type(tokens) == list and len(tokens) == len(self.optoken):
				self.optoken.replace_tokens(tokens)
			else:
				raise TypeError('arg tokens is not proper list')
		if debug: self.printparams()
		self.initialize()

	def printparams(self):
		"""print spec for debugging
		"""
		header = '***** Spec of "'+self.__class__.__name__+'" *****'
		print(header)
		print('Array size = '+str(self.asize))
		print('Token/Opcode map = ')
		tokenop = self.optoken.swap()
		for t in tokenop:
			print('  '+t+' => '+tokenop[t])
		print('*' * (len(header)))

	def lexer(self, src, tokenlist, sep=''):
		"""lexical analysis of src code and return tokens list
		"""
		import re
		tokens=[]
		cur=0
		clen=1
		while cur <= len(src)-1:
			end=cur+clen
			s=src[cur:end]
			if end > len(src):
				break
			if s in tokenlist:
				tokens.append(s)
				cur+=len(s)
				clen=1
			elif s==' ':
				cur+=1
			elif re.match('\s', src):
				cur+=1
			else:
				clen+=1
		return tokens

	def translator(self, tokens, transmap):
		"""translate tokens by transmap
		"""
		return [transmap[t] for t in tokens]

	def executer(self, opcodes):
		"""execute opcodes
		"""
		opcodes = self.prepro(opcodes)
		while self.cur < len(opcodes):
			c = opcodes[self.cur]
			try:
				eval('self.op_'+c+'(opcodes)')
			except NameError:
				print('function for '+c+' ('+self.optoken[c]+') is not defined yet')
				sys.exit() 
			self.cur+=1
		opcodes = self.postpro(opcodes)
		return True

	def initialize(self):
		self.ptr = 0 # pointer in executer()
		self.cur = 0 # index of codes
		self.cell = [0 for i in range(self.asize)] # cell

	def prepro(self, opcodes):
		return opcodes

	def postpro(self, opcodes):
		return opcodes

	def op_nxt(self, opcodes):
		self.ptr+=1

	def op_prv(self, opcodes):
		self.ptr-=1

	def op_inc(self, opcodes):
		self.cell[self.ptr]+=1

	def op_dec(self, opcodes):
		self.cell[self.ptr]-=1

	def op_put(self, opcodes):
		sys.stdout.write(chr(self.cell[self.ptr]))

	def op_get(self, opcodes):
		self.cell[self.ptr] = ord(raw_input("Enter>")[0])

	def op_opn(self, opcodes):
		if self.cell[self.ptr] != 0:
			return False
		level=1
		while opcodes[self.cur]!='cls' or level!=0:
			if self.cur <= len(opcodes): self.cur+=1
			if opcodes[self.cur]=='opn': level+=1
			if opcodes[self.cur]=='cls': level-=1

	def op_cls(self, opcodes):
		if self.cell[self.ptr] == 0:
			return False
		level=1
		while opcodes[self.cur]!='opn' or level!=0:
			if self.cur >= 0: self.cur-=1
			if opcodes[self.cur]=='opn': level-=1
			if opcodes[self.cur]=='cls': level+=1

	def run(self, src):
		"""run
		"""
		self.initialize()
		opcode = self.opcodes(src)
		return self.executer(opcode)

	def opcodes(self, src):
		"""output opcodes list
		"""
		tokens = self.lexer(src, self.optoken.sorted_tokens(), sep=self.sep)
		return self.translator(tokens, self.optoken.swap())

	def opcode2tokens(self, opcodes):
		"""transrate opcodes to tokens
		"""
		return self.translator(opcodes, self.optoken)

	def opcode2src(self, opcodes):
		"""output src from opcodes list
		"""
		return self.sep.join(self.opcode2tokens(opcodes))
		
	def converter(self, src):
		"""convert original BrainFuck code to variant code
		"""
		lex=self.lexer(src, self.BF_OPTOKEN.tokens())
		return self.sep.join(self.translator(lex, dict(zip(self.BF_OPTOKEN.tokens(), self.optoken.tokens()))))

	def hello_world(self):
		"""print "Hello World!" code and the result
		"""
		src=self.converter(self.HELLO_WORLD_SRC)
		print ("src =", src)
		print ("opcode =", self.opcodes(src))
		return self.run(src)

class Ook (BrainFuck):
	OOK_TOKEN=['Ook. Ook?','Ook? Ook.','Ook. Ook.','Ook! Ook!','Ook. Ook!','Ook! Ook.','Ook! Ook?','Ook? Ook!']
	def __init__(self, tokens=OOK_TOKEN):
		BrainFuck.__init__(self, tokens=tokens, sep=' ')

class BrainCrash (BrainFuck):
	BC_OPTOKEN_DICT={
		'or':'|',
		'and':'&',
		'not':'~',
		'xor':'^'
	}
	OPTOKEN_DICT = dict(BrainFuck.OPTOKEN_DICT.items())
	OPTOKEN_DICT.update(BC_OPTOKEN_DICT)
	def __init__(self, optoken_dict=OPTOKEN_DICT, asize=BrainFuck.ARRAY_SIZE, tokens=None, debug=False):
		BrainFuck.__init__(self, optoken_dict=optoken_dict, asize=asize, tokens=tokens)
	def prepro(self, opcodes):
		self.cell[0:12]=[72,101,108,108,111,44,32,119,111,114,108,100,33] ## store "Hello, world!"
		if len(opcodes)>0:
			opcodes=['nxt']*13+opcodes
		return opcodes
	def postpro(self, opcodes):
		while self.cell[self.ptr]!=0:
			sys.stdout.write(chr(self.cell[self.ptr]))
			self.ptr+=1
		return opcodes
	def op_or(self, opcodes):
		self.cell[self.ptr+1]=self.cell[self.ptr] | self.cell[self.ptr+1]
		self.ptr+=1
	def op_and(self, opcodes):
		self.cell[self.ptr+1]=self.cell[self.ptr] & self.cell[self.ptr+1]
		self.ptr+=1
	def op_xor(self, opcodes):
		self.cell[self.ptr+1]=self.cell[self.ptr] ^ self.cell[self.ptr+1]
		self.ptr+=1
	def op_not(self, opcodes):
		self.cell[self.ptr+1]= ~ self.cell[self.ptr]

class CommDisCore(BrainCrash):
	CDC_OPTOKEN_DICT=dict(
		shl = '*',
		shr = '/',
		njm = '{',
		pjm = '}',
		zro = '!',
		hom = '?'
	)
	OPTOKEN_DICT = dict(BrainCrash.OPTOKEN_DICT.items())
	OPTOKEN_DICT.update(CDC_OPTOKEN_DICT)
	ARRAY_SIZE = 32767
	def __init__(self, optoken_dict=OPTOKEN_DICT, asize=ARRAY_SIZE, tokens=None, debug=False):
		BrainCrash.__init__(self, optoken_dict=optoken_dict, asize=asize, tokens=tokens)
	def op_shl(self, opcodes): # left shift
		self.cell[self.ptr]<<1
	def op_shr(self, opcodes): # right shift
		self.cell[self.ptr]>>1
	def op_njm(self, opcodes):
		self.ptr+=self.cell[self.ptr]
	def op_pjm(self, opcodes):
		self.ptr-=self.cell[self.ptr]
	def op_zro(self, opcodes):
		self.cell[self.ptr]=0
	def op_hom(self, opcodes):
		self.ptr=0

class CommDis(CommDisCore):
	CD_TOKEN=['ｱｱ…','ｱｱ､','ｱ…','ｱ､','ｴｯﾄ…','ｴｯﾄ､','ｻｾﾝ…','ｯｽ…','ｱｯ…','ｱｯ､','ｱﾉ…','ｱﾉ､','ｱｰ…','ｱｰ､','ｴ…','ｴ､','ｴｯ…','ｴｯ?']
	def __init__(self, tokens=CD_TOKEN):
		CommDisCore.__init__(self, tokens=tokens)

def test_bf():
	# BrainFuck class
	print('BrainFuck class:')
	b=BrainFuck()
	b.hello_world()
	print(b.opcodes('>>sample<<'))
	b.printparams()
	print('')

def test_bc():
	# BrainCrash class
	print('BrainCrash class:')
	c=BrainCrash()
	c.run('')
	print('')
	c.run('>+++++++++[<++++++++>-]<.>+++++++[<++++>-]<+.+++++++..+++.[-]>++++++++[<++++>-]<.>+++++++++++[<+++++>-]<.>++++++++[<+++>-]<.+++.------.--------.[-]>++++++++[<++++>-]<+.[-]++++++++++.')
	c.run('[-]&&&&&&&&&&&&&+++++++[>++++++++++<-]>-.<+++++++[>++++++<-]>-.++.-----------.-.+++++.--------')
	print('')
	print('')

def test_cd():
	# CommDis class
	print('CommDis class:')
	cd=CommDis()
	cd.hello_world()
	print(cd.opcode2tokens(['nxt','prv','hom','pjm','cls']))
	print('')

def test_ook():
	# Ook class
	print('Ook class:')
	o=Ook()
	o.hello_world()
	print('')

if __name__ == "__main__":
	# test
	test_bf()
	test_bc()
	test_ook()
	test_cd()
	# sample variant of BrainFuck
	# kapibara language
	print('kapibara variant:')
	k=BrainFuck(tokens=['のすのす','もでーん','キュルッ！','もふっ！', 'むぎゅっと','グッ！！','ぬっくし','うっとり'], sep=' ')
	k.hello_world()
