
from __future__ import division
import sys
import math
import timeit
import random
import glob
from operator import itemgetter

# class Unseen: provides lexical rules for unseen words
#
class Unseen:

    # list of part of speech tags for unseen words
    postags = None
    total = None
    mostLikelyTag = None

    def __init__(self, file):
        self.total = 0
        self.postags = {}
        for line in open(file, 'r'):
            line = line[:-1]
            (count, tag) = line.split()
            if tag in self.postags:
                raise ValueError("each postag should occur exactly once")
            self.postags[tag] = int(count)
            self.total += int(count)
        self.computeLogProb()

    def computeLogProb(self):
        for tag in self.postags.keys():
            self.postags[tag] = math.log(self.postags[tag] / self.total, 2)

    def tagsForUnseen(self):
        for tag in self.postags.keys():
            yield (tag, self.postags[tag])

    def getMostLikelyTag(self):
        if self.mostLikelyTag is None:
            (self.mostLikelyTag, logProb) = sorted(self.postags.items(),
                                                   key=itemgetter(1)).pop()
        return self.mostLikelyTag

# end of class Unseen

# class Pcfg:
# Implements a non-strict Chomsky Normal Form probabilitic context free grammar
# can have rules of the form A -> B C, A -> B (hence non-strict), or A -> a
# A, B, C are non-terminals, a are terminals
#
# Format of the file for a rule lhs -> left right with its count is:
# count lhs left [right]
# the logProb for each rule is computed on demand
#
class Pcfg:

    lastRule = -1
    
    # each rule is indexed by a number i, where
    # rule[i] = (lhs, (left, right), count, logProb)
    rules = {}

    # forward index from lhs to list of rule numbers
    lhsRules = {}

    # reverse index from (left,right) to a rule index
    rhs = {}

    # total count over all rhs for each lhs in the pcfg
    lhsCount = {} 
    lhsTotalCount = 0

    # special symbol to mark a unary rule A -> B which is written as A -> B <Unary>
    unary = '<Unary>' 

    # read in the file containing the weighted context-free grammar
    # the prob for each rule is computed on the fly based on the weights
    # normalized by the lhs symbol as per the usual definition of PCFGs
    def __init__(self, filelist):
        for file in filelist:
            print >>sys.stderr, "#reading grammar file:", file
            linenum = 0
            for line in open(file, 'r'):
                line = line[:-1] # remove newline
                linenum += 1
                if line.find('#') != -1:
                    line = line[:line.find('#')] # strip comments
                line = line.strip()
                if line == "":
                    continue
                f = line.split()
                if len(f) > 4:
                    # only CNF rules allowed
                    raise ValueError("Error: more than two symbols in right hand side at line %d: %s" % (linenum, ' '.join(f)))
                if len(f) < 3:
                    # empty rules not allowed
                    raise ValueError("Error: unexpected line at line %d: %s" % (linenum, ' '.join(f)))
                # count lhs left [right]
                (count,lhs,left) = (int(f[0]), f[1], f[2])
                if len(f) < 4:
                    right = self.unary
                else:
                    right = f[3]
                if lhs == left and right == self.unary:
                    print >>sys.stderr, "#Ignored cycle", lhs, "->", left
                    continue
                self.lastRule += 1
                self.rules[self.lastRule] = (lhs, (left, right), count, None)

                if lhs in self.lhsRules: self.lhsRules[lhs].append(self.lastRule)
                else: self.lhsRules[lhs] = [self.lastRule]

                if (left,right) in self.rhs:
                    self.rhs[left,right].append(self.lastRule)
                else:
                    self.rhs[left,right] = [self.lastRule]

                if lhs in self.lhsCount:
                    self.lhsCount[lhs] += count
                else:
                    self.lhsCount[lhs] = count
                self.lhsTotalCount += count

    # computes the logProb of a rule using the counts collected for each lhs
    # it caches the value into the rules table after computing the probabiilty
    # for each rule
    def getLogProb(self, ruleNumber):
        if ruleNumber in self.rules:
            (lhs, rhs, count, logProb) = self.rules[ruleNumber]
            if logProb is not None:
                return logProb
            else:
                logProb = math.log(count / self.lhsCount[lhs], 2)
                self.rules[ruleNumber] = (lhs, rhs, count, logProb)
                return logProb
        else:
            raise ValueError("rule number %d not found" % ruleNumber)
       
    def getRule(self, ruleNumber):
        logProb = self.getLogProb(ruleNumber)
        return self.rules[ruleNumber]

    def ruleIterator(self, left, right):
        if (left,right) in self.rhs:
            for ruleNumber in self.rhs[left, right]:
                yield ruleNumber
        else:
            raise StopIteration

    # returns the prior probability of a nonTerminal
    def getPrior(self, lhs):
        if lhs in self.lhsCount:
            return math.log(self.lhsCount[lhs] / self.lhsTotalCount, 2)
        else:
            raise ValueError("%s: missing lhs" % lhs)
    
    def __str__(self):
        output = ""
        for i in range(0,self.lastRule+1):
            logProb = self.getLogProb(i)
            (lhs, (left, right), count, logProb) = self.rules[i]
            output += " ".join([lhs, left, right, str(count), str(logProb), "\n"])
        for i in self.lhsCount.keys():
            print "#Prior:", i, self.getPrior(i)
        return output

