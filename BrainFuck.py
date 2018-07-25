#!/usr/bin/env python
# -*- coding: utf-8 -*-
## Python3

import sys

class OpToken(dict):
    """OpToken class to store token/opcode transration map
    """
    def __init__(self, optokendict={}):
        if type(optokendict)!= dict:
            raise TypeError('argument is not dict')
        for k in optokendict:
            v = optokendict[k]
            optokendict[k] = [v] if type(v)!=list else v
        super().__init__(optokendict)
    def __setitem__(self, key, val):
        dict.__setitem__(self, key, val if type(val)==list else [val])
    def alltokens(self): ## output all token list
        return sum(self.values(), [])
    def tokens(self): ## output 1st token of all opcodes
        return [self[s][0] for s in self.opcodes()]
    def opcodes(self): ## output opcode list
        return list(self.keys())
    def opcode(self, token): ## output opcode by given token
        for o in self.opcodes():
            if token in self[o]:
                return o
        return None
    def token(self, opcode, index=0): ## output token of given opcode 
        return self[opcode][index]
    def token2opcode_dict(self): ## return dict as {t:o}
        return dict([(t, self.opcode(t)) for t in self.alltokens()])
    def opcode2token_dict(self): ## return dict as {opcode:token} (1st token only)
        return dict(zip(self.opcodes(), self.tokens()))
    def replace_tokens(self, tokens): ## replace tokens with given list
        if type(tokens)!=list:
            raise TypeError('arg tokens is not list')
        if len(self)!=len(tokens):
            raise IndexError('index of given tokens is not matched')
        return self.__init__(dict(zip(self.opcodes(), tokens)))

