#!/usr/bin/env python
# -*- coding: utf-8 -*-
## Python3

import sys

class OpToken(dict):
    """Store token/opcode transration map
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
    def alltokens(self):
        """output all token list
        
        Returns:
            list: flat list of all tokens
        """
        return sum(self.values(), [])
    def tokens(self):
        """output 1st token of all opcodes
        
        Returns:
            list: list of tokens
        """
        return [self[s][0] for s in self.opcodes()]
    def opcodes(self):
        """output opcode list
        
        Returns:
            list: list of opcodes
        """
        return list(self.keys())
    def opcode(self, token):
        """output opcode by given token
        
        Args:
            token (str): token

        Returns:
            str: opcode related with given token
        """
        for o in self.opcodes():
            if token in self[o]:
                return o
        return None
    def token(self, opcode, index=0):
        """output token of given opcode
        
        Args:
            opcode (str): opcode
            index (int): index in token list related with given opcode. default is 0 (1st token).
        
        Returns:
            str: token 
        """
        return self[opcode][index]
    def token2opcode_dict(self):
        """return dict as {token:opcode}
        
        Returns:
            dict: transmap as dict as {token:opcode}, which return opcode by dict[token].
        """
        return dict([(t, self.opcode(t)) for t in self.alltokens()])
    def opcode2token_dict(self): 
        """return dict as {opcode:token}
        
        Returns:
            dict: transmap as dict as {opcode:token}, which return token by dict[opcode]. (1st token only)
        """
        return dict(zip(self.opcodes(), self.tokens()))
    def replace_tokens(self, tokens):
        """replace tokens with given list
        
        Args:
            tokens (list): tokens to be used for replacement
        
        Returns:
            bool: True if replacement is finished successfully
        """
        if type(tokens)!=list:
            raise TypeError('arg tokens is not list')
        if len(self)!=len(tokens):
            raise IndexError('index of given tokens is not matched')
        return self.__init__(dict(zip(self.opcodes(), tokens)))

class BrainFuck:
    """BrainFuck class to generate BrainFuck interpreter and BrainFuck Variants
    
    Refer http://www.muppetlabs.com/~breadbox/bf/ for more detail of BrainFuck.
    
    Variables:
        OPTOKEN_DICT (dict): default dictionary for OpToken class. 
        ARRAY_SIZE (int): default data cell array size.
        SEP (str): default separator for src output.
        TOKENS (list): default token list to replace tokens in optoken.
        BF_HELLO_WORLD_SRC (str)= sample BrainFuck code to output "Hello World!".
    
    Attributes:
        asize (int): data cell array size.
        sep (str): separator for src output.
        optoken (OpToken): OpToken instance to translate token and opcode
        debug (bool): debug flag
        ptr (int): data pointer
        cur (int): instruction pointer
        cell (list): data cell area
        code (list): program area
    """
    OPTOKEN_DICT = dict(
        nxt = '>',
        prv = '<',
        inc = '+',
        dec = '-',
        put = '.',
        get = ',',
        opn = '[',
        cls = ']'
    )
    ARRAY_SIZE = 30000
    SEP = '' 
    TOKENS = None 
    BF_HELLO_WORLD_SRC = '>+++++++++[<++++++++>-]<.>+++++++[<++++>-]<+.+++++++..+++.[-]>++++++++[<++++>-]<.>+++++++++++[<+++++>-]<.>++++++++[<+++>-]<.+++.------.--------.[-]>++++++++[<++++>-]<+.[-]++++++++++.'

    def __init__(self, optoken_dict=None, asize=None, sep=None, tokens=None, debug=False):
        """
        Args: 
            optoken_dict (dict): dict to generate optoken (OpToken).
            asize (int): data cell array size
            sep (str): separator for src output
            tokens (list): token list to replace tokens in optoken
            debug (bool): debug flag
        """
        self.asize = asize if asize!=None else self.ARRAY_SIZE 
        self.sep = sep if sep!=None else self.SEP 
        self.optoken = OpToken(optoken_dict) if optoken_dict!=None else OpToken(self.OPTOKEN_DICT)
        if self.TOKENS!=None:
            self.optoken.replace_tokens(self.TOKENS)
        if tokens!=None:
            self.optoken.replace_tokens(tokens)
        self.debug = debug
        if self.debug:
            self.printparams()
        self.initializer()

    def printparams(self):
        """print specification for debugging
        """
        header = '***** Spec of "'+self.__class__.__name__+'" *****'
        print(header)
        print('Array size = '+str(self.asize))
        print('Token/Opcode map:')
        for t in self.optoken.alltokens():
            print('  '+t+' => '+self.optoken.opcode(t))
        print('*' * (len(header)))
        return True

    def lexer(self, src):
        """lexical analysis of src code and return tokens list
        
        Args:
            src (str): source code
            
        Returns:
            list: token list
        """
        READ_AHEAD_BYTE = 64 # read ahead byte for debugging output
        tokens = [] # output tokens list
        cur = 0 # current position in src
        ctoken = None # token candidate
        tokenlist = self.optoken.alltokens()
        while cur <= len(src)-1:
            str = src[cur:]
            start = len(str)
            for token in tokenlist:
                index = str.find(token)
                if index>=0 and (index<start or (index==start and start+len(ctoken)<index+len(token))):
                    ctoken = token
                    start = index
            if self.debug:
                print('LEXER:', len(tokens), cur, ctoken, str[start:READ_AHEAD_BYTE])
            if ctoken!=None:
                tokens.append(ctoken)
                cur+=str.find(ctoken)+len(ctoken)
                ctoken = None
            else:
                break
        return tokens

    def translator(self, orig, reverse=False):
        """translate each items in original list by self.optoken
        To be used to translate from token to opcode by default. reverse option allow to translate opcode to token.
        
        Args:
            orig (list): list of token or opcode.
            reverse (bool): translate token to opcode if False, else translate opcode to token
            
        Returns:
            list: translated result
        """
        if reverse:
            trans_dict = self.optoken.opcode2token_dict()
        else:
            trans_dict = self.optoken.token2opcode_dict()
        if self.debug:
            for e in orig:
                print('TRANSLATOR:', e, '=>', trans_dict[e])
        return [trans_dict[e] for e in orig]

    def executer(self, opcodes=None):
        """execute opcodes
        
        Call op_"opcode" function at each step. 
        Call preproc function before execution, and call postproc function after to execute all steps. 
        At each step, call stepproc function.
        
        Args:
            opcodes (list): user specified opcode list. if user give opcode list, self.code will be replaced.
        
        Returns:
            bool: Always return True
        """
        if opcodes!=None:
            if type(opcodes)==list:
                self.code = opcodes
            else:
                raise TypeError('given opcode is not list')
        self.preproc()
        while self.cur < len(self.code):
            c = self.code[self.cur]
            if self.debug:
                print('EXECUTER:', c, self.cur, self.ptr, self.cell[self.ptr])
            try:
                eval('self.op_'+c+'()')
            except NameError:
                print('function for '+c+' ('+self.optoken[c]+') is not defined yet')
                sys.exit() 
            self.cur+=1
            self.stepproc()
        self.postproc()
        return True

    def initializer(self):
        """initialize data pointer, instruction pointer, and data cell before running
        """
        self.ptr = 0 # data pointer
        self.cur = 0 # instruction pointer
        self.cell = [0 for i in range(self.asize)] # data cell initialized 0
        self.code = None # program area 
        return True

    def preproc(self):
        """pre-processing"""
        return True

    def stepproc(self):
        """process at each step"""
        return True

    def postproc(self):
        """post-processing"""
        return True

    def op_nxt(self):
        """increment pointer (++ptr)"""
        self.ptr+=1
        return True

    def op_prv(self):
        """decrement pointer (--ptr)"""
        self.ptr-=1
        return True

    def op_inc(self):
        """increment the byte at pointer (++*ptr)"""
        self.cell[self.ptr]+=1
        return True

    def op_dec(self):
        """decrement the byte at pointer (--*ptr)"""
        self.cell[self.ptr]-=1
        return True

    def op_put(self):
        """output the byte at the pointer (putchar(*ptr))
        if the byte is not valid to output as str, output byte instead of.
        """
        try:
            sys.stdout.write(chr(self.cell[self.ptr]))
        except UnicodeEncodeError:
            sys.stdout.write(str(self.cell[self.ptr].to_bytes(1,'big'))+' ')
        return True

    def op_get(self):
        """input a byte and store it in the byte at the pointer (*ptr = getchar())"""
        self.cell[self.ptr] = ord(input("Enter>")[0])
        return True

    def op_opn(self):
        """jump forward past the matching ] if the byte at the pointer is zero (which (*ptr) {)"""
        if self.cell[self.ptr] != 0:
            return False
        level=1
        while self.code[self.cur]!='cls' or level!=0:
            if self.cur <= len(self.code): self.cur+=1
            if self.code[self.cur]=='opn': level+=1
            if self.code[self.cur]=='cls': level-=1
        return True

    def op_cls(self):
        """jump backward to the matching [ unless the byte at the pointer is zero (})"""
        if self.cell[self.ptr] == 0:
            return False
        level=1
        while self.code[self.cur]!='opn' or level!=0:
            if self.cur >= 0: self.cur-=1
            if self.code[self.cur]=='opn': level-=1
            if self.code[self.cur]=='cls': level+=1
        return True

    def run(self, src): 
        """run src code
        
        Args:
            src (str): source code
            
        Returns:
            bool: return code of executor()
        """
        self.initializer()
        tokens = self.lexer(src)
        opcodes = self.translator(tokens)
        return self.executer(opcodes)

    def opcodes(self, src):
        """output opcodes list from src
        
        Args:
            src (str): source code

        Returns:
            list: opcode list
        """
        return self.translator(self.lexer(src))

    def src(self, opcodes):
        """output src from opcodes list
        
        Args:
            list: opcode list

        Returns:
            src (str): source code
        """
        return self.sep.join(self.translator(opcodes, reverse=True))

    def test(self, src):
        """output token list, opcode list and reuslt
        """
        print('Test '+self.__class__.__name__+' class:')
        print('  * src: ', str(src))
        print('  * token: ', self.lexer(src))
        print('  * opcode: ', self.opcodes(src))
        print('  * output: ')
        self.run(src)
        return True

if __name__ == '__main__':
    ## test 
    b=BrainFuck()
    b.printparams()
    print(b.opcodes('>>>sample<<<'))
    b.test(b.BF_HELLO_WORLD_SRC)
    print('')

    ## simple instance creation sample 
    ## Kapibara-san language instance
    print('Kapibara-san variant:')
    k=BrainFuck(tokens=['のすのす','もでーん','キュルッ！','もふっ！', 'むぎゅっと','グッ！！','ぬっくし','うっとり'], sep=' ')
    k.test(k.src(b.opcodes(b.BF_HELLO_WORLD_SRC)))