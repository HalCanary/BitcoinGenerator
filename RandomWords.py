#!/usr/bin/env python
'''
Pull random words from http://world.std.com/~reinhold/diceware.wordlist.asc

Written 2013 Hal Canary.
Dedicated to the public domain.
'''
import random,math,sys,os
useDevRandom = True
def GetRandom():
	if useDevRandom:
		with open('/dev/random', 'r') as f:
			random.seed(f.read(16))
		return random
	else:
		return random.SystemRandom()

with open(os.path.expanduser('~/Downloads/diceware.wordlist.asc')) as f:
	X = [line.split()[1] for nu,line in enumerate(f) if 2 <= nu < 7778]
required_entropy = 128
numwords = int(math.ceil(required_entropy / math.log(len(X),2)))
s = ' '.join(GetRandom().choice(X) for i in xrange(numwords))
sys.stdout.write(s)
sys.stdout.flush()
sys.stderr.write('\n')
