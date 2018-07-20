#!/usr/bin/env python
# -*- coding: utf-8 -*-
## Python3

import sys

class OpToken(dict):
	"""OpToken class to store transrate map
	"""
	def __init__(self, optokendict={}):
		dict.__init__(self, optokendict)
	def tokens(self): ## output token list
		return list(self.values())
	def opcodes(self): ## output opcode list
		return list(self.keys())
	def sorted_tokens(self): ## sorted tokens by length
		return sorted(self.tokens(), key=lambda x: len(x), reverse=True)
	def swap(self): ## return new OpToken object to swap token and opcode
		return OpToken(dict(zip(self.tokens(), self.opcodes())))
	def replace_tokens(self, tokens): ## replace tokens with given list
		index=0
		for k in iter(self):
			self[k]=tokens[index]
			index+=1

class BrainFuck:
	"""BrainFuck class to generate BrainFuck Variants
	http://www.muppetlabs.com/~breadbox/bf/
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
		sep = separator of src code
		token = token list to replace with original token, easy to create variant
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
		tokenlist.sort(key=lambda x: len(x), reverse=True)
		maxtlen=len(tokenlist[0])
		while cur <= len(src)-1:
			end=cur+clen
			s=src[cur:end]
			if end > len(src):
				break
			elif clen > maxtlen:
				cur+=1
				clen=1
				continue
			elif s in tokenlist:
				tokens.append(s)
				cur+=len(s)
				clen=1
			elif s==sep:
				cur+=1
			elif re.match('\s', s):
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
		"""initialize before running
		"""
		self.ptr = 0 # pointer in executer()
		self.cur = 0 # index of codes
		self.cell = [0 for i in range(self.asize)] # cell

	def prepro(self, opcodes): ## pre-processing
		return opcodes

	def postpro(self, opcodes): ## post-processing
		return opcodes

	def op_nxt(self, opcodes): ## increment pointer (++ptr)
		self.ptr+=1

	def op_prv(self, opcodes): ## decrement pointer (--ptr)
		self.ptr-=1

	def op_inc(self, opcodes): ## increment the byte at pointer (++*ptr)
		self.cell[self.ptr]+=1

	def op_dec(self, opcodes): ## decrement the byte at pointer (--*ptr)
		self.cell[self.ptr]-=1

	def op_put(self, opcodes): ## output the byte at the pointer (putchar(*ptr))
		sys.stdout.write(chr(self.cell[self.ptr]))

	def op_get(self, opcodes): ## input a byte and store it in the byte at the pointer (*ptr = getchar())
		self.cell[self.ptr] = ord(raw_input("Enter>")[0])

	def op_opn(self, opcodes): ## jump forward past the matching ] if the byte at the pointer is zero (which (*ptr) {)
		if self.cell[self.ptr] != 0:
			return False
		level=1
		while opcodes[self.cur]!='cls' or level!=0:
			if self.cur <= len(opcodes): self.cur+=1
			if opcodes[self.cur]=='opn': level+=1
			if opcodes[self.cur]=='cls': level-=1

	def op_cls(self, opcodes): ## jump backward to the matching [ unless the byte at the pointer is zero (})
		if self.cell[self.ptr] == 0:
			return False
		level=1
		while opcodes[self.cur]!='opn' or level!=0:
			if self.cur >= 0: self.cur-=1
			if opcodes[self.cur]=='opn': level-=1
			if opcodes[self.cur]=='cls': level+=1

	def run(self, src):
		"""run src code
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

	def bfcode(self, src):
		"""output BrainFuck code
		"""
		op=self.opcodes(src)
		return ''.join(self.translator(op, self.BF_OPTOKEN))

	def hello_world(self):
		"""print "Hello World!" code and the result
		"""
		src=self.converter(self.HELLO_WORLD_SRC)
		print ("src =", src)
		print ("opcode =", self.opcodes(src))
		return self.run(src)

class Ook (BrainFuck):
	"""Ook! language
	http://www.dangermouse.net/esoteric/ook.html
	"""
	OOK_TOKEN=['Ook. Ook?','Ook? Ook.','Ook. Ook.','Ook! Ook!','Ook. Ook!','Ook! Ook.','Ook! Ook?','Ook? Ook!']
	def __init__(self, tokens=OOK_TOKEN):
		BrainFuck.__init__(self, tokens=tokens, sep=' ')