class BrainFuck:
    """BrainFuck class to generate BrainFuck Variants
    http://www.muppetlabs.com/~breadbox/bf/
    """
    OPTOKEN_DICT = dict( # BrainFuck opcode and token
        nxt = '>',
        prv = '<',
        inc = '+',
        dec = '-',
        put = '.',
        get = ',',
        opn = '[',
        cls = ']'
    )
    ARRAY_SIZE = 30000 # default cell array size
    SEP = '' # default separator
    TOKENS = None # default token list to be used replacement
    BF_HELLO_WORLD_SRC = '>+++++++++[<++++++++>-]<.>+++++++[<++++>-]<+.+++++++..+++.[-]>++++++++[<++++>-]<.>+++++++++++[<+++++>-]<.>++++++++[<+++>-]<.+++.------.--------.[-]>++++++++[<++++>-]<+.[-]++++++++++.'

    def __init__(self, optoken_dict=None, asize=None, sep=None, tokens=None, debug=False):
        """parameter description:
        """
        self.asize = asize if asize!=None else self.ARRAY_SIZE # cell array size
        self.sep = sep if sep!=None else self.SEP # separator to output src code
        self.optoken = OpToken(optoken_dict) if optoken_dict!=None else OpToken(self.OPTOKEN_DICT) # OpToken of opcode and token transmap dict
        if self.TOKENS!=None:
            self.optoken.replace_tokens(self.TOKENS)
        if tokens!=None:
            self.optoken.replace_tokens(tokens)
        self.debug = debug
        if self.debug:
            self.printparams()
        self.initializer()

    def printparams(self):
        """print spec for debugging
        """
        header = '***** Spec of "'+self.__class__.__name__+'" *****'
        print(header)
        print('Array size = '+str(self.asize))
        print('Token/Opcode map:')
        for t in self.optoken.alltokens():
            print('  '+t+' => '+self.optoken.opcode(t))
        print('*' * (len(header)))
        return True

    def lexer(self, src, tokenlist):
        """lexical analysis of src code and return tokens list
        """
        tokens = []
        cur = 0 ## current position in src
        ctoken = None
        while cur <= len(src)-1:
            str = src[cur:]
            start = len(str)
            for token in tokenlist:
                index = str.find(token)
                if index>=0 and (index<start or (index==start and start+len(ctoken)<index+len(token))):
                    ctoken = token
                    start = index
            if self.debug:
                print('LEXER:', len(tokens), cur, ctoken, str[start:32])
            if ctoken!=None:
                tokens.append(ctoken)
                cur+=str.find(ctoken)+len(ctoken)
                ctoken = None
            else:
                break
        return tokens

    def translator(self, tokens, trans_dict):
        """translate tokens by transmap
        """
        if self.debug:
            for t in tokens:
                print('TRANSLATOR:', t, '=>', trans_dict[t])
        return [trans_dict[t] for t in tokens]

    def executer(self, opcodes):
        """execute opcodes
        """
        opcodes = self.preproc(opcodes)
        while self.cur < len(opcodes):
            c = opcodes[self.cur]
            if self.debug:
                print('EXECUTER:', c, self.cur, self.ptr, self.cell[self.ptr])
            try:
                eval('self.op_'+c+'(opcodes)')
            except NameError:
                print('function for '+c+' ('+self.optoken[c]+') is not defined yet')
                sys.exit() 
            self.cur+=1
            opcodes = self.stepproc(opcodes)
        opcodes = self.postproc(opcodes)
        return True

    def initializer(self):
        """initialize before running
        """
        self.ptr = 0 # pointer in executer()
        self.cur = 0 # index of codes
        self.cell = [0 for i in range(self.asize)] # cell
        return True

    def preproc(self, opcodes): ## pre-processing
        return opcodes

    def stepproc(self, opcodes): ## process at each step
        return opcodes

    def postproc(self, opcodes): ## post-processing
        return opcodes

    def op_nxt(self, opcodes): ## increment pointer (++ptr)
        self.ptr+=1
        return True

    def op_prv(self, opcodes): ## decrement pointer (--ptr)
        self.ptr-=1
        return True

    def op_inc(self, opcodes): ## increment the byte at pointer (++*ptr)
        self.cell[self.ptr]+=1
        return True

    def op_dec(self, opcodes): ## decrement the byte at pointer (--*ptr)
        self.cell[self.ptr]-=1
        return True

    def op_put(self, opcodes): ## output the byte at the pointer (putchar(*ptr))
        try:
            sys.stdout.write(chr(self.cell[self.ptr]))
        except UnicodeEncodeError:
            sys.stdout.write(str(self.cell[self.ptr].to_bytes(1,'big'))+' ')
        return True

    def op_get(self, opcodes): ## input a byte and store it in the byte at the pointer (*ptr = getchar())
        self.cell[self.ptr] = ord(input("Enter>")[0])
        return True

    def op_opn(self, opcodes): ## jump forward past the matching ] if the byte at the pointer is zero (which (*ptr) {)
        if self.cell[self.ptr] != 0:
            return False
        level=1
        while opcodes[self.cur]!='cls' or level!=0:
            if self.cur <= len(opcodes): self.cur+=1
            if opcodes[self.cur]=='opn': level+=1
            if opcodes[self.cur]=='cls': level-=1
        return True

    def op_cls(self, opcodes): ## jump backward to the matching [ unless the byte at the pointer is zero (})
        if self.cell[self.ptr] == 0:
            return False
        level=1
        while opcodes[self.cur]!='opn' or level!=0:
            if self.cur >= 0: self.cur-=1
            if opcodes[self.cur]=='opn': level-=1
            if opcodes[self.cur]=='cls': level+=1
        return True

    def run(self, src):
        """run src code
        """
        self.initializer()
        opcode = self.opcodes(src)
        return self.executer(opcode)

    def opcodes(self, src):
        """output opcodes list
        """
        return self.tokens2opcodes(self.src2tokens(src))

    def tokens(self, src):
        """output tokens list
        """
        return self.src2tokens(src)

    def src(self, opcodes):
        """output src
        """
        return self.opcodes2src(self.opcode2tokens(self, opcodes))

    def src2tokens(self, src):
        """output token list
        """
        return self.lexer(src, self.optoken.alltokens())

    def tokens2opcodes(self, tokens):
        return self.translator(tokens, self.optoken.token2opcode_dict())

    def opcodes2tokens(self, opcodes):
        """transrate opcodes to tokens (1st token only)
        """
        return self.translator(opcodes, self.optoken.opcode2token_dict())

    def tokens2src(self, tokens):
        """output src from opcodes list
        """
        return self.sep.join(tokens)

    def test(self, src):
        """output token list, opcode list and reuslt
        """
        print('Test '+self.__class__.__name__+' class:')
        print('  * src: ', str(src))
        print('  * token: ', self.tokens(src))
        print('  * opcode: ', self.opcodes(src))
        print('  * output: ')
        self.run(src)
        return True

if __name__ == '__main__':
    ## test 
    b=BrainFuck()
    b.printparams()
    b.test(b.BF_HELLO_WORLD_SRC)
    print('')

    ## simple instance creation sample 
    ## Kapibara-san language instance
    print('Kapibara-san variant:')
    k=BrainFuck(tokens=['のすのす','もでーん','キュルッ！','もふっ！', 'むぎゅっと','グッ！！','ぬっくし','うっとり'], sep=' ')
    k.test(k.tokens2src(k.opcodes2tokens(b.opcodes(b.BF_HELLO_WORLD_SRC))))