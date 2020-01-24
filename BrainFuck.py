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
        CELL_SIZE (int): default data cell size [bit].
        DEM (str): default separator of src.
        TOKENS (list): default token list to replace tokens in optoken.
        BF_HELLO_WORLD_SRC (str): sample BrainFuck code to output "Hello World!".
    
    Attributes:
        array_size (int): data cell array size.
        cell_size (int): data cell size [bit]
        delimiter (str): delimiter of src output.
        optoken (OpToken): OpToken instance to translate token and opcode
        wrap_cell (bool): True to allow wrapping in cell.
        signed_cell (bool): True to allow signed cell data.
        wrap_array (bool): True to allow wrapping in array.
        infinite_array (bool): True to allow auto extend cell array to realize infinite cell array.
        delimit_input (bool): True to use self.dem for lexical anaysys of src code
        debug (bool): debug flag
        ptr (int): data pointer
        cur (int): instruction pointer
        cell (list): data cell area
        code (list): code area
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
    CELL_SIZE = 8
    DEM = ['']
    TOKENS = None
    BF_HELLO_WORLD_SRC = '>+++++++++[<++++++++>-]<.>+++++++[<++++>-]<+.+++++++..+++.[-]>++++++++[<++++>-]<.>+++++++++++[<+++++>-]<.>++++++++[<+++>-]<.+++.------.--------.[-]>++++++++[<++++>-]<+.[-]++++++++++.'

    def __init__(self, optoken_dict=None, array_size=None, cell_size=None, delimiter=None, tokens=None, wrap_cell=False, signed_cell=False, wrap_array=False, infinite_array=False, delimit_input=False, debug=False):
        """
        Args: 
            optoken_dict (dict): dict to generate optoken (OpToken).
            array_size (int): data cell array size
            cell_size (int): data cell size [bit]
            delimiter (str): separator for src output
            tokens (list): token list to replace tokens in optoken
            wrap_cell (bool): True to allow wrapping in cell. (ex. if cell size = 8bit, and cell byte is set as 256, cell byte = 0)
            signed_cell (bool): True to allow signed cell data.
            wrap_array (bool): True to allow wrapping in array. self.cell[-1] => self.cell[len(self.cell)].
            infinite_array (bool): True to allow auto extend cell array to realize infinite cell array (ex. for Turing Machine).
            delimit_input (bool): True to use self.delimiter for lexical analysis of src code
            debug (bool): True to output debug information
        """
        if optoken_dict:
            self.optoken = OpToken(optoken_dict)
        else:
            self.optoken = OpToken(self.OPTOKEN_DICT)
        self.array_size = array_size or self.ARRAY_SIZE
        self.cell_size = cell_size or self.CELL_SIZE
        if delimiter:
            if type(delimiter)!=list and type(delimiter)==str:
                self.delimiter = [delimiter]
            else:
                self.delimiter = delimiter
        else:
            self.delimiter = self.DEM
        if tokens:
            self.optoken.replace_tokens(tokens)
        elif self.TOKENS:
            self.optoken.replace_tokens(self.TOKENS)
        self.wrap_cell = wrap_cell
        self.signed_cell = signed_cell
        self.wrap_array = wrap_array
        self.infinite_array = infinite_array
        self.delimit_input = delimit_input
        self.debug = debug
        if self.debug:
            self.printparams()
        if self.signed_cell:
            self.cell_min = -1*2**self.cell_size/2
            self.cell_max = 2**self.cell_size/2 - 1
        else:
            self.cell_min = 0
            self.cell_max = 2**self.cell_size-1
        self.initializer()

    def outparams(self, oneline=False):
        """output specification for debugging
        """
        indent = '' if oneline else ' '*4
        sep = ', ' if oneline else '\n'
        eq = '=' if oneline else ' = '
        titleend = ' ' if oneline else '\n'
        output = ''
        # header
        if oneline:
            header = self.__class__.__name__+':'+titleend
        else:
            header = '***** Spec of "'+self.__class__.__name__+'" *****'+titleend
        output += header
        output += 'Array:'+titleend
        output += indent+'size'+eq+str(self.array_size)+sep
        output += indent+'Wrapping'+eq+('on' if self.wrap_array else 'off')+sep
        output += indent+'Infinite'+eq+('on' if self.infinite_array else 'off')+sep
        output += 'Cell:'+titleend
        output += indent+'size'+eq+str(self.cell_size)+'bit'+sep
        output += indent+'Wrapping'+eq+('on' if self.wrap_cell else 'off')+sep
        output += indent+'Signed'+eq+('on' if self.signed_cell else 'off')+sep
        output += 'Token/Opcode map:'+titleend
        for t in self.optoken.alltokens():
            output += indent+'\''+t+'\''+eq+self.optoken.opcode(t)+sep
        if oneline:
            output += ''
        else:
            output += '*' * (len(header))
        return output

    def printparams(self):
        """print specification for debugging
        """
        print(self.outparams())
        return True

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.outparams(oneline=True)

    def print_cell(self, start=None, end=None, num_column=30):
        index_min = start or 0
        index_max = end or self.array_size
        num_column = (end>=num_column and num_column) or end
        header = ' '*7 + ' '.join(['+{:02d}'.format(n) for n in range(num_column)])
        print(header)
        for i in range(index_max - index_min):
            index = index_min + i
            if i%num_column==0:
                col = 1
                print('{:6d}{:4d}'.format(index, self.cell[index]), end='')
            elif i%num_column==num_column-1:
                print('{:4d}'.format(self.cell[index]))
            else:
                col += 1
                print('{:4d}'.format(self.cell[index]), end='')

    def lexer(self, src):
        """lexical analysis of src code and return tokens list
        
        Args:
            src (str): source code
            
        Returns:
            list: token list
        """
        ## delimit src by multiple delimiter
        def _delimit(src, dem):
            if type(src)==str: src = [src]
            if len(dem)==1 and dem[0]=='': return src
            if len(dem)==0: return src
            d=dem.pop()
            return _delimit([ss for s in src for ss in s.split(d)], dem)
        ## core of lexer
        def _lexer(src, tokenlist):
            READ_AHEAD_BYTE = 32 # read ahead byte for debugging output
            tokens = [] # output tokens list
            cur = 0 # current position in src
            ctoken = None # token candidate
            while cur <= len(src)-1:
                cstr = src[cur:]
                start = len(cstr)
                for token in tokenlist:
                    index = cstr.find(token)
                    if index>=0 and (index<start or (index==start and start+len(ctoken)<index+len(token))):
                        ctoken = token
                        start = index
                if self.debug:
                    print('LEXER: token = "{}", current pos = {}, # of tokens = {}, ahead src = "{}"'.format(ctoken, cur, len(tokens), cstr[start:READ_AHEAD_BYTE]))
                if ctoken!=None:
                    tokens.append(ctoken)
                    cur += cstr.find(ctoken)+len(ctoken)
                    ctoken = None
                else:
                    break
            return tokens
        ## main of lexer function
        tokens = []
        dsrc = [src]
        if self.delimit_input:
            dsrc = _delimit(src, self.delimiter)
        for src in dsrc:
            tokens += _lexer(src, self.optoken.alltokens())
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
            for s in orig:
                print('TRANSLATOR: {:8} => {}'.format('"'+s+'"', trans_dict[s]))
        return [trans_dict[s] for s in orig]

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
            try:
                eval('self.op_'+c+'()')
            except NameError:
                print('function for '+c+' ('+self.optoken[c]+') is not defined yet')
                sys.exit()
            if self.debug:
                print('EXECUTER: opcode = {}, order = {}/{}, pointer = {}, memory = {}'.format(c, self.cur, len(self.code), self.ptr, self.cell[self.ptr]))
            self.cur += 1
            self.stepproc()
        self.postproc()
        return True

    def initializer(self):
        """initialize data pointer, instruction pointer, and data cell before running
        """
        self.ptr = 0 # data pointer
        self.cur = 0 # instruction pointer
        self.cell = [0 for i in range(self.array_size)] # data cell initialized 0
        self.code = None # program area 
        if self.debug:
            print('INITIALIZER: instruction pointer = {}, data pointer = {}, 1st memory cell = {}, 2nd memory cell = {}'.format(self.cur, self,ptr, self.cell[self.ptr], self.cell[self.ptr+1]))
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
        self.ptr += 1
        if self.ptr>=self.array_size-1:
            if self.infinite_array:
                self.cell.append(0)
            elif self.wrap_array: 
                self.ptr = 0
            else:
                raise IndexError('cell pointer is indicated as '+str(self.ptr)+' over array size ('+str(self.ARRAY_SIZE)+')')
        return True

    def op_prv(self):
        """decrement pointer (--ptr)"""
        self.ptr -= 1
        if self.ptr<0:
            if self.infinite_array:
                self.cell.append(0)
            elif self.wrap_array: 
                pass
            else:
                raise IndexError('cell pointer is indicated as '+str(self.ptr)+' under 0')
        return True

    def op_inc(self):
        """increment the byte at pointer (++*ptr)"""
        self.cell[self.ptr] += 1
        if self.cell[self.ptr]>self.cell_max:
            if self.wrap_cell:
                self.cell[self.ptr] = self.cell_min
            else:
                raise ValueError('Byte at cell pointer is set as '+str(self.cell[self.ptr])+' over maximum value='+str(self.cell_max))
        return True

    def op_dec(self):
        """decrement the byte at pointer (--*ptr)"""
        self.cell[self.ptr] -= 1
        if self.cell[self.ptr]<self.cell_min:
            if self.wrap_cell:
                self.cell[self.ptr] = self.cell_max
            else:
                raise ValueError('Byte at cell pointer is set as '+str(self.cell[self.ptr])+' under minimum value='+str(self.cell_min))
        return True

    def op_put(self):
        """output the byte at the pointer (putchar(*ptr))
        if the byte is not valid to output as str, output byte instead of.
        """
        import math
        try:
            sys.stdout.write(chr(self.cell[self.ptr]))
        except UnicodeEncodeError:
            b = math.ceil(self.cell[self.ptr].bit_length()/8)
            sys.stdout.write(str(self.cell[self.ptr].to_bytes(b,'big'))+' ')
        return True

    def op_get(self):
        """input a byte and store it in the byte at the pointer (*ptr = getchar())"""
        self.cell[self.ptr] = ord(input("Enter>")[0])
        return True

    def op_opn(self):
        """jump forward past the matching ] if the byte at the pointer is zero (which (*ptr) {)"""
        if self.cell[self.ptr] != 0:
            return False
        level = 1
        while self.code[self.cur]!='cls' or level!=0:
            if self.cur <= len(self.code): self.cur += 1
            if self.code[self.cur]=='opn': level += 1
            if self.code[self.cur]=='cls': level -= 1
        return True

    def op_cls(self):
        """jump backward to the matching [ unless the byte at the pointer is zero (})"""
        if self.cell[self.ptr] == 0:
            return False
        level = 1
        while self.code[self.cur]!='opn' or level!=0:
            if self.cur >= 0: self.cur -= 1
            if self.code[self.cur]=='opn': level -= 1
            if self.code[self.cur]=='cls': level += 1
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
        return self.delimiter[0].join(self.translator(opcodes, reverse=True))

    def test(self, src):
        """output token list, opcode list and reuslt
        """
        print('Test '+self.__class__.__name__+' class:')
        print('  * src: ', str(src))
        tokens = self.lexer(src)
        print('  * token: ', tokens)
        opcodes = self.translator(tokens)
        print('  * opcode: ', opcodes)
        print('  * output: ')
        self.executer(opcodes)
        return True

if __name__ == '__main__':
    ## test 
    b=BrainFuck()
    print(b)
    b.printparams()
    print(b.opcodes('>>>sample<<<'))
    b.test(b.BF_HELLO_WORLD_SRC)
    b.print_cell(end=10)
    print('')

    ## simple instance creation sample 
    ## Kapibara-san language instance
    print('Kapibara-san variant:')
    k=BrainFuck(tokens=['のすのす','もでーん','キュルッ！','もふっ！', 'むぎゅっと','グッ！！','ぬっくし','うっとり'], delimiter=' ')
    k.test(k.src(b.opcodes(b.BF_HELLO_WORLD_SRC)))