class BrainCrash (BrainFuck):
	"""BrainCrash language
	https://enpedia.rxy.jp/wiki/BrainCrash
	"""
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
		self.cell[0:12]=[72,101,108,108,111,44,32,119,111,114,108,100,33] # store "Hello, world!"
		if len(opcodes)>0:
			opcodes=['nxt']*13+opcodes # move pointer to run BF code
		return opcodes
	def postpro(self, opcodes):
		while self.cell[self.ptr]!=0: # after run opcodes, increment pointer to output the byte at pointer until byte==0
			sys.stdout.write(chr(self.cell[self.ptr]))
			self.ptr+=1
		return opcodes
	def op_or(self, opcodes): ## or 
		self.cell[self.ptr+1]=self.cell[self.ptr] | self.cell[self.ptr+1]
		self.ptr+=1
	def op_and(self, opcodes): ## and
		self.cell[self.ptr+1]=self.cell[self.ptr] & self.cell[self.ptr+1]
		self.ptr+=1
	def op_xor(self, opcodes): ## xor
		self.cell[self.ptr+1]=self.cell[self.ptr] ^ self.cell[self.ptr+1]
		self.ptr+=1
	def op_not(self, opcodes): ## not 
		self.cell[self.ptr+1]= ~ self.cell[self.ptr]

class CommDisCore(BrainCrash):
	"""extend class for CommDis language
	"""
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
	def op_shl(self, opcodes): ## bit shift left
		self.cell[self.ptr]<<1
	def op_shr(self, opcodes): ## bit shift right
		self.cell[self.ptr]>>1
	def op_njm(self, opcodes): ## increase pointer by the byte at pointer
		self.ptr+=self.cell[self.ptr]
	def op_pjm(self, opcodes): ## decrease pointer by the byte at pointer
		self.ptr-=self.cell[self.ptr]
	def op_zro(self, opcodes): ## set zero the byte at pointer 
		self.cell[self.ptr]=0
	def op_hom(self, opcodes): ## move pointer to 0
		self.ptr=0

class CommDis(CommDisCore):
	"""コミュ障プログラミング言語
	http://www.moonroom.mydns.jp/ls/software/commdis.htm
	"""
	CD_TOKEN=['ｱｱ…','ｱｱ､','ｱ…','ｱ､','ｴｯﾄ…','ｴｯﾄ､','ｻｾﾝ…','ｯｽ…','ｱｯ…','ｱｯ､','ｱﾉ…','ｱﾉ､','ｱｰ…','ｱｰ､','ｴ…','ｴ､','ｴｯ…','ｴｯ?']
	def __init__(self, tokens=CD_TOKEN):
		CommDisCore.__init__(self, tokens=tokens)

def test_bf():
	print('BrainFuck class:')
	b=BrainFuck()
	b.hello_world()
	print(b.opcodes('>>sample<<'))
	b.printparams()
	print('')

def test_bc():
	print('BrainCrash class:')
	c=BrainCrash()
	c.run('')
	print('')
	c.run('>+++++++++[<++++++++>-]<.>+++++++[<++++>-]<+.+++++++..+++.[-]>++++++++[<++++>-]<.>+++++++++++[<+++++>-]<.>++++++++[<+++>-]<.+++.------.--------.[-]>++++++++[<++++>-]<+.[-]++++++++++.')
	c.run('[-]&&&&&&&&&&&&&+++++++[>++++++++++<-]>-.<+++++++[>++++++<-]>-.++.-----------.-.+++++.--------') # output 'Enpedia'
	print('')
	print('')