# end of class Pcfg

# class PcfgGenerator contains the functions that allow sampling
# of derivations from a PCFG. The output can be either the strings
# or the trees.
#
# There is a small chance that the generator function will not
# terminate. To make sure this outcome is avoided we use a limit
# on how unlikely the generated derivation should be. If during
# generation we go below this limit on the probability we stop
# and restart the generation process.
class PcfgGenerator:

    restart_limit = None # can be set using the constructor
    gram = None # PCFG to be used by the generator
    startsym = None # start symbol to start off the generation process

    def __init__(self, gram, startsym, limit=1e-300):
        self.restart_limit = limit
        self.gram = gram
        self.startsym = startsym

    def flattenTree(self, tree):
        sentence = [] 
        if isinstance(tree, tuple):
            (lhs, leftTree, rightTree) = tree
            for n in (self.flattenTree(leftTree), self.flattenTree(rightTree)):
                sentence.extend(n)
        else:
            if tree is not self.gram.unary:
                sentence = [tree]
        return sentence

    def generate(self, parsetree=False):
        rule = self.genPickOne(self.startsym)
        #print self.gram.getRule(rule)
        genTree = self.genFromRule(rule)
        return genTree if parsetree else self.flattenTree(genTree) 

    def genPickOne(self, lhs):
        r = random.random()
        #print >>sys.stderr, "random number:", r
        outputLogProb = math.log(r, 2)
        accumulator = 0.0
        rulePicked = None
        for r in self.gram.lhsRules[lhs]:
            #print self.gram.getRule(r)
            logProb = self.gram.getLogProb(r)
            # convert to prob from logProb in order to add with accumulator 
            prob = math.pow(2,logProb) 
            #print math.pow(2,outputLogProb), prob, accumulator
            if outputLogProb < math.log(prob + accumulator, 2):
                rulePicked = r
                break
            else:
                accumulator += prob
        if rulePicked is None:
            raise ValueError("no rule found for %s" % lhs)
        #print >>sys.stderr, "#picked rule %d: %s" % (rulePicked, self.gram.rules[rulePicked])
        return rulePicked

    def getYield(self, sym):
        return sym if sym not in self.gram.lhsRules else self.genFromRule(self.genPickOne(sym))

    def genFromRule(self, ruleNumber):
        (lhs, (left, right), count, logProb) = self.gram.rules[ruleNumber]
        #print >>sys.stderr, "#%s -> %s %s" % (lhs, left, right)
        leftTree = self.getYield(left)
        rightTree = self.gram.unary if right is self.gram.unary else self.getYield(right)
        return (lhs, leftTree, rightTree)
        

