#!/usr/bin/env python
'''
Pull random words from http://world.std.com/~reinhold/diceware.wordlist.asc

Written 2013 Hal Canary.
Dedicated to the public domain.
'''
import random,math,sys,os
useDevRandom = True
dicewareWordlist = '~/Downloads/diceware.wordlist.asc'
with open(os.path.expanduser(dicewareWordlist)) as f:
	WordList = [line.split()[1]
				for nu,line in enumerate(f) if 2 <= nu < 7778]
def GetRandom():
	if useDevRandom:
		with open('/dev/random', 'rb') as f:
			random.seed(f.read(16))
		return random
	else:
		return random.SystemRandom()
required_entropy = 128
numwords = int(math.ceil(required_entropy / math.log(len(WordList),2)))
s = ' '.join(GetRandom().choice(WordList) for i in xrange(numwords))
sys.stdout.write(s)
sys.stdout.flush()
sys.stderr.write('\n')
