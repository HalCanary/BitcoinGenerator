#!/usr/bin/env python
import hashlib, sys, math
'''
A single Python script to convert a passphrase into a Bitcoin address.

   Copyright 2013 Hal Canary

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''
# PRIVATE: "correct horse battery staple"
# PRIVATE: 5KJvsngHeMpm884wtkJNzQGaCErckhHJBGFsvd3VyK5qMZXj3hS
# PUBLIC:  1JwSSubhmg6iPtRjtyqhUYYH7bZg3Lfy1T

def test1():
	privkey, pubkey = getkeys("correct horse battery staple")
	assert privkey == '5KJvsngHeMpm884wtkJNzQGaCErckhHJBGFsvd3VyK5qMZXj3hS'
	assert pubkey == '1JwSSubhmg6iPtRjtyqhUYYH7bZg3Lfy1T'

secp256k1_p  = long('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F', 16)
secp256k1_Gx = long('79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798', 16)
secp256k1_Gy = long('483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8', 16)

for x in [secp256k1_p, secp256k1_Gx, secp256k1_Gy]:
	assert x >= 0
	assert x.bit_length() <= 256

def shash(s):
	return hashlib.sha256(s).digest()

def ripe(s):
	h = hashlib.new('ripemd160')
	h.update(s)
	return h.digest()

def shex(s):
	'convert a bytestring number to hex'
	return ''.join('%02x'%ord(x) for x in s)

def stringtoint(x):
	'convert a bytestring to an integer'
	return sum(ord(c)*(0x100 ** i) for i, c in enumerate(reversed(x)))

def hextoint(s):
	'convert a hex to an integer'
	return int(s, 16)

def inttohex(x):
	'convert a integer to hex'
	return '%x' % x

def inttostring(x):
	'convert an integer to a bytestring'
	def genbytes(x):
		while (x > 0):
			x, y = divmod(x, 0x100)
			yield chr(y)
	return ''.join(reversed(list(genbytes(x))))

def hextostring(s):
	'convert a hex to a bytestring '
	if len(s) % 2: s = '0' + s
	return ''.join(chr( int (s[i:i+2], 16 ) ) for i in range(0, len(s), 2))

def addcheck(s):
	s1 = chr(0x80) + s
	return s1 + shash(shash(s1))[:4]

def pubcheck(s):
	s1 = chr(0x00) + ripe(shash(s))
	return s1 + shash(shash(s1))[:4]

def encode(s):
	num = stringtoint(s)
	alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
	base_count = len(alphabet)
	encode = ''
	if (num < 0):
		return ''
	while (num > 0):
		num, mod = divmod(num, base_count)
		encode = alphabet[mod] + encode
	if s[0] == chr(0x00):
		encode = alphabet[0] + encode
	return encode

def decode(s):
	alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
	alphadict = dict((x, i) for i, x in enumerate(alphabet))
	base = len(alphabet)
	return sum(alphadict[c] * (base ** i) for i, c in enumerate(reversed(s)))

class ModSecp256k1:
	_p = secp256k1_p
	def __init__(self, v = 0):
		self._v = v % self._p
	def value(self): return self._v
	def __repr__(self):
		return 'ModSecp256k1({})'.format(self.value())
	def __add__(self, o):
		assert isinstance(o, ModSecp256k1)
		return ModSecp256k1(self._v + o._v)
	def __sub__(self, o):
		assert isinstance(o, ModSecp256k1)
		return ModSecp256k1(self._v - o._v)
	def __mul__(self, o):
		if isinstance(o, (int, long)):
			return ModSecp256k1(self._v * o)
		assert isinstance(o, ModSecp256k1)
		return ModSecp256k1(self._v * o._v)

def ExtendedEuclidian(a, b):
	x2, x1, y2, y1 = (ModSecp256k1(v) for v in (1, 0, 0, 1))
	while b > 0:
		q, r = divmod(a, b)
		a, b, x2, x1, y2, y1 = b, r, x1, (x2 - x1 * q), y1, (y2 - y1 * q)
	return (a, x2, y2)

def invert(a):
	d, x, y = ExtendedEuclidian(a.value(), secp256k1_p)
	assert d == 1
	return x

def ecdouble(P):
	x, y = P
	la = x * x * 3 * invert(y * 2)
	xr = la * la - x * 2
	return xr, la * (x - xr) - y

def ecadd(P, Q):
	if P is None:
		return Q
	(xp, yp), (xq, yq) = P, Q
	la = (yq - yp) * invert(xq - xp)
	xr = (la * la - xp - xq)
	return (xr, ((la * (xp - xr) - yp)))

def ecmul(x, G):
	assert x >= 0
	assert x.bit_length() <= 256
	Q = None
	for i in xrange(256 - 1, -1, -1):
		if Q is not None:
			Q = ecdouble(Q)
		if (x >> i) & 1 == 1:
			Q = ecadd(Q, G)
	return Q

def PrivateKeyToPublicKey(privkey):
	G = (ModSecp256k1(secp256k1_Gx), ModSecp256k1(secp256k1_Gy))
	x, y = ecmul(stringtoint(privkey), G)
	return chr(0x04) + inttostring(x.value()) + inttostring(y.value())

def CheckPrivateKey(key):
	n = int('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141', 16)
	return key > n

def getkeys(phrase):
	privkey = shash(phrase)
	assert CheckPrivateKey(privkey)
	pubkey = PrivateKeyToPublicKey(privkey)
	return (encode(addcheck(privkey)), encode(pubcheck(pubkey)))

if __name__ == '__main__':
	test1()
	phrase = sys.stdin.read()
	print 'private phrase', repr(phrase)
	privkey, pubkey = getkeys(phrase)
	print 'private key', privkey
	print 'public key', pubkey
	print >>sys.stderr, 'public key', pubkey

