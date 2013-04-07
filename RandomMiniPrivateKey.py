#!/usr/bin/env python
'''
Written 2013 Hal Canary.
Dedicated to the public domain.
'''
import random, sys, hashlib

useDevRandom = True
alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
base_count = len(alphabet)
N = base_count ** 29

def encode(num):
	encode = ''
	while (num > 0):
		num, mod = divmod(num, base_count)
		encode = alphabet[mod] + encode
	return 'S' + encode

def DevRand(numbytes):
	num = 0
	with open('/dev/random', 'rb') as f:
		for i in xrange(numbytes):
			num = (num * 0x100) + ord(f.read(1))
	return num

def SysRand(n):
	return random.SystemRandom().randrange(n)

def RandomMiniPrivateKey():
	num = DevRand(21) if useDevRandom else SysRand(N)
	while True:
		encoded = encode(num)
		if hashlib.sha256(encoded + '?').digest()[0] == chr(0x00):
			return encoded
		num = (num + 1) % N
if __name__ == '__main__':
	sys.stdout.write(RandomMiniPrivateKey())
	sys.stdout.flush()
	sys.stderr.write('\n')