def test_cd():
	print('CommDis class:')
	cd=CommDis()
	cd.hello_world()
	print(cd.opcode2tokens(['nxt','prv','hom','pjm','cls']))
	print('')
	fizzbuzzsrc="""ｱ…ｱ…ｱ…ｱ…ｱ…ｱ…ｻｾﾝ…ｱ､ｱｱ…ｱ…ｱ…ｱ…ｱ…ｱｱ…ｱｱ…ｱ…ｱｱ…ｱ…
ｱｱ…ｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｯｽ…ｱｱ…ｻｾﾝ…ｱｱ､ｱ…ｱ…ｱ…ｱ…ｱｱ…ｱｱ…ｱ…
ｱ…ｱ…ｱｱ…ｱ…ｱ…ｱ…ｱ…ｱｱ…ｱｱ…ｱ…ｱ…ｱ…ｱｱ…ｱ…ｱ…ｱ…ｱ…ｱ…
ｱｱ…ｱ…ｱ…ｱ…ｱ…ｱ…ｱｱ…ｱｱ…ｱｱ…ｱｱ…ｱｱ…ｱｱ…ｱ…ｱ…ｱｱ…ｱｱ…ｱ…
ｱ…ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱ､ｯｽ…ｱｱ､ｱ…ｱ…
ｱ…ｱ…ｱｱ…ｱ…ｱ…ｱ…ｱｱ…ｱ､ｱ､ｱｱ…ｱ…ｱ…ｱ…ｱｱ…ｱ､ｱｱ…ｱｱ…ｱ､ｱ､ｱ､
ｱｱ…ｱ…ｱ…ｱｱ…ｱｱ…ｱｱ…ｱ…ｱ…ｱ…ｱ…ｱ…ｻｾﾝ…ｱ､ｱｱ…ｱ…ｱ…ｱｱ…ｱ…
ｱ…ｱｱ､ｱｱ､ｯｽ…ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｻｾﾝ…ｱ､ｱｱ…ｱ､ｻｾﾝ…
ｱｱ…ｱｱ…ｱｱ…ｱｱ…ｱｱ…ｱｱ…ｱｱ…ｯｽ…ｱｱ…ｻｾﾝ…ｱｱ､ｱ…ｱ…ｱ…ｱｱ…ｴｯﾄ…
ｱｱ…ｴｯﾄ…ｱｱ…ｱｱ…ｱｱ…ｱｱ…ｴｯﾄ…ｴｯﾄ…ｱｱ…ｱｱ…ｱｱ…ｱ…ｱｱ､ｯｽ…ｱｱ､
ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱ､ｻｾﾝ…ｱｱ…ｱｱ…ｱｱ…ｱｱ…ｯｽ…ｱｱ…ｻｾﾝ…ｱｱ､ｱ…ｱ…ｱ…
ｱ…ｱ…ｱｱ…ｴｯﾄ…ｱｱ…ｴｯﾄ…ｱｱ…ｴｯﾄ…ｴｯﾄ…ｱｱ…ｱｱ…ｱｱ…ｱ…ｱｱ､ｯｽ…
ｱｱ…ｱｱ…ｱｱ…ｱｱ…ｱ…ｱｱ､ｱ､ｻｾﾝ…ｱｱ､ｱｱ､ｱｱ､ｯｽ…ｱｱ､ｻｾﾝ…ｻｾﾝ…ｱ､ｱｱ､
ｱｱ､ｱ…ｱｱ…ｱｱ…ｯｽ…ｱｱ…ｱｱ…ｱｱ…ｱ…ｱｱ…ｱ…ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｻｾﾝ…
ｱ､ｱｱ…ｱｱ…ｱ…ｱｱ…ｱ…ｱｱ…ｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｯｽ…ｱｱ､ｯｽ…ｱｱ…ｱｱ…ｻｾﾝ…
ｻｾﾝ…ｱ､ｯｽ…ｱｱ､ｯｽ…ｱｱ…ｻｾﾝ…ｱｱ…ｱｱ…ｱｱ…ｻｾﾝ…ｱｱ…ｴｯﾄ…ｱｱ､ｱｱ､ｴｯﾄ…
ｱｱ､ｱｱ､ｱｱ､ｯｽ…ｱｱ､ｻｾﾝ…ｴｯﾄ…ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｯｽ…ｱｱ…ｯｽ…ｱｱ…ｴｯﾄ…
ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｯｽ…"""
#	cd.run(fizzbuzzsrc)
	print(cd.bfcode(fizzbuzzsrc))
	print('')

def test_ook():
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
	# JoJo language