# class CkyParse contains the main parsing routines
# including routines for printing out the best tree and pruning
#
class CkyParse:

    gram = None # PCFG to be used by the grammar
    chart = None # chart data structure to be used by the parser
    unseen = None # gives a list of part of speech tags for unseen words
    verbose = 0
    usePrior = False
    usePruning = False
    beam = math.log(0.0001,2) # default value: usually set by getopt
    _NINF = float('1e-323') # 64 bit double underflows for math.log(1e-324)
    _LOG_NINF = math.log(_NINF,2)

    def __init__(self, gram, verbose=0):
        self.gram = gram
        self.verbose = verbose

    def prune(self, i, j):
        if self.usePruning == False:
            return 0
        numPruned = 0
        if (i,j) in self.chart:
            tbl = self.chart[i,j]
            maxLogProb = None
            bestLhs = None

            for lhs in tbl.keys():
                (logProb, backPointer) = tbl[lhs]
                maxLogProb = max(logProb, maxLogProb)
                if maxLogProb == logProb:
                    bestLhs = lhs

            newTbl = {}
            if self.usePrior:
                lowest = maxLogProb + self.beam + self.gram.getPrior(bestLhs)
            else:
                lowest = maxLogProb + self.beam
            for lhs in tbl.keys():
                (logProb, backPointer) = tbl[lhs]
                saveLogProb = logProb
                if self.usePrior:
                    logProb += self.gram.getPrior(lhs)
                if logProb < lowest:
                    print >>sys.stderr, "#pruning:", i, j, lhs, logProb, lowest
                    numPruned += 1
                    continue
                newTbl[lhs] = (saveLogProb, backPointer)
            self.chart[i,j] = newTbl
        return numPruned

    def insert(self, i, j, lhs, logProb, backPointer):
        if (i,j) in self.chart:
            if lhs in self.chart[i,j]:
                prevLogProb = self.chartGetLogProb(i, j, lhs)
                if logProb < prevLogProb:
                    return False
        else:
            self.chart[i,j] = {}
        self.chart[i,j][lhs] = (logProb, backPointer)
        if self.verbose > 1: 
            print >>sys.stderr, "#inserted", i, j, lhs, logProb
        return True

    def handleUnaryRules(self, i, j):
        # we have to allow for the fact that B -> C might lead
        # to another rule A -> B for the same span
        unaryList = [entry for entry in self.chartEntry(i,j)]
        for rhs in unaryList:
            rhsLogProb = self.chartGetLogProb(i, j, rhs)
            for ruleNumber in self.gram.ruleIterator(rhs, self.gram.unary):
                (lhs, (left, right), count, logProb) = self.gram.getRule(ruleNumber)
                # rhs == left
                if lhs == rhs:
                    raise ValueError("Found a cycle", lhs, "->", rhs)
                backPointer = (-1, rhs, self.gram.unary)
                if self.insert(i, j, lhs, logProb + rhsLogProb, backPointer):
                    unaryList.append(lhs)

    def chartEntry(self, i, j):
        if (i,j) in self.chart:
            for item in self.chart[i,j].keys():
                yield item
        else:
            raise StopIteration

    def chartGetLogProb(self, i, j, lhs):
        if (i,j) in self.chart:
            # Each entry in the chart for i,j is a hash table with key lhs
            # and value equals the tuple (logProb, backPointer)
            # This function returns the first element of the tuple
            return self.chart[i,j][lhs][0]
        else:
            raise
        
    def parse(self, input):
        # chart has max size len(input)*len(input)
        # each entry in the chart is a hashtable with
        # key=lhs and value=(logProb, backPointer)
        self.chart = {}
        numPruned = 0

        # insert all rules of type NonTerminal -> terminal
        # where terminal matches some word in the input
        for (i, word) in enumerate(input):
            j = i+1
            if (word, self.gram.unary) in self.gram.rhs:
                for ruleNumber in self.gram.rhs[(word, self.gram.unary)]:
                    (lhs, rhs, count, logProb) = self.gram.getRule(ruleNumber)
                    self.insert(i, j, lhs, logProb, None)
            else:
                print >>sys.stderr, "#using unseen part of speech for", word
                if self.unseen is None:
                    raise ValueError("cannot find terminal symbol", word)
                else:
                    for (tag, logProb) in self.unseen.tagsForUnseen():
                        self.insert(i, j, tag, logProb, None)
            self.handleUnaryRules(i, j)

        # do not prune lexical rules
        
        # recursively insert nonterminal lhs
        # for rule lhs -> left right into chart[(i,j)]
        # if left belongs to the chart for span i,k
        # and right belongs to the chart for span k,j
        N = len(input)+1
        for j in range(2,N):
            for i in range(j-2,-1,-1):
                # handle the case for the binary branching rules lhs -> left right
                for k in range(i+1,j):
                    # handle the unary rules lhs -> rhs
                    for left in self.chartEntry(i,k):
                        for right in self.chartEntry(k,j):
                            leftLogProb = self.chartGetLogProb(i, k, left)
                            rightLogProb = self.chartGetLogProb(k, j, right)
                            for ruleNumber in self.gram.ruleIterator(left, right):
                                (lhs, rhs, count, logProb) = self.gram.getRule(ruleNumber)
                                backPointer = (k,left,right)
                                self.insert(i, j, lhs,
                                            logProb + leftLogProb + rightLogProb,
                                            backPointer)
                # handle the unary rules lhs -> rhs
                self.handleUnaryRules(i, j)
                # prune each span
                numPruned += self.prune(i, j)
        if self.verbose > 0:
            print >>sys.stderr, "#number of items pruned:", numPruned

        sentLogProb = self._LOG_NINF
        N = len(input)
        if (0,N) in self.chart:
            if startsym in self.chart[0,N]:
                (sentLogProb, backPointer) = self.chart[0,N][startsym]
        if self.verbose > 0:
            print >>sys.stderr, "#sentence log prob = ", sentLogProb
        return sentLogProb
        

    # defaultTree provides a parse tree for input w0,..,wN-1 when
    # the parser is unable to find a valid parse (no start symbol in
    # span 0,N). The default parse is simply the start symbol with
    # N children:
    # (TOP (P0 w0) (P1 w1) ... (PN-1 wN-1))
    # where Pi is the most likely part of speech tag for that word
    # from training data.
    # If the word is unknown it receives the most likely tag from
    # training (across all words).
    # if the Unseen class does not return a tag defaultTree uses
    # a default part of speech tag X.
    def defaultTree(self, input, startsym):
        tag = "X" if self.unseen is None else self.unseen.getMostLikelyTag()
        taggedInput = map(lambda z: "(" + tag + " " + z + ")", input)
        return "(" + startsym + " " + " ".join(taggedInput) + ")"
                
    # bestTree returns the most likely parse
    # if there was a parse there must be a start symbol S in span 0,N
    # then the best parse looks like (S (A ...) (B ...)) for some
    # A in span 0,k and B in span k,N; the function extractBestTree
    # recursively fills in the trees under the start symbol S
    def bestTree(self, input, startsym='TOP'):
        N = len(input)
        if (0,N) in self.chart:
            if startsym in self.chart[0,N]:
                return self.extractBestTree(input, 0, N, startsym)
        print >>sys.stderr, "#No parses found for:", " ".join(input)
        return self.defaultTree(input, startsym)

    # extractBestTree uses backPointers to recursively find the
    # best parse top-down:
    # for each span i,j and non-terminal A (sym below), the parsing
    # algorithm has recorded the best path to that non-terminal A
    # using the backPointer (k, leftSym, rightSym) which means
    # there is a rule A -> leftSym rightSym and that leftSym spans
    # i,k and rightSym spans k,j. Recursively calling extractBestTree
    # on spans i,k,leftSym and k,j,rightSym will provide the necessary
    # parts to fill in the dotted parts in the tree:
    # (A (leftSym ...) (rightSym ...))
    # the parser records k == -1 when it inserts a unary rule:
    # A -> leftSym <Unary>
    # so a single recursive call to extractBestTree fills in the
    # dotted parts of the tree:
    # (A (leftSym ...))
    def extractBestTree(self, input, i, j, sym):
        if (i,j) in self.chart:
            if sym in self.chart[i,j]:
                (logProb, backPointer) = self.chart[i,j][sym]
                if backPointer == None:
                    return "(" + sym + " " + input[i] + ")"
                (k,leftSym,rightSym) = backPointer
                if k == -1:
                    # unary rule
                    leftTree = self.extractBestTree(input, i, j, leftSym)
                    rightTree = ""
                else:
                    # binary rule
                    leftTree = self.extractBestTree(input, i, k, leftSym)
                    rightTree = self.extractBestTree(input, k, j, rightSym)
                return "(" + sym + " " + leftTree + " " + rightTree + ")"
        raise ValueError("cannot find span:", i, j, sym)

# end of class CkyParse

if __name__ == "__main__":
    import getopt
    usage = "\n        ".join([sys.argv[0],
                      "[-h|--help]              # [ ] are optional arguments",
                      "[-v|--verbose level]",
                      "[-s|--start] startsymbol",
                      "[-i|--parse]",
                      "[-r|--prior]             # used with --parse",
                      "[-p|--pruning]           # used with --parse",
                      "[-u|--unseen unseenfile] # used with --parse",
                      "[-b|--beam] beamsize     # used with --parse",
                      "[-o|--generate number]   # use either --parse or --generate",
                      "-g|--grammar file1[,file2,file3,...] or -g|--grammar \"*.gr\" do *not* use simply *.gr"])
    longforms = ["parse", "generate", "verbose", "help", "prior", "pruning", "grammar=", "beam=", "start=", "unseen="]
    try:
        opts, args = getopt.getopt(sys.argv[1:], "io:v:hrpg:b:s:u:", longforms)
    except getopt.GetoptError, err:
        print >>sys.stderr, str(err)
        print >>sys.stderr, usage
        sys.exit(2)

    random.seed()

    parse = False
    generate = False
    verbose = 0
    usePrior = False
    usePruning = False
    grammar = None
    beam = math.log(0.0001,2)
    startsym = 'TOP'
    unseenFile = None
    
    for o, a in opts:
        if o in ('-i', '--parse'):
            parse = True
        if o in ('-o', '--generate'):
            generate = True
            num_outputs = int(a)
        if o in ('-v', '--verbose'):
            verbose = int(a)
        if o in ('-h', '--help'):
            print >>sys.stderr, usage
            sys.exit()
        if o in ('-r', '--prior'):
            usePrior = True
        if o in ('-p', '--pruning'):
            usePruning = True
        if o in ('-g', '--grammar'):
            # multiple grammars can be provided as comma separated list
            # wildcards like *.gr are supported
            grammar = [ f for i in a.split(',') for f in glob.glob(i) ]
            grammar = [ f for f in set(grammar) ]
            print >>sys.stderr, "#loading grammar files:", ', '.join(grammar)
        if o in ('-b', '--beam'):
            beam = math.log(float(a),2)
        if o in ('-s', '--start'):
            startsym = a
        if o in ('-u', '--unseen'):
            unseenFile = a

    if grammar is None:
        print >>sys.stderr, usage
        sys.exit(2)

    if not parse and not generate:
        print >>sys.stderr, usage
        sys.exit(2)

    gram = Pcfg(grammar)
    #print gram

    if generate:
        gen = PcfgGenerator(gram, startsym)
        for i in range(num_outputs): print " ".join(gen.generate())
        #for i in range(num_outputs): print gen.generate(parsetree=True)

    if parse:
        parser = CkyParse(gram, verbose)
        parser.usePrior = usePrior
        parser.usePruning = usePruning
        parser.beam = beam
        if unseenFile is not None:
            parser.unseen = Unseen(unseenFile)

        timings = {}
        corpusLen = 0
        totalLogProb = None
        for line in sys.stdin:
            line = line[:-1]
            input = line.split()
            length = len(input)
            if length <= 0: 
                continue
            if line[0] == '#':
                print >>sys.stderr, "#skipping comment line in input:", line
                continue
            corpusLen += length
            sentLogProb = parser.parse(input)
            totalLogProb = sentLogProb if totalLogProb is None else totalLogProb + sentLogProb
            print parser.bestTree(input, startsym)
            if verbose > 0:
                verbose_copy = parser.verbose
                timer = timeit.Timer("parser.parse(input)", "from __main__ import parser; parser.verbose=0; input=%r" % input)
                secs = timer.timeit(number=2)
                if length in timings:
                    timings[length].append(secs)
                else:
                    timings[length] = [secs]
                timings[length].sort()
                print >>sys.stderr, "#parsing time: length=%d secs=%0.3f" % (length, secs)
                parser.verbose = verbose_copy
        if corpusLen > 0:
            print >>sys.stderr, "#-cross entropy (bits/word): %g" % (totalLogProb / corpusLen)
        
        if verbose > 0:
            if len(timings.keys()) > 0:
                print >>sys.stderr, "# LEN SECS MAX MIN"
            for length in timings.keys():
                tlen = len(timings[length])
                average = float(sum(timings[length]) / tlen)
                print >>sys.stderr, length, average, timings[length][0], timings[length][tlen-1]

